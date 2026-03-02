"""
routes/tools_xsd.py  –  XSD & XML tools blueprint
Handles: POST /upload, POST /page_count, POST /run_tool
         Also contains execute_tool() used by run_tool
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from config import CONFIG, logger
from routes.library import LIBRARY_FOLDER, LIBRARY_EXTS, _safe_lib_path

xsd_bp = Blueprint('xsd', __name__)


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in CONFIG['ALLOWED_EXTENSIONS']


# ── Upload ────────────────────────────────────────────────────────────────────

@xsd_bp.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'files[]' not in request.files:
            return jsonify({'success': False, 'error': 'No files uploaded',
                            'error_code': 'NO_FILES'}), 400

        files = request.files.getlist('files[]')
        if len(files) > CONFIG['MAX_FILES_PER_UPLOAD']:
            return jsonify({'success': False,
                            'error': f'Maximum {CONFIG["MAX_FILES_PER_UPLOAD"]} files per upload.',
                            'error_code': 'TOO_MANY_FILES'}), 400

        uploaded, errors = [], []
        max_bytes = CONFIG['MAX_FILE_SIZE_MB'] * 1024 * 1024

        for file in files:
            if not file or not file.filename:
                continue
            if not allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else 'none'
                errors.append({'file': file.filename, 'error': f'Invalid file type: .{ext}',
                                'suggestion': 'Only .xsd, .xml, .zip, .pdf, .yaml, .yml, .json allowed'})
                continue
            file.seek(0, 2); size = file.tell(); file.seek(0)
            if size > max_bytes:
                errors.append({'file': file.filename,
                                'error': f'File too large: {size/1024/1024:.1f}MB (max {CONFIG["MAX_FILE_SIZE_MB"]}MB)'})
                continue
            if size == 0:
                errors.append({'file': file.filename, 'error': 'Empty file'})
                continue
            ts     = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            unique = f"{ts}_{secure_filename(file.filename)}"
            file.save(os.path.join(CONFIG['UPLOAD_FOLDER'], unique))
            uploaded.append(unique)
            logger.info(f"Uploaded: {unique} ({size} bytes)")

        if not uploaded and errors:
            return jsonify({'success': False, 'error': 'All files failed validation',
                            'error_code': 'VALIDATION_FAILED', 'details': errors}), 400
        resp = {'success': True, 'files': uploaded, 'count': len(uploaded)}
        if errors:
            resp['warnings'] = errors
        return jsonify(resp)

    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Upload failed', 'details': str(e)}), 500


# ── PDF page count ─────────────────────────────────────────────────────────────

@xsd_bp.route('/page_count', methods=['POST'])
def page_count():
    try:
        import pdfplumber
        pdf_path = None

        for f in request.files.getlist('files'):
            if f and f.filename:
                dest = Path(CONFIG['UPLOAD_FOLDER']) / f.filename.replace('/', '_')
                f.save(str(dest))
                pdf_path = str(dest)
                break

        if not pdf_path:
            lib_rel = request.form.get('library_path', '')
            if lib_rel:
                try:
                    t = _safe_lib_path(lib_rel)
                    if t.is_file():
                        pdf_path = str(t)
                except Exception:
                    pass

        if not pdf_path and request.is_json:
            data = request.get_json() or {}
            candidate = os.path.join(CONFIG['UPLOAD_FOLDER'],
                                     os.path.basename(data.get('file', '')))
            if os.path.exists(candidate):
                pdf_path = candidate

        if not pdf_path:
            return jsonify({'error': 'File not found'}), 404

        with pdfplumber.open(pdf_path) as pdf:
            return jsonify({'pages': len(pdf.pages), 'file': os.path.basename(pdf_path)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Legacy run_tool (XSD tools via JSON body) ─────────────────────────────────

@xsd_bp.route('/run_tool', methods=['POST'])
def run_tool():
    try:
        data      = request.get_json(force=True, silent=True) or {}
        tool      = data.get('tool', '')
        lib_files = data.get('library_files', [])
        options   = data.get('options', {})

        if not tool:
            return jsonify({'success': False, 'error': 'No tool specified'}), 400

        file_paths = []
        for f in data.get('files', []):
            path = os.path.join(CONFIG['UPLOAD_FOLDER'], os.path.basename(f))
            if os.path.exists(path):
                file_paths.append(path)
        for rel in lib_files:
            try:
                t = _safe_lib_path(rel)
                if t.is_file():
                    file_paths.append(str(t))
            except Exception:
                pass

        if not file_paths:
            return jsonify({'success': False, 'error': 'No valid files found'}), 400

        result = execute_tool(tool, file_paths, Path(file_paths[0]).stem, options)
        return jsonify(result)

    except Exception as e:
        logger.error(f"run_tool error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


# ── execute_tool (XSD tool dispatch — subprocess-based) ───────────────────────

def execute_tool(tool: str, file_paths: list, output_base: str, options: dict) -> dict:
    """Dispatch an XSD/XML tool, running the appropriate Python script via subprocess."""
    output_dir = CONFIG['OUTPUT_FOLDER']
    tools_dir  = CONFIG['TOOLS_FOLDER']
    timeout    = CONFIG['TIMEOUT_SECONDS']

    def _script(name):
        return os.path.join(tools_dir, name)

    def _run_cmd(cmd, out_file):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if r.returncode == 0 and os.path.exists(out_file):
            return {'success': True, 'files': [os.path.basename(out_file)]}
        return {'success': False, 'error': (r.stderr or r.stdout or 'Unknown error')[:400]}

    try:
        if tool == 'comprehensive':
            out = os.path.join(output_dir, f"{output_base}_comprehensive.xlsx")
            r   = _run_cmd([sys.executable, _script('schema_analyzer.py'), file_paths[0], '-o', out], out)
            if r['success']: r['message'] = 'Comprehensive analysis complete with ALL metadata!'
            return r

        elif tool == 'document':
            out = os.path.join(output_dir, f"{output_base}_docs.xlsx")
            r   = _run_cmd([sys.executable, _script('schema_documenter.py'), file_paths[0], '-o', out], out)
            if r['success']: r['message'] = 'Documentation generated!'
            return r

        elif tool == 'compare':
            if len(file_paths) < 2:
                return {'success': False, 'error': 'Two XSD files required'}
            out_base = os.path.join(output_dir, f"{output_base}_comparison")
            cmd = [sys.executable, _script('schema_comparator.py'),
                   file_paths[0], file_paths[1], '-o', out_base,
                   '--name-a', options.get('schema_name_a', 'Schema_A'),
                   '--name-b', options.get('schema_name_b', 'Schema_B')]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            files = [f for f in os.listdir(output_dir)
                     if f.startswith(os.path.basename(out_base))]
            if r.returncode == 0 and files:
                return {'success': True, 'message': 'Schema comparison complete!', 'files': files}
            return {'success': False, 'error': r.stderr or r.stdout or 'Comparison failed'}

        elif tool == 'multi_compare':
            if len(file_paths) < 3:
                return {'success': False, 'error': 'Three or more XSD files required'}
            out_base = os.path.join(output_dir, f"{output_base}_multi_comparison")
            cmd = [sys.executable, _script('multi_comparator.py'), *file_paths, '-o', out_base]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            files = [f for f in os.listdir(output_dir)
                     if f.startswith(os.path.basename(out_base))]
            if r.returncode == 0 and files:
                return {'success': True, 'message': 'Multi-schema comparison complete!', 'files': files}
            return {'success': False, 'error': r.stderr or r.stdout or 'Multi-comparison failed'}

        elif tool == 'test_data':
            out = os.path.join(output_dir, f"{output_base}_test_data.zip")
            r = _run_cmd([sys.executable, _script('xml_generator.py'),
                          file_paths[0], '-o', out,
                          '-n', str(options.get('test_count', 5)),
                          '--profile', str(options.get('test_profile', 'generic'))], out)
            if r['success']: r['message'] = f"Test data generated ({options.get('test_count', 5)} files)!"
            return r

        elif tool == 'xml_validate':
            xsd = next((f for f in file_paths if f.endswith('.xsd')), None)
            xml = next((f for f in file_paths if f.endswith('.xml')), None)
            if not xsd or not xml:
                return {'success': False, 'error': 'Need one .xsd and one .xml file'}
            out = os.path.join(output_dir, f"{output_base}_validation.html")
            r = subprocess.run([sys.executable, _script('xml_validator.py'), xml, xsd, '-o', out],
                               capture_output=True, text=True, timeout=timeout)
            if r.returncode == 0 and os.path.exists(out):
                return {'success': True, 'message': 'Validation complete!',
                        'files': [os.path.basename(out)]}
            return {'success': False, 'error': r.stderr or 'Validation failed'}

        elif tool == 'xml_diff':
            if len(file_paths) < 2:
                return {'success': False, 'error': 'Two XML files required'}
            out = os.path.join(output_dir, f"{output_base}_diff.xlsx")
            cmd = [sys.executable, _script('xml_diff.py'), file_paths[0], file_paths[1], '-o', out]
            if options.get('ignore_order'):
                cmd.append('--ignore-order')
            r = _run_cmd(cmd, out)
            if r['success']: r['message'] = 'XML diff complete!'
            return r

        elif tool == 'batch_validate':
            xsd_files = [f for f in file_paths if f.endswith('.xsd')]
            xml_files = [f for f in file_paths if f.endswith('.xml')]
            if not xsd_files:
                return {'success': False, 'error': 'XSD file required'}
            out = os.path.join(output_dir, f"{output_base}_batch_validation.xlsx")
            r = _run_cmd([sys.executable, _script('batch_validator.py'),
                          xsd_files[0], *xml_files, '-o', out], out)
            if r['success']: r['message'] = f'Batch validation complete ({len(xml_files)} files)!'
            return r

        elif tool == 'mapping_template':
            out = os.path.join(output_dir, f"{output_base}_mapping.xlsx")
            r   = _run_cmd([sys.executable, _script('mapping_generator.py'),
                             file_paths[0], '-o', out], out)
            if r['success']: r['message'] = 'Mapping template generated!'
            return r

        elif tool == 'xml_transform':
            xml  = next((f for f in file_paths if f.endswith('.xml')), None)
            xslt = next((f for f in file_paths if f.endswith(('.xsl', '.xslt'))), None)
            if not xml or not xslt:
                return {'success': False, 'error': 'Need .xml and .xsl/.xslt files'}
            out = os.path.join(output_dir, f"{output_base}_transformed.xml")
            r   = _run_cmd([sys.executable, _script('xml_transformer.py'), xml, xslt, '-o', out], out)
            if r['success']: r['message'] = 'XML transformation complete!'
            return r

        # PDF & Rulebook tools are handled by the /run endpoint
        else:
            return {'success': False, 'error': f'Unknown tool: {tool}'}

    except subprocess.TimeoutExpired:
        logger.error(f"Tool {tool} timed out after {timeout}s")
        return {'success': False, 'error': f'Timeout after {timeout} seconds'}
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return {'success': False, 'error': str(e)}
