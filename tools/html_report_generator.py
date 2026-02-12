#!/usr/bin/env python3
"""
Interactive HTML Report Generator
Generates beautiful, interactive comparison reports that work in any browser
"""

from jinja2 import Template
import json
from datetime import datetime
from pathlib import Path


class InteractiveHTMLGenerator:
    """Generate interactive HTML reports"""
    
    HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XSD Comparison Report - {{ title }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f5f7fa;
            color: #2c3e50;
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .header .subtitle {
            opacity: 0.9;
            font-size: 0.9rem;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }
        
        .card-title {
            font-size: 0.85rem;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        
        .card-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .card.critical { border-left: 4px solid #e74c3c; }
        .card.warning { border-left: 4px solid #f39c12; }
        .card.success { border-left: 4px solid #27ae60; }
        .card.info { border-left: 4px solid #3498db; }
        
        .controls {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .search-box {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.2s;
        }
        
        .search-box:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .filter-buttons {
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 0.5rem 1rem;
            border: 2px solid #e1e8ed;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .filter-btn:hover {
            background: #f8f9fa;
            border-color: #667eea;
            transform: translateY(-1px);
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .filter-separator {
            width: 100%;
            height: 1px;
            background: linear-gradient(to right, transparent, #e1e8ed, transparent);
            margin: 15px 0;
        }
        
        .filter-group-title {
            width: 100%;
            font-size: 0.75rem;
            font-weight: 600;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        
        .differences-table {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        thead {
            background: #f8f9fa;
        }
        
        th {
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: #2c3e50;
            font-size: 0.9rem;
            border-bottom: 2px solid #e1e8ed;
        }
        
        td {
            padding: 1rem;
            border-bottom: 1px solid #f1f3f5;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .severity-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .severity-high {
            background: #fee;
            color: #c0392b;
        }
        
        .severity-medium {
            background: #fef5e7;
            color: #d68910;
        }
        
        .severity-low {
            background: #eafaf1;
            color: #1e8449;
        }
        
        .change-type {
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            background: #f1f3f5;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
        }
        
        .expandable {
            cursor: pointer;
            user-select: none;
        }
        
        .expandable:before {
            content: '▶ ';
            display: inline-block;
            transition: transform 0.2s;
        }
        
        .expandable.expanded:before {
            transform: rotate(90deg);
        }
        
        .details {
            display: none;
            background: #f8f9fa;
            padding: 1rem;
            margin-top: 0.5rem;
            border-radius: 8px;
            font-size: 0.9rem;
        }
        
        .details.show {
            display: block;
        }
        
        .xml-example {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            margin: 0.5rem 0;
        }
        
        .xml-before {
            border-left: 4px solid #e74c3c;
        }
        
        .xml-after {
            border-left: 4px solid #27ae60;
        }
        
        .stats-chart {
            height: 200px;
            margin-top: 1rem;
        }
        
        .no-results {
            text-align: center;
            padding: 3rem;
            color: #7f8c8d;
        }
        
        @media (max-width: 768px) {
            .container { padding: 1rem; }
            .dashboard { grid-template-columns: 1fr; }
            table { font-size: 0.85rem; }
            td, th { padding: 0.5rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 ISO 20022 Payment Schema Comparison</h1>
        <div class="subtitle">{{ subtitle }}</div>
    </div>
    
    <div class="container">
        <!-- Dashboard Cards -->
        <div class="dashboard">
            <div class="card info">
                <div class="card-title">Total Differences</div>
                <div class="card-value">{{ stats.total }}</div>
            </div>
            <div class="card critical">
                <div class="card-title">High Severity</div>
                <div class="card-value">{{ stats.high }}</div>
            </div>
            <div class="card warning">
                <div class="card-title">Medium Severity</div>
                <div class="card-value">{{ stats.medium }}</div>
            </div>
            <div class="card success">
                <div class="card-title">Low Severity</div>
                <div class="card-value">{{ stats.low }}</div>
            </div>
        </div>
        
        <!-- Search and Filters -->
        <div class="controls">
            <input type="text" 
                   class="search-box" 
                   id="searchBox" 
                   placeholder="🔍 Search by field path, element name, or change type...">
            
            <div class="filter-buttons">
                <!-- Quick Filters -->
                <button class="filter-btn active" data-filter="all">📋 All ({{ stats.total }})</button>
                
                <!-- Severity Group -->
                <div class="filter-group-title">By Severity</div>
                <button class="filter-btn" data-filter="HIGH" title="High Severity Changes">🔴 High ({{ stats.high }})</button>
                <button class="filter-btn" data-filter="MEDIUM" title="Medium Severity Changes">🟡 Medium ({{ stats.medium }})</button>
                <button class="filter-btn" data-filter="LOW" title="Low Severity Changes">🟢 Low ({{ stats.low }})</button>
                
                <!-- Change Type Group -->
                <div class="filter-group-title">By Change Type</div>
                {% for change_type, count in change_type_counts.items() %}
                <button class="filter-btn" data-filter="{{ change_type }}" title="{{ change_type }}">
                    {{ change_type_labels.get(change_type, change_type) }} ({{ count }})
                </button>
                {% endfor %}
            </div>
        </div>
        
        <!-- Differences Table -->
        <div class="differences-table">
            <table id="differencesTable">
                <thead>
                    <tr>
                        <th>Severity</th>
                        <th>Change Type</th>
                        <th>Field Path</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {% for diff in differences %}
                    <tr data-severity="{{ diff.severity }}" data-type="{{ diff.type }}">
                        <td>
                            <span class="severity-badge severity-{{ diff.severity|lower }}">
                                {{ diff.severity }}
                            </span>
                        </td>
                        <td>
                            <span class="change-type">{{ diff.type }}</span>
                        </td>
                        <td>
                            <div class="expandable" onclick="toggleDetails(this)">
                                {{ diff.path }}
                            </div>
                            <div class="details">
                                <strong>Element:</strong> {{ diff.element }}<br>
                                <strong>Schema 1:</strong> {{ diff.schema1_value or 'N/A' }}<br>
                                <strong>Schema 2:</strong> {{ diff.schema2_value or 'N/A' }}<br>
                                <strong>Impact:</strong> {{ diff.impact }}<br>
                                
                                {% if diff.xml_example %}
                                <br><strong>Before:</strong>
                                <div class="xml-example xml-before">{{ diff.xml_example.before }}</div>
                                <strong>After:</strong>
                                <div class="xml-example xml-after">{{ diff.xml_example.after }}</div>
                                {% endif %}
                            </div>
                        </td>
                        <td>{{ diff.impact[:100] }}...</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="no-results" id="noResults" style="display: none;">
                <h3>No results found</h3>
                <p>Try adjusting your search or filters</p>
            </div>
        </div>
    </div>
    
    <script>
        // Sample data for interactivity
        const differences = {{ differences_json|safe }};
        
        // Search functionality
        const searchBox = document.getElementById('searchBox');
        const table = document.getElementById('differencesTable');
        const tbody = table.querySelector('tbody');
        const noResults = document.getElementById('noResults');
        
        let currentFilter = 'all';
        
        searchBox.addEventListener('input', filterTable);
        
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentFilter = this.dataset.filter;
                filterTable();
            });
        });
        
        function filterTable() {
            const searchTerm = searchBox.value.toLowerCase();
            const rows = tbody.querySelectorAll('tr');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const severity = row.dataset.severity;
                const type = row.dataset.type;
                const text = row.textContent.toLowerCase();
                
                let matchesFilter = currentFilter === 'all' || 
                                  severity === currentFilter || 
                                  type === currentFilter;
                let matchesSearch = searchTerm === '' || text.includes(searchTerm);
                
                if (matchesFilter && matchesSearch) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
            table.style.display = visibleCount === 0 ? 'none' : 'table';
        }
        
        function toggleDetails(element) {
            element.classList.toggle('expanded');
            const details = element.nextElementSibling;
            details.classList.toggle('show');
        }
        
        // Initial load
        console.log('Loaded ' + differences.length + ' differences');
    </script>
</body>
</html>
    '''
    
    def __init__(self, comparator, output_file):
        self.comparator = comparator
        self.output_file = output_file
        
    def generate(self):
        """Generate interactive HTML report"""
        
        # Calculate statistics
        stats = {
            'total': len(self.comparator.differences),
            'high': len([d for d in self.comparator.differences if d.get('severity') == 'HIGH']),
            'medium': len([d for d in self.comparator.differences if d.get('severity') == 'MEDIUM']),
            'low': len([d for d in self.comparator.differences if d.get('severity') == 'LOW']),
        }
        
        # Calculate change type counts
        from collections import Counter
        change_type_counts = Counter(d.get('type', 'UNKNOWN') for d in self.comparator.differences)
        
        # User-friendly labels for change types
        change_type_labels = {
            'REMOVED': '❌ Removed',
            'ADDED': '➕ Added',
            'TYPE_CHANGED': '🔄 Type Changed',
            'CARDINALITY_CHANGED': '🔢 Cardinality Changed',
            'RESTRICTION_CHANGED': '⚠️ Restriction Changed',
            'FIELD_CLASS_CHANGED': '🟡 Field Classification Changed',
            'ENUMERATION_CHANGED': '📋 Enumeration Changed',
            'RULEBOOK_CHANGED': '📖 Rulebook Changed',
            'USAGE_RULES_CHANGED': '📝 Usage Rules Changed',
            'FIXED_VALUE_CHANGED': '🔒 Fixed Value Changed',
            'DEFAULT_VALUE_CHANGED': '⚙️ Default Value Changed',
            'DOCUMENTATION_CHANGED': '📝 Documentation Changed',
            'NAMESPACE_CHANGED': '🌐 Namespace Changed',
            'PATTERN_CHANGED': '🎯 Pattern Changed',
            'LENGTH_CHANGED': '📏 Length Changed',
            'RANGE_CHANGED': '📊 Range Changed',
        }
        
        # Add XML examples to differences
        differences_with_examples = []
        for diff in self.comparator.differences:
            diff_copy = diff.copy()
            
            # Generate simple XML example
            if diff['type'] in ['REMOVED', 'ADDED', 'TYPE_CHANGED']:
                element_name = diff['path'].split('/')[-1]
                diff_copy['xml_example'] = {
                    'before': self._generate_xml_snippet(diff, 'before'),
                    'after': self._generate_xml_snippet(diff, 'after')
                }
            
            differences_with_examples.append(diff_copy)
        
        # Create subtitle
        schema1_name = self.comparator.name1
        schema2_name = self.comparator.name2
        subtitle = f"Comparing {schema1_name} vs {schema2_name} • Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Render template
        template = Template(self.HTML_TEMPLATE)
        html_content = template.render(
            title=f"{schema1_name} vs {schema2_name}",
            subtitle=subtitle,
            stats=stats,
            change_type_counts=change_type_counts,
            change_type_labels=change_type_labels,
            differences=differences_with_examples,  # Show ALL differences
            differences_json=json.dumps(differences_with_examples)
        )
        
        # Write to file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ Interactive HTML report: {self.output_file}")
        print(f"   📊 {stats['total']} differences")
        print(f"   🔍 Search, filter, and expand details")
        print(f"   🌐 Open in any web browser")
    
    def _generate_xml_snippet(self, diff, when='before'):
        """Generate simple XML snippet"""
        element_name = diff['path'].split('/')[-1]
        
        if diff['type'] == 'REMOVED':
            if when == 'before':
                return f"<{element_name}>sample_value</{element_name}>"
            else:
                return f"<!-- {element_name} removed -->"
        
        elif diff['type'] == 'ADDED':
            if when == 'before':
                return f"<!-- {element_name} did not exist -->"
            else:
                return f"<{element_name}>new_value</{element_name}>"
        
        elif diff['type'] == 'TYPE_CHANGED':
            if when == 'before':
                return f"<{element_name}><!-- {diff['schema1_type'][:30]} --></{element_name}>"
            else:
                return f"<{element_name}><!-- {diff['schema2_type'][:30]} --></{element_name}>"
        
        return f"<{element_name}>value</{element_name}>"


def add_html_to_comparison(comparator, output_base):
    """Add HTML generation to existing comparison"""
    html_file = output_base.replace('.xlsx', '.html')
    html_generator = InteractiveHTMLGenerator(comparator, html_file)
    html_generator.generate()
    return html_file
