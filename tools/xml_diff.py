#!/usr/bin/env python3
"""
ISO 20022 XML Diff / Compare Tool
=================================
Compare two XML messages to find differences.

Features:
✅ Side-by-side comparison
✅ Highlight added/removed/changed elements
✅ Show value differences
✅ Ignore whitespace/formatting options
✅ XPath locations for each difference
✅ HTML and JSON output reports
"""

import xml.etree.ElementTree as ET
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import re


class DiffType(Enum):
    ADDED = "added"
    REMOVED = "removed"
    CHANGED = "changed"
    MOVED = "moved"


@dataclass
class Difference:
    diff_type: str
    path: str
    element: str
    left_value: Optional[str] = None
    right_value: Optional[str] = None
    left_line: Optional[int] = None
    right_line: Optional[int] = None
    details: Optional[str] = None


class XMLDiffTool:
    """Compare two XML files and identify differences"""
    
    def __init__(self, ignore_whitespace: bool = True, ignore_namespace: bool = True,
                 ignore_order: bool = False, ignore_attributes: bool = False):
        self.ignore_whitespace = ignore_whitespace
        self.ignore_namespace = ignore_namespace
        self.ignore_order = ignore_order
        self.ignore_attributes = ignore_attributes
        self.differences: List[Difference] = []
    
    def compare(self, xml_file1: str, xml_file2: str) -> Dict:
        """Compare two XML files and return differences"""
        self.differences = []
        
        # Parse both XML files
        try:
            tree1 = ET.parse(xml_file1)
            root1 = tree1.getroot()
        except ET.ParseError as e:
            return {
                'success': False,
                'error': f"Error parsing {xml_file1}: {str(e)}"
            }
        
        try:
            tree2 = ET.parse(xml_file2)
            root2 = tree2.getroot()
        except ET.ParseError as e:
            return {
                'success': False,
                'error': f"Error parsing {xml_file2}: {str(e)}"
            }
        
        # Compare recursively
        self._compare_elements(root1, root2, "")
        
        # Generate summary
        summary = {
            'total_differences': len(self.differences),
            'added': sum(1 for d in self.differences if d.diff_type == DiffType.ADDED.value),
            'removed': sum(1 for d in self.differences if d.diff_type == DiffType.REMOVED.value),
            'changed': sum(1 for d in self.differences if d.diff_type == DiffType.CHANGED.value),
        }
        
        return {
            'success': True,
            'identical': len(self.differences) == 0,
            'summary': summary,
            'differences': [asdict(d) for d in self.differences],
            'file1': xml_file1,
            'file2': xml_file2
        }
    
    def _normalize_tag(self, tag: str) -> str:
        """Remove namespace from tag if ignore_namespace is True"""
        if self.ignore_namespace and '}' in tag:
            return tag.split('}')[1]
        return tag
    
    def _normalize_text(self, text: Optional[str]) -> str:
        """Normalize text content"""
        if text is None:
            return ""
        if self.ignore_whitespace:
            return ' '.join(text.split())
        return text
    
    def _get_element_key(self, elem: ET.Element, index: int) -> str:
        """Generate a key for element comparison"""
        tag = self._normalize_tag(elem.tag)
        
        # Try to use identifying attributes or child elements
        # Common identifiers in ISO 20022
        identifiers = ['Id', 'MsgId', 'EndToEndId', 'TxId', 'InstrId', 'IBAN', 'BICFI']
        
        for id_elem in identifiers:
            id_child = None
            for child in elem:
                if self._normalize_tag(child.tag) == id_elem:
                    id_child = child
                    break
            if id_child is not None and id_child.text:
                return f"{tag}[{id_elem}={id_child.text}]"
        
        # Fall back to index
        return f"{tag}[{index}]"
    
    def _compare_elements(self, elem1: ET.Element, elem2: ET.Element, path: str):
        """Recursively compare two elements"""
        tag1 = self._normalize_tag(elem1.tag)
        tag2 = self._normalize_tag(elem2.tag)
        current_path = f"{path}/{tag1}" if path else tag1
        
        # Compare tags
        if tag1 != tag2:
            self.differences.append(Difference(
                diff_type=DiffType.CHANGED.value,
                path=current_path,
                element=tag1,
                left_value=tag1,
                right_value=tag2,
                details="Element tag changed"
            ))
            return
        
        # Compare attributes
        if not self.ignore_attributes:
            self._compare_attributes(elem1, elem2, current_path)
        
        # Compare text content
        text1 = self._normalize_text(elem1.text)
        text2 = self._normalize_text(elem2.text)
        
        if text1 != text2:
            self.differences.append(Difference(
                diff_type=DiffType.CHANGED.value,
                path=current_path,
                element=tag1,
                left_value=text1 if text1 else "(empty)",
                right_value=text2 if text2 else "(empty)",
                details="Text content changed"
            ))
        
        # Compare children
        children1 = list(elem1)
        children2 = list(elem2)
        
        if self.ignore_order:
            self._compare_children_unordered(children1, children2, current_path)
        else:
            self._compare_children_ordered(children1, children2, current_path)
    
    def _compare_attributes(self, elem1: ET.Element, elem2: ET.Element, path: str):
        """Compare element attributes"""
        attrs1 = set(elem1.attrib.keys())
        attrs2 = set(elem2.attrib.keys())
        
        # Removed attributes
        for attr in attrs1 - attrs2:
            self.differences.append(Difference(
                diff_type=DiffType.REMOVED.value,
                path=f"{path}/@{attr}",
                element=attr,
                left_value=elem1.attrib[attr],
                right_value=None,
                details="Attribute removed"
            ))
        
        # Added attributes
        for attr in attrs2 - attrs1:
            self.differences.append(Difference(
                diff_type=DiffType.ADDED.value,
                path=f"{path}/@{attr}",
                element=attr,
                left_value=None,
                right_value=elem2.attrib[attr],
                details="Attribute added"
            ))
        
        # Changed attributes
        for attr in attrs1 & attrs2:
            if elem1.attrib[attr] != elem2.attrib[attr]:
                self.differences.append(Difference(
                    diff_type=DiffType.CHANGED.value,
                    path=f"{path}/@{attr}",
                    element=attr,
                    left_value=elem1.attrib[attr],
                    right_value=elem2.attrib[attr],
                    details="Attribute value changed"
                ))
    
    def _compare_children_ordered(self, children1: List[ET.Element], 
                                   children2: List[ET.Element], path: str):
        """Compare children maintaining order"""
        max_len = max(len(children1), len(children2))
        
        for i in range(max_len):
            if i >= len(children1):
                # Element added in file2
                child2 = children2[i]
                tag2 = self._normalize_tag(child2.tag)
                self.differences.append(Difference(
                    diff_type=DiffType.ADDED.value,
                    path=f"{path}/{tag2}[{i+1}]",
                    element=tag2,
                    left_value=None,
                    right_value=self._element_summary(child2),
                    details="Element added"
                ))
            elif i >= len(children2):
                # Element removed from file2
                child1 = children1[i]
                tag1 = self._normalize_tag(child1.tag)
                self.differences.append(Difference(
                    diff_type=DiffType.REMOVED.value,
                    path=f"{path}/{tag1}[{i+1}]",
                    element=tag1,
                    left_value=self._element_summary(child1),
                    right_value=None,
                    details="Element removed"
                ))
            else:
                # Compare elements at same position
                self._compare_elements(children1[i], children2[i], path)
    
    def _compare_children_unordered(self, children1: List[ET.Element], 
                                     children2: List[ET.Element], path: str):
        """Compare children ignoring order"""
        # Build maps by element key
        map1 = {}
        map2 = {}
        
        for i, child in enumerate(children1):
            key = self._get_element_key(child, i)
            map1[key] = child
        
        for i, child in enumerate(children2):
            key = self._get_element_key(child, i)
            map2[key] = child
        
        keys1 = set(map1.keys())
        keys2 = set(map2.keys())
        
        # Removed elements
        for key in keys1 - keys2:
            child = map1[key]
            tag = self._normalize_tag(child.tag)
            self.differences.append(Difference(
                diff_type=DiffType.REMOVED.value,
                path=f"{path}/{key}",
                element=tag,
                left_value=self._element_summary(child),
                right_value=None,
                details="Element removed"
            ))
        
        # Added elements
        for key in keys2 - keys1:
            child = map2[key]
            tag = self._normalize_tag(child.tag)
            self.differences.append(Difference(
                diff_type=DiffType.ADDED.value,
                path=f"{path}/{key}",
                element=tag,
                left_value=None,
                right_value=self._element_summary(child),
                details="Element added"
            ))
        
        # Compare matching elements
        for key in keys1 & keys2:
            self._compare_elements(map1[key], map2[key], path)
    
    def _element_summary(self, elem: ET.Element, max_len: int = 100) -> str:
        """Generate a summary of an element's content"""
        tag = self._normalize_tag(elem.tag)
        text = self._normalize_text(elem.text)
        
        if text:
            summary = f"<{tag}>{text[:50]}{'...' if len(text) > 50 else ''}</{tag}>"
        elif len(list(elem)) > 0:
            child_tags = [self._normalize_tag(c.tag) for c in elem][:3]
            summary = f"<{tag}>[{', '.join(child_tags)}{'...' if len(list(elem)) > 3 else ''}]</{tag}>"
        else:
            summary = f"<{tag}/>"
        
        return summary[:max_len]


def generate_html_report(result: Dict, output_path: str, file1_name: str, file2_name: str):
    """Generate HTML diff report"""
    
    if not result['success']:
        html = f"<html><body><h1>Error</h1><p>{result['error']}</p></body></html>"
        with open(output_path, 'w') as f:
            f.write(html)
        return
    
    status = "✅ IDENTICAL" if result['identical'] else f"❌ {result['summary']['total_differences']} DIFFERENCES"
    status_class = "identical" if result['identical'] else "different"
    
    # Generate differences HTML
    diff_html = ""
    for i, diff in enumerate(result['differences'], 1):
        diff_type = diff['diff_type']
        type_class = diff_type
        type_icon = "➕" if diff_type == "added" else "➖" if diff_type == "removed" else "✏️"
        
        diff_html += f"""
        <div class="diff-item {type_class}">
            <div class="diff-header">
                <span class="diff-type">{type_icon} {diff_type.upper()}</span>
                <span class="diff-path">{diff['path']}</span>
            </div>
            <div class="diff-element"><strong>Element:</strong> {diff['element']}</div>
            {f"<div class='diff-details'><strong>Details:</strong> {diff['details']}</div>" if diff.get('details') else ""}
            <div class="diff-values">
                <div class="left-value">
                    <strong>{file1_name}:</strong>
                    <code>{diff['left_value'] or '(not present)'}</code>
                </div>
                <div class="right-value">
                    <strong>{file2_name}:</strong>
                    <code>{diff['right_value'] or '(not present)'}</code>
                </div>
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>XML Diff Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .file-info {{ color: #94a3b8; font-size: 14px; margin-bottom: 15px; }}
        .status {{ font-size: 24px; padding: 10px 20px; border-radius: 8px; display: inline-block; }}
        .status.identical {{ background: #10b981; }}
        .status.different {{ background: #ef4444; }}
        
        .summary {{ background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .summary h2 {{ margin-top: 0; color: #1a1a2e; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; }}
        .stat {{ background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }}
        .stat .number {{ font-size: 28px; font-weight: bold; }}
        .stat.added .number {{ color: #10b981; }}
        .stat.removed .number {{ color: #ef4444; }}
        .stat.changed .number {{ color: #f59e0b; }}
        .stat .label {{ color: #666; font-size: 12px; text-transform: uppercase; }}
        
        .differences {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .differences h2 {{ margin-top: 0; color: #1a1a2e; }}
        
        .diff-item {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; margin-bottom: 15px; }}
        .diff-item.added {{ border-left: 4px solid #10b981; background: #ecfdf5; }}
        .diff-item.removed {{ border-left: 4px solid #ef4444; background: #fef2f2; }}
        .diff-item.changed {{ border-left: 4px solid #f59e0b; background: #fffbeb; }}
        
        .diff-header {{ display: flex; justify-content: space-between; margin-bottom: 10px; flex-wrap: wrap; gap: 10px; }}
        .diff-type {{ font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
        .diff-item.added .diff-type {{ background: #10b981; color: white; }}
        .diff-item.removed .diff-type {{ background: #ef4444; color: white; }}
        .diff-item.changed .diff-type {{ background: #f59e0b; color: white; }}
        .diff-path {{ font-family: monospace; font-size: 13px; color: #6b7280; word-break: break-all; }}
        
        .diff-values {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px; }}
        .left-value, .right-value {{ padding: 10px; border-radius: 4px; }}
        .left-value {{ background: #fee2e2; }}
        .right-value {{ background: #dcfce7; }}
        code {{ font-family: monospace; font-size: 12px; word-break: break-all; display: block; margin-top: 5px; }}
        
        .diff-details {{ color: #6b7280; font-size: 13px; margin: 5px 0; }}
        
        @media (max-width: 768px) {{
            .diff-values {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 XML Diff Report</h1>
            <div class="file-info">
                <div>📄 Left: {file1_name}</div>
                <div>📄 Right: {file2_name}</div>
                <div>🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
            <div class="status {status_class}">{status}</div>
        </div>
        
        <div class="summary">
            <h2>📊 Summary</h2>
            <div class="stats">
                <div class="stat">
                    <div class="number">{result['summary']['total_differences']}</div>
                    <div class="label">Total</div>
                </div>
                <div class="stat added">
                    <div class="number">{result['summary']['added']}</div>
                    <div class="label">Added</div>
                </div>
                <div class="stat removed">
                    <div class="number">{result['summary']['removed']}</div>
                    <div class="label">Removed</div>
                </div>
                <div class="stat changed">
                    <div class="number">{result['summary']['changed']}</div>
                    <div class="label">Changed</div>
                </div>
            </div>
        </div>
        
        <div class="differences">
            <h2>📋 Differences Detail</h2>
            {diff_html if diff_html else "<p>✅ No differences found - files are identical!</p>"}
        </div>
    </div>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(
        description='ISO 20022 XML Diff Tool - Compare two XML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic comparison
  python xml_diff.py file1.xml file2.xml
  
  # Ignore element order
  python xml_diff.py file1.xml file2.xml --ignore-order
  
  # Include attribute comparison
  python xml_diff.py file1.xml file2.xml --compare-attributes
  
  # Output JSON
  python xml_diff.py file1.xml file2.xml --json
  
  # Save HTML report
  python xml_diff.py file1.xml file2.xml -o diff_report.html
        """
    )
    
    parser.add_argument('file1', help='First XML file (left/original)')
    parser.add_argument('file2', help='Second XML file (right/modified)')
    parser.add_argument('--ignore-order', action='store_true', 
                        help='Ignore element order when comparing')
    parser.add_argument('--compare-attributes', action='store_true',
                        help='Include attribute comparison (default: ignore)')
    parser.add_argument('--keep-namespace', action='store_true',
                        help='Keep namespace in comparison (default: ignore)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('-o', '--output', help='Save report to file (HTML or JSON based on extension)')
    
    args = parser.parse_args()
    
    # Validate files exist
    if not Path(args.file1).exists():
        print(f"❌ Error: File not found: {args.file1}")
        return
    if not Path(args.file2).exists():
        print(f"❌ Error: File not found: {args.file2}")
        return
    
    print(f"\n{'='*70}")
    print("ISO 20022 XML DIFF TOOL")
    print(f"{'='*70}\n")
    print(f"📄 Left:  {args.file1}")
    print(f"📄 Right: {args.file2}")
    print(f"\n⏳ Comparing...")
    
    # Create diff tool with options
    diff_tool = XMLDiffTool(
        ignore_whitespace=True,
        ignore_namespace=not args.keep_namespace,
        ignore_order=args.ignore_order,
        ignore_attributes=not args.compare_attributes
    )
    
    # Run comparison
    result = diff_tool.compare(args.file1, args.file2)
    
    # Handle output
    if args.output:
        if args.output.endswith('.json'):
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n📁 JSON report saved to: {args.output}")
        else:
            generate_html_report(result, args.output, 
                               Path(args.file1).name, Path(args.file2).name)
            print(f"\n📁 HTML report saved to: {args.output}")
    elif args.json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print results
        print(f"\n{'='*70}")
        print("COMPARISON RESULTS")
        print(f"{'='*70}")
        
        if not result['success']:
            print(f"\n❌ Error: {result['error']}")
            return
        
        if result['identical']:
            print("\n✅ Files are IDENTICAL")
        else:
            print(f"\n❌ Files are DIFFERENT")
            print(f"\n📊 Summary:")
            print(f"   Total Differences: {result['summary']['total_differences']}")
            print(f"   Added:    {result['summary']['added']}")
            print(f"   Removed:  {result['summary']['removed']}")
            print(f"   Changed:  {result['summary']['changed']}")
            
            print(f"\n📋 Differences:")
            for i, diff in enumerate(result['differences'][:20], 1):
                icon = "➕" if diff['diff_type'] == "added" else "➖" if diff['diff_type'] == "removed" else "✏️"
                print(f"\n   {icon} #{i} [{diff['diff_type'].upper()}] {diff['path']}")
                print(f"      Element: {diff['element']}")
                if diff['left_value']:
                    print(f"      Left:  {diff['left_value'][:80]}")
                if diff['right_value']:
                    print(f"      Right: {diff['right_value'][:80]}")
            
            if len(result['differences']) > 20:
                print(f"\n   ... and {len(result['differences']) - 20} more differences")
    
    print(f"\n{'='*70}")
    print("COMPLETE")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
