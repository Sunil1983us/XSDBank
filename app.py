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
        'ALLOWED_EXTENSIONS': {'xsd', 'xml', 'zip'},
        
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
                    'suggestion': 'Only .xsd, .xml, and .zip files are allowed'
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
                       'xml_validate', 'xml_diff', 'batch_validate', 'mapping_template', 'xml_transform']
        
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
        
        # Validate file paths
        file_paths = []
        missing_files = []
        
        for f in files:
            fp = os.path.join(CONFIG['UPLOAD_FOLDER'], f)
            if os.path.exists(fp):
                file_paths.append(fp)
            else:
                missing_files.append(f)
        
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
        
        else:
            return {'success': False, 'error': f'Unknown tool: {tool}'}
            
    except subprocess.TimeoutExpired:
        logger.error(f"Tool {tool} timed out after {timeout}s")
        return {'success': False, 'error': f'Timeout after {timeout} seconds'}
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return {'success': False, 'error': str(e)}

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
                'mapping_template', 'xml_transform'
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
