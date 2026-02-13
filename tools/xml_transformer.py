#!/usr/bin/env python3
"""
ISO 20022 XML Transformer
=========================
Transform XML messages between different schema versions or formats.

Features:
✅ Version migration (e.g., pacs.008.001.02 → pacs.008.001.08)
✅ Scheme conversion (e.g., SEPA → ISO base)
✅ Auto-mapping of matching fields
✅ Handle added/removed/renamed elements
✅ Transformation report with mappings used
✅ Validation of output against target schema
"""

import xml.etree.ElementTree as ET
import json
import argparse
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from copy import deepcopy

try:
    from lxml import etree as lxml_etree
    HAS_LXML = True
except ImportError:
    HAS_LXML = False


@dataclass
class TransformAction:
    action: str  # 'mapped', 'added', 'removed', 'renamed', 'transformed', 'default'
    source_path: Optional[str]
    target_path: str
    source_value: Optional[str]
    target_value: Optional[str]
    notes: Optional[str] = None


class SchemaAnalyzer:
    """Analyze XSD schema structure"""
    
    def __init__(self, xsd_file: str):
        self.xsd_file = xsd_file
        self.tree = ET.parse(xsd_file)
        self.root = self.tree.getroot()
        self.ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        self.target_ns = self.root.get('targetNamespace', '')
        self.elements: Dict[str, Dict] = {}
        self.type_cache = {}
        
        self._cache_types()
        self._extract_elements()
    
    def _cache_types(self):
        """Cache all type definitions"""
        for elem in self.root.findall('.//xs:complexType[@name]', self.ns):
            self.type_cache[elem.get('name')] = elem
        for elem in self.root.findall('.//xs:simpleType[@name]', self.ns):
            self.type_cache[elem.get('name')] = elem
    
    def _extract_elements(self):
        """Extract all elements with their paths"""
        root_elem = self.root.find('xs:element', self.ns)
        if root_elem is not None:
            self._process_element(root_elem, "")
    
    def _process_element(self, element, parent_path: str):
        """Process an element and its children"""
        elem_name = element.get('name', '')
        elem_type = element.get('type', '')
        
        if not elem_name:
            return
        
        current_path = f"{parent_path}/{elem_name}" if parent_path else elem_name
        
        # Store element info
        self.elements[current_path] = {
            'name': elem_name,
            'type': elem_type,
            'min_occurs': element.get('minOccurs', '1'),
            'max_occurs': element.get('maxOccurs', '1'),
            'path': current_path
        }
        
        # Process children
        self._process_children(element, elem_type, current_path)
    
    def _process_children(self, element, type_name: str, parent_path: str):
        """Process child elements"""
        complex_type = element.find('xs:complexType', self.ns)
        
        if complex_type is None and type_name:
            type_name_clean = type_name.split(':')[-1]
            complex_type = self.type_cache.get(type_name_clean)
        
        if complex_type is None:
            return
        
        # Process all compositors
        for compositor in ['xs:sequence', 'xs:choice', 'xs:all']:
            for comp in complex_type.findall(f'.//{compositor}', self.ns):
                for child in comp.findall('xs:element', self.ns):
                    child_ref = child.get('ref')
                    if child_ref:
                        ref_name = child_ref.split(':')[-1]
                        ref_elem = self.root.find(f".//xs:element[@name='{ref_name}']", self.ns)
                        if ref_elem is not None:
                            self._process_element(ref_elem, parent_path)
                    else:
                        self._process_element(child, parent_path)
        
        # Handle complex content extension
        complex_content = complex_type.find('xs:complexContent', self.ns)
        if complex_content is not None:
            extension = complex_content.find('xs:extension', self.ns)
            if extension is not None:
                base_type = extension.get('base', '').split(':')[-1]
                if base_type in self.type_cache:
                    self._process_children_from_type(self.type_cache[base_type], parent_path)
    
    def _process_children_from_type(self, type_elem, parent_path: str):
        """Process children from a type definition"""
        for compositor in ['xs:sequence', 'xs:choice', 'xs:all']:
            for comp in type_elem.findall(f'.//{compositor}', self.ns):
                for child in comp.findall('xs:element', self.ns):
                    self._process_element(child, parent_path)
    
    def get_all_paths(self) -> Set[str]:
        """Get all element paths"""
        return set(self.elements.keys())
    
    def get_element_by_name(self, name: str) -> List[str]:
        """Find elements by name (returns all matching paths)"""
        return [path for path, info in self.elements.items() 
                if info['name'] == name]


class XMLTransformer:
    """Transform XML between schema versions"""
    
    def __init__(self, source_xsd: str, target_xsd: str):
        self.source_xsd = source_xsd
        self.target_xsd = target_xsd
        
        print("   Analyzing source schema...")
        self.source_schema = SchemaAnalyzer(source_xsd)
        print("   Analyzing target schema...")
        self.target_schema = SchemaAnalyzer(target_xsd)
        
        self.actions: List[TransformAction] = []
        self.field_mappings: Dict[str, str] = {}
        
        # Build automatic mappings
        self._build_mappings()
    
    def _build_mappings(self):
        """Build field mappings between schemas"""
        source_paths = self.source_schema.get_all_paths()
        target_paths = self.target_schema.get_all_paths()
        
        # Direct path matches
        for path in source_paths:
            if path in target_paths:
                self.field_mappings[path] = path
        
        # Name-based matching for non-direct matches
        source_names = {self.source_schema.elements[p]['name']: p for p in source_paths}
        target_names = {self.target_schema.elements[p]['name']: p for p in target_paths}
        
        for name, source_path in source_names.items():
            if source_path not in self.field_mappings and name in target_names:
                # Check if parent path structure is similar
                target_path = target_names[name]
                source_parts = source_path.split('/')
                target_parts = target_path.split('/')
                
                # If element names in path are mostly similar, map them
                if len(source_parts) == len(target_parts):
                    matching = sum(1 for s, t in zip(source_parts, target_parts) if s == t)
                    if matching >= len(source_parts) * 0.7:  # 70% similarity
                        self.field_mappings[source_path] = target_path
    
    def add_custom_mapping(self, source_path: str, target_path: str):
        """Add a custom field mapping"""
        self.field_mappings[source_path] = target_path
    
    def transform(self, source_xml: str, output_xml: str, 
                  preserve_values: bool = True,
                  add_defaults: bool = True) -> Dict:
        """Transform XML from source to target schema"""
        self.actions = []
        
        # Parse source XML
        try:
            source_tree = ET.parse(source_xml)
            source_root = source_tree.getroot()
        except ET.ParseError as e:
            return {'success': False, 'error': f'Failed to parse source XML: {e}'}
        
        # Extract source namespace
        source_ns = ''
        if source_root.tag.startswith('{'):
            ns_end = source_root.tag.index('}')
            source_ns = source_root.tag[1:ns_end]
        
        # Build source data map
        source_data = self._extract_data(source_root, "", source_ns)
        
        # Create target structure
        target_ns = self.target_schema.target_ns
        target_root = self._build_target_structure(source_data, target_ns, add_defaults)
        
        if target_root is None:
            return {'success': False, 'error': 'Failed to build target structure'}
        
        # Write output
        target_tree = ET.ElementTree(target_root)
        ET.indent(target_tree, space="  ")
        
        # Register namespace
        if target_ns:
            ET.register_namespace('', target_ns)
        
        target_tree.write(output_xml, encoding='UTF-8', xml_declaration=True)
        
        # Validate output if lxml available
        validation_errors = []
        if HAS_LXML:
            validation_errors = self._validate_output(output_xml)
        
        # Generate report
        return {
            'success': True,
            'source_file': source_xml,
            'target_file': output_xml,
            'source_schema': os.path.basename(self.source_xsd),
            'target_schema': os.path.basename(self.target_xsd),
            'summary': {
                'total_actions': len(self.actions),
                'mapped': sum(1 for a in self.actions if a.action == 'mapped'),
                'added_defaults': sum(1 for a in self.actions if a.action == 'default'),
                'not_mapped': sum(1 for a in self.actions if a.action == 'removed'),
                'transformed': sum(1 for a in self.actions if a.action == 'transformed')
            },
            'validation_errors': validation_errors,
            'actions': [asdict(a) for a in self.actions[:100]]  # Limit for report
        }
    
    def _extract_data(self, element, parent_path: str, ns: str) -> Dict[str, str]:
        """Extract all data from source XML"""
        data = {}
        
        # Get element name without namespace
        tag = element.tag
        if '}' in tag:
            tag = tag.split('}')[1]
        
        current_path = f"{parent_path}/{tag}" if parent_path else tag
        
        # Store text content
        if element.text and element.text.strip():
            data[current_path] = element.text.strip()
        
        # Store attributes
        for attr, value in element.attrib.items():
            attr_name = attr.split('}')[-1] if '}' in attr else attr
            data[f"{current_path}/@{attr_name}"] = value
        
        # Process children
        for child in element:
            child_data = self._extract_data(child, current_path, ns)
            data.update(child_data)
        
        return data
    
    def _build_target_structure(self, source_data: Dict[str, str], 
                                 target_ns: str, add_defaults: bool) -> Optional[ET.Element]:
        """Build target XML structure"""
        
        # Find root element in target schema
        target_paths = sorted(self.target_schema.get_all_paths(), key=len)
        if not target_paths:
            return None
        
        root_path = target_paths[0]
        root_name = self.target_schema.elements[root_path]['name']
        
        # Create root element - register namespace to avoid duplication
        if target_ns:
            ET.register_namespace('', target_ns)
            root = ET.Element(f'{{{target_ns}}}{root_name}')
        else:
            root = ET.Element(root_name)
        
        # Build element tree
        created_elements = {root_path: root}
        
        for target_path in sorted(target_paths, key=len):
            if target_path == root_path:
                continue
            
            # Find parent
            parent_path = '/'.join(target_path.split('/')[:-1])
            parent_elem = created_elements.get(parent_path)
            
            if parent_elem is None:
                continue
            
            elem_name = self.target_schema.elements[target_path]['name']
            
            # Check if we have data for this element
            value = None
            source_path = None
            
            # Look for mapped source path
            for sp, tp in self.field_mappings.items():
                if tp == target_path and sp in source_data:
                    value = source_data[sp]
                    source_path = sp
                    break
            
            # Direct path match
            if value is None and target_path in source_data:
                value = source_data[target_path]
                source_path = target_path
            
            # Check if element is mandatory or has data
            is_mandatory = self.target_schema.elements[target_path]['min_occurs'] != '0'
            
            if value is not None or is_mandatory:
                # Create element
                if target_ns:
                    elem = ET.SubElement(parent_elem, f'{{{target_ns}}}{elem_name}')
                else:
                    elem = ET.SubElement(parent_elem, elem_name)
                
                created_elements[target_path] = elem
                
                if value is not None:
                    elem.text = value
                    self.actions.append(TransformAction(
                        action='mapped',
                        source_path=source_path,
                        target_path=target_path,
                        source_value=value,
                        target_value=value
                    ))
                elif is_mandatory and add_defaults:
                    # Add default value for mandatory fields
                    default_value = self._get_default_value(elem_name)
                    if default_value and not list(elem):  # Only if no children
                        elem.text = default_value
                        self.actions.append(TransformAction(
                            action='default',
                            source_path=None,
                            target_path=target_path,
                            source_value=None,
                            target_value=default_value,
                            notes='Default value added for mandatory field'
                        ))
        
        # Track unmapped source fields
        for source_path, value in source_data.items():
            if '@' in source_path:  # Skip attributes for now
                continue
            mapped = any(sp == source_path for sp in self.field_mappings.keys())
            if not mapped and source_path not in self.target_schema.elements:
                self.actions.append(TransformAction(
                    action='removed',
                    source_path=source_path,
                    target_path='',
                    source_value=value,
                    target_value=None,
                    notes='No matching field in target schema'
                ))
        
        return root
    
    def _get_default_value(self, elem_name: str) -> Optional[str]:
        """Get default value for element"""
        defaults = {
            'MsgId': f'MSG{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'CreDtTm': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'NbOfTxs': '1',
            'IntrBkSttlmDt': datetime.now().strftime('%Y-%m-%d'),
            'ChrgBr': 'SLEV',
            'Ccy': 'EUR',
            'Ctry': 'DE',
        }
        return defaults.get(elem_name)
    
    def _validate_output(self, xml_file: str) -> List[str]:
        """Validate output against target schema"""
        errors = []
        try:
            with open(self.target_xsd, 'rb') as f:
                schema_doc = lxml_etree.parse(f)
            schema = lxml_etree.XMLSchema(schema_doc)
            
            with open(xml_file, 'rb') as f:
                xml_doc = lxml_etree.parse(f)
            
            if not schema.validate(xml_doc):
                for error in schema.error_log:
                    errors.append(f"Line {error.line}: {error.message[:100]}")
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
        
        return errors[:20]  # Limit errors
    
    def generate_html_report(self, result: Dict, output_path: str):
        """Generate HTML transformation report"""
        
        summary = result.get('summary', {})
        actions = result.get('actions', [])
        validation_errors = result.get('validation_errors', [])
        
        # Group actions by type
        mapped_actions = [a for a in actions if a['action'] == 'mapped']
        default_actions = [a for a in actions if a['action'] == 'default']
        removed_actions = [a for a in actions if a['action'] == 'removed']
        
        # Generate action tables
        def action_rows(action_list, show_source=True, show_target=True):
            rows = ""
            for a in action_list[:50]:
                rows += f"""
                <tr>
                    {'<td class="path">' + (a.get('source_path') or '-') + '</td>' if show_source else ''}
                    {'<td class="path">' + (a.get('target_path') or '-') + '</td>' if show_target else ''}
                    <td><code>{a.get('source_value') or a.get('target_value') or '-'}</code></td>
                    <td>{a.get('notes') or ''}</td>
                </tr>
                """
            if len(action_list) > 50:
                rows += f'<tr><td colspan="4">... and {len(action_list) - 50} more</td></tr>'
            return rows
        
        validation_html = ""
        if validation_errors:
            validation_html = f"""
            <div class="section errors">
                <h2>⚠️ Validation Warnings</h2>
                <ul>
                    {''.join(f'<li>{e}</li>' for e in validation_errors)}
                </ul>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>XML Transformation Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .meta {{ color: #94a3b8; font-size: 14px; }}
        
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat {{ background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stat .number {{ font-size: 36px; font-weight: bold; }}
        .stat .label {{ color: #666; font-size: 12px; text-transform: uppercase; }}
        .stat.mapped .number {{ color: #10b981; }}
        .stat.defaults .number {{ color: #3b82f6; }}
        .stat.removed .number {{ color: #f59e0b; }}
        
        .section {{ background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .section h2 {{ margin-top: 0; color: #1a1a2e; }}
        .section.errors {{ border-left: 4px solid #ef4444; }}
        .section.errors ul {{ color: #dc2626; }}
        
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th {{ background: #1a1a2e; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px 10px; border-bottom: 1px solid #e5e7eb; }}
        tr:hover {{ background: #f8f9fa; }}
        .path {{ font-family: monospace; font-size: 11px; max-width: 400px; word-break: break-all; }}
        code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 4px; }}
        
        .arrow {{ text-align: center; font-size: 24px; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔁 XML Transformation Report</h1>
            <div class="meta">
                <div>📄 Source: {result.get('source_file', 'N/A')}</div>
                <div>📄 Target: {result.get('target_file', 'N/A')}</div>
                <div>📋 Source Schema: {result.get('source_schema', 'N/A')}</div>
                <div>📋 Target Schema: {result.get('target_schema', 'N/A')}</div>
                <div>🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
        </div>
        
        <div class="summary">
            <div class="stat">
                <div class="number">{summary.get('total_actions', 0)}</div>
                <div class="label">Total Actions</div>
            </div>
            <div class="stat mapped">
                <div class="number">{summary.get('mapped', 0)}</div>
                <div class="label">Fields Mapped</div>
            </div>
            <div class="stat defaults">
                <div class="number">{summary.get('added_defaults', 0)}</div>
                <div class="label">Defaults Added</div>
            </div>
            <div class="stat removed">
                <div class="number">{summary.get('not_mapped', 0)}</div>
                <div class="label">Not Mapped</div>
            </div>
        </div>
        
        {validation_html}
        
        <div class="section">
            <h2>✅ Mapped Fields ({len(mapped_actions)})</h2>
            <table>
                <thead>
                    <tr>
                        <th>Source Path</th>
                        <th>Target Path</th>
                        <th>Value</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {action_rows(mapped_actions)}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>🔷 Default Values Added ({len(default_actions)})</h2>
            <table>
                <thead>
                    <tr>
                        <th>Target Path</th>
                        <th>Default Value</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {action_rows(default_actions, show_source=False)}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>⚠️ Unmapped Source Fields ({len(removed_actions)})</h2>
            <table>
                <thead>
                    <tr>
                        <th>Source Path</th>
                        <th>Value</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {action_rows(removed_actions, show_target=False)}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)


def main():
    parser = argparse.ArgumentParser(
        description='ISO 20022 XML Transformer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transform XML from v2 to v8
  python xml_transformer.py source.xml source_v2.xsd target_v8.xsd -o output.xml
  
  # Transform with HTML report
  python xml_transformer.py input.xml old.xsd new.xsd -o output.xml --report report.html
  
  # Transform without adding defaults
  python xml_transformer.py input.xml old.xsd new.xsd -o output.xml --no-defaults
        """
    )
    
    parser.add_argument('source_xml', help='Source XML file to transform')
    parser.add_argument('source_xsd', help='Source XSD schema')
    parser.add_argument('target_xsd', help='Target XSD schema')
    parser.add_argument('-o', '--output', required=True, help='Output XML file')
    parser.add_argument('--report', help='Generate HTML report')
    parser.add_argument('--no-defaults', action='store_true', 
                        help='Do not add default values for mandatory fields')
    parser.add_argument('--json', action='store_true', help='Output result as JSON')
    
    args = parser.parse_args()
    
    # Validate inputs
    for f, label in [(args.source_xml, 'Source XML'), 
                     (args.source_xsd, 'Source XSD'), 
                     (args.target_xsd, 'Target XSD')]:
        if not Path(f).exists():
            print(f"❌ Error: {label} not found: {f}")
            return
    
    print(f"\n{'='*70}")
    print("ISO 20022 XML TRANSFORMER")
    print(f"{'='*70}\n")
    print(f"📄 Source XML: {args.source_xml}")
    print(f"📋 Source XSD: {args.source_xsd}")
    print(f"📋 Target XSD: {args.target_xsd}")
    print(f"📄 Output:     {args.output}")
    
    print(f"\n⏳ Analyzing schemas...")
    transformer = XMLTransformer(args.source_xsd, args.target_xsd)
    
    print(f"   Found {len(transformer.field_mappings)} automatic field mappings")
    
    print(f"\n⏳ Transforming XML...")
    result = transformer.transform(
        args.source_xml, 
        args.output,
        add_defaults=not args.no_defaults
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result['success']:
            print(f"\n✅ Transformation complete!")
            print(f"\n📊 Summary:")
            print(f"   Fields Mapped:    {result['summary']['mapped']}")
            print(f"   Defaults Added:   {result['summary']['added_defaults']}")
            print(f"   Not Mapped:       {result['summary']['not_mapped']}")
            
            if result['validation_errors']:
                print(f"\n⚠️  Validation warnings: {len(result['validation_errors'])}")
                for err in result['validation_errors'][:5]:
                    print(f"   • {err[:80]}")
            
            print(f"\n📄 Output saved to: {args.output}")
        else:
            print(f"\n❌ Transformation failed: {result.get('error')}")
    
    # Generate HTML report
    if args.report and result['success']:
        transformer.generate_html_report(result, args.report)
        print(f"📊 Report saved to: {args.report}")
    
    print(f"\n{'='*70}")
    print("COMPLETE")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
