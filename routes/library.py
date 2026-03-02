"""routes/library.py – library file browser"""
import os
from pathlib import Path
from flask import Blueprint, jsonify, request, current_app

library_bp = Blueprint('library', __name__)

@library_bp.route('/library')
def library():
    from config import CONFIG
    lib = Path(CONFIG.get('LIBRARY_FOLDER', 'library'))
    lib.mkdir(exist_ok=True)
    items = [{"name": f.name, "size": f.stat().st_size, "is_dir": f.is_dir()}
             for f in sorted(lib.iterdir())]
    return jsonify({"items": items})
