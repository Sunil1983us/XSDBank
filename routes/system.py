"""routes/system.py – home, health, download, preview, status"""
import os, time
from pathlib import Path
from flask import Blueprint, send_from_directory, jsonify, current_app, abort, render_template

system_bp = Blueprint('system', __name__)

@system_bp.route('/')
def home():
    return render_template('index.html')

@system_bp.route('/health')
def health():
    return jsonify({"status": "ok", "time": time.time()})

@system_bp.route('/status')
def status():
    from config import CONFIG
    return jsonify({
        "status": "running",
        "upload_folder": CONFIG['UPLOAD_FOLDER'],
        "output_folder": CONFIG['OUTPUT_FOLDER'],
        "uploads": len(list(Path(CONFIG['UPLOAD_FOLDER']).glob('*'))) if Path(CONFIG['UPLOAD_FOLDER']).exists() else 0,
        "outputs": len(list(Path(CONFIG['OUTPUT_FOLDER']).glob('*'))) if Path(CONFIG['OUTPUT_FOLDER']).exists() else 0,
    })

@system_bp.route('/download/<filename>')
def download(filename):
    from config import CONFIG
    safe = os.path.basename(filename)
    folder = CONFIG['OUTPUT_FOLDER']
    if not (Path(folder) / safe).exists():
        abort(404)
    return send_from_directory(folder, safe, as_attachment=True)

@system_bp.route('/preview/<filename>')
def preview(filename):
    from config import CONFIG
    safe = os.path.basename(filename)
    folder = CONFIG['OUTPUT_FOLDER']
    if not (Path(folder) / safe).exists():
        abort(404)
    return send_from_directory(folder, safe)

@system_bp.route('/cleanup', methods=['POST'])
def cleanup():
    from config import cleanup_old_files
    cleanup_old_files()
    return jsonify({"status": "cleaned"})
