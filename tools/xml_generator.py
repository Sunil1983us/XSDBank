#!/usr/bin/env python3
"""
ISO 20022 Test Data Generator - ENHANCED VERSION
=================================================
✅ Full XSD Rule Support:
   - sequence, choice, all
   - Nested choice within sequence
   - minOccurs, maxOccurs handling
   - Fixed values
   - Pattern, enumeration, length constraints
   - minInclusive, maxInclusive for amounts
   - fractionDigits, totalDigits

✅ ISO 20022 Specific:
   - Usage Rules from annotations
   - Yellow/White field awareness
   - Rulebook constraints parsing

✅ Parameterized Test Data:
   - Configurable Debtor/Creditor IBAN, BIC, Name
   - Test profiles (domestic, cross-border, instant)
   - Amount ranges
   - Date handling

✅ Validation:
   - XSD validation of generated XML
   - Generation report with choices made
"""

import xml.etree.ElementTree as ET
import random
import re
import json
import uuid
from datetime import datetime
from pathlib import Path
import argparse
from decimal import Decimal
from typing import Dict, List, Optional

try:
    import rstr
    HAS_RSTR = True
except ImportError:
    HAS_RSTR = False

try:
    from lxml import etree as lxml_etree
    HAS_LXML = True
except ImportError:
    HAS_LXML = False


# =============================================================================
# TEST DATA PROFILES - Loaded from JSON
# =============================================================================

def load_test_profiles() -> Dict:
    """Load test profiles from JSON file in data folder"""
    # Try multiple locations for the profiles file
    possible_paths = [
        Path(__file__).parent.parent / 'data' / 'test_profiles.json',  # tools/../data/
        Path(__file__).parent / 'data' / 'test_profiles.json',          # tools/data/
        Path('data') / 'test_profiles.json',                             # ./data/
        Path(__file__).parent.parent / 'test_profiles.json',            # tools/../
    ]
    
    for profile_path in possible_paths:
        if profile_path.exists():
            try:
                with open(profile_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('profiles', {})
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load {profile_path}: {e}")
    
    # Fallback to minimal built-in profile if JSON not found
    print("Warning: test_profiles.json not found, using minimal fallback profile")
    return {
        "domestic_sepa": {
            "description": "Domestic SEPA Credit Transfer (Fallback)",
            "debtor": {
                "name": "Test Debtor",
                "iban": "DE89370400440532013000",
                "bic": "DEUTDEFF",
                "country": "DE",
                "address": {"street": "Test Street 1", "city": "Berlin", "postal_code": "10115", "country": "DE"}
            },
            "creditor": {
                "name": "Test Creditor",
                "iban": "DE91100000000123456789",
                "bic": "MARKDEFF",
                "country": "DE",
                "address": {"street": "Test Street 2", "city": "Munich", "postal_code": "80331", "country": "DE"}
            },
            "amount": {"min": 10.00, "max": 50000.00, "currency": "EUR"},
            "service_level": "SEPA",
            "local_instrument": "CORE",
            "charge_bearer": "SLEV"
        }
    }

# Load profiles at module initialization
DEFAULT_TEST_PROFILES = load_test_profiles()


class EnhancedTestDataGenerator:
    """Enhanced ISO 20022 Test XML Generator with full XSD rule support"""
    
    def __init__(self, xsd_file: str, profile: Dict = None, config_file: str = None):
        self.xsd_file = xsd_file
        self.tree = ET.parse(xsd_file)
        self.root = self.tree.getroot()
        self.ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        self.target_ns = self.root.get('targetNamespace', '')
        
        self.type_cache = {}
        self.element_cache = {}
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                self.profile = json.load(f)
        elif profile:
            self.profile = profile
        else:
            self.profile = DEFAULT_TEST_PROFILES.get("domestic_sepa", {})
        
        self.choices_made = []
        self.usage_rules_applied = []
        self.yellow_fields_generated = []
        self.validation_errors = []
        
        # Either/Or rules from ISO 20022 annotations (not enforced by xs:choice)
        # These are element pairs/groups where only ONE should be generated
        # Key is the parent element name or type name pattern
        self.either_or_rules = {
            # RmtInf: Either Ustrd OR Strd (not both)
            'RmtInf': {'pick_one': ['Ustrd', 'Strd'], 'prefer': 'Ustrd'},
            'RemittanceInformation': {'pick_one': ['Ustrd', 'Strd'], 'prefer': 'Ustrd'},
            
            # FinInstnId: Either BICFI OR LEI (not both)  
            'FinInstnId': {'pick_one': ['BICFI', 'LEI'], 'prefer': 'BICFI'},
            
            # OrgId: Either AnyBIC OR LEI OR Othr (only one)
            'OrgId': {'pick_one': ['AnyBIC', 'LEI', 'Othr'], 'prefer': 'Othr'},
            
            # PrvtId: Either DtAndPlcOfBirth OR Othr (only one)
            'PrvtId': {'pick_one': ['DtAndPlcOfBirth', 'Othr'], 'prefer': 'Othr'},
        }
        
        # Track which either/or selection was made at each path
        self.either_or_selections = {}
        
        self._build_caches()
    
    def _build_caches(self):
        for simple_type in self.root.findall('.//xs:simpleType', self.ns):
            name = simple_type.get('name')
            if name:
                self.type_cache[name] = simple_type
        
        for complex_type in self.root.findall('.//xs:complexType', self.ns):
            name = complex_type.get('name')
            if name:
                self.type_cache[name] = complex_type
        
        for elem in self.root.findall('xs:element', self.ns):
            name = elem.get('name')
            if name:
                self.element_cache[name] = elem
    
    def generate_xml(self, output_file: str, mandatory_only: bool = False, 
                     yellow_only: bool = False) -> str:
        self.choices_made = []
        self.usage_rules_applied = []
        self.yellow_fields_generated = []
        self.validation_errors = []
        
        root_elements = list(self.root.findall('xs:element', self.ns))
        if not root_elements:
            raise ValueError("No root element found in XSD")
        
        root_elem_def = root_elements[0]
        xml_root = self._generate_element(root_elem_def, mandatory_only=mandatory_only,
                                         yellow_only=yellow_only, parent_path='')
        
        if xml_root is None:
            raise ValueError("Failed to generate root element")
        
        if self.target_ns:
            xml_root.set('xmlns', self.target_ns)
        
        tree = ET.ElementTree(xml_root)
        ET.indent(tree, space='  ')
        tree.write(output_file, encoding='UTF-8', xml_declaration=True)
        
        if HAS_LXML:
            self._validate_xml(output_file)
        
        return output_file
    
    def _generate_element(self, elem_def, mandatory_only=False, yellow_only=False,
                          parent_path='') -> Optional[ET.Element]:
        elem_name = elem_def.get('name') or elem_def.get('ref', '').split(':')[-1]
        elem_type = elem_def.get('type', '').split(':')[-1]
        min_occurs = elem_def.get('minOccurs', '1')
        fixed_value = elem_def.get('fixed')
        
        current_path = f"{parent_path}/{elem_name}" if parent_path else elem_name
        
        is_yellow = self._is_yellow_field(elem_def)
        if is_yellow:
            self.yellow_fields_generated.append(current_path)
        
        if mandatory_only and min_occurs == '0' and not is_yellow:
            return None
        if yellow_only and not is_yellow and min_occurs == '0':
            return None
        
        if self.target_ns:
            xml_elem = ET.Element(f"{{{self.target_ns}}}{elem_name}")
        else:
            xml_elem = ET.Element(elem_name)
        
        if fixed_value:
            xml_elem.text = fixed_value
            return xml_elem
        
        inline_complex = elem_def.find('xs:complexType', self.ns)
        if inline_complex is not None:
            self._process_complex_type(xml_elem, inline_complex, mandatory_only, 
                                       yellow_only, current_path)
            return xml_elem
        
        inline_simple = elem_def.find('xs:simpleType', self.ns)
        if inline_simple is not None:
            value = self._generate_simple_value(elem_name, inline_simple, current_path)
            xml_elem.text = value
            return xml_elem
        
        if elem_type:
            type_def = self.type_cache.get(elem_type)
            if type_def is not None:
                if type_def.tag.endswith('complexType'):
                    self._process_complex_type(xml_elem, type_def, mandatory_only,
                                              yellow_only, current_path)
                elif type_def.tag.endswith('simpleType'):
                    value = self._generate_simple_value(elem_name, type_def, current_path)
                    xml_elem.text = value
                return xml_elem
            else:
                xml_elem.text = self._generate_basic_value(elem_name, elem_type, current_path)
                return xml_elem
        
        return xml_elem
    
    def _process_complex_type(self, xml_elem, complex_type, mandatory_only, 
                              yellow_only, current_path):
        for attr in complex_type.findall('.//xs:attribute', self.ns):
            attr_name = attr.get('name')
            attr_use = attr.get('use', 'optional')
            attr_fixed = attr.get('fixed')
            
            if attr_fixed:
                xml_elem.set(attr_name, attr_fixed)
            elif attr_use == 'required' or not mandatory_only:
                xml_elem.set(attr_name, self._generate_attribute_value(attr_name, attr))
        
        simple_content = complex_type.find('xs:simpleContent', self.ns)
        if simple_content is not None:
            extension = simple_content.find('xs:extension', self.ns)
            restriction = simple_content.find('xs:restriction', self.ns)
            content_def = extension if extension is not None else restriction
            
            if content_def is not None:
                base_type = content_def.get('base', '').split(':')[-1]
                tag_name = xml_elem.tag.split('}')[-1] if '}' in xml_elem.tag else xml_elem.tag
                
                # Generate text value based on element name and base type
                if 'amt' in tag_name.lower() or 'amount' in tag_name.lower() or 'decimal' in base_type.lower():
                    xml_elem.text = self._generate_amount({}, current_path)
                else:
                    xml_elem.text = self._generate_basic_value(tag_name, base_type, current_path)
                
                # Handle attributes in the extension/restriction
                for attr in content_def.findall('xs:attribute', self.ns):
                    attr_name = attr.get('name')
                    attr_use = attr.get('use', 'optional')
                    attr_fixed = attr.get('fixed')
                    
                    if attr_fixed:
                        xml_elem.set(attr_name, attr_fixed)
                    elif attr_use == 'required' or not mandatory_only:
                        xml_elem.set(attr_name, self._generate_attribute_value(attr_name, attr))
            return
        
        complex_content = complex_type.find('xs:complexContent', self.ns)
        if complex_content is not None:
            restriction = complex_content.find('xs:restriction', self.ns)
            extension = complex_content.find('xs:extension', self.ns)
            content_elem = restriction if restriction is not None else extension
            
            if content_elem is not None:
                self._process_compositor(xml_elem, content_elem, mandatory_only,
                                        yellow_only, current_path)
                return
        
        self._process_compositor(xml_elem, complex_type, mandatory_only,
                                yellow_only, current_path)
    
    def _process_compositor(self, xml_elem, parent, mandatory_only, yellow_only, current_path):
        sequence = parent.find('xs:sequence', self.ns)
        if sequence is not None:
            self._process_sequence(xml_elem, sequence, mandatory_only, yellow_only, current_path)
            return
        
        choice = parent.find('xs:choice', self.ns)
        if choice is not None:
            self._process_choice(xml_elem, choice, mandatory_only, yellow_only, current_path)
            return
        
        all_elem = parent.find('xs:all', self.ns)
        if all_elem is not None:
            self._process_all(xml_elem, all_elem, mandatory_only, yellow_only, current_path)
    
    def _process_sequence(self, parent_xml, sequence, mandatory_only, yellow_only, parent_path):
        # Get parent element name for either/or rule checking
        parent_elem_name = parent_path.split('/')[-1] if parent_path else ''
        
        # Check if parent has either/or rules
        either_or_rule = None
        for rule_key, rule_def in self.either_or_rules.items():
            if rule_key in parent_elem_name:
                either_or_rule = rule_def
                break
        
        # If either/or rule applies, determine which element to pick
        selected_element = None
        if either_or_rule:
            pick_one_elements = either_or_rule['pick_one']
            prefer = either_or_rule.get('prefer')
            
            # Check which elements from pick_one are actually in this sequence
            available_options = []
            for child in sequence:
                if child.tag.split('}')[-1] == 'element':
                    child_name = child.get('name', '')
                    if child_name in pick_one_elements:
                        available_options.append(child_name)
            
            # Select one (prefer the preferred one if available)
            if available_options:
                if prefer and prefer in available_options:
                    selected_element = prefer
                else:
                    selected_element = random.choice(available_options)
                
                # Record the selection
                self.either_or_selections[parent_path] = selected_element
                self.usage_rules_applied.append({
                    'path': parent_path,
                    'rule': f"Either/Or: picked '{selected_element}' from {pick_one_elements}",
                    'options': available_options
                })
        
        # Process sequence elements
        for child in sequence:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            
            if tag == 'element':
                child_name = child.get('name', '')
                
                # Skip elements not selected in either/or rule
                if either_or_rule and child_name in either_or_rule['pick_one']:
                    if child_name != selected_element:
                        continue  # Skip this element, it wasn't selected
                
                child_xml = self._generate_element(child, mandatory_only, yellow_only, parent_path)
                if child_xml is not None:
                    max_occurs = child.get('maxOccurs', '1')
                    parent_xml.append(child_xml)
                    # Only add additional occurrences if allowed AND not in either/or context
                    if not either_or_rule and (max_occurs == 'unbounded' or int(max_occurs) > 1) and random.random() < 0.3:
                        child_xml2 = self._generate_element(child, mandatory_only, yellow_only, parent_path)
                        if child_xml2 is not None:
                            parent_xml.append(child_xml2)
            
            elif tag == 'choice':
                self._process_choice(parent_xml, child, mandatory_only, yellow_only, parent_path)
            
            elif tag == 'sequence':
                self._process_sequence(parent_xml, child, mandatory_only, yellow_only, parent_path)
            
            elif tag == 'group':
                ref = child.get('ref', '').split(':')[-1]
                group_def = self.root.find(f'.//xs:group[@name="{ref}"]', self.ns)
                if group_def is not None:
                    self._process_compositor(parent_xml, group_def, mandatory_only, yellow_only, parent_path)
    
    def _process_choice(self, parent_xml, choice, mandatory_only, yellow_only, parent_path):
        options = []
        for child in choice:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'element':
                options.append(('element', child))
            elif tag == 'sequence':
                options.append(('sequence', child))
            elif tag == 'choice':
                options.append(('choice', child))
        
        if not options:
            return
        
        selected_option = self._select_choice_option(options, parent_path)
        option_type, option_def = selected_option
        
        if option_type == 'element':
            elem_name = option_def.get('name', '')
            self.choices_made.append({
                'path': parent_path,
                'selected': elem_name,
                'options': [o[1].get('name', 'sequence/choice') for o in options]
            })
            child_xml = self._generate_element(option_def, mandatory_only, yellow_only, parent_path)
            if child_xml is not None:
                parent_xml.append(child_xml)
        
        elif option_type == 'sequence':
            self.choices_made.append({
                'path': parent_path,
                'selected': 'sequence',
                'options': [o[1].get('name', 'sequence/choice') for o in options]
            })
            self._process_sequence(parent_xml, option_def, mandatory_only, yellow_only, parent_path)
        
        elif option_type == 'choice':
            self._process_choice(parent_xml, option_def, mandatory_only, yellow_only, parent_path)
    
    def _process_all(self, parent_xml, all_elem, mandatory_only, yellow_only, parent_path):
        elements = list(all_elem.findall('xs:element', self.ns))
        random.shuffle(elements)
        
        for child in elements:
            child_xml = self._generate_element(child, mandatory_only, yellow_only, parent_path)
            if child_xml is not None:
                parent_xml.append(child_xml)
    
    def _select_choice_option(self, options, parent_path) -> tuple:
        path_lower = parent_path.lower()
        
        for opt_type, opt_def in options:
            if opt_type == 'element':
                name = opt_def.get('name', '')
                if name == 'Cd':
                    return (opt_type, opt_def)
        
        for opt_type, opt_def in options:
            if opt_type == 'element':
                name = opt_def.get('name', '')
                if name == 'IBAN':
                    return (opt_type, opt_def)
        
        if 'dbtr' in path_lower or 'cdtr' in path_lower:
            for opt_type, opt_def in options:
                if opt_type == 'element' and opt_def.get('name') == 'OrgId':
                    return (opt_type, opt_def)
        
        return random.choice(options)
    
    def _is_yellow_field(self, elem_def) -> bool:
        annotation = elem_def.find('xs:annotation', self.ns)
        if annotation is not None:
            for doc in annotation.findall('xs:documentation', self.ns):
                source = doc.get('source', '')
                if source == 'Yellow Field':
                    return True
        return False
    
    def _generate_simple_value(self, elem_name: str, simple_type, current_path: str) -> str:
        restrictions = self._extract_all_restrictions(simple_type)
        
        if 'enumeration' in restrictions:
            return self._select_enumeration(restrictions['enumeration'], elem_name, current_path)
        
        if 'pattern' in restrictions:
            return self._generate_from_pattern(restrictions['pattern'], elem_name, restrictions)
        
        return self._generate_restricted_value(elem_name, restrictions, current_path)
    
    def _extract_all_restrictions(self, simple_type) -> Dict:
        restrictions = {}
        restriction = simple_type.find('xs:restriction', self.ns)
        
        if restriction is not None:
            restrictions['base'] = restriction.get('base', '').split(':')[-1]
            
            pattern = restriction.find('xs:pattern', self.ns)
            if pattern is not None:
                restrictions['pattern'] = pattern.get('value')
            
            for tag in ['minLength', 'maxLength', 'length']:
                elem = restriction.find(f'xs:{tag}', self.ns)
                if elem is not None:
                    restrictions[tag] = int(elem.get('value'))
            
            for tag in ['minInclusive', 'maxInclusive', 'minExclusive', 'maxExclusive']:
                elem = restriction.find(f'xs:{tag}', self.ns)
                if elem is not None:
                    restrictions[tag] = Decimal(elem.get('value'))
            
            for tag in ['totalDigits', 'fractionDigits']:
                elem = restriction.find(f'xs:{tag}', self.ns)
                if elem is not None:
                    restrictions[tag] = int(elem.get('value'))
            
            enums = restriction.findall('xs:enumeration', self.ns)
            if enums:
                restrictions['enumeration'] = [e.get('value') for e in enums]
        
        return restrictions
    
    def _select_enumeration(self, enums: List[str], elem_name: str, current_path: str) -> str:
        path_lower = current_path.lower()
        
        if 'svclvl' in path_lower and 'cd' in elem_name.lower():
            if self.profile.get('service_level') in enums:
                return self.profile['service_level']
        
        if 'lclinstrm' in path_lower and 'cd' in elem_name.lower():
            if self.profile.get('local_instrument') in enums:
                return self.profile['local_instrument']
        
        if 'chrgbr' in path_lower:
            if self.profile.get('charge_bearer') in enums:
                return self.profile['charge_bearer']
        
        return random.choice(enums)
    
    def _generate_from_pattern(self, pattern: str, elem_name: str, restrictions: Dict) -> str:
        elem_lower = elem_name.lower()
        
        if 'bic' in elem_lower:
            return self._get_bic_from_context(elem_lower)
        
        if 'iban' in elem_lower:
            return self._get_iban_from_context(elem_lower)
        
        # UUID v4 pattern for UETR
        if pattern and 'a-f0-9' in pattern and '4[a-f0-9]' in pattern:
            return str(uuid.uuid4())
        
        # ISODateTime pattern
        if pattern and '[0-9]{4}(-[0-9]{2}){2}T[0-9]{2}' in pattern:
            return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        
        if HAS_RSTR and pattern:
            try:
                value = rstr.xeger(pattern)
                if 'maxLength' in restrictions and len(value) > restrictions['maxLength']:
                    value = value[:restrictions['maxLength']]
                return value
            except:
                pass
        
        return self._simple_pattern_gen(pattern, restrictions)
    
    def _simple_pattern_gen(self, pattern: str, restrictions: Dict) -> str:
        if not pattern:
            return 'TestValue'
        
        # Country code pattern [A-Z]{2,2} or [A-Z]{2}
        if re.match(r'^\[A-Z\]\{2,?2?\}$', pattern):
            return random.choice(['DE', 'FR', 'GB', 'NL', 'ES', 'IT', 'BE', 'AT'])
        
        # Currency code pattern [A-Z]{3,3} or [A-Z]{3}
        if re.match(r'^\[A-Z\]\{3,?3?\}$', pattern):
            return random.choice(['EUR', 'USD', 'GBP', 'CHF', 'SEK', 'NOK', 'DKK'])
        
        # Numeric pattern [0-9]{1,n}
        match = re.match(r'\[0-9\]\{1,(\d+)\}', pattern)
        if match:
            max_len = int(match.group(1))
            length = random.randint(1, min(max_len, 5))
            return ''.join(random.choices('0123456789', k=length))
        
        # Fixed length uppercase [A-Z]{n,n} or [A-Z]{n}
        match = re.match(r'\[A-Z\]\{(\d+)(?:,\1)?\}', pattern)
        if match:
            length = int(match.group(1))
            return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))
        
        # Fixed length numeric [0-9]{n,n} or [0-9]{n}
        match = re.match(r'\[0-9\]\{(\d+)(?:,\1)?\}', pattern)
        if match:
            length = int(match.group(1))
            return ''.join(random.choices('0123456789', k=length))
        
        # Alphanumeric pattern [A-Za-z0-9]
        if '[A-Za-z0-9]' in pattern or '[a-zA-Z0-9]' in pattern:
            match = re.search(r'\{(\d+)(?:,(\d+))?\}', pattern)
            if match:
                min_len = int(match.group(1))
                max_len = int(match.group(2)) if match.group(2) else min_len
                length = random.randint(min_len, min(max_len, 20))
                chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
                return ''.join(random.choices(chars, k=length))
        
        # BIC pattern [A-Z]{6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3})?
        if '[A-Z]{6}' in pattern and 'A-Z2-9' in pattern:
            return random.choice(['DEUTDEFF', 'BNPAFRPP', 'BARCGB22', 'CRESCHZZ'])
        
        # IBAN-like pattern
        if '[A-Z]{2}' in pattern and '[0-9]' in pattern:
            return 'DE89370400440532013000'
        
        # Default alphanumeric
        return 'TEST' + ''.join(random.choices('0123456789', k=6))
    
    def _generate_restricted_value(self, elem_name: str, restrictions: Dict, current_path: str) -> str:
        base_type = restrictions.get('base', 'string')
        
        if 'decimal' in base_type.lower() or 'amt' in elem_name.lower():
            return self._generate_amount(restrictions, current_path)
        
        if base_type in ['integer', 'int', 'long', 'short']:
            return self._generate_integer(restrictions)
        
        return self._generate_string(elem_name, restrictions, current_path)
    
    def _generate_amount(self, restrictions: Dict, current_path: str) -> str:
        min_val = float(restrictions.get('minInclusive', Decimal('0.01')))
        max_val = float(restrictions.get('maxInclusive', Decimal('999999999.99')))
        fraction_digits = restrictions.get('fractionDigits', 2)
        
        if self.profile.get('amount'):
            min_val = max(min_val, self.profile['amount'].get('min', min_val))
            max_val = min(max_val, self.profile['amount'].get('max', max_val))
        
        amount = round(random.uniform(min_val, max_val), fraction_digits)
        return f"{amount:.{fraction_digits}f}"
    
    def _generate_integer(self, restrictions: Dict) -> str:
        min_val = int(restrictions.get('minInclusive', 0))
        max_val = int(restrictions.get('maxInclusive', 999999))
        return str(random.randint(min_val, max_val))
    
    def _generate_string(self, elem_name: str, restrictions: Dict, current_path: str) -> str:
        min_length = restrictions.get('minLength', 1)
        max_length = restrictions.get('maxLength', 100)
        
        value = self._generate_basic_value(elem_name, 'string', current_path)
        
        if len(value) < min_length:
            value = value + 'X' * (min_length - len(value))
        if len(value) > max_length:
            value = value[:max_length]
        
        return value
    
    def _generate_basic_value(self, elem_name: str, elem_type: str, current_path: str) -> str:
        elem_lower = elem_name.lower()
        path_lower = current_path.lower()
        
        # BIC/BICFI
        if 'bic' in elem_lower or 'bicfi' in elem_lower:
            return self._get_bic_from_context(path_lower)
        
        # IBAN
        if 'iban' in elem_lower:
            return self._get_iban_from_context(path_lower)
        
        # LEI (Legal Entity Identifier) - 20 characters
        if elem_lower == 'lei':
            return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=18)) + '00'
        
        # AnyBIC
        if elem_lower == 'anybic':
            return self._get_bic_from_context(path_lower)
        
        # Name
        if elem_lower == 'nm' or 'name' in elem_lower:
            return self._get_name_from_context(path_lower)
        
        # Country code (2 letters)
        if elem_lower in ['ctry', 'ctryofbirth', 'ctryofres']:
            return self._get_country_from_context(path_lower)
        
        # Currency code (3 letters)
        if 'ccy' in elem_lower:
            return self.profile.get('amount', {}).get('currency', 'EUR')
        
        # Number of transactions (numeric)
        if elem_lower == 'nboftxs':
            return '1'
        
        # Control sum
        if elem_lower == 'ctrlsum':
            return self._generate_amount({}, current_path)
        
        # DateTime handling - check for DtTm pattern (case insensitive)
        if 'dttm' in elem_lower or 'datetime' in elem_lower:
            return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        # Date only fields
        if 'dt' in elem_lower or 'date' in elem_lower:
            return datetime.now().strftime('%Y-%m-%d')
        
        # Amount fields
        if 'amt' in elem_lower:
            return self._generate_amount({}, current_path)
        
        # ID/Reference fields
        if elem_lower in ['id', 'msgid', 'instrid', 'endtoendid', 'txid', 'uetr', 'clrtxid']:
            return self._generate_id(elem_name)
        
        # Address elements
        if elem_lower in ['strtnm', 'bldgnb', 'pstcd', 'twnnm', 'adrline', 'pstladr']:
            return self._get_address_element(elem_lower, path_lower)
        
        # Charge bearer
        if elem_lower == 'chrgbr':
            return self.profile.get('charge_bearer', 'SLEV')
        
        # Settlement method
        if elem_lower == 'sttlmmtd':
            return 'CLRG'
        
        # Purpose code
        if elem_lower == 'cd' and 'purp' in path_lower:
            return 'SALA'
        
        # Generic code fields
        if elem_lower == 'cd':
            return 'TEST'
        
        # Proprietary fields
        if elem_lower == 'prtry':
            return 'PROPRIETARY'
        
        # Issuer
        if elem_lower == 'issr':
            return 'ISSUER'
        
        # Number fields (generic)
        if 'nb' in elem_lower:
            return str(random.randint(1, 100))
        
        # Unstructured remittance
        if elem_lower == 'ustrd':
            return 'Payment for invoice 12345'
        
        # Reference
        if elem_lower == 'ref':
            return f"REF{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        # Default - generate safe alphanumeric
        return f"Test{elem_name}"[:35]
    
    def _get_bic_from_context(self, path_lower: str) -> str:
        if 'dbtr' in path_lower or 'instg' in path_lower:
            return self.profile.get('debtor', {}).get('bic', 'DEUTDEFF')
        elif 'cdtr' in path_lower or 'instd' in path_lower:
            return self.profile.get('creditor', {}).get('bic', 'BNPAFRPP')
        return random.choice(['DEUTDEFF', 'BNPAFRPP', 'BARCGB22', 'CRESCHZZ'])
    
    def _get_iban_from_context(self, path_lower: str) -> str:
        if 'dbtr' in path_lower:
            return self.profile.get('debtor', {}).get('iban', 'DE89370400440532013000')
        elif 'cdtr' in path_lower:
            return self.profile.get('creditor', {}).get('iban', 'FR7630006000011234567890189')
        return random.choice(['DE89370400440532013000', 'FR7630006000011234567890189'])
    
    def _get_name_from_context(self, path_lower: str) -> str:
        if 'ultmtdbtr' in path_lower:
            return self.profile.get('debtor', {}).get('name', 'John Smith') + ' (Ultimate)'
        elif 'dbtr' in path_lower:
            return self.profile.get('debtor', {}).get('name', 'John Smith')
        elif 'ultmtcdtr' in path_lower:
            return self.profile.get('creditor', {}).get('name', 'Jane Doe') + ' (Ultimate)'
        elif 'cdtr' in path_lower:
            return self.profile.get('creditor', {}).get('name', 'Jane Doe')
        return random.choice(['John Smith', 'Jane Doe', 'Global Corp Ltd'])
    
    def _get_country_from_context(self, path_lower: str) -> str:
        if 'dbtr' in path_lower:
            return self.profile.get('debtor', {}).get('country', 'DE')
        elif 'cdtr' in path_lower:
            return self.profile.get('creditor', {}).get('country', 'FR')
        return random.choice(['DE', 'FR', 'GB', 'NL', 'ES', 'IT'])
    
    def _get_address_element(self, elem_lower: str, path_lower: str) -> str:
        if 'dbtr' in path_lower:
            address = self.profile.get('debtor', {}).get('address', {})
        elif 'cdtr' in path_lower:
            address = self.profile.get('creditor', {}).get('address', {})
        else:
            address = {}
        
        if 'strtnm' in elem_lower:
            return address.get('street', 'Main Street 123')
        elif 'pstcd' in elem_lower:
            return address.get('postal_code', '10115')
        elif 'twnnm' in elem_lower:
            return address.get('city', 'Berlin')
        elif 'adrline' in elem_lower:
            return f"{address.get('street', 'Main St')} {address.get('city', 'City')}"
        return 'Address Line'
    
    def _generate_id(self, elem_name: str) -> str:
        elem_lower = elem_name.lower()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_part = ''.join(random.choices('0123456789abcdef', k=12))
        
        if elem_lower == 'msgid':
            return f"MSG{timestamp}{random_part[:6].upper()}"
        elif elem_lower == 'uetr':
            # UETR must be UUID v4 format: [a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}
            return str(uuid.uuid4())
        elif elem_lower == 'endtoendid':
            return f"E2E{timestamp}{random_part[:6].upper()}"
        elif elem_lower == 'txid':
            return f"TX{timestamp}{random_part[:6].upper()}"
        return f"{elem_name}{random_part}"
    
    def _generate_attribute_value(self, attr_name: str, attr_def) -> str:
        if 'ccy' in attr_name.lower():
            return self.profile.get('amount', {}).get('currency', 'EUR')
        return 'AttrValue'
    
    def _validate_xml(self, xml_file: str) -> bool:
        if not HAS_LXML:
            return True
        
        try:
            with open(self.xsd_file, 'rb') as f:
                schema_doc = lxml_etree.parse(f)
            schema = lxml_etree.XMLSchema(schema_doc)
            
            with open(xml_file, 'rb') as f:
                xml_doc = lxml_etree.parse(f)
            
            if not schema.validate(xml_doc):
                for error in schema.error_log:
                    self.validation_errors.append(str(error))
                return False
            return True
        except Exception as e:
            self.validation_errors.append(f"Validation error: {e}")
            return False
    
    def get_generation_report(self) -> Dict:
        return {
            'choices_made': self.choices_made,
            'usage_rules_applied': self.usage_rules_applied,
            'either_or_selections': self.either_or_selections,
            'yellow_fields_generated': self.yellow_fields_generated,
            'validation_errors': self.validation_errors,
            'profile_used': self.profile.get('description', 'Custom profile')
        }


def main():
    parser = argparse.ArgumentParser(
        description='ISO 20022 Enhanced Test Data Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xml_generator.py schema.xsd -o output/
  python xml_generator.py schema.xsd -o output/ --profile instant_payment
  python xml_generator.py schema.xsd -o output/ --mandatory
  python xml_generator.py schema.xsd -o output/ -n 5 --report

Available profiles:
  - domestic_sepa     : Domestic SEPA Credit Transfer
  - cross_border      : Cross-border SEPA Credit Transfer  
  - instant_payment   : SEPA Instant Credit Transfer
  - high_value        : High Value Payment
        """
    )
    
    parser.add_argument('xsd_file', help='XSD schema file')
    parser.add_argument('-n', '--num', type=int, default=1, help='Number of test files')
    parser.add_argument('-o', '--output', default='test_data', help='Output directory')
    parser.add_argument('--profile', choices=list(DEFAULT_TEST_PROFILES.keys()),
                       default='domestic_sepa', help='Test data profile')
    parser.add_argument('--config', help='Custom profile JSON file')
    parser.add_argument('--mandatory', action='store_true', help='Generate only mandatory fields')
    parser.add_argument('--yellow-only', action='store_true', help='Generate only Yellow fields')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')
    
    args = parser.parse_args()
    
    if not Path(args.xsd_file).exists():
        print(f"Error: File '{args.xsd_file}' not found")
        return
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*70}")
    print("ISO 20022 ENHANCED TEST DATA GENERATOR")
    print(f"{'='*70}\n")
    print(f"Schema: {args.xsd_file}")
    
    if args.config:
        profile = None
        config_file = args.config
        print(f"Profile: Custom ({args.config})")
    else:
        profile = DEFAULT_TEST_PROFILES.get(args.profile, {})
        config_file = None
        print(f"Profile: {args.profile} - {profile.get('description', 'N/A')}")
    
    print(f"\nGenerating {args.num} test XML file(s)...")
    
    generator = EnhancedTestDataGenerator(args.xsd_file, profile, config_file)
    
    for i in range(args.num):
        output_file = output_dir / f"test_{args.profile}_{str(i+1).zfill(3)}.xml"
        generator.generate_xml(str(output_file), mandatory_only=args.mandatory,
                              yellow_only=args.yellow_only)
        print(f"  Generated: {output_file.name}")
    
    if args.report:
        report = generator.get_generation_report()
        print(f"\n{'='*70}")
        print("GENERATION REPORT")
        print(f"{'='*70}")
        print(f"\nProfile: {report['profile_used']}")
        
        print(f"\n📋 Choices made (xs:choice): {len(report['choices_made'])}")
        for choice in report['choices_made'][:10]:
            print(f"  {choice['path']}: selected '{choice['selected']}' from {choice['options']}")
        if len(report['choices_made']) > 10:
            print(f"  ... and {len(report['choices_made']) - 10} more")
        
        print(f"\n⚖️  Either/Or rules applied: {len(report['usage_rules_applied'])}")
        for rule in report['usage_rules_applied'][:10]:
            print(f"  {rule['path']}: {rule['rule']}")
        if len(report['usage_rules_applied']) > 10:
            print(f"  ... and {len(report['usage_rules_applied']) - 10} more")
        
        print(f"\n🟡 Yellow fields: {len(report['yellow_fields_generated'])}")
        
        if report['validation_errors']:
            print(f"\n⚠️  Validation errors: {len(report['validation_errors'])}")
            for err in report['validation_errors'][:5]:
                print(f"  {err}")
    
    print(f"\n{'='*70}")
    print("COMPLETE!")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
