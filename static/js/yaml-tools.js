const yamlTools = [
    {
        id: 'yaml_json_explorer', icon: '◈', title: 'YAML / JSON Explorer', badge: 'New',
        description: 'Interactive visual explorer for YAML and JSON files — collapsible tree with type colour-coding, JSONPath copy, statistics panel, and an Excel flat-structure report.',
        features: ['Interactive tree', 'Type colour-coding', 'JSONPath copy', 'Statistics & heatmap'],
        input: 'Upload 1 YAML or JSON file', minFiles: 1, options: null,
        guide: {
            when: '<h4>📌 When to Use This Tool</h4><p>Use YAML / JSON Explorer when you need to:</p><ul><li>Visually browse deeply nested YAML or JSON configuration files</li><li>Understand the structure of an OpenAPI spec, config file, or API response payload</li><li>Copy exact JSONPath expressions for any key in the document</li><li>Analyse type distribution, largest arrays, and most frequent keys at a glance</li><li>Share a self-contained interactive HTML explorer with your team</li></ul>',
            how: '<h4>📖 How to Use</h4><p><strong>Step 1:</strong> Upload a <code>.yaml</code>, <code>.yml</code>, or <code>.json</code> file.</p><p><strong>Step 2:</strong> Click <strong>"Run Tool"</strong>.</p><p><strong>Step 3:</strong> Click <strong>Preview</strong> on the HTML file to open the interactive explorer.</p><p><strong>Step 4:</strong> Download the Excel file for a flat structure report.</p><p><strong>Tips:</strong></p><ul><li>Use <strong>Expand / Collapse</strong> buttons or type <strong>L1/L2/L3</strong> to jump to depth levels.</li><li>Click any node in the tree to see its full value and JSONPath in the right panel.</li><li>Use the <strong>filter buttons</strong> (Objects / Arrays / Strings…) to isolate node types.</li></ul>',
            output: '<h4>📦 Output Files</h4><div class="output-files"><div class="output-file"><span class="output-file-icon">🌐</span><span class="output-file-name">*_explorer.html</span><span class="output-file-desc">— Self-contained interactive tree &amp; statistics explorer</span></div><div class="output-file"><span class="output-file-icon">📊</span><span class="output-file-name">*_structure.xlsx</span><span class="output-file-desc">— Flat structure report with JSONPath, type, depth &amp; value</span></div></div><p style="margin-top:16px;">The HTML file works offline and can be shared without any dependencies.</p>',
            benefits: '<h4>✨ Key Benefits</h4><div class="guide-benefits"><div class="guide-benefit"><div class="guide-benefit-title">Type Colour Coding</div><div class="guide-benefit-text">Object, Array, String, Number, Boolean and Null — each a distinct colour</div></div><div class="guide-benefit"><div class="guide-benefit-title">JSONPath Copy</div><div class="guide-benefit-text">One-click copy of the full JSONPath for any node</div></div><div class="guide-benefit"><div class="guide-benefit-title">Statistics Panel</div><div class="guide-benefit-text">Type distribution, largest arrays, most frequent key names</div></div><div class="guide-benefit"><div class="guide-benefit-title">Works with YAML &amp; JSON</div><div class="guide-benefit-text">Auto-detects format — handles OpenAPI specs, configs, payloads</div></div></div>'
        }
    },
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
            document.getElementById('yamlResultsFiles').innerHTML = (data.files || []).map(f => {
                const isHtml = /\.html$/i.test(f.name);
                const icon   = isHtml ? '🌐' : /\.xlsx$/i.test(f.name) ? '📊' : '📁';
                const preview = isHtml ? `<a href="/preview/${f.name}" target="_blank" class="results-file-btn preview">Preview</a>` : '';
                return `<li class="results-file">
                    <span class="results-file-icon">${icon}</span>
                    <span class="results-file-name">${f.name}</span>
                    <div class="results-file-actions">${preview}<a href="/download/${f.name}" class="results-file-btn download">Download</a></div>
                </li>`;
            }).join('');
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
