#!/usr/bin/env python3
"""Update Flask app.py with comprehensive analyzer mapping"""

file_path = '/home/claude/iso_toolkit_final/app.py'

with open(file_path, 'r') as f:
    content = f.read()

# Add comprehensive analyzer mapping
comprehensive_mapping = '''
        if tool == 'comprehensive':
            # ISO 20022 Comprehensive Analyzer
            script = os.path.join(tools_dir, 'iso20022_comprehensive_analyzer.py')
            output_file = os.path.join(output_dir, f"{output_base}_comprehensive.xlsx")
            
            cmd = [sys.executable, script, file_paths[0], '-o', output_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_file):
                return {
                    'success': True,
                    'message': 'ISO 20022 comprehensive analysis complete!',
                    'files': [os.path.basename(output_file)]
                }
            else:
                return {'success': False, 'error': 'Failed to generate comprehensive analysis'}
        
        elif tool == 'document':
'''

if "tool == 'comprehensive'" not in content:
    # Find the execute_tool function and insert
    match = re.search(r"def execute_tool.*?if tool == 'document':", content, re.DOTALL)
    if match:
        insert_pos = match.end() - len("if tool == 'document':")
        content = content[:insert_pos] + comprehensive_mapping + content[insert_pos + len("if tool == 'document':"):]

with open(file_path, 'w') as f:
    f.write(content)

print("✅ Updated app.py with comprehensive analyzer mapping")
