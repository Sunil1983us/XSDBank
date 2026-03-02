"""
routes/tools_run.py  –  Modern tool runner blueprint
Handles: POST /run (multipart – PDF, Rulebook, YAML tools)
         POST /detect_ig_sections
         POST /detect_yaml_endpoints
"""

import sys
import json as _json
from pathlib import Path

from flask import Blueprint, request, jsonify

from config import CONFIG, logger
from routes.library import LIBRARY_FOLDER, LIBRARY_EXTS, _safe_lib_path

run_bp = Blueprint('run', __name__)


# ── /run  (multipart form: PDF, Rulebook, YAML tools) ────────────────────────

@run_bp.route('/run', methods=['POST'])
def run_tool_alias():
    tool_id = request.form.get('tool', '').strip()
    if not tool_id:
        return jsonify({'success': False, 'error': 'No tool specified'}), 400

    upload_dir = Path(CONFIG['UPLOAD_FOLDER'])
    upload_dir.mkdir(exist_ok=True)
    saved_paths = []

    for f in request.files.getlist('files'):
        if f and f.filename:
            safe = f.filename.replace('..', '').replace('/', '_').replace('\\', '_')
            dest = upload_dir / safe
            f.save(str(dest))
            saved_paths.append(str(dest))

    lib_json = request.form.get('library_files', '')
    if lib_json:
        try:
            for rel in _json.loads(lib_json):
                target = (LIBRARY_FOLDER / rel).resolve()
                try:
                    target.relative_to(LIBRARY_FOLDER.resolve())
                except ValueError:
                    continue
                if target.is_file() and target.suffix.lower() in LIBRARY_EXTS:
                    saved_paths.append(str(target))
        except Exception as e:
            logger.warning(f"library_files parse error: {e}")

    if not saved_paths:
        return jsonify({'success': False, 'error': 'No files provided'}), 400

    params = {k: v for k, v in request.form.items()
              if k not in ('tool', 'files', 'library_files')}
    result = _dispatch_tool(tool_id, saved_paths, params)
    return jsonify(result)


# ── Detect routes ─────────────────────────────────────────────────────────────

@run_bp.route('/detect_ig_sections', methods=['POST'])
def detect_ig_sections():
    try:
        sys.path.insert(0, str(Path(CONFIG['TOOLS_FOLDER'])))
        from ig_extractor import detect_sections

        pdf_path = _resolve_first_upload(['.pdf'])
        if not pdf_path:
            return jsonify({'success': False, 'error': 'No PDF provided'}), 400

        sections = detect_sections(pdf_path)
        logger.info(f"Section detection: {len(sections)} sections in {Path(pdf_path).name}")
        return jsonify({'success': True, 'sections': sections})

    except ImportError:
        return jsonify({'success': False, 'sections': [],
                        'error': 'ig_extractor not available'}), 200
    except Exception as e:
        logger.error(f"Section detection error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@run_bp.route('/detect_yaml_endpoints', methods=['POST'])
def detect_yaml_endpoints():
    try:
        sys.path.insert(0, str(Path(CONFIG['TOOLS_FOLDER'])))
        from yaml_api_extractor import detect_endpoints

        yaml_path = _resolve_first_upload(['.yaml', '.yml', '.json'])
        if not yaml_path:
            return jsonify({'success': False, 'error': 'No YAML/JSON file provided'}), 400

        endpoints = detect_endpoints(yaml_path)
        logger.info(f"Endpoint detection: {len(endpoints)} endpoints in {Path(yaml_path).name}")
        return jsonify({'success': True, 'endpoints': endpoints})

    except ImportError as e:
        return jsonify({'success': False, 'endpoints': [],
                        'error': f'yaml_api_extractor not available: {e}'}), 200
    except Exception as e:
        logger.error(f"Endpoint detection error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ── _dispatch_tool ────────────────────────────────────────────────────────────

def _dispatch_tool(tool_id: str, file_paths: list, params: dict) -> dict:
    """Route tool_id to the correct tool function and return a result dict."""
    sys.path.insert(0, str(Path(CONFIG['TOOLS_FOLDER'])))
    output_dir = Path(CONFIG['OUTPUT_FOLDER'])
    output_dir.mkdir(exist_ok=True)

    try:
        # ── Rulebook: IG Extractor ────────────────────────────────────────────
        if tool_id == 'ig_extract':
            from ig_extractor import extract_ig
            pdfs = [p for p in file_paths if p.endswith('.pdf')]
            if not pdfs:
                return {'success': False, 'error': 'Need at least 1 IG PDF file'}

            filter_sections = _csv_param(params.get('sections', ''))
            filter_messages = _csv_param(params.get('filter_messages', ''))

            import time as _t
            t0 = _t.time()
            out_files, total = [], 0
            for pdf in pdfs:
                out = str(output_dir / f"{Path(pdf).stem}_IG.xlsx")
                result = extract_ig(pdf, out,
                                    filter_messages=filter_messages,
                                    filter_sections=filter_sections)
                total += result.get('total_fields', 0)
                out_files.append({'name': Path(out).name, 'size': Path(out).stat().st_size})
            return {
                'success': True,
                'message': (f"Extracted {total} fields from {len(out_files)} PDF(s). "
                            "One Excel sheet per message section with 🟡 yellow / ⬜ white / 🔴 red colour coding."),
                'files': out_files,
                'execution_time_seconds': round(_t.time() - t0, 2)
            }

        # ── Rulebook: IG Diff ─────────────────────────────────────────────────
        elif tool_id == 'ig_diff':
            from ig_diff import diff_ig
            xl = [p for p in file_paths if p.endswith(('.xlsx', '.xlsm'))]
            if len(xl) < 2:
                return {'success': False, 'error': 'Please provide 2 IG Excel files'}
            label_a = params.get('label_a', 'File A')
            label_b = params.get('label_b', 'File B')
            out = str(output_dir / f"IG_Diff_{label_a}_vs_{label_b}.xlsx")
            diff_ig(xl[0], xl[1], out, label_a=label_a, label_b=label_b)
            return {'success': True, 'message': 'Diff complete',
                    'files': [{'name': Path(out).name, 'size': Path(out).stat().st_size}]}

        # ── Rulebook: Change Tracker ──────────────────────────────────────────
        elif tool_id == 'rulebook_changes':
            from rulebook_change_tracker import track_changes
            pdfs = [p for p in file_paths if p.endswith('.pdf')]
            if not pdfs:
                return {'success': False, 'error': 'Please provide a PDF file'}
            out   = str(output_dir / 'RulebookChanges.xlsx')
            pdf_b = pdfs[1] if len(pdfs) > 1 else None
            track_changes(pdfs[0], out, pdf_b=pdf_b)
            return {'success': True, 'message': 'Change log extracted',
                    'files': [{'name': 'RulebookChanges.xlsx', 'size': Path(out).stat().st_size}]}

        # ── Rulebook: IG Mapping ──────────────────────────────────────────────
        elif tool_id == 'ig_mapping':
            from ig_mapping_template import generate_mapping
            xl = [p for p in file_paths if p.endswith(('.xlsx', '.xlsm'))]
            if not xl:
                return {'success': False, 'error': 'Please provide an IG Excel file'}
            out = str(output_dir / 'Mapping_Template.xlsx')
            generate_mapping(xl[0], out,
                             scheme_label=params.get('scheme_label', 'EPC'),
                             version=params.get('version', ''))
            return {'success': True, 'message': 'Mapping template ready',
                    'files': [{'name': 'Mapping_Template.xlsx', 'size': Path(out).stat().st_size}]}

        # ── Rulebook: IG Mapping (XSD-Enriched) ──────────────────────────────
        elif tool_id == 'ig_mapping_xsd':
            from ig_mapping_template_xsd import generate_mapping_xsd
            xl  = [p for p in file_paths if p.endswith(('.xlsx', '.xlsm'))]
            xsd = [p for p in file_paths if p.endswith('.xsd')]
            if not xl or not xsd:
                return {'success': False, 'error': 'Please provide an IG Excel + XSD file'}
            out = str(output_dir / 'Mapping_XSD.xlsx')
            generate_mapping_xsd(xl[0], xsd[0], out,
                                 scheme_label=params.get('scheme_label', 'EPC'),
                                 version=params.get('version', ''))
            return {'success': True, 'message': 'XSD-enriched mapping ready',
                    'files': [{'name': 'Mapping_XSD.xlsx', 'size': Path(out).stat().st_size}]}

        # ── Rulebook: XSD vs IG Analyser ──────────────────────────────────────
        elif tool_id == 'xsd_ig_analysis':
            import xsd_ig_analyser as xa
            xsd = [p for p in file_paths if p.endswith('.xsd')]
            xl  = [p for p in file_paths if p.endswith(('.xlsx', '.xlsm'))]
            if not xsd or not xl:
                return {'success': False, 'error': 'Please provide 1 XSD + 1 IG Excel'}
            out = str(output_dir / f"{Path(xsd[0]).stem}_XSD_IG_Analysis.xlsx")
            result = xa.analyse(xsd[0], xl[0], out,
                                message_sheet=params.get('message_sheet') or None,
                                scheme_label=params.get('scheme_label', 'EPC'),
                                version=params.get('version', ''))
            return {'success': True,
                    'message': f"{result['total']} fields — {result['aligned']} aligned, {result['status_diff']} status diffs",
                    'files': [{'name': Path(out).name, 'size': Path(out).stat().st_size}]}

        # ── PDF tools ─────────────────────────────────────────────────────────
        elif tool_id in ('pdf_compare', 'pdf_table_extract', 'pdf_merge', 'pdf_split'):
            return _run_pdf_tool(tool_id, file_paths, params)

        # ── YAML: API Schema Extractor ────────────────────────────────────────
        elif tool_id == 'yaml_api_extract':
            from yaml_api_extractor import extract_yaml_api
            yaml_files = [p for p in file_paths
                          if Path(p).suffix.lower() in ('.yaml', '.yml', '.json')]
            if not yaml_files:
                return {'success': False, 'error': 'No YAML/JSON file uploaded'}
            filter_eps = _csv_param(params.get('filter_endpoints', ''))
            out = str(output_dir / f"{Path(yaml_files[0]).stem}_api_schema.xlsx")
            result = extract_yaml_api(yaml_files[0], out, filter_endpoints=filter_eps or None)
            if not result.get('success'):
                return {'success': False, 'error': result.get('error', 'Extraction failed')}
            return {'success': True, 'message': result['message'],
                    'files': [{'name': Path(out).name, 'size': Path(out).stat().st_size}]}

        else:
            return {'success': False, 'error': f'Unknown tool: {tool_id}'}

    except ImportError as e:
        logger.error(f"Tool import error ({tool_id}): {e}")
        return {'success': False, 'error': f'Tool not installed: {e}'}
    except Exception as e:
        logger.error(f"Tool error ({tool_id}): {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


# ── PDF tool dispatcher ───────────────────────────────────────────────────────

def _run_pdf_tool(tool_id: str, file_paths: list, params: dict) -> dict:
    output_dir = Path(CONFIG['OUTPUT_FOLDER'])
    try:
        if tool_id == 'pdf_compare':
            from pdf_comparator import compare_pdfs
            pdfs = [p for p in file_paths if p.endswith('.pdf')]
            if len(pdfs) < 2:
                return {'success': False, 'error': 'Need 2 PDF files'}
            out = str(output_dir / 'PDF_Comparison.xlsx')
            compare_pdfs(pdfs[0], pdfs[1], out)
            return {'success': True, 'message': 'Comparison complete',
                    'files': [{'name': 'PDF_Comparison.xlsx', 'size': Path(out).stat().st_size}]}

        elif tool_id == 'pdf_table_extract':
            from pdf_table_extractor import extract_tables_to_excel
            pdfs = [p for p in file_paths if p.endswith('.pdf')]
            if not pdfs:
                return {'success': False, 'error': 'Need a PDF file'}
            out = str(output_dir / f"{Path(pdfs[0]).stem}_tables.xlsx")
            extract_tables_to_excel(pdfs[0], out)
            return {'success': True, 'message': 'Tables extracted',
                    'files': [{'name': Path(out).name, 'size': Path(out).stat().st_size}]}

        elif tool_id == 'pdf_merge':
            from pdf_merger_splitter import merge_pdfs
            pdfs = [p for p in file_paths if p.endswith('.pdf')]
            if len(pdfs) < 2:
                return {'success': False, 'error': 'Need at least 2 PDF files'}
            out = str(output_dir / 'Merged.pdf')
            merge_pdfs(pdfs, out)
            return {'success': True, 'message': f'Merged {len(pdfs)} PDFs',
                    'files': [{'name': 'Merged.pdf', 'size': Path(out).stat().st_size}]}

        elif tool_id == 'pdf_split':
            from pdf_merger_splitter import split_pdf
            pdfs = [p for p in file_paths if p.endswith('.pdf')]
            if not pdfs:
                return {'success': False, 'error': 'Need a PDF file'}
            ranges = params.get('ranges', '').strip()
            result = split_pdf(pdfs[0], str(output_dir),
                               mode='ranges' if ranges else 'pages',
                               ranges=ranges or None)
            created = result.get('files_created', [])
            return {'success': True, 'message': f'Split into {len(created)} part(s)',
                    'files': [{'name': f['file'],
                               'size': (output_dir / f['file']).stat().st_size}
                              for f in created]}

    except Exception as e:
        return {'success': False, 'error': str(e)}
    return {'success': False, 'error': 'Unknown PDF tool'}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _csv_param(raw: str) -> list | None:
    """Parse a comma-separated param string into a list, or None if empty."""
    parts = [s.strip() for s in raw.split(',') if s.strip()]
    return parts if parts else None


def _resolve_first_upload(exts: list) -> str | None:
    """Save the first uploaded file matching exts and return its path."""
    upload_dir = Path(CONFIG['UPLOAD_FOLDER'])
    upload_dir.mkdir(exist_ok=True)

    for f in request.files.getlist('files'):
        if f and f.filename and Path(f.filename).suffix.lower() in exts:
            dest = upload_dir / f.filename.replace('/', '_')
            f.save(str(dest))
            return str(dest)

    lib_path = request.form.get('library_path', '')
    if lib_path:
        try:
            target = _safe_lib_path(lib_path)
            if target.is_file():
                return str(target)
        except ValueError:
            pass
    return None
