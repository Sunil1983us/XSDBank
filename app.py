#!/usr/bin/env python3
"""
ISO 20022 XSD Toolkit Web Application
Local Bank Network Deployment Version

Key Features:
- Secure configuration for internal networks
- Configurable via environment variables or config file
- Comprehensive logging
- Health monitoring endpoints
- No external cloud dependencies
"""

from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
import os
import sys
import logging
from pathlib import Path
from werkzeug.utils import secure_filename
import subprocess
import time
from datetime import datetime
import zipfile
import shutil
import json


def _generate_validation_html(result: dict, output_path: str, xml_name: str, xsd_name: str):
    """Generate HTML validation report"""
    
    valid_status = "✅ VALID" if result['valid'] else "❌ INVALID"
    status_class = "valid" if result['valid'] else "invalid"
    
    issues_html = ""
    for i, issue in enumerate(result.get('issues', []), 1):
        severity_class = issue['severity'].lower()
        severity_icon = "❌" if issue['severity'] == 'ERROR' else "⚠️" if issue['severity'] == 'WARNING' else "ℹ️"
        
        issues_html += f"""
        <div class="issue {severity_class}">
            <div class="issue-header">
                <span class="severity">{severity_icon} {issue['severity']}</span>
                <span class="category">{issue['category']}</span>
            </div>
            <div class="issue-element"><strong>Element:</strong> {issue['element']}</div>
            {f"<div class='issue-path'><strong>Path:</strong> {issue['path']}</div>" if issue.get('path') else ""}
            {f"<div class='issue-line'><strong>Line:</strong> {issue['line']}</div>" if issue.get('line') else ""}
            <div class="issue-message"><strong>Message:</strong> {issue['message']}</div>
            {f"<div class='issue-value'><strong>Value:</strong> <code>{issue['value']}</code></div>" if issue.get('value') else ""}
            {f"<div class='issue-expected'><strong>Expected:</strong> {issue['expected']}</div>" if issue.get('expected') else ""}
            {f"<div class='issue-suggestion'><strong>💡 Suggestion:</strong> {issue['suggestion']}</div>" if issue.get('suggestion') else ""}
        </div>
        """
    
    categories_html = ""
    for cat, count in sorted(result.get('by_category', {}).items()):
        categories_html += f"<li><strong>{cat}:</strong> {count}</li>"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>XML Validation Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .status {{ font-size: 24px; padding: 10px 20px; border-radius: 8px; display: inline-block; margin-top: 15px; }}
        .status.valid {{ background: #10b981; }}
        .status.invalid {{ background: #ef4444; }}
        .summary {{ background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .summary h2 {{ margin-top: 0; color: #1a1a2e; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat {{ background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }}
        .stat .number {{ font-size: 32px; font-weight: bold; color: #1a1a2e; }}
        .stat .label {{ color: #666; font-size: 14px; }}
        .stat.errors .number {{ color: #ef4444; }}
        .stat.warnings .number {{ color: #f59e0b; }}
        .issues {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .issues h2 {{ margin-top: 0; color: #1a1a2e; }}
        .issue {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; margin-bottom: 15px; }}
        .issue.error {{ border-left: 4px solid #ef4444; background: #fef2f2; }}
        .issue.warning {{ border-left: 4px solid #f59e0b; background: #fffbeb; }}
        .issue.info {{ border-left: 4px solid #3b82f6; background: #eff6ff; }}
        .issue-header {{ display: flex; justify-content: space-between; margin-bottom: 10px; }}
        .severity {{ font-weight: bold; }}
        .category {{ background: #e5e7eb; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
        .issue-message {{ margin: 10px 0; }}
        .issue-suggestion {{ color: #059669; margin-top: 10px; padding: 10px; background: #ecfdf5; border-radius: 4px; }}
        code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
        .file-info {{ color: #94a3b8; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 XML Validation Report</h1>
            <div class="file-info">
                <div>📄 XML: {xml_name}</div>
                <div>📋 XSD: {xsd_name}</div>
                <div>🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
            <div class="status {status_class}">{valid_status}</div>
        </div>
        
        <div class="summary">
            <h2>📊 Summary</h2>
            <div class="stats">
                <div class="stat">
                    <div class="number">{result['summary']['total_issues']}</div>
                    <div class="label">Total Issues</div>
                </div>
                <div class="stat errors">
                    <div class="number">{result['summary']['errors']}</div>
                    <div class="label">Errors</div>
                </div>
                <div class="stat warnings">
                    <div class="number">{result['summary']['warnings']}</div>
                    <div class="label">Warnings</div>
                </div>
                <div class="stat">
                    <div class="number">{result['summary']['info']}</div>
                    <div class="label">Info</div>
                </div>
            </div>
            {f"<h3>By Category</h3><ul>{categories_html}</ul>" if categories_html else ""}
        </div>
        
        <div class="issues">
            <h2>📋 Issues Detail</h2>
            {issues_html if issues_html else "<p>✅ No issues found!</p>"}
        </div>
    </div>
</body>
</html>"""
    
    with open(output_path, 'w') as f:
        f.write(html)

# ============================================================================
# CONFIGURATION
# ============================================================================

def load_config():
    """Load configuration from file or environment variables"""
    config = {
        # Server settings
        'HOST': os.environ.get('TOOLKIT_HOST', '0.0.0.0'),
        'PORT': int(os.environ.get('TOOLKIT_PORT', '5000')),
        'DEBUG': os.environ.get('TOOLKIT_DEBUG', 'False').lower() == 'true',
        
        # Security
        'SECRET_KEY': os.environ.get('TOOLKIT_SECRET_KEY', 'change-this-in-production-' + os.urandom(16).hex()),
        'MAX_CONTENT_LENGTH': int(os.environ.get('TOOLKIT_MAX_UPLOAD_MB', '100')) * 1024 * 1024,
        'MAX_FILE_SIZE_MB': int(os.environ.get('TOOLKIT_MAX_FILE_SIZE_MB', '50')),
        
        # Folders
        'UPLOAD_FOLDER': os.environ.get('TOOLKIT_UPLOAD_FOLDER', 'static/uploads'),
        'OUTPUT_FOLDER': os.environ.get('TOOLKIT_OUTPUT_FOLDER', 'static/outputs'),
        'TOOLS_FOLDER': os.environ.get('TOOLKIT_TOOLS_FOLDER', 'tools'),
        'LOG_FOLDER': os.environ.get('TOOLKIT_LOG_FOLDER', 'logs'),
        
        # Processing
        'TIMEOUT_SECONDS': int(os.environ.get('TOOLKIT_TIMEOUT', '300')),
        'CLEANUP_HOURS': int(os.environ.get('TOOLKIT_CLEANUP_HOURS', '24')),
        'AUTO_CLEANUP_ENABLED': os.environ.get('TOOLKIT_AUTO_CLEANUP', 'True').lower() == 'true',
        
        # Allowed file extensions
        'ALLOWED_EXTENSIONS': {'xsd', 'xml', 'zip', 'pdf', 'yaml', 'yml', 'json'},
        
        # Limits
        'MAX_FILES_PER_UPLOAD': int(os.environ.get('TOOLKIT_MAX_FILES', '50')),
        'MAX_BATCH_FILES': int(os.environ.get('TOOLKIT_MAX_BATCH', '500')),
    }
    
    # Load from config file if exists
    config_file = Path('config.json')
    if config_file.exists():
        try:
            with open(config_file) as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")
    
    return config

# Load configuration
CONFIG = load_config()

# Resolve all folder paths to absolute, anchored to app.py's own directory.
# This ensures tools can be imported and files found regardless of the working
# directory at the time Flask handles a request.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for _key in ('UPLOAD_FOLDER', 'OUTPUT_FOLDER', 'TOOLS_FOLDER', 'LOG_FOLDER'):
    if not os.path.isabs(CONFIG[_key]):
        CONFIG[_key] = os.path.join(_BASE_DIR, CONFIG[_key])

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure comprehensive logging"""
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

# ============================================================================
# FLASK APP
# ============================================================================

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = CONFIG['MAX_CONTENT_LENGTH']
app.config['UPLOAD_FOLDER'] = CONFIG['UPLOAD_FOLDER']
app.config['OUTPUT_FOLDER'] = CONFIG['OUTPUT_FOLDER']
app.config['TOOLS_FOLDER'] = CONFIG['TOOLS_FOLDER']
app.secret_key = CONFIG['SECRET_KEY']

# Ensure folders exist
for folder in [CONFIG['UPLOAD_FOLDER'], CONFIG['OUTPUT_FOLDER'], CONFIG['LOG_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# ============================================================================
# UTILITIES
# ============================================================================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in CONFIG['ALLOWED_EXTENSIONS']

def cleanup_old_files():
    """Remove files older than configured hours"""
    try:
        cutoff = time.time() - (CONFIG['CLEANUP_HOURS'] * 3600)
        
        for folder in [CONFIG['UPLOAD_FOLDER'], CONFIG['OUTPUT_FOLDER']]:
            folder_path = Path(folder)
            if folder_path.exists():
                for file_path in folder_path.iterdir():
                    if file_path.is_file() and file_path.stat().st_mtime < cutoff:
                        file_path.unlink()
                        logger.info(f"Cleaned up old file: {file_path.name}")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve main page"""
    logger.info("Main page accessed")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads with comprehensive validation"""
    try:
        if 'files[]' not in request.files:
            logger.warning("Upload attempted without files")
            return jsonify({
                'success': False,
                'error': 'No files uploaded',
                'error_code': 'NO_FILES',
                'suggestion': 'Please select at least one file to upload'
            }), 400
        
        files = request.files.getlist('files[]')
        
        # Check file count limit
        if len(files) > CONFIG['MAX_FILES_PER_UPLOAD']:
            logger.warning(f"Too many files: {len(files)} > {CONFIG['MAX_FILES_PER_UPLOAD']}")
            return jsonify({
                'success': False,
                'error': f'Too many files. Maximum {CONFIG["MAX_FILES_PER_UPLOAD"]} files per upload.',
                'error_code': 'TOO_MANY_FILES',
                'suggestion': 'Upload files in smaller batches or use a ZIP file'
            }), 400
        
        uploaded_files = []
        errors = []
        max_size_bytes = CONFIG['MAX_FILE_SIZE_MB'] * 1024 * 1024
        
        for file in files:
            if not file or not file.filename:
                continue
                
            filename = file.filename
            
            # Check file extension
            if not allowed_file(filename):
                ext = filename.rsplit('.', 1)[-1] if '.' in filename else 'none'
                errors.append({
                    'file': filename,
                    'error': f'Invalid file type: .{ext}',
                    'suggestion': 'Only .xsd, .xml, .zip, and .pdf files are allowed'
                })
                continue
            
            # Check file size (read content to check)
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
            
            if file_size > max_size_bytes:
                size_mb = file_size / (1024 * 1024)
                errors.append({
                    'file': filename,
                    'error': f'File too large: {size_mb:.1f}MB (max: {CONFIG["MAX_FILE_SIZE_MB"]}MB)',
                    'suggestion': 'Split large files or increase MAX_FILE_SIZE_MB in config'
                })
                continue
            
            if file_size == 0:
                errors.append({
                    'file': filename,
                    'error': 'Empty file',
                    'suggestion': 'Please upload a file with content'
                })
                continue
            
            # Save file
            safe_filename = secure_filename(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            unique_filename = f"{timestamp}_{safe_filename}"
            filepath = os.path.join(CONFIG['UPLOAD_FOLDER'], unique_filename)
            
            file.save(filepath)
            uploaded_files.append(unique_filename)
            logger.info(f"File uploaded: {unique_filename} ({file_size} bytes)")
        
        if not uploaded_files and errors:
            return jsonify({
                'success': False,
                'error': 'All files failed validation',
                'error_code': 'VALIDATION_FAILED',
                'details': errors
            }), 400
        
        if not uploaded_files:
            logger.warning("No valid files in upload")
            return jsonify({
                'success': False,
                'error': 'No valid files uploaded',
                'error_code': 'NO_VALID_FILES',
                'suggestion': 'Only .xsd, .xml, and .zip files are allowed'
            }), 400
        
        response = {
            'success': True,
            'files': uploaded_files,
            'count': len(uploaded_files)
        }
        
        if errors:
            response['warnings'] = errors
            response['message'] = f'{len(uploaded_files)} files uploaded, {len(errors)} skipped'
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Upload failed due to server error',
            'error_code': 'SERVER_ERROR',
            'details': str(e) if CONFIG['DEBUG'] else 'Contact administrator'
        }), 500

@app.route('/page_count', methods=['POST'])
def page_count():
    """Return page count for a PDF.
    Accepts multipart FormData:
      - files: uploaded PDF file  OR
      - library_path: relative library path
    Also accepts legacy JSON: { "file": "filename.pdf" }
    """
    try:
        import pdfplumber
        pdf_path = None

        # Multipart: uploaded file
        for f in request.files.getlist('files'):
            if f and f.filename:
                dest = Path(CONFIG['UPLOAD_FOLDER']) / f.filename.replace('/', '_')
                f.save(str(dest))
                pdf_path = str(dest)
                break

        # Multipart: library file
        if not pdf_path:
            lib_rel = request.form.get('library_path', '')
            if lib_rel:
                try:
                    target = _safe_lib_path(lib_rel)
                    if target.is_file():
                        pdf_path = str(target)
                except Exception:
                    pass

        # Legacy JSON fallback
        if not pdf_path and request.is_json:
            data = request.get_json() or {}
            file_id = data.get('file', '')
            candidate = os.path.join(CONFIG['UPLOAD_FOLDER'], os.path.basename(file_id))
            if os.path.exists(candidate):
                pdf_path = candidate

        if not pdf_path:
            return jsonify({'error': 'File not found'}), 404

        with pdfplumber.open(pdf_path) as pdf:
            return jsonify({'pages': len(pdf.pages), 'file': os.path.basename(pdf_path)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/run_tool', methods=['POST'])
def run_tool():
    """Execute analysis tool with comprehensive error handling"""
    start_time = time.time()
    
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid request: No JSON data',
                'error_code': 'INVALID_REQUEST'
            }), 400
        
        tool = data.get('tool')
        files = data.get('files', [])
        options = data.get('options', {})
        
        # Validate tool
        valid_tools = ['comprehensive', 'document', 'compare', 'multi_compare', 'test_data',
                       'xml_validate', 'xml_diff', 'batch_validate', 'mapping_template', 'xml_transform',
                       'xsd_explorer',
                       'pdf_compare', 'pdf_table_extract', 'pdf_merge', 'pdf_split',
                       'ig_extract', 'ig_diff', 'ig_change_tracker', 'ig_mapping', 'xsd_ig_analysis']
        
        if not tool:
            return jsonify({
                'success': False,
                'error': 'No tool specified',
                'error_code': 'MISSING_TOOL',
                'suggestion': f'Valid tools: {", ".join(valid_tools)}'
            }), 400
        
        if tool not in valid_tools:
            return jsonify({
                'success': False,
                'error': f'Unknown tool: {tool}',
                'error_code': 'INVALID_TOOL',
                'suggestion': f'Valid tools: {", ".join(valid_tools)}'
            }), 400
        
        if not files:
            return jsonify({
                'success': False,
                'error': 'No files specified',
                'error_code': 'MISSING_FILES',
                'suggestion': 'Upload files first, then run the tool'
            }), 400
        
        # Also accept library_files: relative paths within the library folder
        library_files = data.get('library_files', [])

        # Validate file paths
        file_paths = []
        missing_files = []
        
        for f in files:
            fp = os.path.join(CONFIG['UPLOAD_FOLDER'], f)
            if os.path.exists(fp):
                file_paths.append(fp)
            else:
                missing_files.append(f)

        # Resolve library file paths (with security check)
        for rel in library_files:
            try:
                target = (LIBRARY_FOLDER / rel.lstrip('/')).resolve()
                target.relative_to(LIBRARY_FOLDER.resolve())  # raises if escaping
                if target.is_file():
                    file_paths.append(str(target))
                else:
                    missing_files.append(rel)
            except (ValueError, Exception):
                missing_files.append(rel)

        if missing_files:
            logger.error(f"Files not found: {missing_files}")
            return jsonify({
                'success': False,
                'error': f'File(s) not found: {", ".join(missing_files)}',
                'error_code': 'FILES_NOT_FOUND',
                'suggestion': 'Files may have been cleaned up. Please re-upload.'
            }), 400
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_base = f"output_{timestamp}"
        
        logger.info(f"Running tool: {tool} on {len(files)} file(s) with options: {options}")
        result = execute_tool(tool, file_paths, output_base, options)
        
        # Add execution time
        execution_time = time.time() - start_time
        result['execution_time_seconds'] = round(execution_time, 2)
        
        if result.get('success'):
            logger.info(f"Tool {tool} completed successfully in {execution_time:.2f}s")
        else:
            logger.warning(f"Tool {tool} failed: {result.get('error')}")
        
        return jsonify(result)
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        return jsonify({
            'success': False,
            'error': 'Invalid JSON in request',
            'error_code': 'JSON_ERROR'
        }), 400
        
    except subprocess.TimeoutExpired:
        logger.error(f"Tool execution timed out after {CONFIG['TIMEOUT_SECONDS']}s")
        return jsonify({
            'success': False,
            'error': f'Tool execution timed out after {CONFIG["TIMEOUT_SECONDS"]} seconds',
            'error_code': 'TIMEOUT',
            'suggestion': 'Try with fewer/smaller files or increase TOOLKIT_TIMEOUT'
        }), 504
        
    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Tool execution failed',
            'error_code': 'EXECUTION_ERROR',
            'details': str(e) if CONFIG['DEBUG'] else 'Check server logs for details'
        }), 500

def execute_tool(tool, file_paths, output_base, options):
    """Execute the specified analysis tool"""
    try:
        output_dir = CONFIG['OUTPUT_FOLDER']
        tools_dir = CONFIG['TOOLS_FOLDER']
        timeout = CONFIG['TIMEOUT_SECONDS']
        
        if tool == 'comprehensive':
            # Comprehensive analyzer
            script = os.path.join(tools_dir, 'schema_analyzer.py')
            output_file = os.path.join(output_dir, f"{output_base}_comprehensive.xlsx")
            
            cmd = [sys.executable, script, file_paths[0], '-o', output_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0 and os.path.exists(output_file):
                return {
                    'success': True,
                    'message': 'Comprehensive analysis complete with ALL metadata!',
                    'files': [os.path.basename(output_file)]
                }
            else:
                error_msg = result.stderr or result.stdout or 'Unknown error'
                return {'success': False, 'error': f'Analysis failed: {error_msg}'}
        
        elif tool == 'document':
            script = os.path.join(tools_dir, 'schema_documenter.py')
            output_file = os.path.join(output_dir, f"{output_base}_docs.xlsx")
            
            cmd = [sys.executable, script, file_paths[0], '-o', output_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0 and os.path.exists(output_file):
                return {
                    'success': True,
                    'message': 'Documentation generated!',
                    'files': [os.path.basename(output_file)]
                }
            else:
                return {'success': False, 'error': 'Failed to generate documentation'}
        
        elif tool == 'compare':
            if len(file_paths) < 2:
                return {'success': False, 'error': 'Need 2 files to compare'}
            
            script = os.path.join(tools_dir, 'schema_comparator.py')
            output_file = os.path.join(output_dir, f"{output_base}_compare.xlsx")
            
            cmd = [sys.executable, script, file_paths[0], file_paths[1], '-o', output_file]
            
            if options.get('name1'):
                cmd.extend(['-n1', options['name1']])
            if options.get('name2'):
                cmd.extend(['-n2', options['name2']])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                base = output_file.replace('.xlsx', '')
                generated_files = []
                for ext in ['.xlsx', '.docx', '.html']:
                    f = f"{base}{ext}"
                    if os.path.exists(f):
                        generated_files.append(os.path.basename(f))
                
                return {
                    'success': True,
                    'message': f'Comparison completed! {len(generated_files)} files generated',
                    'files': generated_files
                }
            else:
                return {'success': False, 'error': 'Comparison failed'}
        
        elif tool == 'multi_compare':
            if len(file_paths) < 2:
                return {'success': False, 'error': 'Need at least 2 files'}
            
            script = os.path.join(tools_dir, 'multi_comparator.py')
            output_base_path = os.path.join(output_dir, output_base)
            
            cmd = [sys.executable, script] + file_paths + ['-o', output_base_path]
            
            if options.get('names'):
                names = [n.strip() for n in options['names'].split(',') if n.strip()]
                if names:
                    cmd.extend(['-n'] + names)
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * 2)
            
            if result.returncode == 0:
                generated_files = []
                for f in os.listdir(output_dir):
                    if f.startswith(output_base):
                        generated_files.append(f)
                
                if generated_files:
                    return {
                        'success': True,
                        'message': f'Multi-comparison complete! Generated {len(generated_files)} files',
                        'files': sorted(generated_files)
                    }
                else:
                    return {'success': False, 'error': 'No output files generated'}
            else:
                error_msg = result.stderr or result.stdout or 'Unknown error'
                return {'success': False, 'error': f'Multi-comparison failed: {error_msg[:200]}'}
        
        elif tool == 'test_data':
            script = os.path.join(tools_dir, 'xml_generator.py')
            num_files = int(options.get('num_files', 10))
            profile = options.get('profile', 'domestic_sepa')
            mandatory_only = options.get('mandatory_only', False)
            output_folder = os.path.join(output_dir, f"{output_base}_testdata")
            
            cmd = [sys.executable, script, file_paths[0], 
                   '-n', str(num_files), 
                   '--profile', profile,
                   '-o', output_folder]
            
            if mandatory_only:
                cmd.append('--mandatory')
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0 and os.path.exists(output_folder):
                zip_path = f"{output_folder}.zip"
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files_list in os.walk(output_folder):
                        for file in files_list:
                            filepath = os.path.join(root, file)
                            zipf.write(filepath, os.path.basename(filepath))
                
                shutil.rmtree(output_folder)
                
                return {
                    'success': True,
                    'message': f'Generated {num_files} test XML files with {profile} profile!',
                    'files': [os.path.basename(zip_path)]
                }
            else:
                return {'success': False, 'error': 'Test data generation failed'}
        
        elif tool == 'xml_validate':
            script = os.path.join(tools_dir, 'xml_validator.py')
            
            # First file is XML, second is XSD (or ZIP containing XSD)
            if len(file_paths) < 2:
                return {'success': False, 'error': 'Need both XML file and XSD file'}
            
            xml_file = file_paths[0]
            xsd_file = file_paths[1]
            
            # Determine which is XML and which is XSD
            if xml_file.endswith('.xsd') or xml_file.endswith('.zip'):
                xml_file, xsd_file = xsd_file, xml_file
            
            output_json = os.path.join(output_dir, f"{output_base}_validation.json")
            output_html = os.path.join(output_dir, f"{output_base}_validation.html")
            
            cmd = [sys.executable, script, xml_file, xsd_file, '--json', '-o', output_json]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            # Read the JSON result
            if os.path.exists(output_json):
                with open(output_json, 'r') as f:
                    validation_result = json.load(f)
                
                # Generate HTML report
                _generate_validation_html(validation_result, output_html, 
                                         os.path.basename(xml_file), 
                                         os.path.basename(xsd_file))
                
                return {
                    'success': True,
                    'message': f"Validation complete: {'✅ VALID' if validation_result['valid'] else '❌ ' + str(validation_result['summary']['errors']) + ' errors found'}",
                    'files': [os.path.basename(output_html), os.path.basename(output_json)],
                    'validation': validation_result
                }
            else:
                error_msg = result.stderr or result.stdout or 'Validation failed'
                return {'success': False, 'error': f'Validation failed: {error_msg[:200]}'}
        
        elif tool == 'xml_diff':
            script = os.path.join(tools_dir, 'xml_diff.py')
            
            # Need exactly 2 XML files
            if len(file_paths) < 2:
                return {'success': False, 'error': 'Need 2 XML files to compare'}
            
            xml_file1 = file_paths[0]
            xml_file2 = file_paths[1]
            
            output_html = os.path.join(output_dir, f"{output_base}_diff.html")
            output_json = os.path.join(output_dir, f"{output_base}_diff.json")
            
            cmd = [sys.executable, script, xml_file1, xml_file2, '-o', output_html]
            
            # Add options
            if options.get('ignore_order'):
                cmd.append('--ignore-order')
            if options.get('compare_attributes'):
                cmd.append('--compare-attributes')
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if os.path.exists(output_html):
                # Also save JSON
                cmd_json = [sys.executable, script, xml_file1, xml_file2, '--json']
                result_json = subprocess.run(cmd_json, capture_output=True, text=True, timeout=timeout)
                
                if result_json.stdout:
                    try:
                        diff_result = json.loads(result_json.stdout)
                        with open(output_json, 'w') as f:
                            json.dump(diff_result, f, indent=2)
                        
                        status = "✅ IDENTICAL" if diff_result.get('identical') else f"❌ {diff_result['summary']['total_differences']} differences"
                        
                        return {
                            'success': True,
                            'message': f"Comparison complete: {status}",
                            'files': [os.path.basename(output_html), os.path.basename(output_json)],
                            'diff': diff_result
                        }
                    except json.JSONDecodeError:
                        pass
                
                return {
                    'success': True,
                    'message': 'Comparison complete',
                    'files': [os.path.basename(output_html)]
                }
            else:
                error_msg = result.stderr or result.stdout or 'Diff failed'
                return {'success': False, 'error': f'Diff failed: {error_msg[:200]}'}
        
        elif tool == 'batch_validate':
            script = os.path.join(tools_dir, 'batch_validator.py')
            
            # Need at least 1 XSD and 1 XML (or ZIP)
            if len(file_paths) < 2:
                return {'success': False, 'error': 'Need XSD file and XML files (or ZIP)'}
            
            # Find XSD file
            xsd_file = None
            xml_files = []
            
            for fp in file_paths:
                if fp.endswith('.xsd'):
                    xsd_file = fp
                else:
                    xml_files.append(fp)
            
            if not xsd_file:
                return {'success': False, 'error': 'No XSD file found'}
            
            if not xml_files:
                return {'success': False, 'error': 'No XML files found'}
            
            output_html = os.path.join(output_dir, f"{output_base}_batch_validation.html")
            output_json = os.path.join(output_dir, f"{output_base}_batch_validation.json")
            
            cmd = [sys.executable, script, xsd_file] + xml_files + ['-o', output_html]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * 3)
            
            # Also get JSON output
            cmd_json = [sys.executable, script, xsd_file] + xml_files + ['--json']
            result_json = subprocess.run(cmd_json, capture_output=True, text=True, timeout=timeout * 3)
            
            generated_files = []
            if os.path.exists(output_html):
                generated_files.append(os.path.basename(output_html))
            
            if result_json.stdout:
                try:
                    batch_result = json.loads(result_json.stdout)
                    with open(output_json, 'w') as f:
                        json.dump(batch_result, f, indent=2)
                    generated_files.append(os.path.basename(output_json))
                    
                    summary = batch_result.get('summary', {})
                    return {
                        'success': True,
                        'message': f"Batch validation complete: {summary.get('passed', 0)} passed, {summary.get('failed', 0)} failed ({summary.get('pass_rate', 'N/A')})",
                        'files': generated_files,
                        'batch_result': batch_result
                    }
                except json.JSONDecodeError:
                    pass
            
            if generated_files:
                return {
                    'success': True,
                    'message': 'Batch validation complete',
                    'files': generated_files
                }
            else:
                error_msg = result.stderr or result.stdout or 'Batch validation failed'
                return {'success': False, 'error': f'Batch validation failed: {error_msg[:200]}'}
        
        elif tool == 'mapping_template':
            script = os.path.join(tools_dir, 'mapping_generator.py')
            
            if not file_paths:
                return {'success': False, 'error': 'Need XSD file'}
            
            xsd_file = file_paths[0]
            output_xlsx = os.path.join(output_dir, f"{output_base}_mapping_template.xlsx")
            
            cmd = [sys.executable, script, xsd_file, '-o', output_xlsx, '--verbose']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if os.path.exists(output_xlsx):
                return {
                    'success': True,
                    'message': 'Mapping template generated successfully!',
                    'files': [os.path.basename(output_xlsx)]
                }
            else:
                error_msg = result.stderr or result.stdout or 'Generation failed'
                return {'success': False, 'error': f'Mapping template generation failed: {error_msg[:200]}'}
        
        elif tool == 'xml_transform':
            script = os.path.join(tools_dir, 'xml_transformer.py')
            
            # Need 1 XML + 2 XSD files (source and target schema)
            if len(file_paths) < 3:
                return {'success': False, 'error': 'Need 1 XML file + 2 XSD files (source schema and target schema)'}
            
            # Identify files
            xml_file = None
            xsd_files = []
            
            for fp in file_paths:
                if fp.endswith('.xml'):
                    xml_file = fp
                elif fp.endswith('.xsd'):
                    xsd_files.append(fp)
            
            if not xml_file:
                return {'success': False, 'error': 'No XML file found'}
            
            if len(xsd_files) < 2:
                return {'success': False, 'error': 'Need 2 XSD files (source and target schema)'}
            
            source_xsd = xsd_files[0]
            target_xsd = xsd_files[1]
            
            output_xml = os.path.join(output_dir, f"{output_base}_transformed.xml")
            output_html = os.path.join(output_dir, f"{output_base}_transform_report.html")
            
            cmd = [sys.executable, script, xml_file, source_xsd, target_xsd, 
                   '-o', output_xml, '--report', output_html]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            generated_files = []
            if os.path.exists(output_xml):
                generated_files.append(os.path.basename(output_xml))
            if os.path.exists(output_html):
                generated_files.append(os.path.basename(output_html))
            
            if generated_files:
                return {
                    'success': True,
                    'message': f'XML transformation complete! Generated {len(generated_files)} files.',
                    'files': generated_files
                }
            else:
                error_msg = result.stderr or result.stdout or 'Transformation failed'
                return {'success': False, 'error': f'XML transformation failed: {error_msg[:200]}'}
        
        elif tool == 'pdf_compare':
            if len(file_paths) < 2:
                return {'success': False, 'error': 'Need 2 PDF files to compare'}

            pdf_a = next((f for f in file_paths if f.endswith('.pdf')), None)
            pdf_b = next((f for f in file_paths if f.endswith('.pdf') and f != pdf_a), None)
            # If both are PDFs pick first two
            pdfs = [f for f in file_paths if f.endswith('.pdf')]
            if len(pdfs) < 2:
                return {'success': False, 'error': 'Need 2 PDF files to compare'}
            pdf_a, pdf_b = pdfs[0], pdfs[1]

            output_html = os.path.join(output_dir, f"{output_base}_pdf_compare.html")

            try:
                sys.path.insert(0, tools_dir)
                from pdf_comparator import compare_pdfs
                result_data = compare_pdfs(pdf_a, pdf_b, output_html)
                sim = result_data['overall_similarity']
                return {
                    'success': True,
                    'message': f"PDF comparison complete — {sim}% overall similarity ({result_data['identical_pages']} identical, {result_data['changed_pages']} changed pages)",
                    'files': [os.path.basename(output_html)]
                }
            except Exception as e:
                return {'success': False, 'error': f'PDF comparison failed: {e}'}

        elif tool == 'pdf_table_extract':
            pdfs = [f for f in file_paths if f.endswith('.pdf')]
            if not pdfs:
                return {'success': False, 'error': 'Need at least 1 PDF file'}

            output_files = []
            try:
                sys.path.insert(0, tools_dir)
                from pdf_table_extractor import extract_tables_to_excel
                for pdf in pdfs:
                    stem = os.path.splitext(os.path.basename(pdf))[0]
                    out_xlsx = os.path.join(output_dir, f"{output_base}_{stem}_tables.xlsx")
                    result_data = extract_tables_to_excel(pdf, out_xlsx)
                    output_files.append(os.path.basename(out_xlsx))
                total_tables = result_data.get('total_tables', '?')
                return {
                    'success': True,
                    'message': f"Extracted {total_tables} tables from {len(pdfs)} PDF(s) into Excel",
                    'files': output_files
                }
            except Exception as e:
                return {'success': False, 'error': f'PDF table extraction failed: {e}'}

        elif tool == 'pdf_merge':
            pdfs = [f for f in file_paths if f.endswith('.pdf')]
            if len(pdfs) < 2:
                return {'success': False, 'error': 'Need at least 2 PDF files to merge'}

            output_pdf = os.path.join(output_dir, f"{output_base}_merged.pdf")
            try:
                sys.path.insert(0, tools_dir)
                from pdf_merger_splitter import merge_pdfs
                result_data = merge_pdfs(pdfs, output_pdf)
                return {
                    'success': True,
                    'message': f"Merged {len(pdfs)} PDFs into 1 file ({result_data['total_pages']} total pages)",
                    'files': [os.path.basename(output_pdf)]
                }
            except Exception as e:
                return {'success': False, 'error': f'PDF merge failed: {e}'}

        elif tool == 'pdf_split':
            pdfs = [f for f in file_paths if f.endswith('.pdf')]
            if not pdfs:
                return {'success': False, 'error': 'Need 1 PDF file to split'}

            pdf = pdfs[0]
            mode       = options.get('split_mode', 'chunks')
            chunk_size = int(options.get('chunk_size', 10))
            ranges     = options.get('ranges', '')
            split_dir  = os.path.join(output_dir, f"{output_base}_split")

            try:
                sys.path.insert(0, tools_dir)
                from pdf_merger_splitter import split_pdf
                result_data = split_pdf(
                    pdf, split_dir,
                    mode='ranges' if (mode == 'ranges' and ranges) else 'chunks',
                    ranges=ranges if ranges else None,
                    chunk_size=chunk_size,
                    prefix=os.path.splitext(os.path.basename(pdf))[0]
                )
                # Zip the split files
                zip_path = split_dir + '.zip'
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for item in result_data['files_created']:
                        fp = os.path.join(split_dir, item['file'])
                        if os.path.exists(fp):
                            zf.write(fp, item['file'])
                shutil.rmtree(split_dir, ignore_errors=True)
                n = len(result_data['files_created'])
                return {
                    'success': True,
                    'message': f"Split into {n} PDF file(s) — download ZIP to get all",
                    'files': [os.path.basename(zip_path)]
                }
            except Exception as e:
                return {'success': False, 'error': f'PDF split failed: {e}'}

        elif tool == 'ig_extract':
            # ── Rulebook IG Extractor ─────────────────────────────────────────
            # ISO 20022 Implementation Guide PDF → structured Excel workbook
            # One sheet per message section, one row per field.
            # Rows colour-coded: yellow = SEPA core mandatory, red = not permitted.
            pdfs = [f for f in file_paths if f.endswith('.pdf')]
            if not pdfs:
                return {'success': False, 'error': 'Need at least 1 IG PDF file (.pdf)'}

            # filter_sections comes from the section picker (list of section numbers like ['2.1.1'])
            # or from the manual text field; filter_messages is list of message IDs
            filter_messages = options.get('filter_messages', [])   # e.g. ['pacs.008.001.08']
            filter_sections = options.get('filter_sections', [])   # e.g. ['2.1.1', '2.2.1']

            try:
                sys.path.insert(0, tools_dir)
                from ig_extractor import extract_ig

                output_files = []
                total_fields = 0
                for pdf_path in pdfs:
                    stem = os.path.splitext(os.path.basename(pdf_path))[0]
                    out_xlsx = os.path.join(output_dir, f"{output_base}_{stem}_IG.xlsx")
                    result = extract_ig(
                        pdf_path,
                        out_xlsx,
                        filter_messages=filter_messages if filter_messages else None,
                        filter_sections=filter_sections if filter_sections else None,
                    )
                    output_files.append(os.path.basename(out_xlsx))
                    total_fields += result.get('total_fields', 0)

                sections_extracted = sum(len(result.get('sections', [])) for result in [result])
                return {
                    'success': True,
                    'message': (
                        f"Extracted {total_fields} fields from {len(output_files)} PDF(s). "
                        f"One Excel sheet per message section with 🟡 yellow / ⬜ white / 🔴 red colour coding."
                    ),
                    'files': output_files
                }
            except ImportError:
                return {
                    'success': False,
                    'error': 'ig_extractor module not found. Ensure ig_extractor.py is in the tools/ folder.',
                    'suggestion': 'Copy ig_extractor.py into the tools/ directory alongside the other tool scripts.'
                }
            except Exception as e:
                logger.error(f"IG extraction error: {e}", exc_info=True)
                return {'success': False, 'error': f'IG extraction failed: {e}'}

        elif tool == 'ig_diff':
            # ── IG Diff — EPC vs NPC comparator ──────────────────────────────
            xlsxs = [f for f in file_paths if f.lower().endswith('.xlsx')]
            if len(xlsxs) < 2:
                return {'success': False,
                        'error': 'Upload exactly 2 IG Excel files (.xlsx) — e.g. EPC_IG.xlsx and NPC_IG.xlsx.'}

            label_a = options.get('label_a', 'File A').strip() or 'File A'
            label_b = options.get('label_b', 'File B').strip() or 'File B'

            try:
                sys.path.insert(0, tools_dir)
                from ig_diff import diff_ig

                out_name = f"{output_base}_IG_Diff_{label_a}_vs_{label_b}.xlsx"
                out_path = os.path.join(output_dir, out_name)

                result = diff_ig(xlsxs[0], xlsxs[1], out_path, label_a=label_a, label_b=label_b)

                msgs = ', '.join(result['messages_compared'][:5])
                if len(result['messages_compared']) > 5:
                    msgs += f" +{len(result['messages_compared'])-5} more"

                return {
                    'success': True,
                    'message': (
                        f"Diff complete — {result['total_changes']} changes across "
                        f"{len(result['sheets'])} message(s): {msgs}. "
                        f"Unchanged rows grouped/hidden — use row group arrows to expand."
                    ),
                    'files': [os.path.basename(out_path)]
                }
            except ImportError:
                return {'success': False,
                        'error': 'ig_diff module not found. Ensure ig_diff.py is in the tools/ folder.'}
            except Exception as e:
                logger.error(f"IG diff error: {e}", exc_info=True)
                return {'success': False, 'error': f'IG diff failed: {e}'}

        elif tool == 'ig_change_tracker':
            # ── Rulebook Change Tracker ───────────────────────────────────────
            pdfs = [f for f in file_paths if f.lower().endswith('.pdf')]
            if not pdfs:
                return {'success': False,
                        'error': 'Upload 1 or 2 IG PDF files — the tool will extract the change list from each.'}
            try:
                sys.path.insert(0, tools_dir)
                from rulebook_change_tracker import extract_changes, track_changes
                if len(pdfs) == 1:
                    out_name = f"{output_base}_ChangeTracker.xlsx"
                    out_path = os.path.join(output_dir, out_name)
                    result   = extract_changes(pdfs[0], out_path)
                    doc      = result['doc']
                    msg = (f"Extracted {result['total_changes']} changes from "
                           f"{doc.get('doc_number','')} {doc.get('version','')}. "
                           f"Effective: {doc.get('date_effective','N/A')}.")
                else:
                    out_name = f"{output_base}_ChangeTracker_Comparison.xlsx"
                    out_path = os.path.join(output_dir, out_name)
                    result   = track_changes(pdfs[0], pdfs[1], out_path)
                    msg = (f"Extracted {len(result['changes_a'])} changes from "
                           f"{result['doc_a'].get('doc_number','Doc A')} and "
                           f"{len(result['changes_b'])} changes from "
                           f"{result['doc_b'].get('doc_number','Doc B')} — "
                           f"{result['total_changes']} total.")
                return {'success': True, 'message': msg, 'files': [os.path.basename(out_path)]}
            except ImportError:
                return {'success': False, 'error': 'rulebook_change_tracker module not found.'}
            except Exception as e:
                logger.error(f"Change tracker error: {e}", exc_info=True)
                return {'success': False, 'error': f'Change tracker failed: {e}'}

        
        elif tool == 'ig_mapping':
            # ── IG to Mapping Template ────────────────────────────────────────
            xlsxs = [f for f in file_paths if f.lower().endswith('.xlsx')]
            if not xlsxs:
                return {'success': False,
                        'error': 'Upload one IG Extractor Excel (.xlsx) file.'}

            label_a     = options.get('scheme_label', '').strip() or ''
            version_a   = options.get('version', '').strip() or ''
            filter_mode = options.get('filter_mode', 'all').strip() or 'all'

            try:
                sys.path.insert(0, tools_dir)
                from ig_mapping_template import generate_mapping

                suffix = '_MandatoryOnly' if filter_mode == 'mandatory' else ''
                out_name = f"{output_base}_Mapping_Template{suffix}.xlsx"
                out_path = os.path.join(output_dir, out_name)

                result = generate_mapping(
                    xlsxs[0], out_path,
                    scheme_label=label_a, version=version_a,
                    filter_mode=filter_mode
                )

                sheets_str = ', '.join(s['message'] for s in result['sheets'][:5])
                if len(result['sheets']) > 5:
                    sheets_str += f" +{len(result['sheets'])-5} more"

                return {
                    'success': True,
                    'message': (
                        f"Mapping template ready — {result['total_fields']} fields across "
                        f"{len(result['sheets'])} message(s): {sheets_str}. "
                        f"{result['mandatory']} mandatory (🟡), "
                        f"{result['optional']} optional (⬜), "
                        f"{result['not_permitted']} not permitted (🔴). "
                        f"Fill in the green Implementation columns for your team."
                    ),
                    'files': [os.path.basename(out_path)]
                }
            except ImportError:
                return {'success': False,
                        'error': 'ig_mapping_template module not found. Ensure ig_mapping_template.py is in tools/.'}
            except Exception as e:
                logger.error(f"IG mapping error: {e}", exc_info=True)
                return {'success': False, 'error': f'Mapping template failed: {e}'}

        elif tool == 'ig_mapping_xsd':
            # ── IG to Mapping Template (XSD-Enriched) ────────────────────────
            xlsxs = [f for f in file_paths if f.lower().endswith('.xlsx')]
            xsds  = [f for f in file_paths if f.lower().endswith('.xsd')]
            if not xlsxs:
                return {'success': False, 'error': 'Upload one IG Extractor Excel (.xlsx) file.'}
            if not xsds:
                return {'success': False, 'error': 'Upload one XSD file (.xsd) for the target message.'}

            scheme_label = options.get('scheme_label', '').strip() or 'NPC'
            version      = options.get('version', '').strip() or ''
            filter_mode  = options.get('filter_mode', 'all').strip() or 'all'

            try:
                sys.path.insert(0, tools_dir)
                from ig_mapping_template_xsd import generate_mapping_xsd

                suffix   = '_MandatoryOnly' if filter_mode == 'mandatory' else ''
                out_name = f"{output_base}_Mapping_XSD{suffix}.xlsx"
                out_path = os.path.join(output_dir, out_name)

                result = generate_mapping_xsd(
                    ig_excel_path=xlsxs[0],
                    xsd_path=xsds[0],
                    output_path=out_path,
                    scheme_label=scheme_label,
                    version=version,
                    filter_mode=filter_mode,
                )

                sheets_str = ', '.join(s['message'] for s in result['sheets'][:4])
                return {
                    'success': True,
                    'message': (
                        f"XSD-enriched mapping template ready — {result['fields']} fields "
                        f"({result['mandatory']} mandatory, {result['optional']} optional, "
                        f"{result['not_permitted']} not-permitted). "
                        f"{result['xsd_enriched']} fields enriched with XSD constraints "
                        f"(patterns, enumerations, lengths). "
                        f"Sheets: {sheets_str}."
                    ),
                    'files': [os.path.basename(out_path)]
                }
            except ImportError:
                return {'success': False, 'error': 'ig_mapping_template_xsd module not found.'}
            except Exception as e:
                logger.error(f"IG mapping XSD error: {e}", exc_info=True)
                return {'success': False, 'error': f'Mapping template failed: {e}'}

        elif tool == 'xsd_ig_analysis':
            # ── XSD vs IG Cross-Reference Analyser ───────────────────────────
            xsd_files  = [f for f in file_paths if f.lower().endswith('.xsd')]
            xlsx_files = [f for f in file_paths if f.lower().endswith('.xlsx')]

            if not xsd_files:
                return {'success': False, 'error': 'Upload at least one XSD file.'}
            if not xlsx_files:
                return {'success': False, 'error': 'Upload at least one IG Extractor Excel (.xlsx).'}

            scheme_label   = options.get('scheme_label', '').strip() or ''
            version        = options.get('version', '').strip() or ''
            message_sheet  = options.get('message_sheet', '').strip() or ''

            try:
                sys.path.insert(0, tools_dir)
                from xsd_ig_analyser import analyse

                out_name = f"{output_base}_XSD_IG_Analysis.xlsx"
                out_path = os.path.join(output_dir, out_name)

                result = analyse(
                    xsd_files[0], xlsx_files[0], out_path,
                    message_sheet=message_sheet,
                    scheme_label=scheme_label,
                    version=version
                )

                return {
                    'success': True,
                    'message': (
                        f"XSD vs IG analysis complete — {result['total']} fields analysed. "
                        f"✅ {result['aligned']} aligned, "
                        f"🔴 {result['excluded']} excluded by scheme, "
                        f"🟡 {result['status_diff']} status differences, "
                        f"🔵 {result['rules_diff']} rules differences, "
                        f"🟠 {result['xsd_only']} in XSD only. "
                        f"Sheet used: {result['sheet_used']}."
                    ),
                    'files': [os.path.basename(out_path)]
                }
            except ImportError:
                return {'success': False, 'error': 'xsd_ig_analyser module not found.'}
            except Exception as e:
                logger.error(f"XSD IG analysis error: {e}", exc_info=True)
                return {'success': False, 'error': f'XSD IG analysis failed: {e}'}

        elif tool == 'xsd_explorer':
            # ── XSD Explorer – interactive HTML + Excel ───────────────────────
            xsd_files = [f for f in file_paths if f.lower().endswith('.xsd')]
            if not xsd_files:
                return {'success': False, 'error': 'Upload at least one XSD file.'}

            try:
                sys.path.insert(0, tools_dir)
                from xsd_explorer import parse_xsd, generate_html, generate_excel

                xsd_path = xsd_files[0]
                xsd_name = os.path.basename(xsd_path)
                base     = os.path.splitext(xsd_name)[0]

                html_name = f"{output_base}_{base}_explorer.html"
                xlsx_name = f"{output_base}_{base}_structure.xlsx"
                html_path = os.path.join(output_dir, html_name)
                xlsx_path = os.path.join(output_dir, xlsx_name)

                roots, stats, edges, raw = parse_xsd(xsd_path)
                generate_html(roots, stats, edges, raw, xsd_name, html_path)
                generate_excel(roots, xsd_name, xlsx_path)

                return {
                    'success': True,
                    'message': (
                        f"XSD Explorer complete — {stats['total_elements']} elements, "
                        f"{stats['total_types']} types, max depth {stats['max_depth']}."
                    ),
                    'files': [html_name, xlsx_name]
                }
            except ImportError:
                return {'success': False, 'error': 'xsd_explorer module not found.'}
            except Exception as e:
                logger.error(f"XSD Explorer error: {e}", exc_info=True)
                return {'success': False, 'error': f'XSD Explorer failed: {e}'}

        else:
            return {'success': False, 'error': f'Unknown tool: {tool}'}

    except subprocess.TimeoutExpired:
        logger.error(f"Tool {tool} timed out after {timeout}s")
        return {'success': False, 'error': f'Timeout after {timeout} seconds'}
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return {'success': False, 'error': str(e)}

# ── Document Library ─────────────────────────────────────────────────────────

LIBRARY_FOLDER = Path(__file__).parent / 'library'
LIBRARY_EXTS   = {'.xsd', '.xlsx', '.xlsm', '.pdf', '.xml'}
FILE_ICONS     = {'.xsd': '📐', '.xlsx': '📊', '.xlsm': '📊', '.pdf': '📄', '.xml': '📝'}


def _build_library_tree(root: Path) -> list:
    """
    Recursively walk the library folder and return a nested tree:
    [
      { "name": "RB25", "type": "folder", "path": "RB25", "children": [
          { "name": "NPC", "type": "folder", "path": "RB25/NPC", "children": [
              { "name": "pacs_008.xsd", "type": "file", "path": "RB25/NPC/pacs_008.xsd",
                "ext": ".xsd", "icon": "📐", "size_kb": 42 }
          ]}
      ]}
    ]
    """
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
                'name':     entry.name,
                'type':     'folder',
                'path':     rel,
                'children': children,
                'count':    sum(1 for c in children if c['type'] == 'file') +
                            sum(c.get('count', 0) for c in children if c['type'] == 'folder')
            })
        elif entry.is_file() and entry.suffix.lower() in LIBRARY_EXTS:
            items.append({
                'name':    entry.name,
                'type':    'file',
                'path':    rel,
                'ext':     entry.suffix.lower(),
                'icon':    FILE_ICONS.get(entry.suffix.lower(), '📄'),
                'size_kb': round(entry.stat().st_size / 1024, 1)
            })

    return items


def _safe_lib_path(rel: str) -> Path:
    """Resolve a relative library path safely, raising ValueError if escaping."""
    target = (LIBRARY_FOLDER / rel.lstrip('/')).resolve()
    target.relative_to(LIBRARY_FOLDER.resolve())  # raises ValueError if outside
    return target

def _sanitise_name(name: str) -> str:
    """Strip dangerous characters from a file/folder name."""
    import re
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '_', name)  # Windows-unsafe chars
    name = re.sub(r'\.\.+', '.', name)           # no double-dots
    name = name.strip('. ')
    return name[:120] if name else 'unnamed'


@app.route('/library', methods=['GET'])
def get_library():
    """Return the document library tree as JSON."""
    LIBRARY_FOLDER.mkdir(exist_ok=True)
    tree = _build_library_tree(LIBRARY_FOLDER)
    return jsonify({'success': True, 'tree': tree})


@app.route('/library/folder', methods=['POST'])
def library_create_folder():
    """Create a new folder inside the library.
    Body JSON: { "path": "RB25/NPC", "name": "NewFolder" }
    """
    data = request.get_json(force=True, silent=True) or {}
    parent_rel = data.get('path', '').strip('/')
    name       = _sanitise_name(data.get('name', ''))
    if not name:
        return jsonify({'success': False, 'error': 'Folder name is required'}), 400
    try:
        parent = _safe_lib_path(parent_rel) if parent_rel else LIBRARY_FOLDER.resolve()
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


@app.route('/library/upload', methods=['POST'])
def library_upload():
    """Upload one or more files into a library folder.
    Form fields:
      - folder_path: relative path of target folder (empty = root)
      - files: one or more file objects
    """
    folder_rel = request.form.get('folder_path', '').strip('/')
    try:
        target_dir = _safe_lib_path(folder_rel) if folder_rel else LIBRARY_FOLDER.resolve()
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid folder path'}), 403

    if not target_dir.is_dir():
        return jsonify({'success': False, 'error': 'Target folder does not exist'}), 404

    files = request.files.getlist('files')
    if not files:
        return jsonify({'success': False, 'error': 'No files provided'}), 400

    saved = []
    errors = []
    for f in files:
        if not f or not f.filename:
            continue
        ext = Path(f.filename).suffix.lower()
        if ext not in LIBRARY_EXTS:
            errors.append(f'{f.filename}: unsupported type ({ext})')
            continue
        safe_name = _sanitise_name(Path(f.filename).stem) + ext
        dest = target_dir / safe_name
        # If name conflicts, append a counter
        counter = 1
        while dest.exists():
            dest = target_dir / f"{_sanitise_name(Path(f.filename).stem)}_{counter}{ext}"
            counter += 1
        f.save(str(dest))
        rel = dest.relative_to(LIBRARY_FOLDER).as_posix()
        saved.append({'name': dest.name, 'path': rel,
                      'ext': ext, 'icon': FILE_ICONS.get(ext, '📄'),
                      'size_kb': round(dest.stat().st_size / 1024, 1)})
        logger.info(f"Library: uploaded {rel}")

    if not saved and errors:
        return jsonify({'success': False, 'error': '; '.join(errors)}), 400
    return jsonify({'success': True, 'files': saved, 'errors': errors})


@app.route('/library/delete', methods=['POST'])
def library_delete():
    """Delete a file or empty folder from the library.
    Body JSON: { "path": "RB25/NPC/file.xsd" }
    """
    import shutil
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


@app.route('/library/rename', methods=['POST'])
def library_rename():
    """Rename a file or folder in the library.
    Body JSON: { "path": "RB25/NPC/old.xsd", "name": "new.xsd" }
    """
    data    = request.get_json(force=True, silent=True) or {}
    rel     = data.get('path', '').strip('/')
    new_name = _sanitise_name(data.get('name', ''))
    if not rel or not new_name:
        return jsonify({'success': False, 'error': 'path and name required'}), 400
    try:
        target  = _safe_lib_path(rel)
        if not target.exists():
            return jsonify({'success': False, 'error': 'Not found'}), 404
        # Preserve extension for files
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


@app.route('/library_file', methods=['GET'])
def get_library_file():
    """
    Copy a library file into the uploads temp folder and return its temp path.
    The frontend then uses this temp path when submitting tool runs.
    Query param: path=RB25/NPC/pacs_008.xsd
    """
    rel_path = request.args.get('path', '').lstrip('/')
    if not rel_path:
        return jsonify({'success': False, 'error': 'No path specified'}), 400

    # Security: resolve and ensure it stays within library
    try:
        target = (LIBRARY_FOLDER / rel_path).resolve()
        LIBRARY_FOLDER.resolve()  # ensure library exists
        target.relative_to(LIBRARY_FOLDER.resolve())  # raises ValueError if escaping
    except (ValueError, Exception) as e:
        return jsonify({'success': False, 'error': 'Invalid path'}), 403

    if not target.exists() or not target.is_file():
        return jsonify({'success': False, 'error': 'File not found'}), 404

    if target.suffix.lower() not in LIBRARY_EXTS:
        return jsonify({'success': False, 'error': 'File type not allowed'}), 403

    # Serve the file directly (no copy needed — tools read from path)
    return send_file(str(target), as_attachment=False,
                     download_name=target.name,
                     mimetype='application/octet-stream')


@app.route('/run', methods=['POST'])
def run_tool_alias():
    """
    Alias for /run_tool used by the PDF and Rulebook tool panels.
    Accepts multipart/form-data with:
      - tool (str): tool ID
      - files (file[]): uploaded files  OR
      - library_files (str): JSON array of library relative paths
    Mixes uploaded and library files transparently.
    """
    import json as _json

    tool_id = request.form.get('tool', '').strip()
    if not tool_id:
        return jsonify({'success': False, 'error': 'No tool specified'}), 400

    upload_dir = Path(CONFIG['UPLOAD_FOLDER'])
    upload_dir.mkdir(exist_ok=True)

    saved_paths = []

    # 1) Regular uploaded files
    for f in request.files.getlist('files'):
        if f and f.filename:
            safe = f.filename.replace('..', '').replace('/', '_').replace('\\', '_')
            dest = upload_dir / safe
            f.save(str(dest))
            saved_paths.append(str(dest))

    # 2) Library files referenced by relative path
    lib_json = request.form.get('library_files', '')
    if lib_json:
        try:
            lib_paths = _json.loads(lib_json)
            for rel in lib_paths:
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

    # Build a fake request context for run_tool
    # Pass as form params the same way run_tool expects them
    extra_params = {k: v for k, v in request.form.items()
                    if k not in ('tool', 'files', 'library_files')}

    result = _dispatch_tool(tool_id, saved_paths, extra_params)
    return jsonify(result)


def _dispatch_tool(tool_id: str, file_paths: list, params: dict) -> dict:
    """
    Map tool_id → actual tool function/script, call it, return result dict.
    {success, message, files: [{name, size}]}
    """
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).parent / 'tools'))

    output_dir = Path(CONFIG['OUTPUT_FOLDER'])
    output_dir.mkdir(exist_ok=True)

    try:
        # ── IG Extractor ────────────────────────────────────────────────────
        if tool_id == 'ig_extract':
            from ig_extractor import extract_ig
            pdf_files = [p for p in file_paths if p.endswith('.pdf')]
            if not pdf_files:
                return {'success': False, 'error': 'Need at least 1 IG PDF file (.pdf)'}

            # Parse section / message filters from params
            sections_raw  = params.get('sections', '')
            msgs_raw      = params.get('filter_messages', '')
            filter_sections = [s.strip() for s in sections_raw.split(',')  if s.strip()] or None
            filter_messages = [s.strip() for s in msgs_raw.split(',')      if s.strip()] or None

            logger.info(f"Running tool: ig_extract on {len(pdf_files)} file(s) with options: "
                        f"{{'filter_messages': {filter_messages or []}, 'filter_sections': {filter_sections or []}}}")
            import time as _time
            _t0 = _time.time()

            out_files   = []
            total_fields = 0
            try:
                for pdf in pdf_files:
                    stem = Path(pdf).stem
                    out  = str(output_dir / f"{stem}_IG.xlsx")
                    result = extract_ig(pdf, out,
                                        filter_messages=filter_messages,
                                        filter_sections=filter_sections)
                    total_fields += result.get('total_fields', 0)
                    out_files.append({'name': Path(out).name, 'size': Path(out).stat().st_size})

                elapsed = round(_time.time() - _t0, 2)
                logger.info(f"Tool ig_extract completed successfully in {elapsed}s")
                return {
                    'success': True,
                    'message': (f"Extracted {total_fields} fields from {len(out_files)} PDF(s). "
                                f"One Excel sheet per message section with 🟡 yellow / ⬜ white / 🔴 red colour coding."),
                    'files': out_files
                }
            except Exception as e:
                logger.error(f"IG extraction error: {e}", exc_info=True)
                return {'success': False, 'error': f'IG extraction failed: {e}'}

        # ── IG Diff ─────────────────────────────────────────────────────────
        elif tool_id == 'ig_diff':
            from ig_diff import diff_ig
            xl_files = [p for p in file_paths if p.endswith(('.xlsx', '.xlsm'))]
            if len(xl_files) < 2:
                return {'success': False, 'error': 'Please provide 2 IG Excel files'}
            label_a = params.get('label_a', 'File A')
            label_b = params.get('label_b', 'File B')
            out = str(output_dir / f"IG_Diff_{label_a}_vs_{label_b}.xlsx")
            diff_ig(xl_files[0], xl_files[1], out, label_a=label_a, label_b=label_b)
            return {'success': True, 'message': 'Diff complete',
                    'files': [{'name': Path(out).name, 'size': Path(out).stat().st_size}]}

        # ── Rulebook Change Tracker ──────────────────────────────────────────
        elif tool_id == 'rulebook_changes':
            from rulebook_change_tracker import track_changes
            pdf_files = [p for p in file_paths if p.endswith('.pdf')]
            if not pdf_files:
                return {'success': False, 'error': 'Please provide a PDF file'}
            out = str(output_dir / 'RulebookChanges.xlsx')
            # track_changes(pdf_a, output_path, pdf_b=None) — pass second PDF if provided
            pdf_b = pdf_files[1] if len(pdf_files) > 1 else None
            track_changes(pdf_files[0], out, pdf_b=pdf_b)
            return {'success': True, 'message': 'Change log extracted',
                    'files': [{'name': 'RulebookChanges.xlsx', 'size': Path(out).stat().st_size}]}

        # ── IG Mapping Template ──────────────────────────────────────────────
        elif tool_id == 'ig_mapping':
            from ig_mapping_template import generate_mapping
            xl_files = [p for p in file_paths if p.endswith(('.xlsx', '.xlsm'))]
            if not xl_files:
                return {'success': False, 'error': 'Please provide an IG Excel file'}
            scheme = params.get('scheme_label', 'EPC')
            version = params.get('version', '')
            out = str(output_dir / 'Mapping_Template.xlsx')
            generate_mapping(xl_files[0], out, scheme_label=scheme, version=version)
            return {'success': True, 'message': 'Mapping template ready',
                    'files': [{'name': 'Mapping_Template.xlsx', 'size': Path(out).stat().st_size}]}

        # ── IG Mapping (XSD-Enriched) ────────────────────────────────────────
        elif tool_id == 'ig_mapping_xsd':
            from ig_mapping_template_xsd import generate_mapping_xsd
            xl_files = [p for p in file_paths if p.endswith(('.xlsx', '.xlsm'))]
            xsd_files = [p for p in file_paths if p.endswith('.xsd')]
            if not xl_files or not xsd_files:
                return {'success': False, 'error': 'Please provide an IG Excel + XSD file'}
            scheme = params.get('scheme_label', 'EPC')
            version = params.get('version', '')
            out = str(output_dir / 'Mapping_XSD.xlsx')
            generate_mapping_xsd(xl_files[0], xsd_files[0], out,
                                 scheme_label=scheme, version=version)
            return {'success': True, 'message': 'XSD-enriched mapping ready',
                    'files': [{'name': 'Mapping_XSD.xlsx', 'size': Path(out).stat().st_size}]}

        # ── XSD vs IG Analyser ───────────────────────────────────────────────
        elif tool_id == 'xsd_ig_analysis':
            import xsd_ig_analyser as xa
            xsd_files = [p for p in file_paths if p.endswith('.xsd')]
            xl_files  = [p for p in file_paths if p.endswith(('.xlsx', '.xlsm'))]
            if not xsd_files or not xl_files:
                return {'success': False, 'error': 'Please provide 1 XSD + 1 IG Excel'}
            scheme  = params.get('scheme_label', 'EPC')
            version = params.get('version', '')
            sheet   = params.get('message_sheet', '')
            stem    = Path(xsd_files[0]).stem
            out     = str(output_dir / f"{stem}_XSD_IG_Analysis.xlsx")
            result  = xa.analyse(xsd_files[0], xl_files[0], out,
                                 message_sheet=sheet or None,
                                 scheme_label=scheme,
                                 version=version)
            return {'success': True,
                    'message': f"{result['total']} fields — {result['aligned']} aligned, {result['status_diff']} status diffs",
                    'files': [{'name': Path(out).name, 'size': Path(out).stat().st_size}]}

        # ── PDF tools (also reachable via /run) ─────────────────────────────
        elif tool_id in ('pdf_compare', 'pdf_table_extract', 'pdf_merge', 'pdf_split'):
            # Re-use existing run_tool logic by calling it directly
            return _run_pdf_tool(tool_id, file_paths, params)

        # ── YAML / JSON Explorer ─────────────────────────────────────────────
        elif tool_id == 'yaml_json_explorer':
            from yaml_json_explorer import parse_file, generate_html, generate_excel
            yj_files = [p for p in file_paths
                        if Path(p).suffix.lower() in ('.yaml', '.yml', '.json')]
            if not yj_files:
                return {'success': False, 'error': 'Upload a .yaml, .yml, or .json file.'}
            src      = yj_files[0]
            fname    = Path(src).name
            base     = Path(src).stem
            html_name = f"{base}_explorer.html"
            xlsx_name = f"{base}_structure.xlsx"
            html_path = str(output_dir / html_name)
            xlsx_path = str(output_dir / xlsx_name)
            roots, stats, raw = parse_file(src)
            generate_html(roots, stats, raw, fname, html_path)
            generate_excel(roots, fname, xlsx_path)
            ftype = stats['file_type']
            return {
                'success': True,
                'message': (
                    f"{ftype} Explorer complete — {stats['total_nodes']} nodes, "
                    f"{stats['total_objects']} objects, {stats['total_arrays']} arrays, "
                    f"max depth {stats['max_depth']}."
                ),
                'files': [
                    {'name': html_name, 'type': 'html'},
                    {'name': xlsx_name, 'type': 'xlsx'},
                ],
            }

        # ── YAML API Schema Extractor ────────────────────────────────────────
        elif tool_id == 'yaml_api_extract':
            from yaml_api_extractor import extract_yaml_api
            yaml_files = [p for p in file_paths
                          if Path(p).suffix.lower() in ('.yaml', '.yml', '.json')]
            if not yaml_files:
                return {'success': False, 'error': 'No YAML/JSON file uploaded'}
            endpoints_raw = params.get('filter_endpoints', '')
            filter_eps    = [e.strip() for e in endpoints_raw.split(',') if e.strip()] or None
            out           = str(output_dir / (Path(yaml_files[0]).stem + '_api_schema.xlsx'))
            logger.info(f"Running yaml_api_extract on {Path(yaml_files[0]).name}, "
                        f"filter_endpoints={filter_eps or 'ALL'}")
            result = extract_yaml_api(yaml_files[0], out, filter_endpoints=filter_eps)
            if not result.get('success'):
                return {'success': False, 'error': result.get('error', 'Extraction failed')}
            return {
                'success': True,
                'message': result['message'],
                'files':   [{'name': Path(out).name, 'size': Path(out).stat().st_size}],
            }

        else:
            return {'success': False, 'error': f'Unknown tool: {tool_id}'}

    except ImportError as e:
        logger.error(f"Tool import error ({tool_id}): {e}")
        return {'success': False, 'error': f'Tool not installed: {e}'}
    except Exception as e:
        logger.error(f"Tool error ({tool_id}): {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def _run_pdf_tool(tool_id: str, file_paths: list, params: dict) -> dict:
    """Thin wrapper for PDF tools."""
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
            mode   = 'ranges' if ranges else 'pages'
            result = split_pdf(pdfs[0], str(output_dir), mode=mode, ranges=ranges or None)
            files_created = result.get('files_created', [])
            return {'success': True, 'message': f'Split into {len(files_created)} part(s)',
                    'files': [{'name': f['file'], 'size': Path(output_dir / f['file']).stat().st_size}
                               for f in files_created]}

    except Exception as e:
        return {'success': False, 'error': str(e)}
    return {'success': False, 'error': 'Unknown PDF tool'}


@app.route('/detect_ig_sections', methods=['POST'])
def detect_ig_sections():
    """Detect message sections in an uploaded IG PDF for the section picker UI."""
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).parent / 'tools'))
        from ig_extractor import detect_sections

        upload_dir = Path(CONFIG['UPLOAD_FOLDER'])
        upload_dir.mkdir(exist_ok=True)

        # Accept uploaded file or library file path
        pdf_path = None
        for f in request.files.getlist('files'):
            if f and f.filename and f.filename.endswith('.pdf'):
                dest = upload_dir / f.filename.replace('/', '_')
                f.save(str(dest))
                pdf_path = str(dest)
                break

        lib_path = request.form.get('library_path', '')
        if not pdf_path and lib_path:
            target = (LIBRARY_FOLDER / lib_path).resolve()
            try:
                target.relative_to(LIBRARY_FOLDER.resolve())
                if target.is_file():
                    pdf_path = str(target)
            except ValueError:
                pass

        if not pdf_path:
            return jsonify({'success': False, 'error': 'No PDF provided'}), 400

        sections = detect_sections(pdf_path)
        logger.info(f"Section detection: {len(sections)} sections found in {Path(pdf_path).name}")
        return jsonify({'success': True, 'sections': sections})

    except ImportError:
        return jsonify({'success': False, 'sections': [],
                        'error': 'Section detection not available'}), 200
    except Exception as e:
        logger.error(f"Section detection error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/detect_yaml_endpoints', methods=['POST'])
def detect_yaml_endpoints():
    """Detect API endpoints in an uploaded OpenAPI/AsyncAPI YAML for the endpoint picker UI."""
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).parent / 'tools'))
        from yaml_api_extractor import detect_endpoints

        upload_dir = Path(CONFIG['UPLOAD_FOLDER'])
        upload_dir.mkdir(exist_ok=True)

        yaml_path = None
        for f in request.files.getlist('files'):
            if f and f.filename and Path(f.filename).suffix.lower() in ('.yaml', '.yml', '.json'):
                dest = upload_dir / f.filename.replace('/', '_')
                f.save(str(dest))
                yaml_path = str(dest)
                break

        lib_path = request.form.get('library_path', '')
        if not yaml_path and lib_path:
            target = (LIBRARY_FOLDER / lib_path).resolve()
            try:
                target.relative_to(LIBRARY_FOLDER.resolve())
                if target.is_file():
                    yaml_path = str(target)
            except ValueError:
                pass

        if not yaml_path:
            return jsonify({'success': False, 'error': 'No YAML/JSON file provided'}), 400

        endpoints = detect_endpoints(yaml_path)
        logger.info(f"Endpoint detection: {len(endpoints)} endpoints found in {Path(yaml_path).name}")
        return jsonify({'success': True, 'endpoints': endpoints})

    except ImportError as e:
        return jsonify({'success': False, 'endpoints': [],
                        'error': f'yaml_api_extractor not available: {e}'}), 200
    except Exception as e:
        logger.error(f"Endpoint detection error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated file"""
    try:
        logger.info(f"File download: {filename}")
        return send_from_directory(CONFIG['OUTPUT_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Download error for {filename}: {e}")
        return "File not found", 404

@app.route('/preview/<filename>')
def preview_file(filename):
    """Preview HTML files in browser"""
    try:
        if filename.endswith('.html'):
            return send_from_directory(CONFIG['OUTPUT_FOLDER'], filename)
        else:
            return "Only HTML files can be previewed", 400
    except:
        return "File not found", 404


@app.route('/pdf_info', methods=['POST'])
def pdf_info():
    """Return page count and detected IG sections for uploaded PDF(s).
    Body: { "files": ["filename1.pdf", ...] }
    Response: { "success": true, "results": { "filename.pdf": { "pages": N, "sections": [...] } } }
    Each section: { section, label, message, page, display }
    """
    try:
        data   = request.get_json() or {}
        files  = data.get('files', [])
        results = {}

        for fname in files:
            fpath = os.path.join(CONFIG['UPLOAD_FOLDER'], os.path.basename(fname))
            if not os.path.exists(fpath):
                results[fname] = {'error': 'File not found'}
                continue
            try:
                import pdfplumber, re as _re
                with pdfplumber.open(fpath) as pdf:
                    page_count = len(pdf.pages)

                    # Detect "X.Y.Z Use of ... (pacs/camt)" section headings
                    section_re = _re.compile(
                        r'((?:\d+\.)+\d+)[\.\s]+Use of\s+(.+?)\s*'
                        r'\((pacs\.\d+\.\d+\.\d+|camt\.\d+\.\d+\.\d+)\)',
                        _re.IGNORECASE
                    )
                    sections = []
                    seen     = set()
                    for pg_num, page in enumerate(pdf.pages, 1):
                        text = page.extract_text() or ''
                        for m in section_re.finditer(text):
                            # Skip TOC dotted lines (e.g. "2.1.1 Use of ... ......... 11")
                            surrounding = text[max(0, m.start() - 10):m.end() + 30]
                            if _re.search(r'\.{5,}', surrounding):
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

# ============================================================================
# MONITORING ENDPOINTS
# ============================================================================

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0-local'
    })

@app.route('/status')
def status():
    """Detailed status endpoint"""
    try:
        upload_count = len(list(Path(CONFIG['UPLOAD_FOLDER']).glob('*')))
        output_count = len(list(Path(CONFIG['OUTPUT_FOLDER']).glob('*')))
        
        # Calculate folder sizes
        upload_size = sum(f.stat().st_size for f in Path(CONFIG['UPLOAD_FOLDER']).glob('*') if f.is_file())
        output_size = sum(f.stat().st_size for f in Path(CONFIG['OUTPUT_FOLDER']).glob('*') if f.is_file())
        
        return jsonify({
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0-local',
            'config': {
                'host': CONFIG['HOST'],
                'port': CONFIG['PORT'],
                'max_upload_mb': CONFIG['MAX_CONTENT_LENGTH'] // (1024 * 1024),
                'max_file_size_mb': CONFIG['MAX_FILE_SIZE_MB'],
                'max_files_per_upload': CONFIG['MAX_FILES_PER_UPLOAD'],
                'timeout_seconds': CONFIG['TIMEOUT_SECONDS'],
                'cleanup_hours': CONFIG['CLEANUP_HOURS'],
                'auto_cleanup': CONFIG['AUTO_CLEANUP_ENABLED']
            },
            'files': {
                'uploads': upload_count,
                'uploads_size_mb': round(upload_size / (1024 * 1024), 2),
                'outputs': output_count,
                'outputs_size_mb': round(output_size / (1024 * 1024), 2)
            },
            'tools_available': [
                'comprehensive', 'document', 'compare', 'multi_compare', 
                'test_data', 'xml_validate', 'xml_diff', 'batch_validate',
                'mapping_template', 'xml_transform',
                'pdf_compare', 'pdf_table_extract', 'pdf_merge', 'pdf_split',
                'ig_extract',
                'ig_diff',
                'ig_change_tracker',
                'ig_mapping',
                'xsd_ig_analysis',
                'yaml_api_extract'
            ]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/limits')
def get_limits():
    """Get system limits for frontend display"""
    return jsonify({
        'max_file_size_mb': CONFIG['MAX_FILE_SIZE_MB'],
        'max_upload_total_mb': CONFIG['MAX_CONTENT_LENGTH'] // (1024 * 1024),
        'max_files_per_upload': CONFIG['MAX_FILES_PER_UPLOAD'],
        'max_batch_files': CONFIG['MAX_BATCH_FILES'],
        'timeout_seconds': CONFIG['TIMEOUT_SECONDS'],
        'allowed_extensions': list(CONFIG['ALLOWED_EXTENSIONS']),
        'cleanup_hours': CONFIG['CLEANUP_HOURS']
    })

@app.route('/cleanup', methods=['POST'])
def trigger_cleanup():
    """Manual cleanup trigger"""
    try:
        before_uploads = len(list(Path(CONFIG['UPLOAD_FOLDER']).glob('*')))
        before_outputs = len(list(Path(CONFIG['OUTPUT_FOLDER']).glob('*')))
        
        cleanup_old_files()
        
        after_uploads = len(list(Path(CONFIG['UPLOAD_FOLDER']).glob('*')))
        after_outputs = len(list(Path(CONFIG['OUTPUT_FOLDER']).glob('*')))
        
        return jsonify({
            'success': True,
            'message': 'Cleanup completed',
            'cleaned': {
                'uploads': before_uploads - after_uploads,
                'outputs': before_outputs - after_outputs
            }
        })
    except Exception as e:
        logger.error(f"Cleanup error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║              ISO 20022 XSD TOOLKIT - LOCAL DEPLOYMENT                ║
    ║                                                                      ║
    ║  🌐 URL: http://{host}:{port}                                       ║
    ║                                                                      ║
    ║  Features:                                                           ║
    ║    📊 Comprehensive XSD Analysis                                     ║
    ║    📝 Schema Documentation Generation                                ║
    ║    🔄 Schema Comparison (2+ files)                                  ║
    ║    🧪 Test XML Data Generation                                       ║
    ║                                                                      ║
    ║  Endpoints:                                                          ║
    ║    /health  - Health check                                           ║
    ║    /status  - Detailed status                                        ║
    ║    /cleanup - Trigger file cleanup                                   ║
    ║                                                                      ║
    ║  Press Ctrl+C to stop                                                ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """.format(host=CONFIG['HOST'], port=CONFIG['PORT']))
    
    logger.info(f"Starting ISO 20022 Toolkit on {CONFIG['HOST']}:{CONFIG['PORT']}")
    
    # Run initial cleanup
    cleanup_old_files()
    
    # Start server
    app.run(
        host=CONFIG['HOST'],
        port=CONFIG['PORT'],
        debug=CONFIG['DEBUG'],
        threaded=True
    )
