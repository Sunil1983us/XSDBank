"""
routes/system.py  –  System & utility routes blueprint
Handles: GET /, GET /download/<f>, GET /preview/<f>
         POST /pdf_info, GET /health, GET /status, GET /limits, POST /cleanup
"""

import os
import re
import time
from datetime import datetime
from pathlib import Path

from flask import Blueprint, render_template, request, jsonify, send_from_directory

from config import CONFIG, logger, cleanup_old_files

system_bp = Blueprint('system', __name__)


@system_bp.route('/')
def index():
    logger.info("Main page accessed")
    return render_template('index.html')


@system_bp.route('/download/<filename>')
def download_file(filename):
    try:
        logger.info(f"File download: {filename}")
        return send_from_directory(CONFIG['OUTPUT_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Download error for {filename}: {e}")
        return "File not found", 404


@system_bp.route('/preview/<filename>')
def preview_file(filename):
    try:
        if filename.endswith('.html'):
            return send_from_directory(CONFIG['OUTPUT_FOLDER'], filename)
        return "Only HTML files can be previewed", 400
    except Exception:
        return "File not found", 404


@system_bp.route('/pdf_info', methods=['POST'])
def pdf_info():
    try:
        data    = request.get_json() or {}
        files   = data.get('files', [])
        results = {}

        section_re = re.compile(
            r'((?:\d+\.)+\d+)[\.\s]+Use of\s+(.+?)\s*'
            r'\((pacs\.\d+\.\d+\.\d+|camt\.\d+\.\d+\.\d+)\)',
            re.IGNORECASE
        )

        for fname in files:
            fpath = os.path.join(CONFIG['UPLOAD_FOLDER'], os.path.basename(fname))
            if not os.path.exists(fpath):
                results[fname] = {'error': 'File not found'}
                continue
            try:
                import pdfplumber
                with pdfplumber.open(fpath) as pdf:
                    page_count = len(pdf.pages)
                    sections, seen = [], set()
                    for pg_num, page in enumerate(pdf.pages, 1):
                        text = page.extract_text() or ''
                        for m in section_re.finditer(text):
                            surrounding = text[max(0, m.start() - 10):m.end() + 30]
                            if re.search(r'\.{5,}', surrounding):
                                continue
                            key = (m.group(1), m.group(3).lower())
                            if key not in seen:
                                seen.add(key)
                                sections.append({
                                    'section': m.group(1),
                                    'label':   m.group(2).strip(),
                                    'message': m.group(3).lower(),
                                    'page':    pg_num,
                                    'display': f"{m.group(1)} – {m.group(2).strip()} ({m.group(3)})"
                                })
                results[fname] = {'pages': page_count, 'sections': sections}
            except Exception as e:
                logger.error(f"pdf_info error for {fname}: {e}")
                results[fname] = {'error': str(e)}

        return jsonify({'success': True, 'results': results})
    except Exception as e:
        logger.error(f"pdf_info route error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@system_bp.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0-local'
    })


@system_bp.route('/status')
def status():
    try:
        def _folder_stats(folder):
            p = Path(folder)
            files = list(p.glob('*')) if p.exists() else []
            return len(files), sum(f.stat().st_size for f in files if f.is_file())

        up_count, up_size = _folder_stats(CONFIG['UPLOAD_FOLDER'])
        out_count, out_size = _folder_stats(CONFIG['OUTPUT_FOLDER'])

        return jsonify({
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0-local',
            'config': {
                'host': CONFIG['HOST'], 'port': CONFIG['PORT'],
                'max_upload_mb': CONFIG['MAX_CONTENT_LENGTH'] // (1024 * 1024),
                'max_file_size_mb': CONFIG['MAX_FILE_SIZE_MB'],
                'max_files_per_upload': CONFIG['MAX_FILES_PER_UPLOAD'],
                'timeout_seconds': CONFIG['TIMEOUT_SECONDS'],
                'cleanup_hours': CONFIG['CLEANUP_HOURS'],
                'auto_cleanup': CONFIG['AUTO_CLEANUP_ENABLED']
            },
            'files': {
                'uploads': up_count,
                'uploads_size_mb': round(up_size / (1024 * 1024), 2),
                'outputs': out_count,
                'outputs_size_mb': round(out_size / (1024 * 1024), 2)
            },
            'tools_available': [
                'comprehensive', 'document', 'compare', 'multi_compare',
                'test_data', 'xml_validate', 'xml_diff', 'batch_validate',
                'mapping_template', 'xml_transform',
                'pdf_compare', 'pdf_table_extract', 'pdf_merge', 'pdf_split',
                'ig_extract', 'ig_diff', 'ig_change_tracker',
                'ig_mapping', 'ig_mapping_xsd', 'xsd_ig_analysis',
                'yaml_api_extract'
            ]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@system_bp.route('/limits')
def get_limits():
    return jsonify({
        'max_file_size_mb': CONFIG['MAX_FILE_SIZE_MB'],
        'max_upload_total_mb': CONFIG['MAX_CONTENT_LENGTH'] // (1024 * 1024),
        'max_files_per_upload': CONFIG['MAX_FILES_PER_UPLOAD'],
        'max_batch_files': CONFIG['MAX_BATCH_FILES'],
        'timeout_seconds': CONFIG['TIMEOUT_SECONDS'],
        'allowed_extensions': list(CONFIG['ALLOWED_EXTENSIONS']),
        'cleanup_hours': CONFIG['CLEANUP_HOURS']
    })


@system_bp.route('/cleanup', methods=['POST'])
def trigger_cleanup():
    try:
        def _count(folder):
            p = Path(folder)
            return len(list(p.glob('*'))) if p.exists() else 0

        before = (_count(CONFIG['UPLOAD_FOLDER']), _count(CONFIG['OUTPUT_FOLDER']))
        cleanup_old_files()
        after  = (_count(CONFIG['UPLOAD_FOLDER']), _count(CONFIG['OUTPUT_FOLDER']))

        return jsonify({
            'success': True, 'message': 'Cleanup completed',
            'cleaned': {'uploads': before[0] - after[0], 'outputs': before[1] - after[1]}
        })
    except Exception as e:
        logger.error(f"Cleanup error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
