const xsdTools = [
    {
        id: 'comprehensive', icon: '📊', title: 'Comprehensive Analysis', badge: null,
        description: 'Extract ALL metadata from an XSD schema including elements, types, annotations, yellow/white fields.',
        features: ['Complete metadata', 'Yellow/White fields', 'Pattern analysis', 'JSON + Excel'],
        input: 'Upload 1 XSD file', minFiles: 1, options: null,
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use Comprehensive Analysis when you need to:</p><ul><li>Understand the complete structure of an ISO 20022 or any XSD schema</li><li>Extract all element definitions, types, and constraints</li><li>Identify Yellow fields (required for specific schemes) and White fields (optional)</li><li>Get a quick overview before starting implementation</li><li>Document schema requirements for development teams</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your XSD schema file (.xsd)</p><p><strong>Step 2:</strong> Click "Run Tool" to start the analysis</p><p><strong>Step 3:</strong> Download the generated Excel file with all metadata</p><p><strong>Tip:</strong> The analysis extracts annotations, patterns, enumerations, and all constraints defined in the schema.</p>',
            output: '<h4>📦 Output Files</h4><p>This tool generates:</p><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">analysis.xlsx</span><span class="output-file-desc">— Complete schema metadata in Excel format</span></div></div><p style="margin-top:16px;">The Excel file contains sheets for Elements, Types, Patterns, Enumerations, and Yellow/White field indicators.</p>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Save Hours</div><div class="guide-benefit-text">Instantly extract what would take hours to analyze manually</div></div><div class="guide-benefit"><div class="guide-benefit-title">Complete View</div><div class="guide-benefit-text">See every element, type, and constraint in one place</div></div><div class="guide-benefit"><div class="guide-benefit-title">Scheme Awareness</div><div class="guide-benefit-text">Identifies Yellow/White fields specific to payment schemes</div></div><div class="guide-benefit"><div class="guide-benefit-title">Ready to Share</div><div class="guide-benefit-text">Excel format perfect for team collaboration</div></div></div>'
        }
    },
    {
        id: 'document', icon: '📄', title: 'Schema Documentation', badge: null,
        description: 'Generate a comprehensive 3-sheet Excel workbook documenting the complete schema structure.',
        features: ['Hierarchical view', 'Element details', 'Type definitions', 'Professional format'],
        input: 'Upload 1 XSD file', minFiles: 1, options: null,
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use Schema Documentation when you need to:</p><ul><li>Create professional documentation for stakeholders</li><li>Generate a hierarchical view of the schema structure</li><li>Produce documentation for compliance or audit purposes</li><li>Share schema details with non-technical team members</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your XSD schema file</p><p><strong>Step 2:</strong> Click "Run Tool"</p><p><strong>Step 3:</strong> Download the Excel workbook with 3 organized sheets</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">documentation.xlsx</span><span class="output-file-desc">— 3-sheet workbook with hierarchical structure</span></div></div><p style="margin-top:16px;">Sheets include: Overview, Element Hierarchy, and Type Definitions with professional formatting.</p>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Professional Output</div><div class="guide-benefit-text">Ready for stakeholder presentations</div></div><div class="guide-benefit"><div class="guide-benefit-title">Clear Hierarchy</div><div class="guide-benefit-text">Visual tree structure of elements</div></div><div class="guide-benefit"><div class="guide-benefit-title">Audit Ready</div><div class="guide-benefit-text">Complete documentation for compliance</div></div></div>'
        }
    },
    {
        id: 'compare', icon: '🔄', title: 'Compare 2 Schemas', badge: null,
        description: 'Find differences between two XSD schema versions with detailed reports.',
        features: ['Side-by-side diff', 'Change detection', 'Multiple formats', 'Filtering'],
        input: 'Upload 2 XSD files', minFiles: 2,
        options: [{ type: 'text', id: 'name1', label: 'Schema 1 Name', placeholder: 'e.g., Production' }, { type: 'text', id: 'name2', label: 'Schema 2 Name', placeholder: 'e.g., New Version' }],
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use Compare 2 Schemas when you need to:</p><ul><li>Identify differences between schema versions</li><li>Assess impact of schema upgrades</li><li>Document changes for change management</li><li>Compare production vs. development schemas</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload the first (baseline) XSD file</p><p><strong>Step 2:</strong> Upload the second (new/target) XSD file</p><p><strong>Step 3:</strong> Optionally name each schema for clearer reports</p><p><strong>Step 4:</strong> Click "Run Tool" to generate comparison</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">comparison.xlsx</span><span class="output-file-desc">— Detailed diff in Excel with filters</span></div><div class="output-file"><span class="output-file-icon">📝</span><span class="output-file-name">comparison.docx</span><span class="output-file-desc">— Word report for stakeholders</span></div><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">comparison.html</span><span class="output-file-desc">— Interactive HTML report</span></div></div>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Impact Analysis</div><div class="guide-benefit-text">Quickly identify breaking changes</div></div><div class="guide-benefit"><div class="guide-benefit-title">Multiple Formats</div><div class="guide-benefit-text">Excel, Word, and HTML outputs</div></div><div class="guide-benefit"><div class="guide-benefit-title">Change Tracking</div><div class="guide-benefit-text">Added, removed, modified elements</div></div></div>'
        }
    },
    {
        id: 'multi_compare', icon: '📈', title: 'Multi-Schema Comparison', badge: null,
        description: 'Compare 3+ schemas simultaneously with matrix analysis.',
        features: ['Matrix comparison', 'Pairwise analysis', 'Stakeholder reports', 'Version tracking'],
        input: 'Upload 3+ XSD files', minFiles: 3,
        options: [{ type: 'text', id: 'names', label: 'Schema Names (comma-separated)', placeholder: 'e.g., V1.0, V2.0, V3.0' }],
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use Multi-Schema Comparison when you need to:</p><ul><li>Compare multiple schema versions at once</li><li>Track evolution across 3+ releases</li><li>Create a comparison matrix for stakeholders</li><li>Analyze differences across regional variants</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload 3 or more XSD files</p><p><strong>Step 2:</strong> Optionally provide names for each schema</p><p><strong>Step 3:</strong> Click "Run Tool" for comprehensive analysis</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">matrix.xlsx</span><span class="output-file-desc">— Master comparison matrix</span></div><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">report.html</span><span class="output-file-desc">— Interactive dashboard</span></div></div>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Big Picture View</div><div class="guide-benefit-text">See all versions at a glance</div></div><div class="guide-benefit"><div class="guide-benefit-title">Evolution Tracking</div><div class="guide-benefit-text">Understand how schema evolved</div></div></div>'
        }
    },
    {
        id: 'test_data', icon: '🧪', title: 'Test Data Generator', badge: 'Popular',
        description: 'Generate valid XML test files with realistic sample data.',
        features: ['Multiple profiles', 'ISO 20022 compliant', 'Configurable', 'Batch generation'],
        input: 'Upload 1 XSD file', minFiles: 1,
        options: [
            { type: 'number', id: 'num_files', label: 'Number of Files', value: 5, min: 1, max: 100 },
            { type: 'select', id: 'profile', label: 'Test Profile', options: [
                { value: 'domestic_sepa', label: '🇩🇪 Domestic SEPA (DE→DE)' },
                { value: 'cross_border', label: '🇪🇺 Cross-border (FR→IT)' },
                { value: 'instant_payment', label: '⚡ Instant (NL→ES)' },
                { value: 'high_value', label: '💰 High Value (GB→CH)' },
                { value: 'nordic_domestic', label: '🇸🇪 Nordic (SE→DK)' },
                { value: 'uk_faster_payment', label: '🇬🇧 UK Faster Payment' }
            ]},
            { type: 'checkbox', id: 'mandatory_only', label: 'Generate mandatory fields only' }
        ],
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use Test Data Generator when you need to:</p><ul><li>Create valid XML test messages for development</li><li>Generate sample data for QA testing</li><li>Produce realistic payment messages for demos</li><li>Test your system with various payment scenarios</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your XSD schema</p><p><strong>Step 2:</strong> Select number of test files to generate</p><p><strong>Step 3:</strong> Choose a test profile (payment scenario)</p><p><strong>Step 4:</strong> Click "Run Tool" to generate XML files</p><p><strong>Tip:</strong> Each profile includes realistic debtor/creditor data, amounts, and dates.</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📦</span><span class="output-file-name">test_data.zip</span><span class="output-file-desc">— ZIP containing all generated XML files</span></div></div><p style="margin-top:16px;">Each XML file is valid against the schema and contains realistic ISO 20022 payment data.</p>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">XSD Compliant</div><div class="guide-benefit-text">Generated XML validates against schema</div></div><div class="guide-benefit"><div class="guide-benefit-title">Realistic Data</div><div class="guide-benefit-text">IBANs, BICs, names, amounts</div></div><div class="guide-benefit"><div class="guide-benefit-title">Multiple Scenarios</div><div class="guide-benefit-text">Domestic, cross-border, instant</div></div><div class="guide-benefit"><div class="guide-benefit-title">Batch Generation</div><div class="guide-benefit-text">Generate up to 100 files at once</div></div></div>'
        }
    },
    {
        id: 'xml_validate', icon: '✅', title: 'XML Validator', badge: null,
        description: 'Validate XML against XSD with ISO 20022 business rules.',
        features: ['XSD validation', 'Business rules', 'IBAN/BIC check', 'Detailed report'],
        input: 'Upload 1 XML + 1 XSD', minFiles: 2, options: null,
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use XML Validator when you need to:</p><ul><li>Validate an XML message against its schema</li><li>Check ISO 20022 business rules (Either/Or constraints)</li><li>Verify IBAN, BIC, LEI format compliance</li><li>Debug XML validation errors</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your XML message file</p><p><strong>Step 2:</strong> Upload the XSD schema (or ZIP containing it)</p><p><strong>Step 3:</strong> Click "Run Tool" to validate</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">validation.html</span><span class="output-file-desc">— Visual validation report</span></div><div class="output-file"><span class="output-file-icon">{ }</span><span class="output-file-name">validation.json</span><span class="output-file-desc">— Machine-readable results</span></div></div>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Comprehensive</div><div class="guide-benefit-text">XSD + business rule validation</div></div><div class="guide-benefit"><div class="guide-benefit-title">Format Checks</div><div class="guide-benefit-text">IBAN, BIC, LEI, dates verified</div></div><div class="guide-benefit"><div class="guide-benefit-title">Clear Errors</div><div class="guide-benefit-text">XPath location for each issue</div></div></div>'
        }
    },
    {
        id: 'xml_diff', icon: '🔍', title: 'XML Diff', badge: 'New',
        description: 'Compare two XML files to find all differences.',
        features: ['Side-by-side', 'Change detection', 'XPath locations', 'HTML report'],
        input: 'Upload 2 XML files', minFiles: 2,
        options: [{ type: 'checkbox', id: 'ignore_order', label: 'Ignore element order' }, { type: 'checkbox', id: 'compare_attributes', label: 'Compare attributes' }],
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use XML Diff when you need to:</p><ul><li>Compare two XML messages for differences</li><li>Debug why a message is failing</li><li>Verify message transformations</li><li>Regression test XML output</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload the first (baseline) XML file</p><p><strong>Step 2:</strong> Upload the second (comparison) XML file</p><p><strong>Step 3:</strong> Choose comparison options</p><p><strong>Step 4:</strong> Click "Run Tool"</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">diff.html</span><span class="output-file-desc">— Visual side-by-side diff</span></div></div>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Visual Diff</div><div class="guide-benefit-text">Color-coded changes</div></div><div class="guide-benefit"><div class="guide-benefit-title">XPath Locations</div><div class="guide-benefit-text">Exact location of each difference</div></div></div>'
        }
    },
    {
        id: 'batch_validate', icon: '📦', title: 'Batch Validator', badge: 'New',
        description: 'Validate multiple XML files at once.',
        features: ['Bulk validation', 'Progress tracking', 'Pass/fail stats', 'Excel export'],
        input: 'Upload 1 XSD + XML files', minFiles: 2, options: null,
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use Batch Validator when you need to:</p><ul><li>Validate hundreds of XML files at once</li><li>Test migration data sets</li><li>Quality check bulk message exports</li><li>Generate compliance reports</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your XSD schema</p><p><strong>Step 2:</strong> Upload multiple XML files (or a ZIP)</p><p><strong>Step 3:</strong> Click "Run Tool" to validate all</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">batch_report.html</span><span class="output-file-desc">— Dashboard with pass/fail stats</span></div></div>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Bulk Processing</div><div class="guide-benefit-text">100s of files in seconds</div></div><div class="guide-benefit"><div class="guide-benefit-title">Statistics</div><div class="guide-benefit-text">Pass rate, error summary</div></div></div>'
        }
    },
    {
        id: 'mapping_template', icon: '📋', title: 'Mapping Template', badge: 'New',
        description: 'Generate Excel mapping templates for implementation.',
        features: ['Complete field list', 'XPath mapping', 'Sample values', 'Status tracking'],
        input: 'Upload 1 XSD file', minFiles: 1, options: null,
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use Mapping Template when you need to:</p><ul><li>Create field mapping documentation</li><li>Plan source-to-target transformations</li><li>Track implementation status per field</li><li>Document integration requirements</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your target XSD schema</p><p><strong>Step 2:</strong> Click "Run Tool"</p><p><strong>Step 3:</strong> Download and fill in source mappings</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">mapping_template.xlsx</span><span class="output-file-desc">— Complete field mapping worksheet</span></div></div><p style="margin-top:16px;">Columns include: XPath, Element, Type, Sample Value, Source System, Source Field, Transformation Rule, Status.</p>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Implementation Ready</div><div class="guide-benefit-text">Complete field list with XPaths</div></div><div class="guide-benefit"><div class="guide-benefit-title">Track Progress</div><div class="guide-benefit-text">Status column for each field</div></div><div class="guide-benefit"><div class="guide-benefit-title">Sample Values</div><div class="guide-benefit-text">Pre-filled examples for reference</div></div></div>'
        }
    },
    {
        id: 'xml_transform', icon: '🔁', title: 'XML Transformer', badge: 'New',
        description: 'Transform XML between schema versions.',
        features: ['Version migration', 'Auto mapping', 'Handles renames', 'Validation'],
        input: 'Upload 1 XML + 2 XSD', minFiles: 3, options: null,
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use XML Transformer when you need to:</p><ul><li>Migrate XML from old to new schema version</li><li>Convert between regional variants</li><li>Transform pacs.008 v2 to v8 format</li><li>Upgrade messages to newer standards</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your source XML message</p><p><strong>Step 2:</strong> Upload the source (original) XSD schema</p><p><strong>Step 3:</strong> Upload the target (new) XSD schema</p><p><strong>Step 4:</strong> Click "Run Tool" to transform</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📄</span><span class="output-file-name">transformed.xml</span><span class="output-file-desc">— Transformed message</span></div><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">transform_report.html</span><span class="output-file-desc">— Mapping report</span></div></div>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Auto Mapping</div><div class="guide-benefit-text">Automatically maps matching fields</div></div><div class="guide-benefit"><div class="guide-benefit-title">Transparency</div><div class="guide-benefit-text">Report shows all mappings used</div></div></div>'
        }
    },
    {
        id: 'xsd_explorer', icon: '⬡', title: 'XSD Explorer', badge: 'New',
        description: 'Interactive visual XSD explorer with collapsible tree, schema diagram, type inheritance, XPath copy, constraints summary, and statistics.',
        features: ['Interactive tree', 'Schema diagram', 'Type inheritance', 'Statistics & heatmap'],
        input: 'Upload 1 XSD file', minFiles: 1, options: null,
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use XSD Explorer when you need to:</p><ul><li>Visually browse and navigate an XSD schema structure</li><li>Understand type inheritance and content models (sequence/choice/all)</li><li>Copy XPath expressions for specific elements</li><li>Analyse schema statistics — cardinality, type usage heatmap, depth</li><li>Inspect raw XSD source snippets alongside the tree view</li><li>Share an interactive schema reference with your team</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your XSD schema file (.xsd)</p><p><strong>Step 2:</strong> Click "Run Tool" to generate the explorer</p><p><strong>Step 3:</strong> Open the HTML file in your browser for the interactive experience</p><p><strong>Step 4:</strong> Download the Excel file for a flat structure report</p><p><strong>Tip:</strong> Click any node in the tree to inspect its properties, facets, documentation, and inheritance chain in the right-hand panel.</p>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">*_explorer.html</span><span class="output-file-desc">— Interactive tree, diagram &amp; stats explorer</span></div><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">*_structure.xlsx</span><span class="output-file-desc">— Flat structure report with XPath, facets &amp; inheritance</span></div></div><p style="margin-top:16px;">The HTML file is fully self-contained and can be opened offline or shared with colleagues.</p>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Visual Navigation</div><div class="guide-benefit-text">Collapse/expand tree with content model indicators</div></div><div class="guide-benefit"><div class="guide-benefit-title">Schema Diagram</div><div class="guide-benefit-text">D3.js node-link graph of the schema</div></div><div class="guide-benefit"><div class="guide-benefit-title">XPath Copy</div><div class="guide-benefit-text">One-click copy of any element XPath</div></div><div class="guide-benefit"><div class="guide-benefit-title">Statistics</div><div class="guide-benefit-text">Type usage heatmap, cardinality breakdown</div></div></div>'
        }
    }
];

function openTool(toolId) {
    const tool = xsdTools.find(t => t.id === toolId);
    if (!tool) return;
    currentTool = tool;
    uploadedFiles = [];
    fileInput.value = ''; // clear so same file can be re-uploaded on tool switch
    document.getElementById('toolPageIcon').textContent = tool.icon;
    document.getElementById('toolPageTitle').textContent = tool.title;
    document.getElementById('uploadHint').textContent = '— ' + tool.input;
    document.getElementById('fileList').innerHTML = '';
    document.getElementById('resultsSection').classList.remove('active');
    hideMessage();

    // Load guide content
    document.getElementById('guide-when').innerHTML = tool.guide.when;
    document.getElementById('guide-how').innerHTML = tool.guide.how;
    document.getElementById('guide-output').innerHTML = tool.guide.output;
    document.getElementById('guide-benefits').innerHTML = tool.guide.benefits;
    document.querySelectorAll('.guide-tab').forEach((t, i) => t.classList.toggle('active', i === 0));
    document.querySelectorAll('.guide-content').forEach((c, i) => c.classList.toggle('active', i === 0));

    // Options
    const optCard = document.getElementById('optionsCard');
    const optContent = document.getElementById('optionsContent');
    if (tool.options?.length) {
        optCard.style.display = 'block';
        optContent.innerHTML = tool.options.map(o => {
            if (o.type === 'text') return `<div class="option-group"><label class="option-label">${o.label}</label><input type="text" class="option-input" id="${o.id}" placeholder="${o.placeholder||''}"></div>`;
            if (o.type === 'number') return `<div class="option-group"><label class="option-label">${o.label}</label><input type="number" class="option-input" id="${o.id}" value="${o.value||5}" min="${o.min||1}" max="${o.max||100}"></div>`;
            if (o.type === 'select') return `<div class="option-group"><label class="option-label">${o.label}</label><select class="option-select" id="${o.id}">${o.options.map(x=>`<option value="${x.value}">${x.label}</option>`).join('')}</select></div>`;
            if (o.type === 'checkbox') return `<div class="option-group"><label class="option-checkbox"><input type="checkbox" id="${o.id}"> ${o.label}</label></div>`;
            return '';
        }).join('');
    } else { optCard.style.display = 'none'; }
    updateRunButton();
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page-tool').classList.add('active');
}

// File Upload — events handled by _fspInitPanel('xsd') on DOMContentLoaded
const fileInput = document.getElementById('fileInput');

function handleFiles(files) {
    const fd = new FormData();
    let skipped = [];

    Array.from(files).forEach(f => {
        if (/\.(xsd|xml|zip)$/i.test(f.name)) {
            fd.append('files[]', f);
        } else {
            skipped.push(f.name);
        }
    });

    if (skipped.length > 0 && fd.getAll('files[]').length === 0) {
        showMessage(`Invalid file type(s): ${skipped.join(', ')}. Only .xsd, .xml, .zip allowed.`, 'error');
        return;
    }

    if (!fd.getAll('files[]').length) {
        showMessage('Please select .xsd, .xml, or .zip files', 'error');
        return;
    }

    showLoading('Uploading ' + fd.getAll('files[]').length + ' file(s)...');

    fetch('/upload', { method: 'POST', body: fd })
        .then(r => r.json())
        .then(d => {
            hideLoading();
            if (d.success) {
                uploadedFiles.push(...d.files);
                renderFileList();
                updateRunButton();
                fileInput.value = ''; // clear so same file can be re-selected
                if (d.warnings && d.warnings.length > 0) {
                    showMessage(d.message || `${d.files.length} uploaded, ${d.warnings.length} skipped`, 'warning');
                }
            } else {
                // Show detailed error
                let errorMsg = d.error || 'Upload failed';
                if (d.suggestion) errorMsg += '. ' + d.suggestion;
                if (d.details && Array.isArray(d.details)) {
                    errorMsg += ': ' + d.details.map(e => e.file + ' - ' + e.error).join('; ');
                }
                showMessage(errorMsg, 'error');
                fileInput.value = '';
            }
        })
        .catch(e => {
            hideLoading();
            showMessage('Upload failed: Network error', 'error');
        });
}

// renderFileList → handled by FSP (see fspRenderFileList)

function removeFile(i) { uploadedFiles.splice(i, 1); renderFileList(); updateRunButton(); }
function updateRunButton() { document.getElementById('runToolBtn').disabled = !(currentTool && uploadedFiles.length >= currentTool.minFiles); }

// runTool v1 removed → FSP patched version below

function resetTool() { uploadedFiles = []; renderFileList(); updateRunButton(); document.getElementById('resultsSection').classList.remove('active'); hideMessage(); fileInput.value = ''; }
