#!/usr/bin/env python3
"""
Remove Yellow (Inferred) - keep only real XSD annotations
"""

import re

tools_to_fix = [
    'iso20022_comprehensive_analyzer.py',
    'xsd_to_xml_enhanced.py',
    'xsd_comparison_enhanced.py',
]

print("Removing Yellow (Inferred) - keeping only XSD annotations")
print("=" * 70)

for tool_file in tools_to_fix:
    print(f"\nFixing {tool_file}...")
    
    with open(tool_file, 'r') as f:
        content = f.read()
    
    # Find and replace the classification method
    # Remove the heuristic/inference logic completely
    
    new_classification_method = '''
    def _classify_field_from_xsd(self, element, elem_name='', min_occurs='1', annotation=None):
        """
        Read Yellow/White ONLY from XSD annotations - NO ASSUMPTIONS
        Only uses official ISO 20022 spec annotations
        """
        # Only check XSD annotation - NO INFERENCE
        if element is not None:
            ns = getattr(self, 'ns', {'xs': 'http://www.w3.org/2001/XMLSchema'})
            annotation_elem = element.find('xs:annotation', ns)
            if annotation_elem is not None:
                docs = annotation_elem.findall('xs:documentation', ns)
                for doc in docs:
                    source = doc.get('source', '').strip()
                    
                    if source == 'Yellow Field':
                        return '🟡 Yellow (ISO 20022 Spec)'
                    elif source == 'White Field':
                        return '⚪ White (ISO 20022 Spec)'
        
        # NO INFERENCE - if not in XSD, mark as NA
        return '⚫ NA (Not in XSD)'
'''
    
    # Replace the method
    pattern = r'def _classify_field_from_xsd\(self.*?\n(?:\s{4}.*\n)*?(?=\n    def |\nclass |\Z)'
    content = re.sub(pattern, new_classification_method, content, flags=re.MULTILINE)
    
    with open(tool_file, 'w') as f:
        f.write(content)
    
    print(f"  ✅ Fixed - Now only uses XSD annotations, NO inference")

print("\n" + "=" * 70)
print("✅ All tools updated!")
print("   - Yellow/White ONLY from XSD source annotations")
print("   - NO assumptions/inference based on field names")
print("   - If not in XSD → marked as NA")
