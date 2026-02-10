#!/usr/bin/env python3
"""Update UI with ISO branding and comprehensive analyzer"""

import re

file_path = '/home/claude/iso_toolkit_final/templates/index.html'

with open(file_path, 'r') as f:
    content = f.read()

# 1. Update title
content = content.replace(
    '<title>XSD Toolkit', 
    '<title>ISO 20022 Payment Toolkit'
)

# 2. Update main heading
content = content.replace(
    '<h1>🔍 XSD Professional Toolkit</h1>',
    '<h1>💳 ISO 20022 Payment Message Toolkit</h1>'
)
content = content.replace(
    '<p class="subtitle">Enterprise-Grade Schema Analysis Platform</p>',
    '<p class="subtitle">Professional Payment Schema Analysis Platform</p>'
)

# 3. Update version
content = content.replace(
    'v2.0 Ultimate Edition',
    'v3.0 ISO 20022 Edition'
)

# 4. Add comprehensive analyzer tool card (if not present)
comprehensive_card = '''
                <div class="tool-card" data-tool="comprehensive">
                    <div class="tool-header">
                        <div class="icon">📊</div>
                        <h3>Comprehensive Analysis</h3>
                    </div>
                    <div class="description">
                        Extract ALL metadata with Yellow/White fields from ISO 20022 XSD annotations. 
                        Complete 20-column analysis with full paths, restrictions, and rulebook notes.
                    </div>
                    <ul class="features">
                        <li>Yellow/White from XSD annotations</li>
                        <li>20 columns complete metadata</li>
                        <li>Full paths & sequence order</li>
                        <li>All restrictions & patterns</li>
                    </ul>
                    <span class="tool-badge new">⭐ ISO 20022 Spec</span>
                </div>
'''

if 'data-tool="comprehensive"' not in content:
    # Find where to insert (after first tool-card div)
    match = re.search(r'<div class="tool-selector">(.*?)</div>', content, re.DOTALL)
    if match:
        # Insert at beginning of tool-selector
        insert_pos = match.start() + len('<div class="tool-selector">')
        content = content[:insert_pos] + comprehensive_card + content[insert_pos:]

with open(file_path, 'w') as f:
    f.write(content)

print("✅ Updated UI with:")
print("   - ISO 20022 Payment Toolkit branding")
print("   - Comprehensive Analyzer tool card added")
print("   - Version updated to v3.0 ISO 20022 Edition")
