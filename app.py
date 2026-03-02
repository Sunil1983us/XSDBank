#!/usr/bin/env python3
"""
app.py  –  ISO 20022 XSD Toolkit  (entry point)
All routes live in routes/*.py blueprints.
"""

import os
from flask import Flask

from config import CONFIG, logger, cleanup_old_files
from routes.system   import system_bp
from routes.library  import library_bp
from routes.tools_xsd import xsd_bp
from routes.tools_run import run_bp

# ── App ───────────────────────────────────────────────────────────────────────

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = CONFIG['MAX_CONTENT_LENGTH']
app.config['UPLOAD_FOLDER']      = CONFIG['UPLOAD_FOLDER']
app.config['OUTPUT_FOLDER']      = CONFIG['OUTPUT_FOLDER']
app.config['TOOLS_FOLDER']       = CONFIG['TOOLS_FOLDER']
app.secret_key                   = CONFIG['SECRET_KEY']

# Ensure required folders exist
for folder in (CONFIG['UPLOAD_FOLDER'], CONFIG['OUTPUT_FOLDER'], CONFIG['LOG_FOLDER']):
    os.makedirs(folder, exist_ok=True)

# ── Blueprints ────────────────────────────────────────────────────────────────

app.register_blueprint(system_bp)   # /  /download  /preview  /health  /status  /limits  /cleanup
app.register_blueprint(library_bp)  # /library  /library/folder  /library/upload  /library/delete  etc.
app.register_blueprint(xsd_bp)      # /upload  /page_count  /run_tool
app.register_blueprint(run_bp)      # /run  /detect_ig_sections  /detect_yaml_endpoints

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print(f"""
    ╔══════════════════════════════════════════════════════╗
    ║       ISO 20022 XSD Toolkit  –  Local Deployment     ║
    ║  URL: http://{CONFIG['HOST']}:{CONFIG['PORT']}
    ║  Press Ctrl+C to stop                                ║
    ╚══════════════════════════════════════════════════════╝
    """)
    logger.info(f"Starting on {CONFIG['HOST']}:{CONFIG['PORT']}")
    cleanup_old_files()
    app.run(host=CONFIG['HOST'], port=CONFIG['PORT'],
            debug=CONFIG['DEBUG'], threaded=True)
