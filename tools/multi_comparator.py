#!/usr/bin/env python3
"""
Multi-Schema Comparison Tool
- Compare 2+ schemas simultaneously  
- Excel + Word + HTML reports for each pairwise comparison
- Master comparison matrix
- Stakeholder-specific reports (Management, Business, Developer, QA)
"""

import sys
import os
from pathlib import Path

# Add tools directory to path to import other modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from schema_comparator import XSDComparator, ComparisonReportGenerator, WordDocumentGenerator
    from html_report_generator import InteractiveHTMLGenerator
except ImportError as e:
    print(f"⚠️  Warning: Could not import comparison modules: {e}")
    print("   Some features may be limited.")

import xml.etree.ElementTree as ET
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import argparse
from datetime import datetime
from collections import defaultdict


class MultiSchemaComparator:
    """Compare multiple XSD schemas (2+)"""
    
    def __init__(self, schema_files, schema_names=None):
        self.schema_files = schema_files
        self.schema_names = schema_names or [Path(f).stem for f in schema_files]
        self.schemas = []
        self.all_fields = set()
        self.comparison_matrix = {}
        self.pairwise_comparisons = []
        
    def parse_all(self):
        """Parse all schemas"""
        print(f"\n⏳ Parsing {len(self.schema_files)} schemas...")
        
        for i, (file, name) in enumerate(zip(self.schema_files, self.schema_names), 1):
            print(f"   {i}. {name}")
            try:
                # Use XSDComparator to parse
                comp = XSDComparator(file, file, name, name)
                schema_data = comp.schema1
                self.schemas.append({
                    'name': name,
                    'file': file,
                    'elements': schema_data['elements'],
                    'metadata': schema_data
                })
                self.all_fields.update(schema_data['elements'].keys())
            except Exception as e:
                print(f"   ⚠️  Error parsing {name}: {e}")
        
        print(f"   ✅ Found {len(self.all_fields)} unique fields across all schemas")
    
    def build_comparison_matrix(self):
        """Build field-by-field comparison matrix"""
        print("\n⏳ Building comparison matrix...")
        
        for field_path in sorted(self.all_fields):
            self.comparison_matrix[field_path] = {}
            
            for schema in self.schemas:
                elem = schema['elements'].get(field_path)
                if elem:
                    self.comparison_matrix[field_path][schema['name']] = {
                        'present': True,
                        'type': elem.get('type', ''),
                        'min_occurs': elem.get('min_occurs', ''),
                        'max_occurs': elem.get('max_occurs', ''),
                        'restrictions': elem.get('restrictions', '')
                    }
                else:
                    self.comparison_matrix[field_path][schema['name']] = {
                        'present': False
                    }
        
        print(f"   ✅ Matrix built: {len(self.comparison_matrix)} fields")
    
    def perform_pairwise_comparisons(self):
        """Perform pairwise comparisons between consecutive schemas"""
        print("\n⏳ Performing pairwise comparisons...")
        
        for i in range(len(self.schema_files) - 1):
            schema1_file = self.schema_files[i]
            schema2_file = self.schema_files[i + 1]
            schema1_name = self.schema_names[i]
            schema2_name = self.schema_names[i + 1]
            
            print(f"   Comparing {schema1_name} → {schema2_name}")
            
            try:
                comparator = XSDComparator(schema1_file, schema2_file, schema1_name, schema2_name)
                differences = comparator.compare()
                
                self.pairwise_comparisons.append({
                    'schema1': schema1_name,
                    'schema2': schema2_name,
                    'comparator': comparator,
                    'differences': differences
                })
                
                print(f"      ✅ {len(differences)} differences found")
            except Exception as e:
                print(f"      ⚠️  Error: {e}")
        
        print(f"   ✅ Completed {len(self.pairwise_comparisons)} pairwise comparisons")


class EnhancedReportGenerator:
    """Generate comprehensive reports for multi-schema comparison"""
    
    def __init__(self, multi_comparator, output_base):
        self.multi_comparator = multi_comparator
        self.output_base = output_base
        self.generated_files = []
        
    def generate_all_reports(self):
        """Generate all reports"""
        print("\n⏳ Generating comprehensive reports...")
        
        # 1. Generate pairwise comparison reports (Excel + Word + HTML)
        for i, comparison in enumerate(self.multi_comparator.pairwise_comparisons):
            # Sanitize names for filenames
            name1 = self._sanitize_filename(comparison['schema1'])
            name2 = self._sanitize_filename(comparison['schema2'])
            output_file = f"{self.output_base}_{name1}_vs_{name2}.xlsx"
            self._generate_pairwise_report(comparison, output_file)
        
        # 2. Generate master matrix (Excel)
        self._generate_master_matrix()
        
        # 3. Generate stakeholder reports (Word)
        self._generate_stakeholder_reports()
        
        print("\n✅ All reports generated!")
        return self.generated_files
    
    def _sanitize_filename(self, name):
        """Sanitize string for use in filename"""
        # Replace spaces and special chars with underscores
        import re
        return re.sub(r'[^\w\-]', '_', name)
    
    def _generate_pairwise_report(self, comparison, output_file):
        """Generate full comparison report (Excel + Word + HTML)"""
        comparator = comparison['comparator']
        
        try:
            # Excel report
            excel_gen = ComparisonReportGenerator(comparator, output_file)
            excel_gen.generate()
            self.generated_files.append(output_file)
            
            # Word document
            word_file = output_file.replace('.xlsx', '.docx')
            word_gen = WordDocumentGenerator(comparator, word_file)
            word_gen.generate()
            self.generated_files.append(word_file)
            
            # HTML report
            html_file = output_file.replace('.xlsx', '.html')
            try:
                html_gen = InteractiveHTMLGenerator(comparator, html_file)
                html_gen.generate()
                self.generated_files.append(html_file)
            except Exception as e:
                print(f"   ⚠️  HTML generation skipped: {e}")
            
        except Exception as e:
            print(f"   ⚠️  Error generating report: {e}")
    
    def _generate_master_matrix(self):
        """Generate master comparison matrix"""
        filename = f"{self.output_base}_MASTER_MATRIX.xlsx"
        wb = Workbook()
        
        # Matrix sheet
        ws = wb.active
        ws.title = "Comparison Matrix"
        
        # Headers
        headers = ['Field Path', 'Element'] + [s['name'] for s in self.multi_comparator.schemas] + ['Status']
        ws.append(headers)
        
        # Style headers
        for cell in ws[1]:
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
            cell.alignment = Alignment(horizontal='center', wrap_text=True)
        
        # Data
        for field_path, schema_data in self.multi_comparator.comparison_matrix.items():
            element_name = field_path.split('/')[-1]
            row = [field_path, element_name]
            
            present_count = 0
            for schema in self.multi_comparator.schemas:
                schema_name = schema['name']
                if schema_data[schema_name]['present']:
                    cell_value = f"✓ {schema_data[schema_name].get('type', '')[:25]}"
                    present_count += 1
                else:
                    cell_value = "✗ Missing"
                row.append(cell_value)
            
            # Status column
            total_schemas = len(self.multi_comparator.schemas)
            if present_count == total_schemas:
                status = "✅ All"
            elif present_count == 0:
                status = "❌ None"
            else:
                status = f"⚠️ {present_count}/{total_schemas}"
            row.append(status)
            
            ws.append(row)
            
            # Highlight rows with differences
            if present_count < total_schemas and present_count > 0:
                for cell in ws[ws.max_row]:
                    cell.fill = PatternFill(start_color='FFF3CD', end_color='FFF3CD', fill_type='solid')
        
        # Column widths
        ws.column_dimensions['A'].width = 50
        ws.column_dimensions['B'].width = 25
        for col_idx in range(3, len(headers) + 1):
            ws.column_dimensions[get_column_letter(col_idx)].width = 30
        
        ws.freeze_panes = 'C2'
        ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{ws.max_row}"
        
        # Summary sheet
        ws_summary = wb.create_sheet("Summary")
        ws_summary.append(['Metric', 'Value'])
        ws_summary.append(['Total Unique Fields', len(self.multi_comparator.comparison_matrix)])
        ws_summary.append(['Schemas Compared', len(self.multi_comparator.schemas)])
        ws_summary.append(['Pairwise Comparisons', len(self.multi_comparator.pairwise_comparisons)])
        
        for cell in ws_summary[1]:
            cell.font = Font(bold=True)
        
        wb.save(filename)
        self.generated_files.append(filename)
        print(f"   ✅ Master matrix: {filename}")
    
    def _generate_stakeholder_reports(self):
        """Generate stakeholder-specific reports"""
        
        # Management Summary
        self._generate_management_summary()
        
        # Business Impact
        self._generate_business_impact()
        
        # Developer Guide  
        self._generate_developer_guide()
        
        # QA Checklist
        self._generate_qa_checklist()
    
    def _generate_management_summary(self):
        """Generate management summary"""
        filename = f"{self.output_base}_MANAGEMENT_SUMMARY.docx"
        doc = Document()
        
        # Title
        title = doc.add_heading('Multi-Schema Comparison Report', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(f"Executive Summary")
        doc.add_paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        doc.add_paragraph()
        
        # Schemas compared
        doc.add_heading('Schemas Compared', 1)
        for i, schema in enumerate(self.multi_comparator.schemas, 1):
            doc.add_paragraph(f"{i}. {schema['name']}", style='List Number')
        
        # Key metrics
        doc.add_paragraph()
        doc.add_heading('Key Metrics', 1)
        doc.add_paragraph(f"• Total unique fields analyzed: {len(self.multi_comparator.all_fields)}")
        doc.add_paragraph(f"• Pairwise comparisons performed: {len(self.multi_comparator.pairwise_comparisons)}")
        
        # Comparison summary
        doc.add_paragraph()
        doc.add_heading('Comparison Summary', 1)
        
        total_differences = 0
        for comparison in self.multi_comparator.pairwise_comparisons:
            diff_count = len(comparison['differences'])
            total_differences += diff_count
            doc.add_paragraph(
                f"{comparison['schema1']} → {comparison['schema2']}: "
                f"{diff_count} differences",
                style='List Bullet'
            )
        
        doc.add_paragraph()
        doc.add_paragraph(f"Total differences across all comparisons: {total_differences}", 
                         style='Intense Quote')
        
        doc.save(filename)
        self.generated_files.append(filename)
        print(f"   ✅ Management summary: {filename}")
    
    def _generate_business_impact(self):
        """Generate business impact report"""
        filename = f"{self.output_base}_BUSINESS_IMPACT.docx"
        doc = Document()
        
        doc.add_heading('Business Impact Report', 0)
        doc.add_paragraph("Analysis of changes and their business implications")
        doc.add_paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        for comparison in self.multi_comparator.pairwise_comparisons:
            doc.add_page_break()
            doc.add_heading(f"{comparison['schema1']} → {comparison['schema2']}", 1)
            
            differences = comparison['differences']
            
            # Categorize by severity
            high_severity = [d for d in differences if d.get('severity') == 'HIGH']
            medium_severity = [d for d in differences if d.get('severity') == 'MEDIUM']
            low_severity = [d for d in differences if d.get('severity') == 'LOW']
            
            doc.add_paragraph(f"Total changes: {len(differences)}")
            
            if high_severity:
                doc.add_heading('High Priority Changes', 2)
                doc.add_paragraph(f"Found {len(high_severity)} critical changes requiring immediate attention:")
                for diff in high_severity[:20]:  # Limit to 20
                    doc.add_paragraph(f"• {diff['path']}: {diff['type']}", style='List Bullet')
                if len(high_severity) > 20:
                    doc.add_paragraph(f"... and {len(high_severity) - 20} more")
            
            if medium_severity:
                doc.add_heading('Medium Priority Changes', 2)
                doc.add_paragraph(f"Found {len(medium_severity)} changes requiring review:")
                for diff in medium_severity[:15]:
                    doc.add_paragraph(f"• {diff['path']}: {diff['type']}", style='List Bullet')
                if len(medium_severity) > 15:
                    doc.add_paragraph(f"... and {len(medium_severity) - 15} more")
            
            if not high_severity and not medium_severity:
                doc.add_paragraph("No high or medium priority changes found.")
        
        doc.save(filename)
        self.generated_files.append(filename)
        print(f"   ✅ Business impact: {filename}")
    
    def _generate_developer_guide(self):
        """Generate developer guide"""
        filename = f"{self.output_base}_DEVELOPER_GUIDE.docx"
        doc = Document()
        
        doc.add_heading('Developer Migration Guide', 0)
        doc.add_paragraph("Technical implementation details for schema transitions")
        doc.add_paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        for comparison in self.multi_comparator.pairwise_comparisons:
            doc.add_page_break()
            doc.add_heading(f"Migrating: {comparison['schema1']} → {comparison['schema2']}", 1)
            
            differences = comparison['differences']
            removed = [d for d in differences if d['type'] == 'REMOVED']
            added = [d for d in differences if d['type'] == 'ADDED']
            modified = [d for d in differences if d['type'] not in ['REMOVED', 'ADDED']]
            
            if removed:
                doc.add_heading('Fields Removed (Action: Delete)', 2)
                for diff in removed[:30]:
                    doc.add_paragraph(f"• {diff['path']}", style='List Bullet')
                if len(removed) > 30:
                    doc.add_paragraph(f"... and {len(removed) - 30} more fields")
            
            if added:
                doc.add_heading('Fields Added (Action: Implement)', 2)
                for diff in added[:30]:
                    doc.add_paragraph(f"• {diff['path']}", style='List Bullet')
                if len(added) > 30:
                    doc.add_paragraph(f"... and {len(added) - 30} more fields")
            
            if modified:
                doc.add_heading('Fields Modified (Action: Update)', 2)
                for diff in modified[:30]:
                    doc.add_paragraph(f"• {diff['path']}: {diff['type']}", style='List Bullet')
                if len(modified) > 30:
                    doc.add_paragraph(f"... and {len(modified) - 30} more fields")
            
            if not differences:
                doc.add_paragraph("No differences found - schemas are identical.")
        
        doc.save(filename)
        self.generated_files.append(filename)
        print(f"   ✅ Developer guide: {filename}")
    
    def _generate_qa_checklist(self):
        """Generate QA checklist"""
        filename = f"{self.output_base}_QA_CHECKLIST.docx"
        doc = Document()
        
        doc.add_heading('QA Testing Checklist', 0)
        doc.add_paragraph("Comprehensive testing requirements for schema migrations")
        doc.add_paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        for comparison in self.multi_comparator.pairwise_comparisons:
            doc.add_page_break()
            doc.add_heading(f"Testing: {comparison['schema1']} → {comparison['schema2']}", 1)
            
            differences = comparison['differences']
            
            doc.add_heading('Pre-Migration Testing', 2)
            scenarios = [
                "☐ Backup existing production data",
                "☐ Document current system behavior",
                "☐ Identify all affected integrations",
            ]
            for scenario in scenarios:
                doc.add_paragraph(scenario, style='List Bullet')
            
            doc.add_heading('Schema Validation Testing', 2)
            scenarios = [
                "☐ Validate sample messages against new schema",
                f"☐ Test {len([d for d in differences if d['type'] == 'ADDED'])} new fields with valid data",
                f"☐ Verify {len([d for d in differences if d['type'] == 'REMOVED'])} removed fields cause validation errors",
                "☐ Test boundary conditions for modified fields",
            ]
            for scenario in scenarios:
                doc.add_paragraph(scenario, style='List Bullet')
            
            doc.add_heading('Integration Testing', 2)
            scenarios = [
                "☐ Test upstream system compatibility",
                "☐ Test downstream system compatibility",
                "☐ Verify error handling for rejected messages",
                "☐ End-to-end transaction testing",
            ]
            for scenario in scenarios:
                doc.add_paragraph(scenario, style='List Bullet')
            
            doc.add_heading('Post-Migration Verification', 2)
            scenarios = [
                "☐ Monitor error rates for 24-48 hours",
                "☐ Verify all business functions operational",
                "☐ Confirm reporting accuracy",
                "☐ Document any issues encountered",
            ]
            for scenario in scenarios:
                doc.add_paragraph(scenario, style='List Bullet')
        
        doc.save(filename)
        self.generated_files.append(filename)
        print(f"   ✅ QA checklist: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Multi-Schema Comparison Tool - Compare 2+ XSD schemas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare 2 schemas (full reports)
  python %(prog)s schema1.xsd schema2.xsd -o comparison
  
  # Compare 4 versions with custom names
  python %(prog)s v1.xsd v2.xsd v3.xsd v4.xsd -n "V1.0" "V2.0" "V3.0" "V4.0" -o evolution
  
  # Compare vendor schemas
  python %(prog)s vendor_a.xsd vendor_b.xsd vendor_c.xsd -o vendors
        """
    )
    
    parser.add_argument('schemas', nargs='+', help='XSD files to compare (2 or more)')
    parser.add_argument('-o', '--output', help='Output base name', default='comparison')
    parser.add_argument('-n', '--names', nargs='+', help='Names for schemas (optional)')
    
    args = parser.parse_args()
    
    if len(args.schemas) < 2:
        print("❌ Error: Need at least 2 schemas to compare")
        sys.exit(1)
    
    # Validate files exist
    for schema_file in args.schemas:
        if not Path(schema_file).exists():
            print(f"❌ Error: File not found: {schema_file}")
            sys.exit(1)
    
    print(f"\n{'='*70}")
    print("MULTI-SCHEMA COMPARISON TOOL")
    print(f"Comparing {len(args.schemas)} schemas")
    print("Generates: Excel + Word + HTML reports")
    print(f"{'='*70}")
    
    # Parse all schemas
    comparator = MultiSchemaComparator(args.schemas, args.names)
    comparator.parse_all()
    comparator.build_comparison_matrix()
    comparator.perform_pairwise_comparisons()
    
    # Generate reports
    reporter = EnhancedReportGenerator(comparator, args.output)
    generated_files = reporter.generate_all_reports()
    
    print(f"\n{'='*70}")
    print("✅ COMPLETE!")
    print(f"{'='*70}\n")
    
    # Summary
    print("Generated Reports:")
    print(f"\nPairwise Comparisons ({len(comparator.pairwise_comparisons)}):")
    for comp in comparator.pairwise_comparisons:
        print(f"  • {comp['schema1']} vs {comp['schema2']}: Excel + Word + HTML")
    
    print(f"\nMaster Reports:")
    print(f"  • {args.output}_MASTER_MATRIX.xlsx")
    print(f"  • {args.output}_MANAGEMENT_SUMMARY.docx")
    print(f"  • {args.output}_BUSINESS_IMPACT.docx")
    print(f"  • {args.output}_DEVELOPER_GUIDE.docx")
    print(f"  • {args.output}_QA_CHECKLIST.docx")
    
    print(f"\n📊 Total files generated: {len(generated_files)}")
    print()


if __name__ == '__main__':
    main()
