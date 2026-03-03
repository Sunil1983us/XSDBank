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

function showLoading(t) { document.getElementById('loadingSubtext').textContent = t; document.getElementById('loadingOverlay').classList.add('active'); }
function hideLoading() { document.getElementById('loadingOverlay').classList.remove('active'); }
function showMessage(t, type) { const b = document.getElementById('messageBox'); b.textContent = t; b.className = 'message active ' + type; }
function hideMessage() { document.getElementById('messageBox').className = 'message'; }

document.addEventListener('DOMContentLoaded', () => renderToolsGrid());
