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
