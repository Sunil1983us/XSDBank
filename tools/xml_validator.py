#!/usr/bin/env python3
"""
ISO 20022 XML Validator
=======================
Validates XML messages against XSD schemas with comprehensive rule checking:

✅ XSD Schema Validation:
   - Structure validation
   - Type checking
   - Pattern matching
   - Length constraints
   - Enumeration values

✅ ISO 20022 Business Rules:
   - Either/Or rules (Ustrd/Strd, BICFI/LEI, etc.)
   - Cardinality rules
   - Conditional requirements

✅ Format Validation:
   - IBAN format
   - BIC format
   - Date/DateTime formats
   - Amount formats

✅ Detailed Error Reporting:
   - Line numbers
   - XPath locations
   - Severity levels
   - Suggested fixes
"""

import xml.etree.ElementTree as ET
import re
import json
import zipfile
import os
from datetime import datetime
from pathlib import Path
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from lxml import etree as lxml_etree
    HAS_LXML = True
except ImportError:
    HAS_LXML = False


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    severity: str
    category: str
    path: str
    element: str
    message: str
    line: Optional[int] = None
    value: Optional[str] = None
    expected: Optional[str] = None
    suggestion: Optional[str] = None


class ISO20022XMLValidator:
    """Comprehensive XML validator for ISO 20022 messages"""
    
    def __init__(self, xsd_file: str):
        self.xsd_file = xsd_file
        self.issues: List[ValidationIssue] = []
        self.xml_tree = None
        self.xml_root = None
        self.namespaces = {}
        
        # ISO 20022 Either/Or Rules
        self.either_or_rules = {
            'RmtInf': {
                'elements': ['Ustrd', 'Strd'],
                'rule': "Either 'Unstructured' or 'Structured' may be present, not both",
                'max_allowed': 1
            },
            'FinInstnId': {
                'elements': ['BICFI', 'LEI'],
                'rule': "Either 'BICFI' or 'LEI' is allowed for identification",
                'max_allowed': 1
            },
            'OrgId': {
                'elements': ['AnyBIC', 'LEI', 'Othr'],
                'rule': "Either 'AnyBIC', 'LEI' or 'Other' is allowed",
                'max_allowed': 1
            },
            'PrvtId': {
                'elements': ['DtAndPlcOfBirth', 'Othr'],
                'rule': "Either 'Date and Place of Birth' or 'Other' is allowed",
                'max_allowed': 1
            }
        }
        
        # Format patterns
        self.format_patterns = {
            'IBAN': r'^[A-Z]{2}[0-9]{2}[A-Z0-9]{4,30}$',
            'BIC': r'^[A-Z]{6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3})?$',
            'LEI': r'^[A-Z0-9]{18}[0-9]{2}$',
            'CountryCode': r'^[A-Z]{2}$',
            'CurrencyCode': r'^[A-Z]{3}$',
            'ISODate': r'^\d{4}-\d{2}-\d{2}$',
            'ISODateTime': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
            'UUID': r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$'
        }
        
        # Element to format mapping
        self.element_formats = {
            'IBAN': 'IBAN',
            'BICFI': 'BIC',
            'BIC': 'BIC',
            'AnyBIC': 'BIC',
            'LEI': 'LEI',
            'Ctry': 'CountryCode',
            'CtryOfBirth': 'CountryCode',
            'CtryOfRes': 'CountryCode',
            'Ccy': 'CurrencyCode',
            'CreDtTm': 'ISODateTime',
            'AccptncDtTm': 'ISODateTime',
            'IntrBkSttlmDt': 'ISODate',
            'ReqdExctnDt': 'ISODate',
            'UETR': 'UUID'
        }
    
    def validate(self, xml_file: str) -> Dict:
        """Run all validations on XML file"""
        self.issues = []
        
        # Parse XML
        if not self._parse_xml(xml_file):
            return self._generate_report()
        
        # XSD Schema Validation (if lxml available)
        if HAS_LXML:
            self._validate_xsd(xml_file)
        else:
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING.value,
                category="Setup",
                path="",
                element="",
                message="lxml not installed - XSD validation skipped. Install with: pip install lxml",
                suggestion="pip install lxml"
            ))
        
        # Business Rules Validation
        self._validate_either_or_rules()
        
        # Format Validation
        self._validate_formats()
        
        # Amount Validation
        self._validate_amounts()
        
        # Cardinality Validation
        self._validate_cardinality()
        
        return self._generate_report()
    
    def _parse_xml(self, xml_file: str) -> bool:
        """Parse XML file and extract namespaces"""
        try:
            self.xml_tree = ET.parse(xml_file)
            self.xml_root = self.xml_tree.getroot()
            
            # Extract namespace
            if self.xml_root.tag.startswith('{'):
                ns_end = self.xml_root.tag.index('}')
                self.namespaces['ns'] = self.xml_root.tag[1:ns_end]
            
            return True
        except ET.ParseError as e:
            self.issues.append(ValidationIssue(
                severity=Severity.ERROR.value,
                category="XML Parsing",
                path="",
                element="Document",
                message=f"XML parsing error: {str(e)}",
                line=getattr(e, 'position', (None,))[0]
            ))
            return False
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity=Severity.ERROR.value,
                category="XML Parsing",
                path="",
                element="Document",
                message=f"Failed to parse XML: {str(e)}"
            ))
            return False
    
    def _validate_xsd(self, xml_file: str):
        """Validate XML against XSD schema using lxml"""
        try:
            # Parse XSD
            with open(self.xsd_file, 'rb') as f:
                schema_doc = lxml_etree.parse(f)
            schema = lxml_etree.XMLSchema(schema_doc)
            
            # Parse and validate XML
            with open(xml_file, 'rb') as f:
                xml_doc = lxml_etree.parse(f)
            
            if not schema.validate(xml_doc):
                for error in schema.error_log:
                    # Parse error message to extract details
                    msg = str(error.message)
                    
                    # Determine category based on error type
                    category = "XSD Validation"
                    if 'pattern' in msg.lower():
                        category = "Pattern Mismatch"
                    elif 'enumeration' in msg.lower():
                        category = "Invalid Value"
                    elif 'length' in msg.lower():
                        category = "Length Constraint"
                    elif 'missing' in msg.lower() or 'expected' in msg.lower():
                        category = "Missing Element"
                    
                    # Extract element name from path
                    element = error.path.split('/')[-1] if error.path else ""
                    if '}' in element:
                        element = element.split('}')[-1]
                    
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR.value,
                        category=category,
                        path=error.path or "",
                        element=element,
                        message=msg,
                        line=error.line
                    ))
        
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity=Severity.ERROR.value,
                category="XSD Validation",
                path="",
                element="",
                message=f"XSD validation error: {str(e)}"
            ))
    
    def _validate_either_or_rules(self):
        """Validate ISO 20022 either/or business rules"""
        
        for parent_name, rule in self.either_or_rules.items():
            # Find all instances of the parent element
            parent_elements = self._find_elements_by_local_name(parent_name)
            
            for parent_elem in parent_elements:
                found_elements = []
                
                for child_name in rule['elements']:
                    children = self._find_children_by_local_name(parent_elem, child_name)
                    if children:
                        found_elements.append(child_name)
                
                # Check if more than one either/or element is present
                if len(found_elements) > rule['max_allowed']:
                    path = self._get_element_path(parent_elem)
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR.value,
                        category="Business Rule",
                        path=path,
                        element=parent_name,
                        message=f"Multiple mutually exclusive elements found: {', '.join(found_elements)}",
                        expected=f"Only one of: {', '.join(rule['elements'])}",
                        suggestion=f"Remove one of: {', '.join(found_elements)}. {rule['rule']}"
                    ))
    
    def _validate_formats(self):
        """Validate element formats (IBAN, BIC, dates, etc.)"""
        
        for elem_name, format_type in self.element_formats.items():
            elements = self._find_elements_by_local_name(elem_name)
            
            for elem in elements:
                value = elem.text
                if value:
                    pattern = self.format_patterns.get(format_type)
                    if pattern and not re.match(pattern, value.strip()):
                        path = self._get_element_path(elem)
                        
                        # Generate specific suggestion based on format type
                        suggestion = self._get_format_suggestion(format_type, value)
                        
                        self.issues.append(ValidationIssue(
                            severity=Severity.ERROR.value,
                            category="Format Validation",
                            path=path,
                            element=elem_name,
                            message=f"Invalid {format_type} format",
                            value=value,
                            expected=f"Pattern: {pattern}",
                            suggestion=suggestion
                        ))
    
    def _validate_amounts(self):
        """Validate amount fields"""
        
        amount_elements = ['Amt', 'IntrBkSttlmAmt', 'TtlIntrBkSttlmAmt', 'InstdAmt', 'EqvtAmt']
        
        for amt_name in amount_elements:
            elements = self._find_elements_by_local_name(amt_name)
            
            for elem in elements:
                value = elem.text
                path = self._get_element_path(elem)
                
                # Check if amount has a value
                if not value or not value.strip():
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR.value,
                        category="Amount Validation",
                        path=path,
                        element=amt_name,
                        message="Amount element is empty",
                        suggestion="Provide a numeric value (e.g., 1234.56)"
                    ))
                    continue
                
                # Check if amount is valid number
                try:
                    amount = float(value)
                    
                    # Check for negative amounts
                    if amount < 0:
                        self.issues.append(ValidationIssue(
                            severity=Severity.ERROR.value,
                            category="Amount Validation",
                            path=path,
                            element=amt_name,
                            message="Amount cannot be negative",
                            value=value,
                            suggestion="Use a positive amount value"
                        ))
                    
                    # Check decimal places (max 2 for most currencies)
                    if '.' in value:
                        decimals = len(value.split('.')[1])
                        if decimals > 2:
                            self.issues.append(ValidationIssue(
                                severity=Severity.WARNING.value,
                                category="Amount Validation",
                                path=path,
                                element=amt_name,
                                message=f"Amount has {decimals} decimal places (max 2 recommended)",
                                value=value,
                                suggestion="Round to 2 decimal places"
                            ))
                
                except ValueError:
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR.value,
                        category="Amount Validation",
                        path=path,
                        element=amt_name,
                        message="Amount is not a valid number",
                        value=value,
                        suggestion="Provide a valid numeric value"
                    ))
                
                # Check for currency attribute
                ccy = elem.get('Ccy')
                if not ccy:
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR.value,
                        category="Amount Validation",
                        path=path,
                        element=amt_name,
                        message="Missing 'Ccy' (currency) attribute",
                        suggestion="Add Ccy attribute (e.g., Ccy=\"EUR\")"
                    ))
                elif not re.match(r'^[A-Z]{3}$', ccy):
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR.value,
                        category="Amount Validation",
                        path=path,
                        element=amt_name,
                        message=f"Invalid currency code: {ccy}",
                        value=ccy,
                        expected="3-letter ISO currency code",
                        suggestion="Use valid ISO 4217 currency code (e.g., EUR, USD, GBP)"
                    ))
    
    def _validate_cardinality(self):
        """Validate element cardinality rules"""
        
        # Elements that should appear only once
        single_occurrence = ['MsgId', 'CreDtTm', 'NbOfTxs', 'TtlIntrBkSttlmAmt', 'IntrBkSttlmDt']
        
        for elem_name in single_occurrence:
            elements = self._find_elements_by_local_name(elem_name)
            
            if len(elements) > 1:
                self.issues.append(ValidationIssue(
                    severity=Severity.WARNING.value,
                    category="Cardinality",
                    path="",
                    element=elem_name,
                    message=f"Element '{elem_name}' appears {len(elements)} times (expected 1)",
                    suggestion=f"Remove duplicate '{elem_name}' elements"
                ))
    
    def _find_elements_by_local_name(self, local_name: str) -> List[ET.Element]:
        """Find all elements by local name (ignoring namespace)"""
        results = []
        
        def search(elem):
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag == local_name:
                results.append(elem)
            for child in elem:
                search(child)
        
        if self.xml_root is not None:
            search(self.xml_root)
        
        return results
    
    def _find_children_by_local_name(self, parent: ET.Element, local_name: str) -> List[ET.Element]:
        """Find direct children by local name"""
        results = []
        for child in parent:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == local_name:
                results.append(child)
        return results
    
    def _get_element_path(self, elem: ET.Element) -> str:
        """Get XPath-like path to element"""
        path_parts = []
        
        def build_path(element, root):
            for parent in root.iter():
                for child in parent:
                    if child == element:
                        parent_path = build_path(parent, root)
                        tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
                        return f"{parent_path}/{tag}" if parent_path else tag
            tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
            return tag
        
        if self.xml_root is not None:
            return build_path(elem, self.xml_root)
        return ""
    
    def _get_format_suggestion(self, format_type: str, value: str) -> str:
        """Generate specific suggestion based on format type"""
        suggestions = {
            'IBAN': "IBAN should be 2 letters + 2 digits + up to 30 alphanumeric (e.g., DE89370400440532013000)",
            'BIC': "BIC should be 8 or 11 characters (e.g., DEUTDEFF or DEUTDEFFXXX)",
            'LEI': "LEI should be 20 characters: 18 alphanumeric + 2 digits",
            'CountryCode': "Use 2-letter ISO 3166 country code (e.g., DE, FR, GB)",
            'CurrencyCode': "Use 3-letter ISO 4217 currency code (e.g., EUR, USD, GBP)",
            'ISODate': "Use format YYYY-MM-DD (e.g., 2024-01-15)",
            'ISODateTime': "Use format YYYY-MM-DDThh:mm:ss (e.g., 2024-01-15T14:30:00)",
            'UUID': "UETR must be UUID v4 format (e.g., 123e4567-e89b-42d3-a456-426614174000)"
        }
        return suggestions.get(format_type, "Check the format requirements")
    
    def _generate_report(self) -> Dict:
        """Generate validation report"""
        
        # Count by severity
        error_count = sum(1 for i in self.issues if i.severity == Severity.ERROR.value)
        warning_count = sum(1 for i in self.issues if i.severity == Severity.WARNING.value)
        info_count = sum(1 for i in self.issues if i.severity == Severity.INFO.value)
        
        # Count by category
        categories = {}
        for issue in self.issues:
            categories[issue.category] = categories.get(issue.category, 0) + 1
        
        return {
            'valid': error_count == 0,
            'summary': {
                'total_issues': len(self.issues),
                'errors': error_count,
                'warnings': warning_count,
                'info': info_count
            },
            'by_category': categories,
            'issues': [asdict(issue) for issue in self.issues]
        }


def validate_xml(xml_file: str, xsd_file: str) -> Dict:
    """Main validation function"""
    validator = ISO20022XMLValidator(xsd_file)
    return validator.validate(xml_file)


def extract_xsd_from_zip(zip_file: str, output_dir: str) -> List[str]:
    """Extract XSD files from a zip archive"""
    xsd_files = []
    
    with zipfile.ZipFile(zip_file, 'r') as zf:
        for name in zf.namelist():
            if name.endswith('.xsd'):
                zf.extract(name, output_dir)
                xsd_files.append(os.path.join(output_dir, name))
    
    return xsd_files


def main():
    parser = argparse.ArgumentParser(
        description='ISO 20022 XML Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate XML against XSD
  python xml_validator.py message.xml schema.xsd
  
  # Validate with XSD from zip file
  python xml_validator.py message.xml schemas.zip
  
  # Output as JSON
  python xml_validator.py message.xml schema.xsd --json
  
  # Save report to file
  python xml_validator.py message.xml schema.xsd -o report.json
        """
    )
    
    parser.add_argument('xml_file', help='XML file to validate')
    parser.add_argument('xsd_file', help='XSD schema file or ZIP containing XSD files')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('-o', '--output', help='Save report to file')
    
    args = parser.parse_args()
    
    # Check files exist
    if not Path(args.xml_file).exists():
        print(f"❌ Error: XML file '{args.xml_file}' not found")
        return
    
    if not Path(args.xsd_file).exists():
        print(f"❌ Error: XSD file '{args.xsd_file}' not found")
        return
    
    # Handle ZIP file
    xsd_file = args.xsd_file
    if args.xsd_file.endswith('.zip'):
        import tempfile
        temp_dir = tempfile.mkdtemp()
        xsd_files = extract_xsd_from_zip(args.xsd_file, temp_dir)
        if not xsd_files:
            print(f"❌ Error: No XSD files found in '{args.xsd_file}'")
            return
        xsd_file = xsd_files[0]  # Use first XSD found
        print(f"📂 Using XSD from ZIP: {os.path.basename(xsd_file)}")
    
    print(f"\n{'='*70}")
    print("ISO 20022 XML VALIDATOR")
    print(f"{'='*70}\n")
    print(f"📄 XML: {args.xml_file}")
    print(f"📋 XSD: {xsd_file}")
    
    if not HAS_LXML:
        print("\n⚠️  lxml not installed - XSD validation will be skipped")
        print("   Install with: pip install lxml")
    
    print(f"\n⏳ Validating...")
    
    # Run validation
    report = validate_xml(args.xml_file, xsd_file)
    
    # Output results
    if args.json or args.output:
        json_output = json.dumps(report, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(json_output)
            print(f"\n📁 Report saved to: {args.output}")
        else:
            print(json_output)
    else:
        # Pretty print results
        print(f"\n{'='*70}")
        print("VALIDATION RESULTS")
        print(f"{'='*70}")
        
        if report['valid']:
            print("\n✅ XML is VALID")
        else:
            print("\n❌ XML has ERRORS")
        
        print(f"\n📊 Summary:")
        print(f"   Total Issues: {report['summary']['total_issues']}")
        print(f"   Errors:       {report['summary']['errors']}")
        print(f"   Warnings:     {report['summary']['warnings']}")
        print(f"   Info:         {report['summary']['info']}")
        
        if report['by_category']:
            print(f"\n📂 By Category:")
            for cat, count in sorted(report['by_category'].items()):
                print(f"   {cat}: {count}")
        
        if report['issues']:
            print(f"\n{'='*70}")
            print("ISSUES DETAIL")
            print(f"{'='*70}")
            
            for i, issue in enumerate(report['issues'], 1):
                severity_icon = "❌" if issue['severity'] == 'ERROR' else "⚠️" if issue['severity'] == 'WARNING' else "ℹ️"
                print(f"\n{severity_icon} Issue #{i}: [{issue['severity']}] {issue['category']}")
                print(f"   Element: {issue['element']}")
                if issue['path']:
                    print(f"   Path: {issue['path']}")
                if issue['line']:
                    print(f"   Line: {issue['line']}")
                print(f"   Message: {issue['message']}")
                if issue['value']:
                    print(f"   Value: {issue['value']}")
                if issue['expected']:
                    print(f"   Expected: {issue['expected']}")
                if issue['suggestion']:
                    print(f"   💡 Suggestion: {issue['suggestion']}")
    
    print(f"\n{'='*70}")
    print("VALIDATION COMPLETE")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
