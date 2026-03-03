// ─── Rulebook Tools ───────────────────────────────────────────────────────────

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

// ─── Rulebook Tool State ──────────────────────────────────────────────────────
let currentRbTool = null, uploadedRbFiles = [];

// ─── renderRulebookToolsGrid ──────────────────────────────────────────────────
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

// ─── openRbTool ───────────────────────────────────────────────────────────────
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

// ─── _origShowPage patch (rulebook tool — detects IG sections when opening rb tool) ───
const _origShowPage = showPage;
showPage = function(pageId) {
    _origShowPage(pageId);
};

// ── IG Section Picker ──────────────────────────────────────────────────────────
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
// ── End IG Section Picker ──────────────────────────────────────────────────────
