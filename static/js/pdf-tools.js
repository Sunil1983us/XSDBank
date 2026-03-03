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
