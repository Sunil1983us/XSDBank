#!/usr/bin/env python3
"""
XSD Test Data Generator
Generates valid XML test files from XSD schemas
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import random
import string
from datetime import datetime, timedelta
from code_set_loader import get_code_sets
import argparse
from pathlib import Path


class TestDataGenerator:
    def _classify_field_from_xsd(self, element, elem_name='', min_occurs='1', annotation=None):
        """Read Yellow/White from XSD annotations - ISO 20022 Spec"""
        # Try to get element if passed as string
        if isinstance(element, str):
            elem_name = element
            element = None
        
        # Check XSD annotation first
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
        
        # Fallback to heuristics
        elem_lower = elem_name.lower() if elem_name else ''
        core_fields = ['id', 'iban', 'bic', 'amount', 'amt', 'currency', 'ccy',
                       'debtor', 'creditor', 'name', 'nm', 'date', 'dt',
                       'ref', 'msgid', 'code', 'cd', 'status', 'sts']
        
        if any(core in elem_lower for core in core_fields):
            return '🟡 Yellow (Inferred)'
        
        return '⚫ NA (Not Specified)'

    """Generate test XML data from XSD schemas"""
    
    NAMESPACES = {
        'xs': 'http://www.w3.org/2001/XMLSchema',
        'xsd': 'http://www.w3.org/2001/XMLSchema'
    }
    
    def __init__(self, xsd_file):
        self.xsd_file = xsd_file
        self.tree = ET.parse(xsd_file)
        self.root = self.tree.getroot()
        self.ns_prefix = self._detect_namespace()
        self.type_cache = {}
        self._build_type_cache()
        self.target_namespace = self.root.get('targetNamespace', '')
        
    def _detect_namespace(self):
        tag = self.root.tag
        if '{http://www.w3.org/2001/XMLSchema}' in tag:
            return '{http://www.w3.org/2001/XMLSchema}'
        return ''
    
    def _build_type_cache(self):
        """Build cache of all types"""
        for complex_type in self.root.findall(f'{self.ns_prefix}complexType', self.NAMESPACES):
            type_name = complex_type.get('name', '')
            if type_name:
                self.type_cache[type_name] = complex_type
        
        for simple_type in self.root.findall(f'{self.ns_prefix}simpleType', self.NAMESPACES):
            type_name = simple_type.get('name', '')
            if type_name:
                self.type_cache[type_name] = simple_type
    
    def generate_test_xml(self, num_files=1, output_dir='test_data', scenario='valid'):
        """Generate test XML files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n⏳ Generating {num_files} test XML file(s)...")
        print(f"   Scenario: {scenario}")
        print(f"   Output: {output_dir}/")
        
        generated_files = []
        
        for i in range(num_files):
            filename = f"test_{scenario}_{i+1:03d}.xml"
            filepath = output_path / filename
            
            xml_content = self._generate_message(scenario)
            
            # Pretty print
            pretty_xml = self._prettify_xml(xml_content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)
            
            generated_files.append(str(filepath))
            
            if (i + 1) % 10 == 0:
                print(f"   Generated {i+1}/{num_files}...")
        
        print(f"\n✅ Generated {len(generated_files)} test files")
        return generated_files
    
    def _generate_message(self, scenario='valid'):
        """Generate a complete message"""
        # Find root element
        root_elem = self.root.find(f'{self.ns_prefix}element', self.NAMESPACES)
        if root_elem is None:
            raise Exception("No root element found in XSD")
        
        element_name = root_elem.get('name', 'Document')
        element_type = root_elem.get('type', '')
        
        # Create XML root
        if self.target_namespace:
            xml_root = ET.Element(element_name, xmlns=self.target_namespace)
        else:
            xml_root = ET.Element(element_name)
        
        # Generate content
        self._populate_element(xml_root, element_name, element_type, scenario)
        
        return xml_root
    
    def _populate_element(self, xml_elem, element_name, element_type, scenario, depth=0):
        """Populate an XML element with data"""
        
        if depth > 10:  # Prevent infinite recursion
            return
        
        # Get type definition
        type_def = self.type_cache.get(element_type)
        if type_def is None:
            # Simple built-in type
            xml_elem.text = self._generate_simple_value(element_type, element_name, scenario)
            return
        
        tag_name = self._get_tag_name(type_def)
        
        if tag_name == 'simpleType':
            # Generate value for simple type
            xml_elem.text = self._generate_simple_type_value(type_def, element_name, scenario)
        
        elif tag_name == 'complexType':
            # Handle complex type
            self._populate_complex_type(xml_elem, type_def, scenario, depth)
    
    def _populate_complex_type(self, xml_elem, complex_type, scenario, depth):
        """Populate complex type"""
        
        # Handle complexContent
        complex_content = complex_type.find(f'{self.ns_prefix}complexContent', self.NAMESPACES)
        if complex_content is not None:
            restriction = complex_content.find(f'{self.ns_prefix}restriction', self.NAMESPACES)
            extension = complex_content.find(f'{self.ns_prefix}extension', self.NAMESPACES)
            
            target = restriction if restriction is not None else extension
            if target is not None:
                base = target.get('base', '')
                base_type = self.type_cache.get(base)
                if base_type is not None:
                    self._populate_complex_type(xml_elem, base_type, scenario, depth)
                
                self._populate_type_content(xml_elem, target, scenario, depth)
        else:
            self._populate_type_content(xml_elem, complex_type, scenario, depth)
    
    def _populate_type_content(self, xml_elem, type_node, scenario, depth):
        """Populate type content (sequence, choice, etc.)"""
        
        # Handle sequence
        for seq in type_node.findall(f'{self.ns_prefix}sequence', self.NAMESPACES):
            for child_elem in seq.findall(f'{self.ns_prefix}element', self.NAMESPACES):
                child_name = child_elem.get('name', '')
                child_type = child_elem.get('type', '')
                min_occurs = child_elem.get('minOccurs', '1')
                max_occurs = child_elem.get('maxOccurs', '1')
                
                # Decide whether to include (always include if required)
                if scenario == 'valid':
                    include = min_occurs != '0' or random.random() > 0.3
                elif scenario == 'minimal':
                    include = min_occurs != '0'
                else:  # maximal
                    include = True
                
                if include:
                    # Determine occurrences
                    if max_occurs == 'unbounded':
                        occurrences = random.randint(1, 3) if scenario == 'valid' else 1
                    else:
                        try:
                            occurrences = min(int(max_occurs), 1)
                        except:
                            occurrences = 1
                    
                    for _ in range(occurrences):
                        child_xml = ET.SubElement(xml_elem, child_name)
                        self._populate_element(child_xml, child_name, child_type, scenario, depth + 1)
        
        # Handle choice (pick first option for simplicity)
        for choice in type_node.findall(f'{self.ns_prefix}choice', self.NAMESPACES):
            choice_elems = choice.findall(f'{self.ns_prefix}element', self.NAMESPACES)
            if choice_elems:
                # Pick random choice element
                child_elem = random.choice(choice_elems)
                child_name = child_elem.get('name', '')
                child_type = child_elem.get('type', '')
                
                child_xml = ET.SubElement(xml_elem, child_name)
                self._populate_element(child_xml, child_name, child_type, scenario, depth + 1)
        
        # Handle attributes
        for attr in type_node.findall(f'{self.ns_prefix}attribute', self.NAMESPACES):
            attr_name = attr.get('name', '')
            attr_type = attr.get('type', '')
            use = attr.get('use', 'optional')
            
            if use == 'required' or (scenario != 'minimal' and random.random() > 0.5):
                attr_value = self._generate_simple_value(attr_type, attr_name, scenario)
                xml_elem.set(attr_name, attr_value)
    
    def _generate_simple_type_value(self, simple_type, element_name, scenario):
        """Generate value for simple type with restrictions"""
        
        restriction = simple_type.find(f'{self.ns_prefix}restriction', self.NAMESPACES)
        if restriction is None:
            return self._generate_default_value(element_name)
        
        base = restriction.get('base', 'string')
        
        # Check for enumeration
        enums = [e.get('value', '') for e in restriction.findall(f'{self.ns_prefix}enumeration', self.NAMESPACES)]
        if enums:
            return random.choice(enums)
        
        # Check for pattern
        pattern = restriction.find(f'{self.ns_prefix}pattern', self.NAMESPACES)
        if pattern is not None:
            pattern_value = pattern.get('value', '')
            return self._generate_from_pattern(pattern_value, element_name)
        
        # Check for length constraints
        min_length = restriction.find(f'{self.ns_prefix}minLength', self.NAMESPACES)
        max_length = restriction.find(f'{self.ns_prefix}maxLength', self.NAMESPACES)
        length = restriction.find(f'{self.ns_prefix}length', self.NAMESPACES)
        
        if length is not None:
            target_length = int(length.get('value', '10'))
            return self._generate_string(target_length, element_name)
        elif max_length is not None:
            max_len = int(max_length.get('value', '35'))
            min_len = int(min_length.get('value', '1')) if min_length is not None else 1
            target_length = random.randint(min_len, max_len)
            return self._generate_string(target_length, element_name)
        
        # Fallback to base type
        return self._generate_simple_value(base, element_name, scenario)
    
    def _generate_simple_value(self, type_name, element_name, scenario):
        """Generate value for simple type"""
        
        type_lower = type_name.lower() if type_name else ''
        elem_lower = element_name.lower()
        
        # Date/Time types
        if 'datetime' in type_lower:
            return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        elif 'date' in type_lower:
            return datetime.now().strftime('%Y-%m-%d')
        elif 'time' in type_lower:
            return datetime.now().strftime('%H:%M:%S')
        
        # Numeric types
        elif 'decimal' in type_lower or 'amount' in elem_lower:
            return str(round(random.uniform(1.0, 10000.0), 2))
        elif 'integer' in type_lower or 'int' in type_lower:
            return str(random.randint(1, 100))
        elif 'boolean' in type_lower:
            return random.choice(['true', 'false'])
        
        # String types - context-aware
        elif 'iban' in elem_lower:
            return self._generate_iban()
        elif 'bic' in elem_lower or 'swift' in elem_lower:
            return self._generate_bic()
        elif 'currency' in elem_lower or elem_lower == 'ccy':
            return random.choice(['EUR', 'USD', 'GBP'])
        elif 'country' in elem_lower or elem_lower == 'ctry':
            return random.choice(['DE', 'FR', 'GB', 'US'])
        elif 'msgid' in elem_lower or 'id' in elem_lower:
            return f"{element_name.upper()}{random.randint(1000, 9999)}"
        elif 'name' in elem_lower or 'nm' in elem_lower:
            return f"Test {element_name}"
        else:
            return self._generate_default_value(element_name)
    
    def _generate_from_pattern(self, pattern, element_name):
        """Generate value matching pattern"""
        
        # Common patterns
        if pattern == '[A-Z]{3,3}':
            return ''.join(random.choices(string.ascii_uppercase, k=3))
        elif pattern == '[A-Z]{2}[0-9]{2}[A-Z0-9]+':
            return self._generate_iban()
        elif '[A-Z]' in pattern and '{2}' in pattern:
            return ''.join(random.choices(string.ascii_uppercase, k=2))
        elif '[0-9]' in pattern:
            try:
                count = int(pattern.split('{')[1].split('}')[0])
                return ''.join(random.choices(string.digits, k=count))
            except:
                return '123456'
        else:
            return f"PATTERN_{element_name.upper()}"
    
    def _generate_string(self, length, element_name):
        """Generate string of specific length"""
        if length <= 10:
            return element_name[:length].ljust(length, 'X')
        else:
            base = f"Test{element_name}"
            return (base * (length // len(base) + 1))[:length]
    
    def _generate_default_value(self, element_name):
        """Generate default value"""
        return f"Sample{element_name}"
    
    def _generate_iban(self):
        """Generate valid-looking IBAN"""
        country = random.choice(['DE', 'FR', 'GB'])
        check = random.randint(10, 99)
        account = ''.join(random.choices(string.digits + string.ascii_uppercase, k=18))
        return f"{country}{check}{account}"
    
    def _generate_bic(self):
        """Generate valid-looking BIC"""
        bank = ''.join(random.choices(string.ascii_uppercase, k=4))
        country = random.choice(['DE', 'FR', 'GB'])
        location = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
        branch = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        return f"{bank}{country}{location}{branch}"
    
    def _get_tag_name(self, element):
        tag = element.tag
        if '}' in tag:
            return tag.split('}')[1]
        return tag
    
    def _prettify_xml(self, elem):
        """Return a pretty-printed XML string"""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


def main():
    parser = argparse.ArgumentParser(
        description='Generate test XML files from XSD schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 10 valid test files
  python %(prog)s schema.xsd -n 10
  
  # Generate minimal test files (only required fields)
  python %(prog)s schema.xsd -n 5 --scenario minimal
  
  # Generate maximal test files (all fields)
  python %(prog)s schema.xsd -n 5 --scenario maximal
  
  # Custom output directory
  python %(prog)s schema.xsd -n 20 -o my_test_data/
        """
    )
    
    parser.add_argument('xsd_file', help='XSD schema file')
    parser.add_argument('-n', '--num', type=int, default=1, help='Number of test files to generate')
    parser.add_argument('-o', '--output', default='test_data', help='Output directory')
    parser.add_argument('--scenario', choices=['valid', 'minimal', 'maximal'],
                       default='valid', help='Test scenario type')
    parser.add_argument('--mandatory', action='store_true',
                       help='Generate only mandatory fields (minOccurs != 0)')
    
    args = parser.parse_args()
    
    if not Path(args.xsd_file).exists():
        print(f"❌ Error: File '{args.xsd_file}' not found")
        return
    
    print(f"\n{'='*70}")
    print("XSD TEST DATA GENERATOR")
    print(f"{'='*70}")
    print(f"\n📂 Schema: {args.xsd_file}")
    
    # Generate test data
    generator = TestDataGenerator(args.xsd_file)
    files = generator.generate_test_xml(
        num_files=args.num,
        output_dir=args.output,
        scenario=args.scenario
    )
    
    print(f"\n{'='*70}")
    print("✅ GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"\n📁 Files saved to: {args.output}/")
    print(f"📊 Total files: {len(files)}")
    print(f"\nYou can now use these files for:")
    print("  • Testing your XML parser")
    print("  • Validation testing")
    print("  • Integration testing")
    print("  • Performance testing")
    print()


if __name__ == '__main__':
    main()
