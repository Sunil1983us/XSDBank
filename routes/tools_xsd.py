"""routes/tools_xsd.py – file upload endpoint"""
import os, uuid
from pathlib import Path
from flask import Blueprint, request, jsonify

xsd_bp = Blueprint('xsd', __name__)

ALLOWED = {'xsd','xml','zip','pdf','yaml','yml','json'}

def allowed(name):
    return '.' in name and name.rsplit('.', 1)[1].lower() in ALLOWED

@xsd_bp.route('/upload', methods=['POST'])
def upload():
    from config import CONFIG
    folder = Path(CONFIG['UPLOAD_FOLDER'])
    folder.mkdir(parents=True, exist_ok=True)
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files provided"}), 400
    saved = []
    for f in files:
        if f and allowed(f.filename):
            safe = f"{uuid.uuid4().hex}_{os.path.basename(f.filename)}"
            dest = folder / safe
            f.save(str(dest))
            saved.append({"original": f.filename, "saved": safe, "path": str(dest)})
    return jsonify({"uploaded": saved})

@xsd_bp.route('/page_count', methods=['POST'])
def page_count():
    """Detect page count for PDF files (stub)."""
    return jsonify({"pages": 0})
