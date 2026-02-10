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
        
        # Folders
        'UPLOAD_FOLDER': os.environ.get('TOOLKIT_UPLOAD_FOLDER', 'static/uploads'),
        'OUTPUT_FOLDER': os.environ.get('TOOLKIT_OUTPUT_FOLDER', 'static/outputs'),
        'TOOLS_FOLDER': os.environ.get('TOOLKIT_TOOLS_FOLDER', 'tools'),
        'LOG_FOLDER': os.environ.get('TOOLKIT_LOG_FOLDER', 'logs'),
        
        # Processing
        'TIMEOUT_SECONDS': int(os.environ.get('TOOLKIT_TIMEOUT', '300')),
        'CLEANUP_HOURS': int(os.environ.get('TOOLKIT_CLEANUP_HOURS', '24')),
        
        # Allowed file extensions
        'ALLOWED_EXTENSIONS': {'xsd', 'xml'},
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
    """Handle file uploads"""
    try:
        if 'files[]' not in request.files:
            logger.warning("Upload attempted without files")
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files[]')
        uploaded_files = []
        
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(CONFIG['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                uploaded_files.append(unique_filename)
                logger.info(f"File uploaded: {unique_filename}")
        
        if not uploaded_files:
            logger.warning("No valid files in upload")
            return jsonify({'error': 'No valid files uploaded. Only .xsd and .xml files are allowed.'}), 400
            
        return jsonify({'success': True, 'files': uploaded_files})
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/run_tool', methods=['POST'])
def run_tool():
    """Execute analysis tool"""
    try:
        data = request.json
        tool = data.get('tool')
        files = data.get('files', [])
        options = data.get('options', {})
        
        if not tool or not files:
            return jsonify({'error': 'Missing tool or files'}), 400
        
        file_paths = [os.path.join(CONFIG['UPLOAD_FOLDER'], f) for f in files]
        
        for fp in file_paths:
            if not os.path.exists(fp):
                logger.error(f"File not found: {fp}")
                return jsonify({'error': 'File not found'}), 400
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_base = f"output_{timestamp}"
        
        logger.info(f"Running tool: {tool} on {len(files)} file(s)")
        result = execute_tool(tool, file_paths, output_base, options)
        
        if result.get('success'):
            logger.info(f"Tool {tool} completed successfully")
        else:
            logger.warning(f"Tool {tool} failed: {result.get('error')}")
        
        return jsonify(result)
            
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return jsonify({'error': str(e)}), 500

def execute_tool(tool, file_paths, output_base, options):
    """Execute the specified analysis tool"""
    try:
        output_dir = CONFIG['OUTPUT_FOLDER']
        tools_dir = CONFIG['TOOLS_FOLDER']
        timeout = CONFIG['TIMEOUT_SECONDS']
        
        if tool == 'comprehensive':
            # Comprehensive analyzer
            script = os.path.join(tools_dir, 'iso20022_comprehensive_analyzer.py')
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
            script = os.path.join(tools_dir, 'xsd_to_xml_enhanced.py')
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
            
            script = os.path.join(tools_dir, 'xsd_comparison_enhanced.py')
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
            
            script = os.path.join(tools_dir, 'xsd_ultimate_compare_enhanced.py')
            output_base_path = os.path.join(output_dir, output_base)
            
            cmd = [sys.executable, script] + file_paths + ['-o', output_base_path]
            
            if options.get('names'):
                names = [n.strip() for n in options['names'].split(',')]
                cmd.extend(['-n'] + names)
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * 2)
            
            if result.returncode == 0:
                generated_files = []
                for f in os.listdir(output_dir):
                    if f.startswith(os.path.basename(output_base)):
                        generated_files.append(f)
                
                return {
                    'success': True,
                    'message': f'Generated {len(generated_files)} files!',
                    'files': sorted(generated_files)
                }
            else:
                return {'success': False, 'error': 'Multi-comparison failed'}
        
        elif tool == 'test_data':
            script = os.path.join(tools_dir, 'test_data_generator.py')
            num_files = int(options.get('num_files', 10))
            scenario = options.get('scenario', 'valid')
            output_folder = os.path.join(output_dir, f"{output_base}_testdata")
            
            cmd = [sys.executable, script, file_paths[0], 
                   '-n', str(num_files), 
                   '--scenario', scenario,
                   '-o', output_folder]
            
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
                    'message': f'Generated {num_files} test XML files!',
                    'files': [os.path.basename(zip_path)]
                }
            else:
                return {'success': False, 'error': 'Test data generation failed'}
        
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
        
        return jsonify({
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0-local',
            'config': {
                'host': CONFIG['HOST'],
                'port': CONFIG['PORT'],
                'max_upload_mb': CONFIG['MAX_CONTENT_LENGTH'] // (1024 * 1024),
                'timeout_seconds': CONFIG['TIMEOUT_SECONDS']
            },
            'files': {
                'uploads': upload_count,
                'outputs': output_count
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/cleanup', methods=['POST'])
def trigger_cleanup():
    """Manual cleanup trigger"""
    try:
        cleanup_old_files()
        return jsonify({'success': True, 'message': 'Cleanup completed'})
    except Exception as e:
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
