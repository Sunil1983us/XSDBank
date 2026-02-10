#!/usr/bin/env python3
"""Update test data generator with code sets and mandatory mode"""

import re

file_path = '/home/claude/iso_toolkit_final/tools/test_data_generator.py'

with open(file_path, 'r') as f:
    content = f.read()

# 1. Add import for code sets at the top
if 'from code_set_loader import get_code_sets' not in content:
    # Find imports section
    import_pos = content.find('import argparse')
    if import_pos > 0:
        content = content[:import_pos] + 'from code_set_loader import get_code_sets\n' + content[import_pos:]

# 2. Initialize code sets in SampleValueGenerator __init__
init_addition = '''
        # Initialize ISO 20022 code sets
        try:
            self.code_sets = get_code_sets()
        except:
            self.code_sets = None
'''

if 'self.code_sets = get_code_sets()' not in content:
    # Find SampleValueGenerator init
    match = re.search(r'class SampleValueGenerator.*?def __init__\(self\):', content, re.DOTALL)
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + init_addition + content[insert_pos:]

# 3. Use code sets in generate method
code_set_check = '''
        # ISSUE 4: Check if type is an external code set
        if elem_type and self.code_sets and 'External' in elem_type and 'Code' in elem_type:
            sample = self.code_sets.get_sample_value(elem_type)
            if sample:
                return sample
'''

if 'Check if type is an external code set' not in content:
    # Find generate method
    match = re.search(r'def generate\(self, element_name, elem_type.*?\):', content)
    if match:
        # Find first line after method definition
        insert_pos = content.find('\n', match.end()) + 1
        content = content[:insert_pos] + code_set_check + content[insert_pos:]

# 4. Add mandatory mode support in main
if '--mandatory' not in content:
    # Add argument
    parser_section = content.find("parser.add_argument('--scenario'")
    if parser_section > 0:
        next_line = content.find('\n', parser_section)
        mandatory_arg = "\n    parser.add_argument('--mandatory', action='store_true',\n                       help='Generate only mandatory fields (minOccurs != 0)')"
        content = content[:next_line] + mandatory_arg + content[next_line:]

# 5. Update scenario handling
content = content.replace(
    "scenario = args.scenario",
    "scenario = 'mandatory' if args.mandatory else args.scenario"
)

with open(file_path, 'w') as f:
    f.write(content)

print("✅ Updated test_data_generator.py with:")
print("   - ISO 20022 code set integration")
print("   - Mandatory-only mode (--mandatory flag)")
