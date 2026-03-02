        // Tool Definitions with Detailed Guides
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
            }
        ];

        let currentPage = 'home', currentTool = null, uploadedFiles = [];

        // Navigation
        function showPage(pageId) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById('page-' + pageId)?.classList.add('active');
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.querySelector(`.nav-item[data-page="${pageId}"]`)?.classList.add('active');
            currentPage = pageId;
            if (pageId === 'xsd-tools') renderToolsGrid();
            if (pageId === 'pdf-tools') renderPdfToolsGrid();
            if (pageId === 'rulebook-tools') renderRulebookToolsGrid();
            if (pageId === 'yaml-tools') renderYamlToolsGrid();
            if (pageId === 'library') initLibrary();
            document.getElementById('sidebar').classList.remove('open');
            document.getElementById('sidebarOverlay').classList.remove('active');
        }

        function toggleSidebar() {

            document.getElementById('sidebar').classList.toggle('open');
            document.getElementById('sidebarOverlay').classList.toggle('active');
        }

        function renderToolsGrid() {
            document.getElementById('xsdToolsGrid').innerHTML = xsdTools.map(t => `
                <div class="tool-card" onclick="openTool('${t.id}')">
                    <div class="tool-card-header"><div class="tool-card-icon">${t.icon}</div><div><span class="tool-card-title">${t.title}</span>${t.badge ? `<span class="tool-card-badge">${t.badge}</span>` : ''}</div></div>
                    <p class="tool-card-description">${t.description}</p>
                    <div class="tool-card-features">${t.features.map(f => `<div class="tool-card-feature">${f}</div>`).join('')}</div>
                    <div class="tool-card-input">📁 ${t.input}</div>
                    <div class="tool-card-arrow">→</div>
                </div>
            `).join('');
        }

        function switchGuideTab(tab, contentId) {
            document.querySelectorAll('.guide-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.guide-content').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById('guide-' + contentId).classList.add('active');
        }

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

        function showResults(files, msg) {
            document.getElementById('resultsSubtitle').textContent = msg || 'Files ready';
            document.getElementById('resultsFiles').innerHTML = files.map(f => `
                <li class="results-file"><span class="results-file-icon">${getIcon(f)}</span><span class="results-file-name">${f}</span>
                <div class="results-file-actions">${/\.html$/i.test(f)?`<a href="/preview/${f}" target="_blank" class="results-file-btn preview">Preview</a>`:''}<a href="/download/${f}" class="results-file-btn download">Download</a></div></li>
            `).join('');
            document.getElementById('resultsSection').classList.add('active');
            showMessage(msg, 'success');
        }

        function getIcon(f) { if (/\.xlsx$/i.test(f)) return '📊'; if (/\.docx$/i.test(f)) return '📝'; if (/\.html$/i.test(f)) return '🌐'; if (/\.json$/i.test(f)) return '{ }'; if (/\.xml$/i.test(f)) return '📄'; if (/\.zip$/i.test(f)) return '📦'; return '📁'; }
        function resetTool() { uploadedFiles = []; renderFileList(); updateRunButton(); document.getElementById('resultsSection').classList.remove('active'); hideMessage(); fileInput.value = ''; }
        function showLoading(t) { document.getElementById('loadingSubtext').textContent = t; document.getElementById('loadingOverlay').classList.add('active'); }
        function hideLoading() { document.getElementById('loadingOverlay').classList.remove('active'); }
        function showMessage(t, type) { const b = document.getElementById('messageBox'); b.textContent = t; b.className = 'message active ' + type; }
        function hideMessage() { document.getElementById('messageBox').className = 'message'; }

        // ── PDF Tools ──────────────────────────────────────────────────────────
        const pdfTools = [

            {
                id: 'pdf_compare', icon: '🔍', title: 'PDF Comparator', badge: 'New',
                description: 'Compare two PDF documents side-by-side with word-level diff, similarity scores, and table comparisons.',
                features: ['Word-level diff', 'Similarity score', 'Table comparison', 'Page-by-page'],
                input: 'Upload 2 PDF files', minFiles: 2, options: null,
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use PDF Comparator when you need to:</p><ul><li>Compare two versions of an ISO 20022 implementation guide</li><li>Find what changed between EPC and NPC spec documents</li><li>Audit differences between two regulatory PDFs</li><li>Verify that only expected changes were made to a document</li></ul>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload PDF A (baseline document)</p><p><strong>Step 2:</strong> Upload PDF B (new/comparison document)</p><p><strong>Step 3:</strong> Click "Run Tool" — the report is generated in seconds</p><p><strong>Tip:</strong> Identical pages are collapsed by default in the report. Click any page to expand it.</p>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">comparison.html</span><span class="output-file-desc">— Interactive HTML report with page-by-page diff</span></div></div><p style="margin-top:16px;">The report includes: overall similarity %, metadata comparison, and per-page word-level diffs with colour-coded additions and deletions.</p>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Instant Insight</div><div class="guide-benefit-text">Know at a glance what % has changed</div></div><div class="guide-benefit"><div class="guide-benefit-title">Word-Level Diff</div><div class="guide-benefit-text">See exact additions and deletions</div></div><div class="guide-benefit"><div class="guide-benefit-title">Table Aware</div><div class="guide-benefit-text">Compares tables side by side</div></div><div class="guide-benefit"><div class="guide-benefit-title">Collapsed View</div><div class="guide-benefit-text">Identical pages hidden for focus</div></div></div>'
                }
            },
            {
                id: 'pdf_table_extract', icon: '📊', title: 'PDF Table to Excel', badge: 'New',
                description: 'Extract all tables from a PDF into a formatted Excel workbook. Each table gets its own sheet with professional styling.',
                features: ['All tables extracted', 'One sheet per table', 'Professional formatting', 'Summary sheet'],
                input: 'Upload 1 or more PDF files', minFiles: 1, options: null,
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use PDF Table to Excel when you need to:</p><ul><li>Extract ISO 20022 message element tables from spec PDFs</li><li>Get field definitions into Excel for mapping work</li><li>Pull data tables from regulatory documents for analysis</li><li>Convert PDF tables into editable, filterable spreadsheets</li></ul>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your PDF file(s)</p><p><strong>Step 2:</strong> Click "Run Tool"</p><p><strong>Step 3:</strong> Download the Excel workbook</p><p><strong>Tip:</strong> Each table is placed on its own sheet named "P{page}_T{table}" (e.g. P12_T1 = page 12, table 1). A Summary sheet lists all tables found.</p>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">tables.xlsx</span><span class="output-file-desc">— All tables in formatted Excel workbook</span></div></div><p style="margin-top:16px;">The workbook includes: Summary sheet, one sheet per table, frozen headers, alternating row colours, and auto-fit column widths.</p>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">All Tables</div><div class="guide-benefit-text">Every table extracted automatically</div></div><div class="guide-benefit"><div class="guide-benefit-title">Professional Style</div><div class="guide-benefit-text">Navy headers, alternating rows</div></div><div class="guide-benefit"><div class="guide-benefit-title">Easy Navigation</div><div class="guide-benefit-text">Summary sheet with page references</div></div><div class="guide-benefit"><div class="guide-benefit-title">Filterable</div><div class="guide-benefit-text">Excel format — sort, filter, search</div></div></div>'
                }
            },
            {
                id: 'pdf_merge', icon: '🔗', title: 'PDF Merger', badge: null,
                description: 'Combine multiple PDF files into a single document. Files are merged in upload order.',
                features: ['Unlimited PDFs', 'Preserves content', 'Ordered merge', 'Fast output'],
                input: 'Upload 2+ PDF files', minFiles: 2, options: null,
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use PDF Merger when you need to:</p><ul><li>Combine multiple spec documents into one reference file</li><li>Bundle EPC + NPC implementation guides together</li><li>Create a single PDF from multiple separate chapters</li><li>Consolidate monthly reports into one document</li></ul>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload all PDFs you want to merge (they merge in upload order)</p><p><strong>Step 2:</strong> Click "Run Tool"</p><p><strong>Step 3:</strong> Download the merged PDF</p><p><strong>Tip:</strong> The order files appear in the file list is the order they will appear in the merged PDF.</p>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📄</span><span class="output-file-name">merged.pdf</span><span class="output-file-desc">— Single combined PDF</span></div></div>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Simple</div><div class="guide-benefit-text">Upload and merge in one click</div></div><div class="guide-benefit"><div class="guide-benefit-title">Ordered</div><div class="guide-benefit-text">Files merged in upload sequence</div></div><div class="guide-benefit"><div class="guide-benefit-title">Lossless</div><div class="guide-benefit-text">Content fully preserved</div></div></div>'
                }
            },
            {
                id: 'pdf_split', icon: '✂️', title: 'PDF Splitter', badge: null,
                description: 'Split a PDF into multiple files by fixed chunk size or custom page ranges.',
                features: ['Chunk mode', 'Custom ranges', 'Live preview', 'ZIP download'],
                input: 'Upload 1 PDF file', minFiles: 1,
                options: [
                    { type: 'info', id: 'page_count_info', label: '' },
                    { type: 'select', id: 'split_mode', label: 'Split Mode', options: [
                        { value: 'chunks', label: 'Fixed chunk size (e.g. every 10 pages)' },
                        { value: 'ranges', label: 'Custom page ranges (e.g. 1-5, 8, 10-12)' }
                    ]},
                    { type: 'number', id: 'chunk_size', label: 'Pages per chunk (Chunk mode)', value: 10, min: 1, max: 200 },
                    { type: 'text', id: 'ranges', label: 'Page ranges (Ranges mode)', placeholder: 'e.g. 1-5, 8, 10-12' }
                ],
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use PDF Splitter when you need to:</p><ul><li>Extract specific chapters from a large ISO 20022 Implementation Guide</li><li>Break a 160-page IG into manageable sections — e.g. just the pacs.008 pages (11–38) or camt.056 pages (60–69)</li><li>Share only the relevant message pages with your team without the full document</li><li>Create smaller PDFs for emailing, archiving, or regulatory submissions</li><li>Quickly isolate a problematic section for focused review</li></ul><p style="margin-top:10px;"><strong>Tip:</strong> For IG PDFs, use the <strong>Rulebook IG Extractor</strong> instead — it auto-detects sections and extracts them into structured Excel with colour-coded fields.</p>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your PDF. The tool instantly shows the <strong>total page count</strong> so you can plan your split — no guessing needed.</p><p><strong>Chunk mode:</strong> Choose a fixed page count per output file. The preview tells you exactly how many files will be created before you click Run. Example: 10 pages/chunk on a 38-page PDF → 4 files.</p><p><strong>Ranges mode:</strong> Type page ranges like <code>1-5, 8, 10-15</code> — each comma-separated range becomes its own file. Reference the page count shown above to target the right pages.</p><p><strong>Step 3:</strong> Click <strong>"Run Tool"</strong> and download the ZIP containing all split files.</p>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📦</span><span class="output-file-name">split_files.zip</span><span class="output-file-desc">— ZIP containing all split PDF files</span></div></div><p style="margin-top:14px;">Each output file is automatically named with its page range, e.g. <code>document_p0001-p0010.pdf</code>, <code>document_p0011-p0020.pdf</code>. The live preview tells you the exact count before you run.</p>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Live Preview</div><div class="guide-benefit-text">See total pages and output file count before splitting — no surprises</div></div><div class="guide-benefit"><div class="guide-benefit-title">Flexible Splitting</div><div class="guide-benefit-text">Fixed chunks OR fully custom page ranges per your needs</div></div><div class="guide-benefit"><div class="guide-benefit-title">Auto-Named Files</div><div class="guide-benefit-text">Output files named with their page range for easy reference</div></div><div class="guide-benefit"><div class="guide-benefit-title">Single ZIP Download</div><div class="guide-benefit-text">All split files bundled into one download</div></div></div>'
                }
            }
        ];

        const rulebookTools = [
            {
                id: 'ig_extract', icon: '📋', title: 'Rulebook IG Extractor', badge: 'New',
                description: 'Extracts ISO 20022 Implementation Guide tables into structured Excel — one sheet per message, one row per field, with full XPath and colour coding.',
                features: ['🟡 Yellow = Core Mandatory', '⬜ White = Optional', '🔴 Red = Not Permitted', 'Smart section picker'],
                input: 'Upload 1 or more IG PDF files', minFiles: 1,
                options: [
                    { type: 'ig_section_picker', id: 'ig_section_picker', label: 'Extract sections' },
                    { type: 'text', id: 'filter_messages', label: 'Or filter by message ID (optional)', placeholder: 'e.g. pacs.008.001.08, camt.056.001.08' },
                    { type: 'text', id: 'filter_sections', label: 'Or filter by section number (optional)', placeholder: 'e.g. 2.1.1  or  2.1.1, 2.2.1' }
                ],
                guide: {
                    when: `<h4>📌 When to Use This Tool</h4><p>Use Rulebook IG Extractor when you need to:</p><ul><li>Extract all message field definitions from an EPC or NPC Implementation Guide PDF into Excel</li><li>Get a structured workbook with one row per field — XPath, XML Tag, ISO/SEPA Length, usage rules, rulebook references</li><li>Identify which fields are SEPA/NPC Core Mandatory (🟡 yellow), optional (⬜ white), or not permitted (🔴 red) — colours match the original PDF exactly</li><li>Extract only one specific message (e.g. just pacs.008) or one specific section (e.g. 2.1.1) from a multi-message IG</li><li>Compare EPC vs NPC rules side-by-side in Excel</li><li>Build mapping templates, gap analyses, or compliance checklists from the IG</li></ul>`,
                    how: `<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your ISO 20022 IG PDF (e.g. EPC122-16 SCT Inst Inter-PSP IG or NPC012-01).</p><p><strong>Step 2 — Choose sections (optional):</strong> Click <strong>"Detect Sections in PDF"</strong> to see all message sections with their page ranges. Tick the ones you want to extract. Leave all unchecked to extract everything.</p><p><strong>Alternatively</strong> — filter by message ID: <code>pacs.008.001.08</code> or by section number: <code>2.1.1</code>. Useful when the same message type (e.g. pacs.028) appears in multiple sections.</p><p><strong>Step 3:</strong> Click <strong>"Run Tool"</strong>. Processing takes about 10–20 seconds for a 160-page IG.</p><p><strong>Tip:</strong> Upload both EPC and NPC PDFs together — each gets its own output Excel for easy side-by-side comparison.</p>`,
                    output: `<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">{document}_IG.xlsx</span><span class="output-file-desc">— Structured Excel workbook (one per PDF)</span></div></div><p style="margin-top:12px;"><strong>Workbook structure:</strong></p><ul><li><strong>Summary sheet</strong> — all sections with total / core (yellow) / optional (white) field counts and page ranges</li><li><strong>One sheet per message section</strong> — named e.g. <code>pacs_008_001_08</code>, <code>camt_056_001_08</code></li></ul><p><strong>Columns per row:</strong> Index · Multiplicity · XPath · Element Name · ISO Name · ISO Definition · XML Tag · Type · ISO Length · SEPA/NPC Length · Usage Rules · Rulebook · Format Rules · FractDigits · Inclusive · Code Restrictions</p><p><strong>Row colours (match the original PDF exactly):</strong></p><ul><li>🟡 <strong>Yellow</strong> = SEPA/NPC Core Mandatory — required for inter-PSP processing</li><li>⬜ <strong>White</strong> = Optional / AOS — not required for SEPA core</li><li>🔴 <strong>Light Red</strong> = Not permitted in SEPA (blocked proprietary alternatives)</li></ul>`,
                    benefits: `<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">One Row per Field</div><div class="guide-benefit-text">Multi-line PDF rows collapsed — no more copy-paste from PDF</div></div><div class="guide-benefit"><div class="guide-benefit-title">Full XPath</div><div class="guide-benefit-text">Hierarchy rebuilt from +/++/+++ notation e.g. GroupHeader/SettlementInfo/Code</div></div><div class="guide-benefit"><div class="guide-benefit-title">Colour Faithful</div><div class="guide-benefit-text">🟡 Yellow / ⬜ white / 🔴 red rows exactly match the original PDF</div></div><div class="guide-benefit"><div class="guide-benefit-title">Smart Section Picker</div><div class="guide-benefit-text">Detect and select only the sections you need — e.g. just pacs.008 section 2.1.1</div></div></div>`
                }
            }
            ,
            {
                id: 'ig_diff', icon: '⚖️', title: 'IG Diff (EPC vs NPC)', badge: 'New',
                description: 'Compare two IG Extractor Excel outputs side-by-side — highlights every field that was added, removed, or changed in status or rules between EPC and NPC (or any two IGs).',
                features: ['🟢 Added fields', '🔴 Removed fields', '🟡 Status changes', '🔵 Rule/length changes'],
                input: 'Upload 2 IG Excel files (.xlsx from IG Extractor)', minFiles: 2,
                options: [
                    { type: 'text', id: 'label_a', label: 'Label for File 1 (left side)', placeholder: 'e.g. EPC' },
                    { type: 'text', id: 'label_b', label: 'Label for File 2 (right side)', placeholder: 'e.g. NPC' }
                ],
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use IG Diff when you need to:</p><ul><li>Compare EPC and NPC Implementation Guides field-by-field — know exactly what differs</li><li>Identify which fields changed from SEPA Core Mandatory (yellow) to Optional (white) or vice versa</li><li>Find length, usage rule, rulebook, or format rule differences between two IGs</li><li>See fields added in NPC that are not in EPC, or removed entirely</li><li>Track what changed between two versions of the same IG (e.g. EPC122-15 vs EPC122-16)</li></ul><p style="margin-top:10px;"><strong>Tip:</strong> Run the IG Extractor on both PDFs first, then upload both output Excel files here.</p>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Run the Rulebook IG Extractor on both IGs (e.g. EPC and NPC). This gives you two .xlsx files.</p><p><strong>Step 2:</strong> Upload both Excel files here. Enter labels — e.g. "EPC" and "NPC" — so you can tell them apart in the output.</p><p><strong>Step 3:</strong> Click <strong>"Run Tool"</strong>. The diff runs in seconds.</p><p><strong>Reading the output:</strong> Each message section (pacs.008, camt.056, etc.) gets its own sheet. Identical rows are grouped and hidden by default — click the <strong>row group arrows on the left</strong> to expand them. Changed rows are colour-coded by change type.</p>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">IG_Diff_EPC_vs_NPC.xlsx</span><span class="output-file-desc">— Colour-coded diff workbook</span></div></div><p style="margin-top:12px;"><strong>Workbook structure:</strong></p><ul><li><strong>Summary sheet</strong> — all message sections with change counts by category</li><li><strong>One sheet per message</strong> — side-by-side File A and File B columns, with a "What Changed" summary column</li></ul><p><strong>Change categories:</strong></p><ul><li>🟢 <strong>Added</strong> — field exists in File B only</li><li>🔴 <strong>Removed</strong> — field exists in File A only</li><li>🟡 <strong>Status</strong> — mandatory/optional/not-permitted changed</li><li>🔵 <strong>Rules</strong> — length, usage rules, rulebook, or format rules changed</li><li>🟠 <strong>Both</strong> — status AND rules changed</li><li>⬜ <strong>Same</strong> — identical (grouped and hidden by default)</li></ul>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Side-by-Side</div><div class="guide-benefit-text">EPC and NPC columns next to each other — no manual VLOOKUP needed</div></div><div class="guide-benefit"><div class="guide-benefit-title">Change Categories</div><div class="guide-benefit-text">6 colour-coded change types — instantly see what kind of difference it is</div></div><div class="guide-benefit"><div class="guide-benefit-title">Focus on Changes</div><div class="guide-benefit-text">Identical rows hidden by default — only see what actually changed</div></div><div class="guide-benefit"><div class="guide-benefit-title">All Messages</div><div class="guide-benefit-text">Every shared message section compared in one workbook</div></div></div>'
                }
            }
            ,
            {
                id: 'rulebook_changes', icon: '📋', title: 'Rulebook Change Tracker', badge: 'New',
                description: 'Extracts the official "List of Changes" section from any EPC or NPC IG PDF — structures every change entry into a searchable, colour-coded Excel with business impact notes.',
                features: ['🟠 Content changes (CHAN)', '🔵 Clarifications (CLAR)', '🟡 Typo fixes (TYPO)', '📝 Business notes per entry'],
                input: 'Upload 1 or 2 IG PDFs (.pdf)',
                options: [],
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use the Rulebook Change Tracker when you need to:</p><ul><li>Understand what officially changed between IG versions (e.g. 2023 v1.2 → 2025 v1.0)</li><li>Extract the complete change log from an EPC or NPC IG PDF into a structured, filterable Excel</li><li>Categorise changes by type — CHAN (content), CLAR (clarification), TYPO (typo fix)</li><li>Get implementation notes for each change — which changes require code updates vs. no action</li><li>Compare the change logs of two IGs side-by-side (e.g. EPC vs NPC changes in the same version period)</li></ul><p style="margin-top:10px;"><strong>Tip:</strong> For field-level comparison between EPC and NPC, use the IG Diff tool instead. This tool focuses on the official change entries published by EPC / NPC.</p>',
                    how: '<h4>📖 How to Use</h4><p><strong>Single PDF:</strong> Upload one IG PDF (e.g. EPC122-16). The tool finds the "List of Changes" section and extracts every numbered entry into a structured Excel.</p><p><strong>Two PDFs:</strong> Upload two PDFs (e.g. EPC and NPC). The tool produces one sheet per document plus a Summary sheet for quick comparison.</p><p><strong>Step-by-step:</strong></p><ol><li>Upload 1 or 2 IG PDFs</li><li>Click <strong>"Run Tool"</strong></li><li>Download the Excel — one tab per document, with change type filter colour coding</li></ol>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">RulebookChanges.xlsx</span><span class="output-file-desc">— Structured change log workbook</span></div></div><p style="margin-top:12px;"><strong>Workbook contents per sheet:</strong></p><ul><li><strong>N°</strong> — Official change entry number</li><li><strong>Section Ref</strong> — IG section or index reference</li><li><strong>Element / Index Ref</strong> — Specific field or element affected</li><li><strong>Dataset / Message</strong> — Which message/dataset (pacs.008, camt.056 etc.) this change belongs to</li><li><strong>Change Type</strong> — 🟠 CHAN / 🔵 CLAR / 🟡 TYPO with colour coding</li><li><strong>Description of Change</strong> — Full text from the IG change list</li><li><strong>Business Note & Implementation Guidance</strong> — Plain-English note on what action is needed</li></ul>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Official Source</div><div class="guide-benefit-text">Extracts directly from the IG PDF change list — no manual copying</div></div><div class="guide-benefit"><div class="guide-benefit-title">Categorised</div><div class="guide-benefit-text">CHAN / CLAR / TYPO with colour coding — instantly filter what needs attention</div></div><div class="guide-benefit"><div class="guide-benefit-title">Business Notes</div><div class="guide-benefit-text">Auto-generated implementation guidance per entry — mandatory, optional, blocked, length changes</div></div><div class="guide-benefit"><div class="guide-benefit-title">Dataset Grouped</div><div class="guide-benefit-text">Changes grouped by message/dataset (pacs.008, camt.056 etc.) for easy navigation</div></div></div>'
                }
            }
            ,
            {
                id: 'ig_mapping', icon: '🗂️', title: 'IG to Mapping Template', badge: 'New',
                description: 'Takes an IG Extractor Excel output and generates a pre-filled implementation mapping workbook — one sheet per message, 21 columns, colour-coded by field status, with dropdown Impl Status tracking.',
                features: ['🟡 Mandatory fields pre-identified', '⬜ Optional fields included', '🟢 8 implementation columns ready to fill', '📋 Impl Status dropdown: TODO / IN PROGRESS / DONE'],
                input: 'Upload 1 IG Extractor Excel (.xlsx) output', minFiles: 1,
                options: [
                    { type: 'text', id: 'scheme_label', label: 'Scheme Label (e.g. EPC, NPC)', placeholder: 'e.g. EPC' },
                    { type: 'text', id: 'version', label: 'Version (e.g. 2025 v1.0)', placeholder: 'e.g. 2025 v1.0' },
                    { type: 'select', id: 'filter_mode', label: 'Field Filter', options: [
                        { value: 'all', label: 'All fields (mandatory + optional + not permitted)' },
                        { value: 'exclude_notperm', label: 'Exclude Not Permitted fields' },
                        { value: 'mandatory', label: 'Mandatory fields only (smaller, focused)' }
                    ]}
                ],
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use IG to Mapping Template when you need to:</p><ul><li>Start a new ISO 20022 message implementation — get a structured mapping document instantly rather than building from scratch</li><li>Hand off a mapping task to developers — they get all IG context (rules, lengths, ISO definitions) plus blank implementation columns to fill in</li><li>Create a project deliverable showing field-level mapping between your source system and the ISO 20022 message</li><li>Track implementation progress field by field using the built-in Impl Status column</li></ul><p style="margin-top:10px;"><strong>Tip:</strong> Run the Rulebook IG Extractor first, download the output, then upload it here. This tool works best with IG Extractor output that has proper yellow/white/red colour coding.</p>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Run the <strong>Rulebook IG Extractor</strong> on your target IG PDF to get a colour-coded Excel. Download it.</p><p><strong>Step 2:</strong> Upload that Excel here. Enter a scheme label (EPC / NPC) and version string. Choose a field filter if needed.</p><p><strong>Step 3:</strong> Download the Mapping Template Excel. Open it and start filling in the green Implementation columns.</p><p><strong>Implementation columns to fill in:</strong></p><ul><li><strong>Source System</strong> — which system provides this field (e.g. Core Banking, CRM, Generated)</li><li><strong>Source Field</strong> — the actual field name or column in your source system</li><li><strong>Transformation</strong> — any mapping logic, format conversion, or lookup needed</li><li><strong>Default Value</strong> — for hardcoded fields (e.g. ChrgBr=SLEV, Ccy=EUR)</li><li><strong>Impl Status</strong> — dropdown: TODO / IN PROGRESS / DONE / N/A / BLOCKED</li></ul>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">Mapping_Template.xlsx</span><span class="output-file-desc">— Pre-filled implementation mapping workbook</span></div></div><p style="margin-top:12px;"><strong>Workbook structure:</strong></p><ul><li><strong>Summary sheet</strong> — field counts per message, implementation guide</li><li><strong>One sheet per message</strong> — 21 columns, colour-coded by field status</li></ul><p><strong>Column groups:</strong> 13 pre-filled IG Reference columns (Status, Index, XML Tag, Element Name, XPath, Multiplicity, Data Type, Length, Usage Rule, Rulebook Ref, Format Rule, Code Values, ISO Definition) + 8 blank Implementation columns (Source System, Source Field, Transformation, Default Value, Validation Rule, Dev Owner, Impl Status, Notes)</p>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Saves 2–3 Hours</div><div class="guide-benefit-text">No manual copy-paste from the IG PDF — all field metadata pre-populated</div></div><div class="guide-benefit"><div class="guide-benefit-title">Mandatory Fields First</div><div class="guide-benefit-text">🟡 Yellow rows are immediately visible — team knows exactly what must be mapped</div></div><div class="guide-benefit"><div class="guide-benefit-title">Progress Tracking</div><div class="guide-benefit-text">Built-in Impl Status dropdown (TODO / IN PROGRESS / DONE) — filter column T to see what\'s left</div></div><div class="guide-benefit"><div class="guide-benefit-title">Ready to Share</div><div class="guide-benefit-text">Formatted workbook with ISO definitions included — share with developers, business analysts, or auditors</div></div></div>'
                }
            },
            {
                id: 'ig_mapping_xsd', icon: '🔗', title: 'IG Mapping (XSD-Enriched)', badge: 'New',
                description: 'Combines an IG Extractor Excel with the originating XSD to produce a richer mapping template — adds XSD-derived data types, restrictions, min/max occurs, and pattern constraints alongside every IG field.',
                features: ['📐 XSD data types & restrictions', '🔢 minOccurs / maxOccurs', '🟡 IG colour coding preserved', '📋 Impl Status tracking'],
                input: 'Upload 1 IG Excel (.xlsx) + 1 XSD file', minFiles: 2,
                options: [
                    { type: 'text', id: 'scheme_label', label: 'Scheme Label (e.g. EPC, NPC)', placeholder: 'e.g. EPC' },
                    { type: 'text', id: 'version', label: 'Version (e.g. 2025 v1.0)', placeholder: 'e.g. 2025 v1.0' },
                    { type: 'select', id: 'filter_mode', label: 'Field Filter', options: [
                        { value: 'all', label: 'All fields (mandatory + optional + not permitted)' },
                        { value: 'exclude_notperm', label: 'Exclude Not Permitted fields' },
                        { value: 'mandatory', label: 'Mandatory fields only' }
                    ]}
                ],
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use IG Mapping (XSD-Enriched) when you need to:</p><ul><li>Build a mapping template that shows both the IG business rules <strong>and</strong> the XSD technical constraints side-by-side</li><li>Validate that your implementation respects both the IG colour-coded rules and the underlying schema restrictions (patterns, enumerations, maxLength)</li><li>Give developers a single sheet with everything — XPath, ISO length, XSD type, allowed patterns, and implementation columns</li><li>Produce a more technically complete deliverable than the standard IG Mapping Template</li></ul>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Run the <strong>Rulebook IG Extractor</strong> on your IG PDF to get the colour-coded Excel.</p><p><strong>Step 2:</strong> Upload that Excel <strong>and</strong> the corresponding XSD file (e.g. pacs_008_001_08.xsd) together.</p><p><strong>Step 3:</strong> Set a Scheme Label and Version, choose a field filter, then click <strong>Run Tool</strong>.</p><p><strong>Step 4:</strong> Download the enriched mapping workbook. The extra XSD columns appear after the standard IG Reference columns.</p>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">Mapping_XSD.xlsx</span><span class="output-file-desc">— XSD-enriched implementation mapping workbook</span></div></div><p style="margin-top:12px;"><strong>Additional XSD columns:</strong> XSD Type, Base Type, Min Length, Max Length, Pattern, Enumeration Values, minOccurs, maxOccurs — all resolved from the schema registry.</p>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Technical + Business in One Sheet</div><div class="guide-benefit-text">IG colour rules and XSD constraints combined — no cross-referencing between two documents</div></div><div class="guide-benefit"><div class="guide-benefit-title">Schema-Accurate Types</div><div class="guide-benefit-text">XSD-derived data types and patterns catch implementation errors early</div></div><div class="guide-benefit"><div class="guide-benefit-title">Developer Ready</div><div class="guide-benefit-text">Developers get exact field constraints without reading the XSD manually</div></div></div>'
                }
            },
            {
                id: 'xsd_ig_analysis', icon: '🔍', title: 'XSD vs IG Analyser', badge: 'New',
                description: 'Cross-references every element in an XSD schema against an IG Excel to detect status mismatches, fields present in XSD but missing from the IG, and alignment discrepancies between schema cardinality and IG usage rules.',
                features: ['✅ Aligned fields', '⚠️ Status mismatches (XSD vs IG)', '❌ XSD-only elements missing from IG', '📊 Summary dashboard'],
                input: 'Upload 1 XSD file + 1 IG Excel (.xlsx)', minFiles: 2,
                options: [
                    { type: 'text', id: 'scheme_label', label: 'Scheme Label (e.g. EPC, NPC)', placeholder: 'e.g. EPC' },
                    { type: 'text', id: 'version', label: 'Version', placeholder: 'e.g. RB25' },
                    { type: 'text', id: 'message_sheet', label: 'IG Sheet name to analyse (optional)', placeholder: 'e.g. pacs_008_001_08  — leave blank for first sheet' }
                ],
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use XSD vs IG Analyser when you need to:</p><ul><li>Validate a new rulebook IG release against its XSD — find fields the IG forgot to document</li><li>Compare EPC vs NPC IG field status against the same shared XSD</li><li>Audit an existing IG for completeness — every XSD element should appear in the IG</li><li>Detect STATUS_DIFF cases where the XSD says optional but the IG says mandatory (or vice versa)</li></ul>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload the XSD file (e.g. pacs_008_001_08.xsd) and the corresponding IG Extractor Excel together.</p><p><strong>Step 2:</strong> Optionally specify the IG sheet name to analyse (leave blank to use the first sheet).</p><p><strong>Step 3:</strong> Click <strong>Run Tool</strong>. The analyser cross-references every XSD path against the IG rows.</p><p><strong>Step 4:</strong> Review the output — ALIGNED rows are correct; STATUS_DIFF rows need investigation; XSD_ONLY rows are missing from the IG.</p>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">{xsd_name}_XSD_IG_Analysis.xlsx</span><span class="output-file-desc">— Cross-reference analysis workbook</span></div></div><p style="margin-top:12px;"><strong>Result categories:</strong></p><ul><li><strong>ALIGNED</strong> — XSD and IG agree on field status</li><li><strong>STATUS_DIFF</strong> — Status differs between XSD cardinality and IG colour</li><li><strong>XSD_ONLY</strong> — Element in XSD but not documented in the IG</li><li><strong>IG_ONLY</strong> — Row in IG but no matching XSD element</li></ul>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">IG Completeness Audit</div><div class="guide-benefit-text">Instantly see if any XSD elements are missing from the IG documentation</div></div><div class="guide-benefit"><div class="guide-benefit-title">Catch Rule Conflicts Early</div><div class="guide-benefit-text">STATUS_DIFF rows flag contradictions between schema and business rules before implementation</div></div><div class="guide-benefit"><div class="guide-benefit-title">EPC vs NPC Comparison</div><div class="guide-benefit-text">Run twice with EPC and NPC IGs against the same XSD to see where they diverge</div></div></div>'
                }
            }
        ];


        // (stale xsdTools fragment removed)

        let currentPdfTool = null, uploadedPdfFiles = [];

        function renderPdfToolsGrid() {
            document.getElementById('pdfToolsGrid').innerHTML = pdfTools.map(t => `
                <div class="tool-card" onclick="openPdfTool('${t.id}')">
                    <div class="tool-card-header"><div class="tool-card-icon" style="background:linear-gradient(135deg,#ef4444 0%,#f97316 100%);">${t.icon}</div><div><span class="tool-card-title">${t.title}</span>${t.badge ? `<span class="tool-card-badge">${t.badge}</span>` : ''}</div></div>
                    <p class="tool-card-description">${t.description}</p>
                    <div class="tool-card-features">${t.features.map(f => `<div class="tool-card-feature">${f}</div>`).join('')}</div>
                    <div class="tool-card-input">📁 ${t.input}</div>
                    <div class="tool-card-arrow">→</div>
                </div>
            `).join('');
        }

        function renderRulebookToolsGrid() {
            document.getElementById('rulebookToolsGrid').innerHTML = rulebookTools.map(t => `
                <div class="tool-card" onclick="openRbTool('${t.id}')">
                    <div class="tool-card-header"><div class="tool-card-icon" style="background:linear-gradient(135deg,#0ea5e9 0%,#6366f1 100%);">${t.icon}</div><div><span class="tool-card-title">${t.title}</span>${t.badge ? `<span class="tool-card-badge">${t.badge}</span>` : ''}</div></div>
                    <p class="tool-card-description">${t.description}</p>
                    <div class="tool-card-features">${t.features.map(f => `<div class="tool-card-feature">${f}</div>`).join('')}</div>
                    <div class="tool-card-input">📁 ${t.input}</div>
                    <div class="tool-card-arrow">→</div>
                </div>
            `).join('');
        }

        function openPdfTool(toolId) {
            const tool = pdfTools.find(t => t.id === toolId);
            if (!tool) return;
            currentPdfTool = tool;
            uploadedPdfFiles = [];
            _splitTotalPages = 0;   // reset page-count from previous session
            _igSections = [];       // reset section list from previous session
            pdfFileInput.value = ''; // clear so same file can be re-uploaded
            document.getElementById('pdfToolPageIcon').textContent = tool.icon;
            document.getElementById('pdfToolPageTitle').textContent = tool.title;
            document.getElementById('pdfUploadHint').textContent = '— ' + tool.input;
            document.getElementById('pdfFileList').innerHTML = '';
            document.getElementById('pdfResultsSection').classList.remove('active');
            hidePdfMessage();

            document.getElementById('guide-pdf-when').innerHTML = tool.guide.when;
            document.getElementById('guide-pdf-how').innerHTML = tool.guide.how;
            document.getElementById('guide-pdf-output').innerHTML = tool.guide.output;
            document.getElementById('guide-pdf-benefits').innerHTML = tool.guide.benefits;
            document.querySelectorAll('#page-pdf-tool .guide-tab').forEach((t,i) => t.classList.toggle('active', i===0));
            document.querySelectorAll('#page-pdf-tool .guide-content').forEach((c,i) => c.classList.toggle('active', i===0));

            const optCard = document.getElementById('pdfOptionsCard');
            const optContent = document.getElementById('pdfOptionsContent');
            if (tool.options?.length) {
                optCard.style.display = 'block';
                optContent.innerHTML = tool.options.map(o => {
                    if (o.type === 'info') return `<div class="option-group" id="pdf_${o.id}_wrap" style="display:none;"><div id="pdf_${o.id}" style="background:#f0f7ff;border:1px solid #bbd4f5;border-radius:6px;padding:10px 14px;font-size:13px;color:#1e4a8a;"></div></div>`;
                    if (o.type === 'ig_section_picker') return `
                        <div class="option-group" id="pdf_ig_section_picker_wrap">
                          <label class="option-label">Extract sections</label>
                          <button type="button" class="option-btn-detect" onclick="detectIGSections()" id="igDetectBtn" style="margin-bottom:8px;padding:7px 16px;background:#2E74B5;color:#fff;border:none;border-radius:6px;font-size:13px;cursor:pointer;">
                            🔍 Detect Sections in PDF
                          </button>
                          <div id="igSectionList" style="display:none;margin-top:8px;border:1px solid #bbd4f5;border-radius:8px;overflow:hidden;background:#f8fbff;"></div>
                          <div id="igSectionNote" style="font-size:11px;color:#888;margin-top:6px;">
                            Tip: Leave all unchecked to extract every section in the IG.
                          </div>
                        </div>`;
                    if (o.type === 'text') return `<div class="option-group"><label class="option-label">${o.label}</label><input type="text" class="option-input" id="pdf_${o.id}" placeholder="${o.placeholder||''}"></div>`;
                    if (o.type === 'number') return `<div class="option-group"><label class="option-label">${o.label}</label><input type="number" class="option-input" id="pdf_${o.id}" value="${o.value||10}" min="${o.min||1}" max="${o.max||500}" oninput="updateSplitPreview()"></div>`;
                    if (o.type === 'select') return `<div class="option-group"><label class="option-label">${o.label}</label><select class="option-select" id="pdf_${o.id}" onchange="updateSplitPreview()">${o.options.map(x=>`<option value="${x.value}">${x.label}</option>`).join('')}</select></div>`;
                    return '';
                }).join('');
            } else { optCard.style.display = 'none'; }

            updatePdfRunButton();
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById('page-pdf-tool').classList.add('active');
        }

        // ─── Rulebook Tool Functions ──────────────────────────────────────────
        let currentRbTool = null, uploadedRbFiles = [];

        function openRbTool(toolId) {
            const tool = rulebookTools.find(t => t.id === toolId);
            if (!tool) return;
            currentRbTool = tool;
            uploadedRbFiles = [];
            document.getElementById('rbFileInput').value = '';
            document.getElementById('rulebookToolPageIcon').textContent = tool.icon;
            document.getElementById('rulebookToolPageTitle').textContent = tool.title;
            document.getElementById('rbUploadHint').textContent = '— ' + tool.input;
            document.getElementById('rbFileList').innerHTML = '';
            document.getElementById('rbResultsSection').classList.remove('active');
            document.getElementById('rbMessageBox').innerHTML = '';
            document.getElementById('rbMessageBox').style.display = 'none';

            // Accept filter based on tool
            const rbInput = document.getElementById('rbFileInput');
            if (['ig_extract', 'ig_diff', 'ig_change_tracker', 'rulebook_changes'].includes(toolId)) {
                rbInput.accept = '.pdf';
                document.getElementById('rbUploadSubtitle').textContent = 'Supports .pdf files';
            } else if (toolId === 'xsd_ig_analysis') {
                rbInput.accept = '.xsd,.xlsx,.xlsm';
                document.getElementById('rbUploadSubtitle').textContent = 'Upload 1 XSD + 1 Excel (.xsd, .xlsx)';
            } else {
                rbInput.accept = '.xlsx,.xlsm,.xsd';
                document.getElementById('rbUploadSubtitle').textContent = 'Supports Excel and XSD files';
            }

            document.getElementById('guide-rb-when').innerHTML = tool.guide.when;
            document.getElementById('guide-rb-how').innerHTML = tool.guide.how;
            document.getElementById('guide-rb-output').innerHTML = tool.guide.output;
            document.getElementById('guide-rb-benefits').innerHTML = tool.guide.benefits;
            document.querySelectorAll('#page-rulebook-tool .guide-tab').forEach((t,i) => t.classList.toggle('active', i===0));
            document.querySelectorAll('#page-rulebook-tool .guide-content').forEach((c,i) => c.classList.toggle('active', i===0));

            const optCard = document.getElementById('rbOptionsCard');
            const optContent = document.getElementById('rbOptionsContent');
            if (tool.options?.length) {
                optCard.style.display = 'block';
                optContent.innerHTML = tool.options.map(o => {
                    if (o.type === 'info') return `<div class="option-group" id="rb_${o.id}_wrap" style="display:none;"><div id="rb_${o.id}" style="background:#f0f7ff;border:1px solid #bbd4f5;border-radius:6px;padding:10px 14px;font-size:13px;color:#1e4a8a;"></div></div>`;
                    if (o.type === 'ig_section_picker') return `
                        <div class="option-group" id="rb_ig_section_picker_wrap">
                          <label class="option-label" style="margin-bottom:6px;display:block;">📋 Message Sections <span style="font-weight:400;color:#888;font-size:11px;">(auto-detected on upload)</span></label>
                          <div id="rbIgSectionList" style="display:none;margin-bottom:8px;border:1px solid #bbd4f5;border-radius:8px;overflow:hidden;background:#f8fbff;"></div>
                          <button type="button" onclick="detectRbIGSections()" id="rbIgDetectBtn" style="padding:5px 12px;background:#f0f7ff;color:#0ea5e9;border:1px solid #bbd4f5;border-radius:6px;font-size:12px;cursor:pointer;">
                            🔄 Re-scan PDF
                          </button>
                          <div id="rbIgSectionNote" style="font-size:11px;color:#888;margin-top:6px;">Sections detected automatically. Tick the ones to extract, or leave all unchecked to extract everything.</div>
                        </div>`;
                    if (o.type === 'text') return `<div class="option-group"><label class="option-label">${o.label}</label><input type="text" class="option-input" id="rb_${o.id}" placeholder="${o.placeholder||''}"></div>`;
                    if (o.type === 'select') return `<div class="option-group"><label class="option-label">${o.label}</label><select class="option-select" id="rb_${o.id}">${o.options.map(x=>`<option value="${x.value}">${x.label}</option>`).join('')}</select></div>`;
                    return '';
                }).join('');
            } else { optCard.style.display = 'none'; }

            updateRbRunButton();
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById('page-rulebook-tool').classList.add('active');
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.querySelector('.nav-item[data-page="rulebook-tools"]')?.classList.add('active');
        }

        function updateRbRunButton() {
            const t = currentRbTool;
            if (!t) return;
            const btn = document.getElementById('runRbToolBtn');
            let needed = t.requiredFiles || 1;
            btn.disabled = uploadedRbFiles.length < needed;
        }

        function resetRbTool() {
            uploadedRbFiles = [];
            document.getElementById('rbFileInput').value = '';
            document.getElementById('rbFileList').innerHTML = '';
            document.getElementById('rbResultsSection').classList.remove('active');
            document.getElementById('rbMessageBox').innerHTML = '';
            document.getElementById('rbMessageBox').style.display = 'none';
            updateRbRunButton();
        }

        function showRbMessage(msg, type='error') {
            const box = document.getElementById('rbMessageBox');
            box.textContent = msg;
            box.className = 'message ' + type;
            box.style.display = 'block';
        }

        function hideRbMessage() {
            const box = document.getElementById('rbMessageBox');
            box.style.display = 'none';
        }

        // RB file upload — events handled by _fspInitPanel('rb') on DOMContentLoaded
        const rbFileInput = document.getElementById('rbFileInput');

        function _rbMaybeAutoDetect() {
            if (!currentRbTool || currentRbTool.id !== 'ig_extract') return;
            const hasPdf = uploadedRbFiles.some(f => f.name && f.name.toLowerCase().endsWith('.pdf'));
            if (!hasPdf) return;
            // Small delay to ensure openRbTool has rendered the options DOM
            setTimeout(detectRbIGSections, 80);
        }

        function handleRbFiles(files) {
            Array.from(files).forEach(f => {
                if (!uploadedRbFiles.find(u => u.name === f.name)) uploadedRbFiles.push(f);
            });
            renderRbFileList();
            updateRbRunButton();
            // Auto-detect sections when a PDF is added to ig_extract
            _rbMaybeAutoDetect();
        }

        // renderRbFileList v1 removed → FSP

        // removeRbFile → FSP

        async function runRbTool() {
            if (!currentRbTool || uploadedRbFiles.length === 0) return;
            hideRbMessage();
            document.getElementById('rbResultsSection').classList.remove('active');
            document.getElementById('loadingOverlay').style.display = 'flex';
            document.getElementById('loadingSubtext').textContent = 'Running ' + currentRbTool.title + '...';

            // Build FormData: real File objects as 'files', library paths as JSON
            const fd = new FormData();
            fd.append('tool', currentRbTool.id);
            const rbLibPaths = [];
            uploadedRbFiles.forEach(f => {
                if (f._isLib) rbLibPaths.push(f._libPath);
                else fd.append('files', f);
            });
            if (rbLibPaths.length) fd.append('library_files', JSON.stringify(rbLibPaths));

            // Append options
            if (currentRbTool.options) {
                currentRbTool.options.forEach(o => {
                    if (o.type === 'text' || o.type === 'select') {
                        const el = document.getElementById('rb_' + o.id);
                        if (el) fd.append(o.id, el.value || '');
                    }
                    if (o.type === 'ig_section_picker') {
                        const checked = document.querySelectorAll('#rbIgSectionList input[type=checkbox]:checked');
                        if (checked.length > 0) fd.append('sections', Array.from(checked).map(c => c.value).join(','));
                    }
                });
            }

            try {
                const res = await fetch('/run', { method: 'POST', body: fd });
                const data = await res.json();
                document.getElementById('loadingOverlay').style.display = 'none';
                if (data.success) {
                    document.getElementById('rbResultsSubtitle').textContent = data.message || 'Complete';
                    document.getElementById('rbResultsFiles').innerHTML = (data.files || []).map(f => `
                        <li class="results-file-item">
                            <span class="results-file-icon">📊</span>
                            <span class="results-file-name">${f.name}</span>
                            <a href="/download/${f.name}" class="results-download-btn" download>⬇ Download</a>
                        </li>`).join('');
                    document.getElementById('rbResultsSection').classList.add('active');
                } else {
                    showRbMessage('Error: ' + (data.error || 'Unknown error'), 'error');
                }
            } catch(e) {
                document.getElementById('loadingOverlay').style.display = 'none';
                showRbMessage('Network error: ' + e.message, 'error');
            }
        }

        async function detectRbIGSections() {
            const pdfFiles = uploadedRbFiles.filter(f => f.name && f.name.toLowerCase().endsWith('.pdf'));
            if (pdfFiles.length === 0) return;  // silently skip if no PDF yet

            const btn      = document.getElementById('rbIgDetectBtn');
            const list     = document.getElementById('rbIgSectionList');
            const note     = document.getElementById('rbIgSectionNote');
            if (!btn || !list) return;

            // ── Show progress bar ──────────────────────────────────────────────
            btn.disabled = true;
            list.style.display = 'block';
            list.innerHTML = `
                <div style="padding:14px 16px;">
                    <div style="font-size:12px;color:#555;margin-bottom:8px;">
                        📄 Scanning <strong>${pdfFiles[0].name || 'PDF'}</strong> for message sections…
                    </div>
                    <div style="background:#e2e8f0;border-radius:99px;height:8px;overflow:hidden;">
                        <div id="rbSectionProgressBar" style="height:100%;width:0%;background:linear-gradient(90deg,#0ea5e9,#6366f1);border-radius:99px;transition:width 0.3s ease;"></div>
                    </div>
                    <div id="rbSectionProgressLabel" style="font-size:11px;color:#888;margin-top:6px;">Starting…</div>
                </div>`;

            // Animate progress bar to give feedback while waiting
            const bar   = document.getElementById('rbSectionProgressBar');
            const label = document.getElementById('rbSectionProgressLabel');
            const steps = [
                [15, 'Reading PDF pages…'],
                [40, 'Extracting text…'],
                [70, 'Scanning for section headings…'],
                [90, 'Almost done…'],
            ];
            let stepIdx = 0;
            const ticker = setInterval(() => {
                if (stepIdx < steps.length) {
                    const [pct, msg] = steps[stepIdx++];
                    if (bar)   bar.style.width   = pct + '%';
                    if (label) label.textContent = msg;
                }
            }, 600);

            // ── Send to backend ────────────────────────────────────────────────
            const fd = new FormData();
            pdfFiles.forEach(f => {
                if (f._isLib) fd.append('library_path', f._libPath);
                else fd.append('files', f);
            });

            try {
                const res  = await fetch('/detect_ig_sections', { method: 'POST', body: fd });
                const data = await res.json();

                clearInterval(ticker);
                btn.disabled = false;

                if (data.sections && data.sections.length > 0) {
                    // ── Complete progress bar then show sections ───────────────
                    if (bar)   bar.style.width   = '100%';
                    if (label) label.textContent  = `Found ${data.sections.length} section(s)`;
                    await new Promise(r => setTimeout(r, 300));   // brief "done" flash

                    list.innerHTML = data.sections.map(s => `
                        <label class="ig-section-row" style="display:flex;align-items:center;gap:10px;padding:9px 14px;border-bottom:1px solid #e2eaf5;cursor:pointer;user-select:none;" onmouseover="this.style.background='#f0f7ff'" onmouseout="this.style.background=''">
                            <input type="checkbox" value="${s.id}" style="width:15px;height:15px;flex-shrink:0;cursor:pointer;">
                            <span style="font-weight:600;font-size:13px;min-width:60px;color:#1e4a8a;">${s.id}</span>
                            <span style="font-size:12px;color:#374151;flex:1;">${s.label}</span>
                            <span style="font-size:11px;color:#0ea5e9;font-weight:600;">${s.title || ''}</span>
                            <span style="font-size:11px;color:#888;white-space:nowrap;margin-left:8px;">p.${s.page_start}–${s.page_end}</span>
                        </label>`).join('');

                    if (note) note.textContent = `${data.sections.length} section(s) detected — tick the ones to extract, or leave all unchecked to extract everything.`;
                    hideRbMessage();

                } else if (data.error) {
                    list.style.display = 'none';
                    showRbMessage('Section detection error: ' + data.error, 'error');
                } else {
                    list.style.display = 'none';
                    if (note) note.textContent = 'No named sections found — the tool will extract all content automatically.';
                }

            } catch (e) {
                clearInterval(ticker);
                btn.disabled = false;
                list.style.display = 'none';
                showRbMessage('Detection failed: ' + e.message, 'error');
            }
        }



        // PDF file upload — events handled by _fspInitPanel('pdf') on DOMContentLoaded
        const pdfFileInput = document.getElementById('pdfFileInput');

        function handlePdfFiles(files) {
            const valid = Array.from(files).filter(f => /\.pdf$/i.test(f.name));
            if (!valid.length) { showPdfMessage('Please select .pdf files', 'error'); return; }
            valid.forEach(f => { if (!uploadedPdfFiles.find(u => u.name === f.name)) uploadedPdfFiles.push(f); });
            renderPdfFileList();
            updatePdfRunButton();
            // Side-effects for specific tools
            if (currentPdfTool?.id === 'pdf_split' && uploadedPdfFiles.length > 0) {
                fetchPdfPageCount(uploadedPdfFiles[0]);
            }
            if (currentPdfTool?.id === 'ig_extract') {
                autoDetectIGSections();
            }
        }

        // renderPdfFileList v1 removed → FSP
        // removePdfFile → FSP
        function updatePdfRunButton() { document.getElementById('runPdfToolBtn').disabled = !(currentPdfTool && uploadedPdfFiles.length >= currentPdfTool.minFiles); }

        let _splitTotalPages = 0;

        function fetchPdfPageCount(fileOrLibMock) {
            const fd = new FormData();
            if (fileOrLibMock._isLib) {
                fd.append('library_path', fileOrLibMock._libPath);
            } else {
                fd.append('files', fileOrLibMock);
            }
            fetch('/page_count', { method: 'POST', body: fd })
            .then(r => r.json())
            .then(d => {
                if (d.pages) {
                    _splitTotalPages = d.pages;
                    const infoEl = document.getElementById('pdf_page_count_info');
                    const wrapEl = document.getElementById('pdf_page_count_info_wrap');
                    if (infoEl && wrapEl) {
                        wrapEl.style.display = 'block';
                        updateSplitPreview();
                    }
                }
            }).catch(() => {});
        }

        function updateSplitPreview() {
            const infoEl = document.getElementById('pdf_page_count_info');
            if (!infoEl || !_splitTotalPages) return;
            const mode = document.getElementById('pdf_split_mode')?.value || 'chunks';
            if (mode === 'chunks') {
                const size = parseInt(document.getElementById('pdf_chunk_size')?.value || 10);
                const numFiles = Math.ceil(_splitTotalPages / size);
                infoEl.innerHTML = `📄 <strong>${_splitTotalPages} pages</strong> total &nbsp;·&nbsp; ${size} pages per chunk &nbsp;→&nbsp; <strong>${numFiles} file${numFiles===1?'':'s'}</strong> will be created`;
            } else {
                infoEl.innerHTML = `📄 <strong>${_splitTotalPages} pages</strong> total &nbsp;·&nbsp; Enter page ranges below (e.g. 1-5, 8, 10-38)`;
            }
        }

        function runPdfTool() {
            if (!currentPdfTool) return;
            const opts = {};

            // ── Step 1: collect regular inputs ───────────────────────────────
            currentPdfTool.options?.forEach(o => {
                if (o.type === 'ig_section_picker') return; // handled separately below
                const el = document.getElementById('pdf_' + o.id);
                if (!el) return;
                if (o.id === 'filter_messages') {
                    // Split comma-separated IDs into array; support partial IDs (pacs.008)
                    opts['filter_messages'] = el.value ? el.value.split(',').map(s => s.trim()).filter(Boolean) : [];
                } else if (o.id === 'filter_sections') {
                    // Only use text box value if the section picker has NO checked boxes
                    // (picker takes priority — text box is the fallback)
                    const pickerChecked = document.querySelectorAll('.ig-section-check:checked');
                    if (pickerChecked.length === 0) {
                        opts['filter_sections'] = el.value ? el.value.split(',').map(s => s.trim()).filter(Boolean) : [];
                    }
                } else {
                    opts[o.id] = el.value;
                }
            });

            // ── Step 2: section picker checkboxes (highest priority) ─────────
            const checkedBoxes = document.querySelectorAll('.ig-section-check:checked');
            if (checkedBoxes.length > 0) {
                opts['filter_sections'] = Array.from(checkedBoxes).map(c => c.dataset.section);
            }
            showLoading('Running ' + currentPdfTool.title + '...');
            // Build FormData: real File objects go as 'files', library paths as JSON
            const pdfFd = new FormData();
            pdfFd.append('tool', currentPdfTool.id);
            const pdfLibPaths = [];
            uploadedPdfFiles.forEach(f => {
                if (f._isLib) pdfLibPaths.push(f._libPath);
                else pdfFd.append('files', f);
            });
            if (pdfLibPaths.length) pdfFd.append('library_files', JSON.stringify(pdfLibPaths));
            // Append opts as individual form fields
            Object.entries(opts).forEach(([k, v]) => {
                if (Array.isArray(v)) pdfFd.append(k, JSON.stringify(v));
                else if (v !== undefined && v !== null) pdfFd.append(k, v);
            });
            fetch('/run', { method: 'POST', body: pdfFd })
            .then(r => r.json())
            .then(d => {
                hideLoading();
                if (d.success) showPdfResults(d.files ? d.files.map(f => f.name || f) : [], d.message || 'Complete!');
                else showPdfMessage(d.error || 'Tool failed', 'error');
            })
            .catch(e => { hideLoading(); showPdfMessage('Error: ' + e.message, 'error'); });
        }

        function showPdfResults(files, msg) {
            document.getElementById('pdfResultsSubtitle').textContent = msg;
            document.getElementById('pdfResultsFiles').innerHTML = files.map(f => `
                <li class="results-file"><span class="results-file-icon">${getIcon(f)}</span><span class="results-file-name">${f}</span>
                <div class="results-file-actions">${/\.html$/i.test(f)?`<a href="/preview/${f}" target="_blank" class="results-file-btn preview">Preview</a>`:''}<a href="/download/${f}" class="results-file-btn download">Download</a></div></li>
            `).join('');
            document.getElementById('pdfResultsSection').classList.add('active');
            showPdfMessage(msg, 'success');
        }

        function resetPdfTool() { uploadedPdfFiles=[]; renderPdfFileList(); updatePdfRunButton(); document.getElementById('pdfResultsSection').classList.remove('active'); hidePdfMessage(); pdfFileInput.value=''; }
        function showPdfMessage(t, type) { const b=document.getElementById('pdfMessageBox'); b.textContent=t; b.className='message active '+type; }
        function hidePdfMessage() { document.getElementById('pdfMessageBox').className='message'; }

        // Extend showPage to render PDF grid
        const _origShowPage = showPage;
        showPage = function(pageId) {
            _origShowPage(pageId);
        };


        // ── IG Section Picker ──────────────────────────────────────────────────────
        let _igSections = [];

        function autoDetectIGSections() {
            if (uploadedPdfFiles.length === 0) return;
            detectIGSections();
        }

        function detectIGSections() {
            const listEl = document.getElementById('igSectionList');
            const detectBtn = document.getElementById('igDetectBtn');
            if (!listEl || uploadedPdfFiles.length === 0) {
                if (!uploadedPdfFiles.length) showPdfMessage('Upload a PDF first, then detect sections.', 'error');
                return;
            }
            detectBtn.textContent = '⏳ Detecting...';
            detectBtn.disabled = true;
            listEl.innerHTML = '';
            listEl.style.display = 'none';

            const fd = new FormData();
            uploadedPdfFiles.forEach(f => {
                if (f._isLib) fd.append('library_path', f._libPath);
                else fd.append('files', f);
            });

            fetch('/detect_ig_sections', { method: 'POST', body: fd })
            .then(r => r.json())
            .then(d => {
                detectBtn.textContent = '🔍 Detect Sections in PDF';
                detectBtn.disabled = false;
                if (!d.success) { showPdfMessage('Section detection failed: ' + (d.error||''), 'error'); return; }
                _igSections = d.sections || [];
                renderIGSectionList();
            })
            .catch(() => {
                detectBtn.textContent = '🔍 Detect Sections in PDF';
                detectBtn.disabled = false;
                showPdfMessage('Section detection failed — network error', 'error');
            });
        }

        function renderIGSectionList() {
            const listEl = document.getElementById('igSectionList');
            const noteEl = document.getElementById('igSectionNote');
            if (!_igSections.length) {
                listEl.innerHTML = '<div style="padding:12px 16px;color:#888;font-size:13px;">No IG sections detected. Try running without a filter to extract all sections.</div>';
                listEl.style.display = 'block';
                return;
            }
            listEl.style.display = 'block';
            let html = '<div style="padding:8px 14px;background:#e8f0fb;border-bottom:1px solid #bbd4f5;display:flex;align-items:center;gap:12px;">'
                + '<span style="font-size:12px;font-weight:600;color:#1e4a8a;">' + _igSections.length + ' sections detected</span>'
                + '<button type="button" onclick="igCheckAll(true)" style="font-size:11px;padding:2px 8px;border:1px solid #2E74B5;border-radius:4px;background:#fff;color:#2E74B5;cursor:pointer;">All</button>'
                + '<button type="button" onclick="igCheckAll(false)" style="font-size:11px;padding:2px 8px;border:1px solid #aaa;border-radius:4px;background:#fff;color:#555;cursor:pointer;">None</button>'
                + '<span style="font-size:11px;color:#666;margin-left:auto;">&#9745; = will be extracted</span>'
                + '</div>';
            _igSections.forEach(function(s, i) {
                var bg = i % 2 === 0 ? '#fff' : '#f5f9ff';
                html += '<label class="ig-section-row" style="display:flex;align-items:flex-start;gap:10px;padding:8px 14px;cursor:pointer;border-bottom:1px solid #e8f0fb;background:' + bg + ';"'
                    + ' onmouseover="this.style.background=\'#ddeeff\'" onmouseout="this.style.background=\'' + bg + '\'">'
                    + '<input type="checkbox" class="ig-section-check" data-section="' + s.section + '" data-message="' + s.message + '" style="margin-top:3px;cursor:pointer;">'
                    + '<div>'
                    + '<div style="font-size:13px;font-weight:600;color:#1F3864;">' + s.section + ' \u2014 ' + s.label + '</div>'
                    + '<div style="font-size:11px;color:#555;margin-top:2px;">' + s.message + ' &nbsp;&middot;&nbsp; page ' + s.page + ' &nbsp;&middot;&nbsp; <span style="color:#888;font-size:10px;">' + s.file + '</span></div>'
                    + '</div>'
                    + '</label>';
            });
            listEl.innerHTML = html;
            if (noteEl) noteEl.textContent = 'Check sections to extract. Leave all unchecked to extract everything.';
        }

        function igCheckAll(state) {
            document.querySelectorAll('.ig-section-check').forEach(c => c.checked = state);
        }
        // ── End IG Section Picker ──────────────────────────────────────────────────

        renderToolsGrid();
    
        // ═══════════════════════════════════════════════════════
        // DOCUMENT LIBRARY
        // ═══════════════════════════════════════════════════════
        let _libTree = [];           // full tree from server
        let _libSelected = {};       // { path: fileNode }
        let _libPickerContext = null; // 'pdf' | 'rb'
        let _libPickerSel = {};      // { path: fileNode } inside picker modal
        let _libCurrentFolder = null; // folder node shown in picker right panel

        async function initLibrary() {
            if (_libTree.length) { renderLibTree(); return; }
            document.getElementById('libTreeScroll').innerHTML = '<div class="lib-empty-state">Loading…</div>';
            try {
                const res = await fetch('/library');
                const data = await res.json();
                _libTree = data.tree || [];
                renderLibTree();
            } catch(e) {
                document.getElementById('libTreeScroll').innerHTML = '<div class="lib-empty-state">⚠️ Could not load library</div>';
            }
        }

        function renderLibTree() {
            const el = document.getElementById('libTreeScroll');
            if (!_libTree.length) {
                el.innerHTML = '<div class="lib-empty-state">📂 Library is empty.<br><small>Add files to the <code>library/</code> folder.</small></div>';
                return;
            }
            el.innerHTML = _buildTreeHTML(_libTree, true);
        }

        // _buildTreeHTML v1 removed → extended version below

        function toggleLibFolder(row) {
            row.classList.toggle('open');
            const icon = row.querySelector('span:nth-child(2)');
            if (icon) icon.textContent = row.classList.contains('open') ? '📂' : '📁';
            const children = row.nextElementSibling;
            if (children) children.classList.toggle('open');
        }

        function toggleLibFile(el, path, node) {
            if (_libSelected[path]) {
                delete _libSelected[path];
                el.classList.remove('selected');
            } else {
                _libSelected[path] = node;
                el.classList.add('selected');
            }
            updateLibSelectionBar();
            showLibDetail(node);
        }

        function updateLibSelectionBar() {
            const keys = Object.keys(_libSelected);
            const bar  = document.getElementById('libSelectionBar');
            const tags = document.getElementById('libSelTags');
            const cnt  = document.getElementById('libSelCount');
            if (!keys.length) { bar.classList.add('hidden'); return; }
            bar.classList.remove('hidden');
            cnt.textContent = keys.length + (keys.length === 1 ? ' file selected' : ' files selected');
            tags.innerHTML = keys.map(p => {
                const n = _libSelected[p];
                return `<span class="lib-sel-tag">${n.icon} ${n.name}<span class="lib-sel-remove" onclick="deselLibFile('${p.replace(/'/g,"\'")}')">×</span></span>`;
            }).join('');
        }

        function deselLibFile(path) {
            delete _libSelected[path];
            // Remove selected class from tree row
            document.querySelectorAll('#libTreeScroll .lib-file-row.selected').forEach(el => {
                if (el.getAttribute('onclick')?.includes(path.replace(/'/g,"\'"))) el.classList.remove('selected');
            });
            updateLibSelectionBar();
        }

        function showLibDetail(node) {
            const TYPE_LABELS = {'.xsd':'XSD Schema','.xlsx':'Excel Workbook','.xlsm':'Excel Workbook','.pdf':'PDF Document','.xml':'XML File'};
            document.getElementById('libDetailPanel').innerHTML = `
                <div class="lib-detail-card">
                    <div class="lib-detail-name">${node.icon} ${node.name}</div>
                    <div class="lib-detail-path">${node.path}</div>
                    <div class="lib-detail-grid">
                        <div class="lib-detail-prop"><div class="lib-detail-prop-label">Type</div><div class="lib-detail-prop-value">${TYPE_LABELS[node.ext] || node.ext}</div></div>
                        <div class="lib-detail-prop"><div class="lib-detail-prop-label">Size</div><div class="lib-detail-prop-value">${node.size_kb} KB</div></div>
                        <div class="lib-detail-prop"><div class="lib-detail-prop-label">Extension</div><div class="lib-detail-prop-value">${node.ext}</div></div>
                        <div class="lib-detail-prop"><div class="lib-detail-prop-label">Location</div><div class="lib-detail-prop-value">${node.path.split('/').slice(0,-1).join(' › ')}</div></div>
                    </div>
                    <div style="margin-top:16px;">
                        <button class="lib-use-btn" onclick="quickSendToTool('${node.path.replace(/'/g,"\'")}')" style="font-size:12px;padding:6px 14px;">🚀 Open in Tool</button>
                    </div>
                </div>`;
        }

        // ── Send-to-tool modal ───────────────────────────────────────────────
        const ALL_TOOLS = [
            {id:'ig_extract',    label:'IG Extractor',          icon:'📋', panel:'rb', ext:['.pdf']},
            {id:'ig_diff',       label:'IG Diff',               icon:'⚖️', panel:'rb', ext:['.xlsx','.xlsm']},
            {id:'rulebook_changes',label:'Change Tracker',      icon:'📋', panel:'rb', ext:['.pdf']},
            {id:'ig_mapping',    label:'Mapping Template',      icon:'🗂️', panel:'rb', ext:['.xlsx','.xlsm']},
            {id:'ig_mapping_xsd',label:'Mapping (XSD-Enriched)',icon:'🗺️', panel:'rb', ext:['.xlsx','.xlsm','.xsd']},
            {id:'xsd_ig_analysis',label:'XSD vs IG Analyser',  icon:'🔬', panel:'rb', ext:['.xsd','.xlsx','.xlsm']},
            {id:'pdf_compare',   label:'PDF Comparator',        icon:'🔍', panel:'pdf',ext:['.pdf']},
            {id:'pdf_table_extract',label:'PDF Table Extract',  icon:'📊', panel:'pdf',ext:['.pdf']},
            {id:'pdf_merge',     label:'PDF Merger',            icon:'🔗', panel:'pdf',ext:['.pdf']},
            {id:'pdf_split',     label:'PDF Splitter',          icon:'✂️', panel:'pdf',ext:['.pdf']},
        ];

        function openSendToToolModal() {
            const selExts = [...new Set(Object.values(_libSelected).map(n => n.ext))];
            const list = document.getElementById('sendToToolList');
            list.innerHTML = ALL_TOOLS.map(t => {
                const compatible = t.ext.some(e => selExts.includes(e));
                const opacity = compatible ? '' : 'opacity:0.4;cursor:not-allowed;';
                return `<div style="background:var(--gray-50);border:1px solid var(--gray-200);border-radius:10px;padding:12px;${compatible?'cursor:pointer;':''}${opacity}" 
                             ${compatible ? `onclick="sendToTool('${t.id}','${t.panel}')"` : ''}>
                    <div style="font-size:18px;margin-bottom:6px;">${t.icon}</div>
                    <div style="font-size:13px;font-weight:600;color:var(--gray-900);">${t.label}</div>
                    <div style="font-size:11px;color:var(--gray-500);margin-top:2px;">${t.ext.join(' · ')}</div>
                    ${!compatible ? '<div style="font-size:10px;color:#f97316;margin-top:4px;">Needs: '+t.ext.join('/')+'</div>' : ''}
                </div>`;
            }).join('');
            const n = Object.keys(_libSelected).length;
            document.getElementById('sendToToolSelInfo').textContent = n + ' file(s) selected from library';
            document.getElementById('sendToToolBackdrop').classList.add('open');
            document.getElementById('sendToToolModal').classList.add('open');
        }

        function closeSendToToolModal() {
            document.getElementById('sendToToolBackdrop').classList.remove('open');
            document.getElementById('sendToToolModal').classList.remove('open');
        }

        function quickSendToTool(path) {
            // Select just this file and open send-to-tool
            if (!_libSelected[path]) {
                const node = _findNodeByPath(_libTree, path);
                if (node) { _libSelected[path] = node; updateLibSelectionBar(); }
            }
            openSendToToolModal();
        }

        function _findNodeByPath(nodes, path) {
            for (const n of nodes) {
                if (n.type === 'file' && n.path === path) return n;
                if (n.type === 'folder') {
                    const found = _findNodeByPath(n.children || [], path);
                    if (found) return found;
                }
            }
            return null;
        }

        function sendToTool(toolId, panel) {
            closeSendToToolModal();
            const libPaths = Object.keys(_libSelected);
            // Store for the tool panel to pick up
            window._pendingLibFiles = { paths: libPaths, nodes: {..._libSelected} };
            if (panel === 'rb') {
                // Find and open the rulebook tool
                const tool = rulebookTools.find(t => t.id === toolId);
                if (tool) {
                    openRbTool(toolId);
                    // After short delay, inject the library files
                    setTimeout(() => injectLibFilesIntoPanel('rb'), 150);
                }
            } else {
                const tool = pdfTools.find(t => t.id === toolId);
                if (tool) {
                    openPdfTool(toolId);
                    setTimeout(() => injectLibFilesIntoPanel('pdf'), 150);
                }
            }
        }

        function injectLibFilesIntoPanel(panel) {
            if (!window._pendingLibFiles) return;
            const { paths, nodes } = window._pendingLibFiles;
            if (panel === 'rb') {
                paths.forEach(p => {
                    const n = nodes[p];
                    if (!uploadedRbFiles.find(f => f._libPath === p)) {
                        // Create a mock File-like object that carries the library path
                        const mock = { name: n.name, size: n.size_kb * 1024, _libPath: p, _isLib: true };
                        uploadedRbFiles.push(mock);
                    }
                });
                renderRbFileList();
                updateRbRunButton();
                _rbMaybeAutoDetect();
            } else {
                paths.forEach(p => {
                    const n = nodes[p];
                    if (!uploadedPdfFiles.find(f => f._libPath === p)) {
                        const mock = { name: n.name, size: n.size_kb * 1024, _libPath: p, _isLib: true };
                        uploadedPdfFiles.push(mock);
                    }
                });
                renderPdfFileList();
                updatePdfRunButton();
            }
            window._pendingLibFiles = null;
        }

        // ── Library picker modal (inside tool pages) ─────────────────────────
        function openLibPicker(context) {
            _libPickerContext = context;
            _libPickerSel = {};
            document.getElementById('libPickerSelInfo').textContent = '0 files selected';
            document.getElementById('libPickerConfirmBtn').disabled = true;
            _renderPickerTree();
            document.getElementById('libPickerFiles').innerHTML = '<div style="color:var(--gray-400);text-align:center;padding:40px 20px;font-size:13px;">Click a folder in the tree to browse files</div>';
            document.getElementById('libPickerBackdrop').classList.add('open');
            document.getElementById('libPickerModal').classList.add('open');
            // Load library if not already loaded
            if (!_libTree.length) initLibrary().then(() => _renderPickerTree());
        }

        function closeLibPicker() {
            document.getElementById('libPickerBackdrop').classList.remove('open');
            document.getElementById('libPickerModal').classList.remove('open');
        }

        function _renderPickerTree() {
            document.getElementById('libPickerTree').innerHTML = _buildPickerTreeHTML(_libTree, true);
        }

        function _buildPickerTreeHTML(nodes, expanded) {
            return nodes.map(n => {
                if (n.type === 'folder') {
                    const childHTML = _buildPickerTreeHTML(n.children || [], false);
                    return `<div>
                        <div style="display:flex;align-items:center;gap:6px;padding:6px 10px;cursor:pointer;font-size:12px;font-weight:600;color:var(--gray-700);" 
                             onclick="pickerShowFolder(this,'${n.path.replace(/'/g,"\'")}')">
                            <span style="font-size:10px;color:var(--gray-400);">▶</span>
                            <span>📁</span>
                            <span style="flex:1;">${n.name}</span>
                            ${n.count ? `<span style="background:var(--gray-200);color:var(--gray-600);font-size:9px;padding:1px 5px;border-radius:8px;">${n.count}</span>` : ''}
                        </div>
                        <div style="display:none;padding-left:14px;border-left:2px solid var(--gray-200);margin-left:18px;">${childHTML}</div>
                    </div>`;
                }
                return '';
            }).join('');
        }

        function pickerShowFolder(el, folderPath) {
            // Toggle expand
            const children = el.nextElementSibling;
            if (children) children.style.display = children.style.display === 'none' ? 'block' : 'none';
            // Show files of this folder in right panel
            const node = _findFolderByPath(_libTree, folderPath);
            if (!node) return;
            const files = (node.children || []).filter(c => c.type === 'file');
            if (!files.length) {
                document.getElementById('libPickerFiles').innerHTML = '<div style="color:var(--gray-400);text-align:center;padding:40px;font-size:13px;">📂 No files in this folder yet</div>';
                return;
            }
            document.getElementById('libPickerFiles').innerHTML = files.map(f => {
                const sel = _libPickerSel[f.path] ? ' selected' : '';
                return `<div class="lib-modal-file-item${sel}" onclick="togglePickerFile('${f.path.replace(/'/g,"\'")}')" id="picker_${f.path.replace(/[^a-z0-9]/gi,'_')}">
                    <input type="checkbox" class="lib-modal-file-check" ${_libPickerSel[f.path]?'checked':''} onclick="event.stopPropagation();togglePickerFile('${f.path.replace(/'/g,"\'")}')">
                    <span class="lib-modal-file-icon">${f.icon}</span>
                    <div class="lib-modal-file-info">
                        <div class="lib-modal-file-name">${f.name}</div>
                        <div class="lib-modal-file-meta">${f.size_kb} KB · ${f.path}</div>
                    </div>
                </div>`;
            }).join('');
            // Store current folder files for reference
            window._pickerCurrentFiles = Object.fromEntries(files.map(f => [f.path, f]));
        }

        function _findFolderByPath(nodes, path) {
            for (const n of nodes) {
                if (n.type === 'folder') {
                    if (n.path === path) return n;
                    const found = _findFolderByPath(n.children || [], path);
                    if (found) return found;
                }
            }
            return null;
        }

        function togglePickerFile(path) {
            const node = (window._pickerCurrentFiles || {})[path] || _findNodeByPath(_libTree, path);
            if (!node) return;
            const el = document.getElementById('picker_' + path.replace(/[^a-z0-9]/gi,'_'));
            if (_libPickerSel[path]) {
                delete _libPickerSel[path];
                if (el) { el.classList.remove('selected'); const cb = el.querySelector('input'); if(cb) cb.checked=false; }
            } else {
                _libPickerSel[path] = node;
                if (el) { el.classList.add('selected'); const cb = el.querySelector('input'); if(cb) cb.checked=true; }
            }
            const n = Object.keys(_libPickerSel).length;
            document.getElementById('libPickerSelInfo').textContent = n + (n===1?' file selected':' files selected');
            document.getElementById('libPickerConfirmBtn').disabled = n === 0;
        }

        function confirmLibPick() {
            const ctx = _libPickerContext;
            const nodes = {..._libPickerSel};
            closeLibPicker();
            Object.entries(nodes).forEach(([path, node]) => {
                const mock = { name: node.name, size: node.size_kb * 1024, _libPath: path, _isLib: true };
                if (ctx === 'pdf') {
                    if (!uploadedPdfFiles.find(f => f._libPath === path)) uploadedPdfFiles.push(mock);
                } else {
                    if (!uploadedRbFiles.find(f => f._libPath === path)) uploadedRbFiles.push(mock);
                }
            });
            if (ctx === 'pdf') { renderPdfFileList(); updatePdfRunButton(); }
            else               { renderRbFileList(); updateRbRunButton(); _rbMaybeAutoDetect(); }
        }

        // ── Patch file list renderers to show library badge ──────────────────
        const _origRenderPdfFileList = typeof renderPdfFileList === 'function' ? renderPdfFileList : null;
        const _origRenderRbFileList  = typeof renderRbFileList  === 'function' ? renderRbFileList  : null;

        // renderPdfFileList v2 removed → FSP

        // renderRbFileList v2 removed → FSP

        // ── Patch runRbTool/runPdfTool to include library_files in FormData ──
        // Store original run functions and wrap them
        const _origRunRb  = window.runRbTool;
        const _origRunPdf = window.runPdfTool;

        function _buildFormDataWithLib(files) {
            const fd = new FormData();
            const libPaths = [];
            files.forEach(f => {
                if (f._isLib) { libPaths.push(f._libPath); }
                else          { fd.append('files', f); }
            });
            if (libPaths.length) fd.append('library_files', JSON.stringify(libPaths));
            return fd;
        }

        // Override the run functions' FormData building
        window._buildLibFormData = _buildFormDataWithLib;

    

        // ═══════════════════════════════════════════════════════════════════
        // UNIFIED FILE SOURCE PANEL (FSP)  — v2 clean implementation
        //
        // Each tool page has one FSP with two tabs:
        //   ⬆️ Upload  — drag/drop or browse local files
        //   🗄️ Library — browse server library, tick files to select
        //
        // Panel keys:  'xsd' | 'pdf' | 'rb'
        //
        // How XSD tool works differently:
        //   Uploaded files are POSTed to /upload → server returns filenames
        //   uploadedFiles[] stores those server-side filename strings
        //   Library files for XSD are stored as { _libPath, name, _isLib:true }
        //   runTool() sends { files: [...strings], library_files: [...paths] }
        //
        // How PDF/RB tools work:
        //   uploadedPdfFiles / uploadedRbFiles store File objects + lib mocks
        //   runPdfTool/runRbTool build FormData including library_files JSON
        // ═══════════════════════════════════════════════════════════════════

        // ── Shared library tree cache ─────────────────────────────────────────
        // _libTree is already declared in the Library page section below,
        // but may not be loaded yet. FSP loads it on demand.

        // Per-panel folder state (last opened folder path)
        const _fspFolder = { xsd: null, pdf: null, rb: null };

        // ── Tab switch ────────────────────────────────────────────────────────
        function fspSwitchTab(panel, tab, clickedTabEl) {
            const wrapper = document.getElementById('fsp-' + panel);
            if (!wrapper) return;
            wrapper.querySelectorAll('.fsp-tab').forEach(t => t.classList.remove('active'));
            wrapper.querySelectorAll('.fsp-tab-pane').forEach(p => p.classList.remove('active'));
            clickedTabEl.classList.add('active');
            wrapper.querySelector('#fsp-' + panel + '-' + tab)?.classList.add('active');
            if (tab === 'library') _fspLoadTree(panel);
        }

        // ── Library tree ──────────────────────────────────────────────────────
        function _fspLoadTree(panel) {
            const treeEl = document.getElementById('fspTree-' + panel);
            if (!treeEl) return;
            const render = () => _fspRenderTree(panel, _libTree, treeEl, true);
            if (_libTree && _libTree.length) { render(); return; }
            treeEl.innerHTML = '<div style="padding:16px;font-size:12px;color:var(--gray-400);">Loading…</div>';
            fetch('/library').then(r => r.json()).then(d => { _libTree = d.tree || []; render(); })
                             .catch(() => { treeEl.innerHTML = '<div style="padding:16px;font-size:12px;color:#ef4444;">⚠️ Could not load library</div>'; });
        }

        function _fspRenderTree(panel, nodes, containerEl, isRoot) {
            if (isRoot) containerEl.innerHTML = '';
            if (!nodes || !nodes.length) {
                if (isRoot) containerEl.innerHTML = '<div style="padding:16px;font-size:12px;color:var(--gray-400);">Library is empty.<br>Go to Document Library to add files.</div>';
                return;
            }
            nodes.forEach(n => {
                if (n.type !== 'folder') return;
                const wrap    = document.createElement('div');
                const pathEnc = n.path.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
                wrap.innerHTML = `
                    <div class="fsp-lib-folder-row" data-path="${n.path}"
                         onclick="_fspFolderClick(event,'${panel}','${pathEnc}',this)">
                        <span class="fsp-lib-folder-toggle">▶</span>
                        <span>📁</span>
                        <span style="flex:1;">${n.name}</span>
                        ${n.count ? `<span style="font-size:10px;color:var(--gray-400);">${n.count}</span>` : ''}
                    </div>
                    <div class="fsp-lib-folder-children"></div>`;
                containerEl.appendChild(wrap);
            });
        }

        function _fspFolderClick(e, panel, folderPath, row) {
            e.stopPropagation();
            // Highlight
            const treeEl = document.getElementById('fspTree-' + panel);
            treeEl?.querySelectorAll('.fsp-lib-folder-row').forEach(r => r.classList.remove('active'));
            row.classList.add('active');
            // Toggle expand
            row.classList.toggle('open');
            const childContainer = row.nextElementSibling;
            if (row.classList.contains('open')) {
                childContainer.classList.add('open');
                if (!childContainer.children.length) {
                    const node = _fspFindFolder(_libTree, folderPath);
                    _fspRenderTree(panel, node?.children || [], childContainer, false);
                }
            } else {
                childContainer.classList.remove('open');
            }
            // Show files on right
            _fspFolder[panel] = folderPath;
            _fspShowFiles(panel, folderPath);
        }

        function _fspFindFolder(nodes, path) {
            for (const n of (nodes || [])) {
                if (n.type === 'folder') {
                    if (n.path === path) return n;
                    const found = _fspFindFolder(n.children, path);
                    if (found) return found;
                }
            }
            return null;
        }

        function _fspShowFiles(panel, folderPath) {
            const filesEl = document.getElementById('fspFiles-' + panel);
            if (!filesEl) return;
            const node  = _fspFindFolder(_libTree, folderPath);
            const files = (node?.children || []).filter(c => c.type === 'file');
            if (!files.length) {
                filesEl.innerHTML = '<div style="padding:20px;text-align:center;font-size:12px;color:var(--gray-400);">No files in this folder.<br>Use the Document Library page to upload.</div>';
                return;
            }
            filesEl.innerHTML = files.map(f => {
                const selected = _fspIsSelected(panel, f.path);
                const idSafe   = 'fsp_' + panel + '_' + f.path.replace(/[^a-z0-9]/gi,'_');
                const fJson    = JSON.stringify(f).replace(/"/g, '&quot;');
                return `<div class="fsp-lib-file-item${selected?' selected':''}" id="${idSafe}"
                              onclick="_fspToggleFile('${panel}','${f.path.replace(/'/g,"\'")}',this)">
                    <input type="checkbox" class="fsp-lib-file-check" ${selected?'checked':''}
                           onclick="event.stopPropagation();_fspToggleFile('${panel}','${f.path.replace(/'/g,"\'")}',this.closest('.fsp-lib-file-item'))">
                    <span style="font-size:16px;">${f.icon}</span>
                    <div style="flex:1;min-width:0;">
                        <div class="fsp-lib-file-name">${f.name}</div>
                        <div style="font-size:10px;color:var(--gray-400);">${f.size_kb} KB · ${f.path}</div>
                    </div>
                </div>`;
            }).join('');
        }

        function _fspIsSelected(panel, libPath) {
            const arr = _fspGetFiles(panel);
            return arr.some(f => f._libPath === libPath || (typeof f === 'object' && f._libPath === libPath));
        }

        function _fspToggleFile(panel, libPath, itemEl) {
            const arr  = _fspGetFiles(panel);
            const node = _fspFindFileInTree(_libTree, libPath);
            if (!node) return;
            const idx = arr.findIndex(f => f._libPath === libPath);
            if (idx >= 0) {
                arr.splice(idx, 1);
                itemEl.classList.remove('selected');
                itemEl.querySelector('input[type=checkbox]').checked = false;
            } else {
                arr.push({ name: node.name, size: node.size_kb * 1024, _libPath: libPath, _isLib: true });
                itemEl.classList.add('selected');
                itemEl.querySelector('input[type=checkbox]').checked = true;
            }
            _fspSetFiles(panel, arr);
            _fspRenderStagedList(panel);
            _fspUpdateRunBtn(panel);
        }

        function _fspFindFileInTree(nodes, path) {
            for (const n of (nodes || [])) {
                if (n.type === 'file' && n.path === path) return n;
                if (n.type === 'folder') {
                    const f = _fspFindFileInTree(n.children, path);
                    if (f) return f;
                }
            }
            return null;
        }

        // ── File array getters/setters ─────────────────────────────────────────
        function _fspGetFiles(panel) {
            if (panel === 'xsd') return uploadedFiles;
            if (panel === 'pdf') return uploadedPdfFiles;
            if (panel === 'yaml') return uploadedYamlFiles;
            return uploadedRbFiles;
        }
        function _fspSetFiles(panel, arr) {
            if (panel === 'xsd') uploadedFiles = arr;
            else if (panel === 'pdf') uploadedPdfFiles = arr;
            else if (panel === 'yaml') uploadedYamlFiles = arr;
            else uploadedRbFiles = arr;
        }
        function _fspGetListElId(panel) {
            return panel === 'xsd' ? 'fileList' : panel === 'pdf' ? 'pdfFileList' : panel === 'yaml' ? 'yamlFileList' : 'rbFileList';
        }
        function _fspUpdateRunBtn(panel) {
            if (panel === 'xsd') updateRunButton();
            else if (panel === 'pdf') updatePdfRunButton();
            else if (panel === 'yaml') updateYamlRunButton();
            else updateRbRunButton();
        }

        // ── Staged file list renderer (shared across all panels) ──────────────
        function _fspRenderStagedList(panel) {
            const el  = document.getElementById(_fspGetListElId(panel));
            if (!el) return;
            const arr = _fspGetFiles(panel);
            if (!arr.length) { el.innerHTML = ''; return; }
            const _icon = name => {
                const ext = (name || '').split('.').pop().toLowerCase();
                return { xsd:'📐', xml:'📝', zip:'📦', pdf:'📄', xlsx:'📊', xlsm:'📊' }[ext] || '📄';
            };
            el.innerHTML = arr.map((f, i) => {
                const name = typeof f === 'string' ? f : f.name;
                const kb   = typeof f === 'string' ? '' : (f.size / 1024).toFixed(1) + ' KB';
                const isLib = typeof f === 'object' && f._isLib;
                return `<div class="fsp-file-row">
                    <span class="fsp-file-row-icon">${_icon(name)}</span>
                    <span class="fsp-file-row-name">${name}</span>
                    ${isLib ? '<span class="fsp-file-row-badge">Library</span>' : ''}
                    ${kb ? `<span class="fsp-file-row-size">${kb}</span>` : ''}
                    <span class="fsp-file-row-remove" onclick="_fspRemove('${panel}',${i})" title="Remove">✕</span>
                </div>`;
            }).join('');
        }

        function _fspRemove(panel, idx) {
            const arr = _fspGetFiles(panel);
            arr.splice(idx, 1);
            _fspSetFiles(panel, arr);
            _fspRenderStagedList(panel);
            _fspUpdateRunBtn(panel);
            // Refresh library file checkboxes if library tab is showing
            const folder = _fspFolder[panel];
            if (folder) _fspShowFiles(panel, folder);
        }

        // ── Wire file input + drop zone for each panel (called once on load) ──
        function _fspInitPanel(panel) {
            const zone     = document.getElementById('fspDropZone-' + panel);
            const inputId  = panel === 'xsd' ? 'fileInput' : panel === 'pdf' ? 'pdfFileInput' : panel === 'yaml' ? 'yamlFileInput' : 'rbFileInput';
            const input    = document.getElementById(inputId);
            if (!zone || !input) return;

            zone.ondragover  = e => { e.preventDefault(); zone.classList.add('dragover'); };
            zone.ondragleave = e => { if (!zone.contains(e.relatedTarget)) zone.classList.remove('dragover'); };
            zone.ondrop      = e => {
                e.preventDefault(); zone.classList.remove('dragover');
                if (panel === 'xsd') handleFiles(e.dataTransfer.files);
                else if (panel === 'pdf') handlePdfFiles(e.dataTransfer.files);
                else if (panel === 'yaml') handleYamlFiles(e.dataTransfer.files);
                else handleRbFiles(e.dataTransfer.files);
            };
            input.onchange = e => {
                if (panel === 'xsd') handleFiles(e.target.files);
                else if (panel === 'pdf') handlePdfFiles(e.target.files);
                else if (panel === 'yaml') handleYamlFiles(e.target.files);
                else handleRbFiles(e.target.files);
                input.value = '';
            };
        }

        // ── Override renderFileList functions to use FSP renderer ─────────────
        function renderFileList()    { _fspRenderStagedList('xsd'); }
        function renderPdfFileList() { _fspRenderStagedList('pdf'); }
        function renderRbFileList()  { _fspRenderStagedList('rb');  }
        function removePdfFile(i) { _fspRemove('pdf', i); }
        function removeRbFile(i)  { _fspRemove('rb',  i); }

        // ── Reset FSP state when a tool page opens ────────────────────────────
        function _fspResetPanel(panel) {
            _fspFolder[panel] = null;
            const filesEl = document.getElementById('fspFiles-' + panel);
            if (filesEl) filesEl.innerHTML = '<div class="fsp-lib-click-hint">← Select a folder to browse files</div>';
            // Switch back to Upload tab
            const wrapper = document.getElementById('fsp-' + panel);
            if (wrapper) {
                wrapper.querySelectorAll('.fsp-tab').forEach((t, i) => t.classList.toggle('active', i === 0));
                wrapper.querySelectorAll('.fsp-tab-pane').forEach((p, i) => p.classList.toggle('active', i === 0));
            }
        }

        // ── Patch runTool (XSD) to include library_files in its JSON payload ──
        // The existing runTool sends: { tool, files: [...serverFilenames], options }
        // We extend it to also send: { library_files: [...libPaths] }
        const _origRunTool = window.runTool;
        function runTool() {
            if (!currentTool) return;
            const opts = {};
            currentTool.options?.forEach(o => {
                const el = document.getElementById(o.id);
                if (el) opts[o.id] = o.type === 'checkbox' ? el.checked : el.value;
            });

            // Split uploadedFiles into server-uploaded filenames vs library refs
            const serverFiles  = uploadedFiles.filter(f => typeof f === 'string');
            const libraryFiles = uploadedFiles.filter(f => typeof f === 'object' && f._isLib).map(f => f._libPath);

            showLoading('Running ' + currentTool.title + '...');
            fetch('/run_tool', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tool: currentTool.id, files: serverFiles, library_files: libraryFiles, options: opts })
            })
            .then(r => { if (!r.ok && r.status === 504) throw new Error('Tool timed out'); return r.json(); })
            .then(d => {
                hideLoading();
                if (d.success) {
                    showResults(d.files, d.message || 'Complete!' + (d.execution_time_seconds ? ` (${d.execution_time_seconds}s)` : ''));
                } else {
                    let msg = d.error || 'Tool failed';
                    if (d.suggestion) msg += '. 💡 ' + d.suggestion;
                    showMessage(msg, 'error');
                }
            })
            .catch(e => { hideLoading(); showMessage(e.message || 'Network error', 'error'); });
        }

        // ── Init on DOM ready ─────────────────────────────────────────────────
        document.addEventListener('DOMContentLoaded', () => {
            _fspInitPanel('xsd');
            _fspInitPanel('pdf');
            _fspInitPanel('rb');
            _fspInitPanel('yaml');
        });

        // ── Patch open functions to reset panel when switching tools ──────────
        // Wrap after DOM ready so the original functions exist
        document.addEventListener('DOMContentLoaded', () => {
            const _origOpenTool    = window.openTool;
            const _origOpenPdfTool = window.openPdfTool;
            const _origOpenRbTool  = window.openRbTool;
            const _origOpenYamlTool = window.openYamlTool;
            window.openTool = function(id) {
                _fspResetPanel('xsd');
                if (_origOpenTool) _origOpenTool.call(this, id);
            };
            window.openPdfTool = function(id) {
                _fspResetPanel('pdf');
                if (_origOpenPdfTool) _origOpenPdfTool.call(this, id);
            };
            window.openRbTool = function(id) {
                _fspResetPanel('rb');
                if (_origOpenRbTool) _origOpenRbTool.call(this, id);
            };
            window.openYamlTool = function(id) {
                _fspResetPanel('yaml');
                if (_origOpenYamlTool) _origOpenYamlTool.call(this, id);
            };
        });

                // ═══════════════════════════════════════════════════════════════
        // LIBRARY MANAGEMENT
        // ═══════════════════════════════════════════════════════════════

        let _ctxTarget  = null;   // { type:'folder'|'file', path, name } for context menu
        let _uploadTargetPath = null;   // folder path for upload modal
        let _newFolderParentPath = null; // folder path for new-folder modal
        let _deleteTarget = null;       // { path, name, type }
        let _pendingUploadFiles = [];   // File objects staged in upload modal

        // ── Refresh ──────────────────────────────────────────────────────────
        async function libRefresh() {
            _libTree = [];
            _libSelected = {};
            updateLibSelectionBar();
            document.getElementById('libTreeScroll').innerHTML = '<div class="lib-empty-state">Refreshing…</div>';
            await initLibrary();
        }

        // ── Tree rendering (override to add right-click + drag) ───────────────
        // Extend _buildTreeHTML to add context menu + drag-drop events
        const _origBuildTreeHTML = _buildTreeHTML;
        function _buildTreeHTML(nodes, expanded) {
            return nodes.map(n => {
                if (n.type === 'folder') {
                    const childHTML = _buildTreeHTML(n.children || [], false);
                    const hasFiles = n.count > 0;
                    return `<div class="lib-folder" data-path="${n.path}">
                        <div class="lib-folder-row${expanded ? ' open' : ''}"
                             onclick="toggleLibFolder(this)"
                             oncontextmenu="showLibCtxMenu(event,${JSON.stringify({type:'folder',path:n.path,name:n.name}).replace(/"/g,'&quot;')})"
                             ondragover="libDragOver(event,this)"
                             ondragleave="libDragLeave(event,this)"
                             ondrop="libDrop(event,'${n.path.replace(/'/g,"\'")}')">
                            <span class="lib-folder-toggle">▶</span>
                            <span>${expanded ? '📂' : '📁'}</span>
                            <span class="lib-folder-name" data-path="${n.path}">${n.name}</span>
                            ${hasFiles ? `<span class="lib-folder-count">${n.count}</span>` : ''}
                        </div>
                        <div class="lib-folder-children${expanded ? ' open' : ''}">${childHTML}</div>
                    </div>`;
                } else {
                    const sel = _libSelected[n.path] ? ' selected' : '';
                    return `<div class="lib-file-row${sel}"
                                 draggable="true"
                                 oncontextmenu="showLibCtxMenu(event,${JSON.stringify({type:'file',path:n.path,name:n.name,ext:n.ext,size_kb:n.size_kb,icon:n.icon}).replace(/"/g,'&quot;')})"
                                 onclick="toggleLibFile(this,'${n.path.replace(/'/g,"\'")}',${JSON.stringify(n).replace(/"/g,'&quot;')})"
                                 title="${n.name}">
                        <span class="lib-file-icon">${n.icon}</span>
                        <span class="lib-file-name">${n.name}</span>
                        <span class="lib-file-size">${n.size_kb}KB</span>
                    </div>`;
                }
            }).join('');
        }

        // ── Drag & Drop onto tree panel ────────────────────────────────────────
        document.addEventListener('DOMContentLoaded', () => {
            const panel = document.getElementById('libTreePanel');
            if (!panel) return;
            panel.addEventListener('dragover',  e => { e.preventDefault(); panel.classList.add('drag-over'); });
            panel.addEventListener('dragleave', e => { if (!panel.contains(e.relatedTarget)) panel.classList.remove('drag-over'); });
            panel.addEventListener('drop', e => {
                e.preventDefault();
                panel.classList.remove('drag-over');
                const files = e.dataTransfer.files;
                if (files.length) { _uploadTargetPath = null; _pendingUploadFiles = Array.from(files); openUploadModal(null, files); }
            });
        });

        function libDragOver(e, row) {
            e.preventDefault(); e.stopPropagation();
            row.classList.add('drag-target');
        }
        function libDragLeave(e, row) {
            row.classList.remove('drag-target');
        }
        function libDrop(e, folderPath) {
            e.preventDefault(); e.stopPropagation();
            e.currentTarget.classList.remove('drag-target');
            document.getElementById('libTreePanel')?.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length) openUploadModal(folderPath, files);
        }

        // ── Context menu ──────────────────────────────────────────────────────
        function showLibCtxMenu(e, nodeData) {
            e.preventDefault();
            e.stopPropagation();
            _ctxTarget = typeof nodeData === 'string' ? JSON.parse(nodeData) : nodeData;

            const isFolder = _ctxTarget.type === 'folder';
            document.getElementById('ctxUpload').style.display    = isFolder ? '' : 'none';
            document.getElementById('ctxNewFolder').style.display  = isFolder ? '' : 'none';
            document.getElementById('ctxSep1').style.display       = isFolder ? '' : 'none';

            const menu = document.getElementById('libCtxMenu');
            menu.style.left = e.clientX + 'px';
            menu.style.top  = e.clientY + 'px';
            menu.classList.add('open');

            // Click-away to close
            setTimeout(() => document.addEventListener('click', closeCtxMenu, {once: true}), 0);
        }

        function closeCtxMenu() {
            document.getElementById('libCtxMenu').classList.remove('open');
        }

        function ctxAction(action) {
            closeCtxMenu();
            const t = _ctxTarget;
            if (!t) return;
            if (action === 'upload')    openUploadModal(t.path);
            if (action === 'newFolder') openNewFolderModal(t.path);
            if (action === 'rename')    startInlineRename(t);
            if (action === 'delete')    openDeleteModal(t);
        }

        // ── Inline rename ─────────────────────────────────────────────────────
        function startInlineRename(target) {
            // Find the name span in the tree and replace it with an input
            const selector = target.type === 'folder'
                ? `.lib-folder-name[data-path="${target.path}"]`
                : null; // simplified
            const span = document.querySelector(`.lib-folder-name[data-path="${CSS.escape(target.path)}"]`)
                      || [...document.querySelectorAll('.lib-file-row .lib-file-name')]
                            .find(el => el.closest('.lib-file-row')?.getAttribute('onclick')?.includes(target.path));
            if (!span) { alert('Could not find element to rename.'); return; }

            const oldName = target.name;
            const input = document.createElement('input');
            input.className = 'lib-rename-input';
            input.value = oldName;
            input.onclick = e => e.stopPropagation();
            span.replaceWith(input);
            input.focus();
            input.select();

            const commit = async () => {
                const newName = input.value.trim();
                if (!newName || newName === oldName) { await libRefresh(); return; }
                const res = await fetch('/library/rename', {
                    method: 'POST',
                    headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({path: target.path, name: newName})
                });
                const data = await res.json();
                if (!data.success) alert('Rename failed: ' + data.error);
                await libRefresh();
            };

            input.addEventListener('blur',    commit);
            input.addEventListener('keydown', e => {
                if (e.key === 'Enter')  { input.blur(); }
                if (e.key === 'Escape') { input.removeEventListener('blur', commit); libRefresh(); }
            });
        }

        // ── Upload modal ──────────────────────────────────────────────────────
        function openUploadModal(folderPath, preloadFiles) {
            _uploadTargetPath  = folderPath || null;
            _pendingUploadFiles = preloadFiles ? Array.from(preloadFiles) : [];
            document.getElementById('uploadTargetPath').textContent = folderPath || 'library root';
            document.getElementById('libUploadProgress').innerHTML = '';
            document.getElementById('libUploadInfo').textContent = 'No files selected';
            document.getElementById('libUploadBtn').disabled = true;
            document.getElementById('libUploadFileInput').value = '';

            if (_pendingUploadFiles.length) _renderUploadStaged();

            // Drag-drop on the upload zone
            const zone = document.getElementById('libUploadZone');
            zone.ondragover  = e => { e.preventDefault(); zone.classList.add('drag-over'); };
            zone.ondragleave = () => zone.classList.remove('drag-over');
            zone.ondrop = e => {
                e.preventDefault(); zone.classList.remove('drag-over');
                handleLibUploadFiles(e.dataTransfer.files);
            };

            document.getElementById('libUploadBackdrop').classList.add('open');
            document.getElementById('libUploadModal').classList.add('open');
        }

        function closeUploadModal() {
            document.getElementById('libUploadBackdrop').classList.remove('open');
            document.getElementById('libUploadModal').classList.remove('open');
            _pendingUploadFiles = [];
        }

        function handleLibUploadFiles(fileList) {
            Array.from(fileList).forEach(f => {
                if (!_pendingUploadFiles.find(x => x.name === f.name)) _pendingUploadFiles.push(f);
            });
            _renderUploadStaged();
        }

        function _renderUploadStaged() {
            const n = _pendingUploadFiles.length;
            document.getElementById('libUploadInfo').textContent = n ? n + ' file(s) ready' : 'No files selected';
            document.getElementById('libUploadBtn').disabled = n === 0;
            document.getElementById('libUploadProgress').innerHTML = _pendingUploadFiles.map((f, i) => `
                <div class="lib-upload-item">
                    <span style="font-size:16px;">${_extIcon(f.name)}</span>
                    <span class="lib-upload-item-name">${f.name}</span>
                    <span style="color:var(--gray-400);font-size:11px;">${(f.size/1024).toFixed(1)} KB</span>
                    <span style="cursor:pointer;color:var(--gray-400);font-size:14px;" onclick="removeUploadFile(${i})">✕</span>
                </div>`).join('');
        }

        function _extIcon(name) {
            const ext = name.split('.').pop().toLowerCase();
            return {xsd:'📐', xlsx:'📊', xlsm:'📊', pdf:'📄', xml:'📝'}[ext] || '📄';
        }

        function removeUploadFile(idx) {
            _pendingUploadFiles.splice(idx, 1);
            _renderUploadStaged();
        }

        async function doLibUpload() {
            if (!_pendingUploadFiles.length) return;
            const btn = document.getElementById('libUploadBtn');
            btn.disabled = true; btn.textContent = '⏳ Uploading…';

            const fd = new FormData();
            fd.append('folder_path', _uploadTargetPath || '');
            _pendingUploadFiles.forEach(f => fd.append('files', f));

            try {
                const res  = await fetch('/library/upload', {method:'POST', body: fd});
                const data = await res.json();
                if (data.success) {
                    const n = (data.files || []).length;
                    document.getElementById('libUploadProgress').innerHTML =
                        `<div style="background:#d1fae5;border:1px solid #6ee7b7;border-radius:8px;padding:10px 14px;font-size:13px;color:#065f46;margin-top:8px;">
                            ✅ ${n} file(s) uploaded successfully${data.errors?.length ? '<br>⚠️ ' + data.errors.join(', ') : ''}
                        </div>`;
                    document.getElementById('libUploadInfo').textContent = 'Done!';
                    _pendingUploadFiles = [];
                    await libRefresh();
                    setTimeout(closeUploadModal, 1200);
                } else {
                    document.getElementById('libUploadInfo').textContent = '❌ ' + data.error;
                    btn.disabled = false; btn.textContent = '⬆️ Upload';
                }
            } catch(e) {
                document.getElementById('libUploadInfo').textContent = '❌ Network error';
                btn.disabled = false; btn.textContent = '⬆️ Upload';
            }
        }

        // ── New folder modal ──────────────────────────────────────────────────
        function openNewFolderModal(parentPath) {
            _newFolderParentPath = parentPath || null;
            document.getElementById('newFolderParentLabel').textContent = parentPath || 'library root';
            document.getElementById('newFolderNameInput').value = '';
            document.getElementById('newFolderMsg').textContent = '';
            document.getElementById('libNewFolderBackdrop').classList.add('open');
            document.getElementById('libNewFolderModal').classList.add('open');
            setTimeout(() => document.getElementById('newFolderNameInput').focus(), 80);
        }

        function closeNewFolderModal() {
            document.getElementById('libNewFolderBackdrop').classList.remove('open');
            document.getElementById('libNewFolderModal').classList.remove('open');
        }

        async function doCreateFolder() {
            const name = document.getElementById('newFolderNameInput').value.trim();
            if (!name) { document.getElementById('newFolderMsg').textContent = 'Please enter a name.'; return; }
            const res  = await fetch('/library/folder', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({path: _newFolderParentPath || '', name})
            });
            const data = await res.json();
            if (data.success) {
                closeNewFolderModal();
                await libRefresh();
            } else {
                document.getElementById('newFolderMsg').textContent = data.error || 'Failed';
            }
        }

        // ── Delete modal ──────────────────────────────────────────────────────
        function openDeleteModal(target) {
            _deleteTarget = target;
            document.getElementById('deleteTargetName').textContent = target.name;
            document.getElementById('deleteWarning').textContent =
                target.type === 'folder'
                    ? '⚠️ This will delete the folder and ALL its contents.'
                    : 'This cannot be undone.';
            document.getElementById('libDeleteBackdrop').classList.add('open');
            document.getElementById('libDeleteModal').classList.add('open');
        }

        function closeDeleteModal() {
            document.getElementById('libDeleteBackdrop').classList.remove('open');
            document.getElementById('libDeleteModal').classList.remove('open');
        }

        async function doDelete() {
            if (!_deleteTarget) return;
            const res  = await fetch('/library/delete', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({path: _deleteTarget.path})
            });
            const data = await res.json();
            closeDeleteModal();
            if (data.success) {
                // Remove from selection if selected
                delete _libSelected[_deleteTarget.path];
                updateLibSelectionBar();
                await libRefresh();
            } else {
                alert('Delete failed: ' + data.error);
            }
        }


// ============================================================
// YAML TOOLS
// ============================================================

        const yamlTools = [
            {
                id: 'yaml_api_extract', icon: '📄', title: 'API Schema Extractor', badge: 'New',
                description: 'Upload an OpenAPI / AsyncAPI YAML spec. Detects every endpoint, lets you pick which ones to extract, and produces a structured Excel workbook — one sheet per endpoint with all parameters, request body, and response schemas fully expanded.',
                features: ['🔗 Full $ref resolution', '📐 allOf / anyOf / oneOf merging', '🗂 One sheet per endpoint', '🎯 Endpoint picker UI'],
                input: 'Upload 1 YAML or JSON file', minFiles: 1,
                options: [
                    { type: 'yaml_endpoint_picker', id: 'yaml_endpoint_picker', label: 'Select endpoints to extract' }
                ],
                guide: {
                    when: '<h4>📌 When to Use This Tool</h4><p>Use API Schema Extractor when you need to:</p><ul><li>Document an OpenAPI or AsyncAPI specification as a structured Excel workbook</li><li>Extract all parameters, request bodies, and response schemas per endpoint into a readable format</li><li>Understand deeply nested schema structures with <code>$ref</code>, <code>allOf</code>, <code>anyOf</code>, or <code>oneOf</code> compositions</li><li>Share API field-level documentation with teams who prefer Excel over YAML</li><li>Extract only specific endpoints rather than the entire spec</li></ul>',
                    how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload your OpenAPI 3.x or AsyncAPI 2.x YAML (or JSON) file.</p><p><strong>Step 2 — Choose endpoints (optional):</strong> The tool automatically scans and lists all endpoints grouped by tag. Tick the ones you want to extract — or leave all checked to extract everything.</p><p><strong>Step 3:</strong> Click <strong>"Run Tool"</strong>. Processing takes a few seconds even for large specs.</p><p><strong>Tip:</strong> Use <strong>"Select All"</strong> / <strong>"Clear All"</strong> buttons to quickly manage your selection.</p>',
                    output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">{filename}_api_schema.xlsx</span><span class="output-file-desc">— Structured Excel schema workbook</span></div></div><p style="margin-top:12px;"><strong>Workbook structure:</strong></p><ul><li><strong>📋 Summary sheet</strong> — lists all endpoints with method, path, summary, tag, and sheet name</li><li><strong>One sheet per endpoint</strong> — named by HTTP method + path (e.g. POST payments)</li></ul><p><strong>Columns per row:</strong> # · Field Name (indented by depth) · Full Path · Type · Format · Required · Nullable · Description · Enum Values · Example · Default · Min · Max · Pattern · Read Only · Write Only · Deprecated</p><p><strong>Row colours:</strong> 🔵 Blue = Required fields · 🟡 Yellow = Array item rows · 🔴 Red = Deprecated fields</p>',
                    benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Deep Expansion</div><div class="guide-benefit-text">All $ref, allOf, anyOf, oneOf resolved — every nested field visible in one flat list</div></div><div class="guide-benefit"><div class="guide-benefit-title">Endpoint Picker</div><div class="guide-benefit-text">Auto-detects endpoints on upload — select only what you need</div></div><div class="guide-benefit"><div class="guide-benefit-title">Grouped by Tag</div><div class="guide-benefit-text">Endpoints grouped by OpenAPI tag — easy navigation for large APIs</div></div><div class="guide-benefit"><div class="guide-benefit-title">Summary Sheet</div><div class="guide-benefit-text">One-page overview of all endpoints with direct sheet links</div></div></div>'
                }
            }
        ];

        let currentYamlTool = null, uploadedYamlFiles = [];

        function renderYamlToolsGrid() {
            document.getElementById('yamlToolsGrid').innerHTML = yamlTools.map(t => `
                <div class="tool-card" onclick="openYamlTool('${t.id}')">
                    <div class="tool-card-header"><div class="tool-card-icon" style="background:linear-gradient(135deg,#0e7490 0%,#10b981 100%);">${t.icon}</div><div><span class="tool-card-title">${t.title}</span>${t.badge ? `<span class="tool-card-badge">${t.badge}</span>` : ''}</div></div>
                    <p class="tool-card-description">${t.description}</p>
                    <div class="tool-card-features">${t.features.map(f => `<div class="tool-card-feature">${f}</div>`).join('')}</div>
                    <div class="tool-card-input">📁 ${t.input}</div>
                    <div class="tool-card-arrow">→</div>
                </div>
            `).join('');
        }

        function openYamlTool(toolId) {
            const tool = yamlTools.find(t => t.id === toolId);
            if (!tool) return;
            currentYamlTool = tool;
            uploadedYamlFiles = [];
            document.getElementById('yamlFileInput').value = '';
            document.getElementById('yamlToolPageIcon').textContent = tool.icon;
            document.getElementById('yamlToolPageTitle').textContent = tool.title;
            document.getElementById('yamlUploadHint').textContent = '— ' + tool.input;
            document.getElementById('yamlFileList').innerHTML = '';
            document.getElementById('yamlResultsSection').classList.remove('active');
            document.getElementById('yamlMessageBox').innerHTML = '';
            document.getElementById('yamlMessageBox').style.display = 'none';
            document.getElementById('yamlUploadSubtitle').textContent = 'Supports .yaml · .yml · .json files';

            document.getElementById('guide-yaml-when').innerHTML = tool.guide.when;
            document.getElementById('guide-yaml-how').innerHTML = tool.guide.how;
            document.getElementById('guide-yaml-output').innerHTML = tool.guide.output;
            document.getElementById('guide-yaml-benefits').innerHTML = tool.guide.benefits;
            document.querySelectorAll('#page-yaml-tool .guide-tab').forEach((t,i) => t.classList.toggle('active', i===0));
            document.querySelectorAll('#page-yaml-tool .guide-content').forEach((c,i) => c.classList.toggle('active', i===0));

            const optCard = document.getElementById('yamlOptionsCard');
            const optContent = document.getElementById('yamlOptionsContent');
            if (tool.options?.length) {
                optCard.style.display = 'block';
                optContent.innerHTML = tool.options.map(o => {
                    if (o.type === 'yaml_endpoint_picker') return `
                        <div class="option-group" id="yaml_endpoint_picker_wrap">
                          <label class="option-label" style="margin-bottom:6px;display:block;">🎯 Endpoint Selection <span style="font-weight:400;color:#888;font-size:11px;">(auto-detected on upload)</span></label>
                          <div style="display:flex;gap:8px;margin-bottom:8px;">
                            <button type="button" onclick="yamlSelectAll(true)"  class="btn btn-secondary" style="font-size:11px;padding:4px 12px;">Select All</button>
                            <button type="button" onclick="yamlSelectAll(false)" class="btn btn-secondary" style="font-size:11px;padding:4px 12px;">Clear All</button>
                            <button type="button" onclick="detectYamlEndpoints()" id="yamlDetectBtn" class="btn btn-secondary" style="font-size:11px;padding:4px 12px;">🔄 Re-scan</button>
                          </div>
                          <div id="yamlEndpointList" style="display:none;border:1px solid #d1e0f5;border-radius:8px;overflow:hidden;background:#f8fbff;max-height:340px;overflow-y:auto;"></div>
                          <div id="yamlEndpointNote" style="font-size:11px;color:#888;margin-top:6px;">Upload a YAML file — endpoints will be detected automatically.</div>
                        </div>`;
                    if (o.type === 'text') return `<div class="option-group"><label class="option-label">${o.label}</label><input type="text" class="option-input" id="yaml_${o.id}" placeholder="${o.placeholder||''}"></div>`;
                    if (o.type === 'select') return `<div class="option-group"><label class="option-label">${o.label}</label><select class="option-select" id="yaml_${o.id}">${o.options.map(x=>`<option value="${x.value}">${x.label}</option>`).join('')}</select></div>`;
                    return '';
                }).join('');
            } else { optCard.style.display = 'none'; }

            updateYamlRunButton();
            _fspResetPanel('yaml');
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById('page-yaml-tool').classList.add('active');
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.querySelector('.nav-item[data-page="yaml-tools"]')?.classList.add('active');
        }

        function updateYamlRunButton() {
            const btn = document.getElementById('runYamlToolBtn');
            if (btn) btn.disabled = uploadedYamlFiles.length < 1;
        }

        function resetYamlTool() {
            uploadedYamlFiles = [];
            document.getElementById('yamlFileInput').value = '';
            document.getElementById('yamlFileList').innerHTML = '';
            document.getElementById('yamlResultsSection').classList.remove('active');
            document.getElementById('yamlMessageBox').innerHTML = '';
            document.getElementById('yamlMessageBox').style.display = 'none';
            const epList = document.getElementById('yamlEndpointList');
            if (epList) { epList.style.display = 'none'; epList.innerHTML = ''; }
            const epNote = document.getElementById('yamlEndpointNote');
            if (epNote) epNote.textContent = 'Upload a YAML file — endpoints will be detected automatically.';
            updateYamlRunButton();
            _fspResetPanel('yaml');
        }

        function handleYamlFiles(files) {
            const valid = Array.from(files).filter(f => /\.(yaml|yml|json)$/i.test(f.name));
            if (!valid.length) { showYamlMessage('Please upload a .yaml, .yml, or .json file.', 'error'); return; }
            valid.forEach(f => { if (!uploadedYamlFiles.find(u => u.name === f.name)) uploadedYamlFiles.push(f); });
            renderYamlFileList();
            updateYamlRunButton();
            _rbMaybeAutoDetectYaml();
        }

        function renderYamlFileList() { _fspRenderStagedList('yaml'); }
        function removeYamlFile(i) { _fspRemove('yaml', i); }

        function _rbMaybeAutoDetectYaml() {
            if (!currentYamlTool || currentYamlTool.id !== 'yaml_api_extract') return;
            const hasYaml = uploadedYamlFiles.some(f => /\.(yaml|yml|json)$/i.test(f.name));
            if (!hasYaml) return;
            setTimeout(detectYamlEndpoints, 80);
        }

        async function detectYamlEndpoints() {
            const yamlFiles = uploadedYamlFiles.filter(f => /\.(yaml|yml|json)$/i.test(f.name));
            if (!yamlFiles.length) return;

            const btn  = document.getElementById('yamlDetectBtn');
            const list = document.getElementById('yamlEndpointList');
            const note = document.getElementById('yamlEndpointNote');
            if (!list) return;

            if (btn) btn.disabled = true;
            list.style.display = 'block';
            list.innerHTML = `
                <div style="padding:14px 16px;">
                    <div style="font-size:12px;color:#555;margin-bottom:8px;">
                        📄 Scanning <strong>${yamlFiles[0].name}</strong> for API endpoints…
                    </div>
                    <div style="background:#e2e8f0;border-radius:99px;height:8px;overflow:hidden;">
                        <div id="yamlProgressBar" style="height:100%;width:0%;background:linear-gradient(90deg,#0e7490,#10b981);border-radius:99px;transition:width 0.3s ease;"></div>
                    </div>
                    <div id="yamlProgressLabel" style="font-size:11px;color:#888;margin-top:6px;">Starting…</div>
                </div>`;

            const steps = [[25,'Parsing YAML…'],[55,'Resolving schemas…'],[80,'Detecting endpoints…'],[92,'Almost done…']];
            let si = 0;
            const ticker = setInterval(() => {
                if (si < steps.length) {
                    const [pct, msg] = steps[si++];
                    const b = document.getElementById('yamlProgressBar');
                    const l = document.getElementById('yamlProgressLabel');
                    if (b) b.style.width = pct + '%';
                    if (l) l.textContent = msg;
                }
            }, 500);

            const fd = new FormData();
            const f = yamlFiles[0];
            if (f._isLib) fd.append('library_path', f._libPath);
            else fd.append('files', f);

            try {
                const res  = await fetch('/detect_yaml_endpoints', { method: 'POST', body: fd });
                const data = await res.json();
                clearInterval(ticker);
                if (btn) btn.disabled = false;

                if (data.endpoints && data.endpoints.length > 0) {
                    const b = document.getElementById('yamlProgressBar');
                    const l = document.getElementById('yamlProgressLabel');
                    if (b) b.style.width = '100%';
                    if (l) l.textContent = `Found ${data.endpoints.length} endpoint(s)`;
                    await new Promise(r => setTimeout(r, 300));

                    const METHOD_COLORS = {
                        GET:['#16a34a','#d1fae5'], POST:['#2563eb','#dbeafe'],
                        PUT:['#d97706','#fef3c7'], PATCH:['#9333ea','#fae8ff'],
                        DELETE:['#dc2626','#fee2e2'], HEAD:['#0891b2','#e0f7fa'],
                        OPTIONS:['#64748b','#f1f5f9']
                    };
                    const byTag = {};
                    data.endpoints.forEach(ep => { const t = ep.tag || 'General'; (byTag[t] = byTag[t]||[]).push(ep); });

                    let html = '';
                    for (const [tag, eps] of Object.entries(byTag)) {
                        html += `<div style="padding:8px 14px 4px;font-size:11px;font-weight:700;color:#0e7490;background:#f0fdf9;border-bottom:1px solid #d0f4f1;letter-spacing:.5px;">${tag.toUpperCase()}</div>`;
                        eps.forEach(ep => {
                            const [tc, bc] = METHOD_COLORS[ep.method] || ['#374151','#f9fafb'];
                            html += `
                                <label class="ig-section-row" style="display:flex;align-items:center;gap:10px;padding:9px 14px;border-bottom:1px solid #e2eaf5;cursor:pointer;user-select:none;" onmouseover="this.style.background='#f0f7ff'" onmouseout="this.style.background=''">
                                    <input type="checkbox" value="${ep.id}" checked style="width:15px;height:15px;flex-shrink:0;cursor:pointer;">
                                    <span style="background:${bc};color:${tc};font-weight:700;font-size:10px;padding:2px 7px;border-radius:4px;min-width:52px;text-align:center;">${ep.method}</span>
                                    <span style="font-size:12px;color:#1e3a5f;font-family:monospace;flex:1;">${ep.path}</span>
                                    <span style="font-size:11px;color:#6b7280;max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${ep.summary||''}</span>
                                </label>`;
                        });
                    }
                    list.innerHTML = html;
                    if (note) note.textContent = `${data.endpoints.length} endpoint(s) detected — tick the ones to extract, or leave all checked to extract everything.`;
                    hideYamlMessage();
                } else if (data.error) {
                    list.style.display = 'none';
                    showYamlMessage('Endpoint detection error: ' + data.error, 'error');
                } else {
                    list.innerHTML = `<div style="padding:14px;color:#6b7280;font-size:12px;">No named endpoints found — the tool will process the full specification.</div>`;
                    if (note) note.textContent = 'No endpoints detected.';
                }
            } catch(e) {
                clearInterval(ticker);
                if (btn) btn.disabled = false;
                list.style.display = 'none';
                showYamlMessage('Detection failed: ' + e.message, 'error');
            }
        }

        function yamlSelectAll(checked) {
            document.querySelectorAll('#yamlEndpointList input[type=checkbox]').forEach(cb => cb.checked = checked);
        }

        async function runYamlTool() {
            if (!currentYamlTool || uploadedYamlFiles.length === 0) return;
            hideYamlMessage();
            document.getElementById('yamlResultsSection').classList.remove('active');
            document.getElementById('loadingOverlay').style.display = 'flex';
            document.getElementById('loadingSubtext').textContent = 'Running ' + currentYamlTool.title + '...';

            const fd = new FormData();
            fd.append('tool', currentYamlTool.id);
            const libPaths = [];
            uploadedYamlFiles.forEach(f => {
                if (f._isLib) libPaths.push(f._libPath);
                else fd.append('files', f);
            });
            if (libPaths.length) fd.append('library_files', JSON.stringify(libPaths));

            // Endpoint picker
            if (currentYamlTool.options?.some(o => o.type === 'yaml_endpoint_picker')) {
                const allCbs  = document.querySelectorAll('#yamlEndpointList input[type=checkbox]');
                const checked = Array.from(allCbs).filter(cb => cb.checked).map(cb => cb.value);
                if (checked.length > 0 && checked.length < allCbs.length) {
                    fd.append('filter_endpoints', checked.join(','));
                }
            }

            try {
                const res  = await fetch('/run', { method: 'POST', body: fd });
                const data = await res.json();
                document.getElementById('loadingOverlay').style.display = 'none';
                if (data.success) {
                    document.getElementById('yamlResultsSubtitle').textContent = data.message || 'Complete';
                    document.getElementById('yamlResultsFiles').innerHTML = (data.files || []).map(f => `
                        <li class="results-file-item">
                            <span class="results-file-icon">📊</span>
                            <span class="results-file-name">${f.name}</span>
                            <a href="/download/${f.name}" class="results-download-btn" download>⬇ Download</a>
                        </li>`).join('');
                    document.getElementById('yamlResultsSection').classList.add('active');
                } else {
                    showYamlMessage('Error: ' + (data.error || 'Unknown error'), 'error');
                }
            } catch(e) {
                document.getElementById('loadingOverlay').style.display = 'none';
                showYamlMessage('Network error: ' + e.message, 'error');
            }
        }

        function showYamlMessage(text, type) {
            const el = document.getElementById('yamlMessageBox');
            el.textContent = text;
            el.className = 'message message-' + (type || 'info');
            el.style.display = 'block';
        }
        function hideYamlMessage() {
            const el = document.getElementById('yamlMessageBox');
            if (el) { el.style.display = 'none'; el.textContent = ''; }
        }