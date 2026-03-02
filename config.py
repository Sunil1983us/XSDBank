"""
config.py  –  Shared configuration, logging, and utilities
Imported by app.py and all route blueprints.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime


def load_config() -> dict:
    config = {
        'HOST':              os.environ.get('TOOLKIT_HOST', '0.0.0.0'),
        'PORT':              int(os.environ.get('TOOLKIT_PORT', '5000')),
        'DEBUG':             os.environ.get('TOOLKIT_DEBUG', 'False').lower() == 'true',
        'SECRET_KEY':        os.environ.get('TOOLKIT_SECRET_KEY',
                                            'change-this-in-production-' + os.urandom(16).hex()),
        'MAX_CONTENT_LENGTH': int(os.environ.get('TOOLKIT_MAX_UPLOAD_MB', '100')) * 1024 * 1024,
        'MAX_FILE_SIZE_MB':  int(os.environ.get('TOOLKIT_MAX_FILE_SIZE_MB', '50')),
        'UPLOAD_FOLDER':     os.environ.get('TOOLKIT_UPLOAD_FOLDER', 'static/uploads'),
        'OUTPUT_FOLDER':     os.environ.get('TOOLKIT_OUTPUT_FOLDER', 'static/outputs'),
        'TOOLS_FOLDER':      os.environ.get('TOOLKIT_TOOLS_FOLDER', 'tools'),
        'LOG_FOLDER':        os.environ.get('TOOLKIT_LOG_FOLDER', 'logs'),
        'TIMEOUT_SECONDS':   int(os.environ.get('TOOLKIT_TIMEOUT', '300')),
        'CLEANUP_HOURS':     int(os.environ.get('TOOLKIT_CLEANUP_HOURS', '24')),
        'AUTO_CLEANUP_ENABLED': os.environ.get('TOOLKIT_AUTO_CLEANUP', 'True').lower() == 'true',
        'ALLOWED_EXTENSIONS': {'xsd', 'xml', 'zip', 'pdf', 'yaml', 'yml', 'json'},
        'MAX_FILES_PER_UPLOAD': int(os.environ.get('TOOLKIT_MAX_FILES', '50')),
        'MAX_BATCH_FILES':   int(os.environ.get('TOOLKIT_MAX_BATCH', '500')),
    }

    config_file = Path('config.json')
    if config_file.exists():
        try:
            with open(config_file) as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")

    # Make all folder paths absolute relative to this file's directory
    base = os.path.dirname(os.path.abspath(__file__))
    for key in ('UPLOAD_FOLDER', 'OUTPUT_FOLDER', 'TOOLS_FOLDER', 'LOG_FOLDER'):
        if not os.path.isabs(config[key]):
            config[key] = os.path.join(base, config[key])

    return config


CONFIG = load_config()


def setup_logging() -> logging.Logger:
    log_folder = Path(CONFIG['LOG_FOLDER'])
    log_folder.mkdir(exist_ok=True)
    log_file = log_folder / f"toolkit_{datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(
        level=logging.DEBUG if CONFIG['DEBUG'] else logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def cleanup_old_files():
    """Remove upload and output files older than CLEANUP_HOURS."""
    try:
        cutoff = time.time() - (CONFIG['CLEANUP_HOURS'] * 3600)
        for folder in (CONFIG['UPLOAD_FOLDER'], CONFIG['OUTPUT_FOLDER']):
            fp = Path(folder)
            if fp.exists():
                for f in fp.iterdir():
                    if f.is_file() and f.stat().st_mtime < cutoff:
                        f.unlink()
                        logger.info(f"Cleaned up: {f.name}")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
