"""
routes/library.py  –  Document Library blueprint
Handles: GET /library, POST /library/folder, POST /library/upload,
         POST /library/delete, POST /library/rename, GET /library_file
"""

import re
import shutil
from pathlib import Path
from flask import Blueprint, request, jsonify, send_file

from config import CONFIG, logger

library_bp = Blueprint('library', __name__)

# ── Library constants ─────────────────────────────────────────────────────────

LIBRARY_FOLDER = Path(__file__).parent.parent / 'library'
LIBRARY_EXTS   = {'.xsd', '.xlsx', '.xlsm', '.pdf', '.xml'}
FILE_ICONS     = {'.xsd': '📐', '.xlsx': '📊', '.xlsm': '📊', '.pdf': '📄', '.xml': '📝'}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_library_tree(root: Path) -> list:
    items = []
    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        return items
    for entry in entries:
        if entry.name.startswith('.') or entry.name == 'README.md':
            continue
        rel = entry.relative_to(LIBRARY_FOLDER).as_posix()
        if entry.is_dir():
            children = _build_library_tree(entry)
            items.append({
                'name': entry.name, 'type': 'folder', 'path': rel,
                'children': children,
                'count': sum(1 for c in children if c['type'] == 'file') +
                         sum(c.get('count', 0) for c in children if c['type'] == 'folder')
            })
        elif entry.is_file() and entry.suffix.lower() in LIBRARY_EXTS:
            items.append({
                'name': entry.name, 'type': 'file', 'path': rel,
                'ext': entry.suffix.lower(),
                'icon': FILE_ICONS.get(entry.suffix.lower(), '📄'),
                'size_kb': round(entry.stat().st_size / 1024, 1)
            })
    return items


def _safe_lib_path(rel: str) -> Path:
    """Resolve a relative library path, raising ValueError if it escapes."""
    target = (LIBRARY_FOLDER / rel.lstrip('/')).resolve()
    target.relative_to(LIBRARY_FOLDER.resolve())   # raises ValueError if outside
    return target


def _sanitise_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    name = re.sub(r'\.\.+', '.', name)
    name = name.strip('. ')
    return name[:120] if name else 'unnamed'


# ── Routes ────────────────────────────────────────────────────────────────────

@library_bp.route('/library', methods=['GET'])
def get_library():
    LIBRARY_FOLDER.mkdir(exist_ok=True)
    return jsonify({'success': True, 'tree': _build_library_tree(LIBRARY_FOLDER)})


@library_bp.route('/library/folder', methods=['POST'])
def library_create_folder():
    data       = request.get_json(force=True, silent=True) or {}
    parent_rel = data.get('path', '').strip('/')
    name       = _sanitise_name(data.get('name', ''))
    if not name:
        return jsonify({'success': False, 'error': 'Folder name is required'}), 400
    try:
        parent  = _safe_lib_path(parent_rel) if parent_rel else LIBRARY_FOLDER.resolve()
        new_dir = parent / name
        if new_dir.exists():
            return jsonify({'success': False, 'error': f'"{name}" already exists'}), 409
        new_dir.mkdir(parents=True)
        rel = new_dir.relative_to(LIBRARY_FOLDER).as_posix()
        logger.info(f"Library: created folder {rel}")
        return jsonify({'success': True, 'path': rel})
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid path'}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/library/upload', methods=['POST'])
def library_upload():
    folder_rel = request.form.get('folder_path', '').strip('/')
    try:
        target_dir = _safe_lib_path(folder_rel) if folder_rel else LIBRARY_FOLDER.resolve()
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid folder path'}), 403
    if not target_dir.is_dir():
        return jsonify({'success': False, 'error': 'Target folder does not exist'}), 404

    files  = request.files.getlist('files')
    saved, errors = [], []
    for f in files:
        if not f or not f.filename:
            continue
        ext = Path(f.filename).suffix.lower()
        if ext not in LIBRARY_EXTS:
            errors.append(f'{f.filename}: unsupported type ({ext})')
            continue
        safe_name = _sanitise_name(Path(f.filename).stem) + ext
        dest = target_dir / safe_name
        counter = 1
        while dest.exists():
            dest = target_dir / f"{_sanitise_name(Path(f.filename).stem)}_{counter}{ext}"
            counter += 1
        f.save(str(dest))
        rel = dest.relative_to(LIBRARY_FOLDER).as_posix()
        saved.append({'name': dest.name, 'path': rel, 'ext': ext,
                      'icon': FILE_ICONS.get(ext, '📄'),
                      'size_kb': round(dest.stat().st_size / 1024, 1)})
        logger.info(f"Library: uploaded {rel}")

    if not saved and errors:
        return jsonify({'success': False, 'error': '; '.join(errors)}), 400
    return jsonify({'success': True, 'files': saved, 'errors': errors})


@library_bp.route('/library/delete', methods=['POST'])
def library_delete():
    data = request.get_json(force=True, silent=True) or {}
    rel  = data.get('path', '').strip('/')
    if not rel:
        return jsonify({'success': False, 'error': 'Path required'}), 400
    try:
        target = _safe_lib_path(rel)
        if not target.exists():
            return jsonify({'success': False, 'error': 'Not found'}), 404
        if target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(str(target))
        logger.info(f"Library: deleted {rel}")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid path'}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/library/rename', methods=['POST'])
def library_rename():
    data     = request.get_json(force=True, silent=True) or {}
    rel      = data.get('path', '').strip('/')
    new_name = _sanitise_name(data.get('name', ''))
    if not rel or not new_name:
        return jsonify({'success': False, 'error': 'path and name required'}), 400
    try:
        target = _safe_lib_path(rel)
        if not target.exists():
            return jsonify({'success': False, 'error': 'Not found'}), 404
        if target.is_file():
            ext = target.suffix
            if not new_name.endswith(ext):
                new_name = _sanitise_name(Path(new_name).stem) + ext
        dest = target.parent / new_name
        if dest.exists():
            return jsonify({'success': False, 'error': f'"{new_name}" already exists'}), 409
        target.rename(dest)
        new_rel = dest.relative_to(LIBRARY_FOLDER).as_posix()
        logger.info(f"Library: renamed {rel} → {new_rel}")
        return jsonify({'success': True, 'path': new_rel, 'name': dest.name})
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid path'}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/library_file', methods=['GET'])
def get_library_file():
    rel_path = request.args.get('path', '').lstrip('/')
    if not rel_path:
        return jsonify({'success': False, 'error': 'No path specified'}), 400
    try:
        target = (LIBRARY_FOLDER / rel_path).resolve()
        target.relative_to(LIBRARY_FOLDER.resolve())
    except (ValueError, Exception):
        return jsonify({'success': False, 'error': 'Invalid path'}), 403
    if not target.exists() or not target.is_file():
        return jsonify({'success': False, 'error': 'File not found'}), 404
    if target.suffix.lower() not in LIBRARY_EXTS:
        return jsonify({'success': False, 'error': 'File type not allowed'}), 403
    return send_file(str(target), as_attachment=False,
                     download_name=target.name,
                     mimetype='application/octet-stream')
