"""routes/tools_run.py – run_tool dispatcher + xsd_explorer integration"""
import os, uuid, traceback
from pathlib import Path
from flask import Blueprint, request, jsonify

run_bp = Blueprint('run', __name__)

# ── Tool catalogue (mirrors index.html) ──────────────────────────────────────
TOOL_MAP = {
    # XSD Tools
    'schema_analyzer':       'schema_analyzer',
    'schema_documenter':     'schema_documenter',
    'schema_comparator':     'schema_comparator',
    'multi_comparator':      'multi_comparator',
    'xml_validator':         'xml_validator',
    'batch_validator':       'batch_validator',
    'xml_generator':         'xml_generator',
    'xml_diff':              'xml_diff',
    'xml_transformer':       'xml_transformer',
    # IG / PDF Tools
    'ig_extractor':          'ig_extractor',
    'ig_diff':               'ig_diff',
    'ig_mapping_template':   'ig_mapping_template',
    'xsd_ig_analyser':       'xsd_ig_analyser',
    'rulebook_change_tracker':'rulebook_change_tracker',
    'mapping_generator':     'mapping_generator',
    # PDF Tools
    'pdf_comparator':        'pdf_comparator',
    'pdf_table_extractor':   'pdf_table_extractor',
    # YAML / API Tools
    'yaml_api_extractor':    'yaml_api_extractor',
    # ✨ NEW: XSD Explorer
    'xsd_explorer':          'xsd_explorer',
}

@run_bp.route('/run_tool', methods=['POST'])
def run_tool():
    from config import CONFIG, logger
    data   = request.get_json(force=True) or {}
    tool   = data.get('tool', '').strip()
    files  = data.get('files', [])   # list of saved filenames in UPLOAD_FOLDER
    params = data.get('params', {})

    if tool not in TOOL_MAP:
        return jsonify({"error": f"Unknown tool: {tool}"}), 400

    upload_dir = Path(CONFIG['UPLOAD_FOLDER'])
    output_dir = Path(CONFIG['OUTPUT_FOLDER'])
    output_dir.mkdir(parents=True, exist_ok=True)
    tools_dir  = Path(CONFIG['TOOLS_FOLDER'])

    # Resolve uploaded file paths
    file_paths = []
    for f in files:
        p = upload_dir / os.path.basename(f)
        if p.exists():
            file_paths.append(str(p))

    out_name = f"{uuid.uuid4().hex}_{tool}"

    try:
        # ── XSD Explorer (special: generates HTML + Excel) ──────────────────
        if tool == 'xsd_explorer':
            if not file_paths:
                return jsonify({"error": "Please upload an XSD file"}), 400
            xsd_path = file_paths[0]
            html_name = out_name + '_explorer.html'
            xlsx_name = out_name + '_structure.xlsx'

            import sys
            sys.path.insert(0, str(tools_dir))
            from xsd_explorer import parse_xsd, generate_html, generate_excel
            import json as _json

            roots, stats, edges, raw = parse_xsd(xsd_path)
            generate_html(roots, stats, edges, raw,
                          os.path.basename(xsd_path),
                          str(output_dir / html_name))
            generate_excel(roots, os.path.basename(xsd_path),
                           str(output_dir / xlsx_name))

            return jsonify({
                "status":  "success",
                "tool":    tool,
                "outputs": [
                    {"file": html_name, "label": "Interactive Explorer (HTML)", "preview": True},
                    {"file": xlsx_name, "label": "Structure Report (Excel)"},
                ],
                "stats": stats,
            })

        # ── Generic tool dispatch ────────────────────────────────────────────
        # For other tools call their main entry-point function if available
        # Otherwise return a helpful stub message
        return jsonify({
            "status": "success",
            "tool": tool,
            "message": f"Tool '{tool}' dispatched. Integrate specific tool call here.",
            "outputs": []
        })

    except Exception as e:
        logger.error(f"Tool {tool} failed: {e}\n{traceback.format_exc()}")
        return jsonify({"error": str(e), "detail": traceback.format_exc()}), 500


@run_bp.route('/detect_ig_sections', methods=['POST'])
def detect_ig_sections():
    """Detect message sections in an IG PDF."""
    return jsonify({"sections": []})


@run_bp.route('/detect_yaml_endpoints', methods=['POST'])
def detect_yaml_endpoints():
    """Detect endpoints in a YAML file."""
    return jsonify({"endpoints": []})
