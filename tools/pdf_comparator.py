"""
PDF Comparator
Compares two PDFs – text content, structure, tables – and produces
a detailed HTML diff report styled to match the ISO Toolkit theme.
"""

import os
import re
import html
import hashlib
from pathlib import Path
from datetime import datetime

import pdfplumber
from pypdf import PdfReader


# ── helpers ──────────────────────────────────────────────────────────────────

def _clean(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def _page_text(pdf_path):
    """Return list of cleaned text strings, one per page."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages.append(_clean(page.extract_text() or ""))
    return pages


def _page_tables(pdf_path):
    """Return {page_num: [table, ...]} where each table is list-of-rows."""
    result = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables() or []
            cleaned = []
            for t in tables:
                cleaned.append([[_clean(c) for c in row] for row in t])
            if cleaned:
                result[i] = cleaned
    return result


def _metadata(pdf_path):
    reader = PdfReader(str(pdf_path))
    m = reader.metadata or {}
    return {
        "title":    m.get("/Title",    ""),
        "author":   m.get("/Author",   ""),
        "creator":  m.get("/Creator",  ""),
        "subject":  m.get("/Subject",  ""),
        "pages":    len(reader.pages),
    }


def _diff_lines(text_a, text_b):
    """
    Word-level diff between two texts.
    Returns list of (tag, word) where tag is 'eq'|'del'|'ins'.
    Simple LCS-based approach.
    """
    words_a = text_a.split()
    words_b = text_b.split()

    # Build LCS table
    m, n = len(words_a), len(words_b)
    # For large texts, chunk to avoid memory issues
    if m > 2000 or n > 2000:
        # fall back to paragraph-level diff
        return _paragraph_diff(text_a, text_b)

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if words_a[i-1] == words_b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    result = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and words_a[i-1] == words_b[j-1]:
            result.append(("eq", words_a[i-1]))
            i -= 1; j -= 1
        elif j > 0 and (i == 0 or dp[i][j-1] >= dp[i-1][j]):
            result.append(("ins", words_b[j-1]))
            j -= 1
        else:
            result.append(("del", words_a[i-1]))
            i -= 1
    result.reverse()
    return result


def _paragraph_diff(text_a, text_b):
    """Fallback line-level diff for long texts."""
    lines_a = text_a.splitlines()
    lines_b = text_b.splitlines()
    result = []
    set_b = set(lines_b)
    set_a = set(lines_a)
    for line in lines_a:
        tag = "eq" if line in set_b else "del"
        result.append((tag, line))
    for line in lines_b:
        if line not in set_a:
            result.append(("ins", line))
    return result


def _render_diff(diff_tokens):
    """Convert diff tokens to HTML spans."""
    parts = []
    for tag, word in diff_tokens:
        w = html.escape(word)
        if tag == "eq":
            parts.append(f'<span class="eq">{w}</span>')
        elif tag == "del":
            parts.append(f'<span class="del">{w}</span>')
        else:
            parts.append(f'<span class="ins">{w}</span>')
    return " ".join(parts)


def _table_to_html(table, css_class=""):
    rows_html = []
    for i, row in enumerate(table):
        tag = "th" if i == 0 else "td"
        cells = "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in row)
        rows_html.append(f"<tr>{cells}</tr>")
    return f'<table class="data-table {css_class}">{"".join(rows_html)}</table>'


def _similarity(text_a, text_b):
    if not text_a and not text_b:
        return 100.0
    if not text_a or not text_b:
        return 0.0
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    if not words_a and not words_b:
        return 100.0
    intersection = words_a & words_b
    union = words_a | words_b
    return round(100 * len(intersection) / len(union), 1)


# ── main comparison ──────────────────────────────────────────────────────────

def compare_pdfs(pdf_a: str, pdf_b: str, output_path: str | None = None) -> dict:
    """
    Compare two PDFs and produce an HTML report.

    Returns result dict with output_file, summary stats.
    """
    pdf_a, pdf_b = Path(pdf_a), Path(pdf_b)
    for p in (pdf_a, pdf_b):
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")

    if output_path is None:
        output_path = pdf_a.parent / f"compare_{pdf_a.stem}_vs_{pdf_b.stem}.html"
    output_path = Path(output_path)

    meta_a = _metadata(pdf_a)
    meta_b = _metadata(pdf_b)
    pages_a = _page_text(pdf_a)
    pages_b = _page_text(pdf_b)
    tables_a = _page_tables(pdf_a)
    tables_b = _page_tables(pdf_b)

    max_pages = max(meta_a["pages"], meta_b["pages"])
    min_pages = min(meta_a["pages"], meta_b["pages"])

    # Per-page similarity scores
    page_sims = []
    for i in range(min_pages):
        page_sims.append(_similarity(pages_a[i], pages_b[i]))

    overall_sim = round(sum(page_sims) / len(page_sims), 1) if page_sims else 0.0

    # Count changed / added / removed pages
    changed_pages  = sum(1 for s in page_sims if s < 99.0)
    identical_pages = sum(1 for s in page_sims if s >= 99.0)
    extra_in_b = meta_b["pages"] - meta_a["pages"]

    # ── Build HTML ──────────────────────────────────────────────────────────
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    page_sections = []
    for i in range(max_pages):
        pg = i + 1
        txt_a = pages_a[i] if i < len(pages_a) else ""
        txt_b = pages_b[i] if i < len(pages_b) else ""
        sim   = page_sims[i] if i < len(page_sims) else 0.0

        if sim >= 99.0:
            badge = '<span class="badge identical">Identical</span>'
        elif sim >= 70.0:
            badge = f'<span class="badge similar">Similar ({sim}%)</span>'
        else:
            badge = f'<span class="badge changed">Changed ({sim}%)</span>'

        if i >= len(pages_a):
            badge = '<span class="badge added">Added in B</span>'
        elif i >= len(pages_b):
            badge = '<span class="badge removed">Only in A</span>'

        # Text diff
        diff_html = ""
        if txt_a or txt_b:
            diff = _diff_lines(txt_a, txt_b)
            diff_html = _render_diff(diff)

        # Table comparison
        t_a = tables_a.get(pg, [])
        t_b = tables_b.get(pg, [])
        table_html = ""
        if t_a or t_b:
            tbl_parts = []
            max_t = max(len(t_a), len(t_b))
            for ti in range(max_t):
                ta_html = _table_to_html(t_a[ti], "tbl-a") if ti < len(t_a) else "<em>—</em>"
                tb_html = _table_to_html(t_b[ti], "tbl-b") if ti < len(t_b) else "<em>—</em>"
                tbl_parts.append(f"""
                <div class="table-compare">
                  <div class="tbl-panel"><h5>PDF A – Table {ti+1}</h5>{ta_html}</div>
                  <div class="tbl-panel"><h5>PDF B – Table {ti+1}</h5>{tb_html}</div>
                </div>""")
            table_html = "".join(tbl_parts)

        collapsed = "collapsed" if sim >= 99.0 else ""
        page_sections.append(f"""
        <div class="page-section {collapsed}" id="pg{pg}">
          <div class="page-header" onclick="toggle('pg{pg}')">
            <span class="pg-num">Page {pg}</span>
            {badge}
            <span class="pg-toggle">▾</span>
          </div>
          <div class="page-body">
            <div class="diff-box">{diff_html or "<em class='muted'>No text content</em>"}</div>
            {f'<div class="tables-section"><h4>Tables</h4>{table_html}</div>' if table_html else ""}
          </div>
        </div>""")

    # Metadata rows
    def meta_row(label, va, vb):
        diff_cls = "meta-diff" if va != vb else ""
        return f'<tr class="{diff_cls}"><td>{label}</td><td>{html.escape(str(va))}</td><td>{html.escape(str(vb))}</td></tr>'

    meta_html = "".join([
        meta_row("Pages",   meta_a["pages"],   meta_b["pages"]),
        meta_row("Title",   meta_a["title"],   meta_b["title"]),
        meta_row("Author",  meta_a["author"],  meta_b["author"]),
        meta_row("Creator", meta_a["creator"], meta_b["creator"]),
        meta_row("Subject", meta_a["subject"], meta_b["subject"]),
    ])

    sim_color = "#27ae60" if overall_sim >= 90 else "#e67e22" if overall_sim >= 70 else "#e74c3c"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PDF Comparison Report</title>
<style>
  :root {{
    --navy: #1F3864; --blue: #2E74B5; --light: #D9E1F2;
    --ins: #d4edda; --ins-border: #28a745;
    --del: #f8d7da; --del-border: #dc3545;
    --eq: inherit;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: Arial, sans-serif; font-size: 13px; background: #f4f6fb; color: #222; }}
  header {{ background: var(--navy); color: white; padding: 18px 32px; }}
  header h1 {{ font-size: 20px; }}
  header p  {{ font-size: 12px; opacity: .7; margin-top: 4px; }}
  .container {{ max-width: 1400px; margin: 0 auto; padding: 24px 20px; }}

  /* Summary cards */
  .summary {{ display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 24px; }}
  .card {{ background: white; border-radius: 8px; padding: 16px 22px;
           box-shadow: 0 1px 4px rgba(0,0,0,.1); flex: 1; min-width: 140px; text-align: center; }}
  .card .val {{ font-size: 28px; font-weight: bold; color: var(--navy); }}
  .card .lbl {{ font-size: 11px; color: #666; margin-top: 4px; }}

  /* Metadata table */
  .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 28px; background: white;
                 border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
  .meta-table th {{ background: var(--navy); color: white; padding: 8px 14px; font-size: 12px; text-align: left; }}
  .meta-table td {{ padding: 7px 14px; border-bottom: 1px solid #eee; font-size: 12px; }}
  .meta-diff td {{ background: #fff3cd; }}

  /* Badges */
  .badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; }}
  .badge.identical {{ background:#d4edda; color:#155724; }}
  .badge.similar   {{ background:#fff3cd; color:#856404; }}
  .badge.changed   {{ background:#f8d7da; color:#721c24; }}
  .badge.added     {{ background:#cce5ff; color:#004085; }}
  .badge.removed   {{ background:#e2e3e5; color:#383d41; }}

  /* Page sections */
  .page-section {{ background: white; border-radius: 8px; margin-bottom: 12px;
                   box-shadow: 0 1px 4px rgba(0,0,0,.1); overflow: hidden; }}
  .page-header  {{ display: flex; align-items: center; gap: 12px; padding: 12px 18px;
                   cursor: pointer; user-select: none; background: #f8f9ff;
                   border-bottom: 1px solid #e2e8f0; }}
  .page-header:hover {{ background: var(--light); }}
  .pg-num  {{ font-weight: bold; color: var(--navy); min-width: 60px; }}
  .pg-toggle {{ margin-left: auto; font-size: 16px; color: var(--blue); transition: transform .2s; }}
  .page-section.collapsed .page-body {{ display: none; }}
  .page-section.collapsed .pg-toggle {{ transform: rotate(-90deg); }}
  .page-body {{ padding: 16px 18px; }}

  /* Diff */
  .diff-box {{ font-size: 12px; line-height: 1.8; word-wrap: break-word;
               border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px; background: #fafbff; }}
  span.del {{ background: var(--del); color: #721c24; text-decoration: line-through;
              border-radius: 3px; padding: 0 2px; }}
  span.ins {{ background: var(--ins); color: #155724; border-radius: 3px; padding: 0 2px; }}
  span.eq  {{ color: #444; }}
  .muted   {{ color: #aaa; font-style: italic; }}

  /* Tables */
  .tables-section {{ margin-top: 16px; }}
  .tables-section h4 {{ color: var(--navy); margin-bottom: 10px; font-size: 13px; }}
  .table-compare {{ display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }}
  .tbl-panel {{ flex: 1; min-width: 300px; overflow-x: auto; }}
  .tbl-panel h5 {{ font-size: 11px; color: #666; margin-bottom: 6px; }}
  table.data-table {{ border-collapse: collapse; font-size: 11px; width: 100%; }}
  table.data-table th {{ background: var(--navy); color: white; padding: 5px 8px; text-align: left; }}
  table.data-table td {{ padding: 4px 8px; border: 1px solid #e0e6f0; vertical-align: top; }}
  table.tbl-a th {{ background: #2E74B5; }}
  table.tbl-b th {{ background: #27ae60; }}
  tr:nth-child(even) td {{ background: #f4f6fb; }}

  /* Section titles */
  h2 {{ color: var(--navy); font-size: 15px; margin-bottom: 14px; border-left: 4px solid var(--blue);
        padding-left: 10px; }}
  .section {{ margin-bottom: 32px; }}
</style>
</head>
<body>
<header>
  <h1>📄 PDF Comparison Report</h1>
  <p>Generated: {now}</p>
</header>
<div class="container">

  <!-- Summary cards -->
  <div class="summary">
    <div class="card">
      <div class="val" style="color:{sim_color}">{overall_sim}%</div>
      <div class="lbl">Overall Similarity</div>
    </div>
    <div class="card">
      <div class="val">{meta_a['pages']}</div>
      <div class="lbl">Pages in PDF A</div>
    </div>
    <div class="card">
      <div class="val">{meta_b['pages']}</div>
      <div class="lbl">Pages in PDF B</div>
    </div>
    <div class="card">
      <div class="val" style="color:#27ae60">{identical_pages}</div>
      <div class="lbl">Identical Pages</div>
    </div>
    <div class="card">
      <div class="val" style="color:#e67e22">{changed_pages}</div>
      <div class="lbl">Changed Pages</div>
    </div>
    <div class="card">
      <div class="val" style="color:#2E74B5">{abs(extra_in_b)}</div>
      <div class="lbl">{'Extra Pages in B' if extra_in_b>0 else 'Extra Pages in A' if extra_in_b<0 else 'Same Page Count'}</div>
    </div>
  </div>

  <!-- File info -->
  <div class="section">
    <h2>Document Metadata</h2>
    <table class="meta-table">
      <tr>
        <th>Property</th>
        <th>📄 PDF A – {html.escape(pdf_a.name)}</th>
        <th>📄 PDF B – {html.escape(pdf_b.name)}</th>
      </tr>
      {meta_html}
    </table>
  </div>

  <!-- Page diff -->
  <div class="section">
    <h2>Page-by-Page Comparison
      <small style="font-size:11px;font-weight:normal;color:#666;margin-left:8px">
        (Identical pages are collapsed – click to expand)
      </small>
    </h2>
    {"".join(page_sections)}
  </div>

</div>
<script>
function toggle(id) {{
  document.getElementById(id).classList.toggle('collapsed');
}}
// Collapse all identical pages by default (already done in HTML class)
</script>
</body>
</html>"""

    output_path.write_text(html_content, encoding="utf-8")

    return {
        "output_file":       str(output_path),
        "overall_similarity": overall_sim,
        "pages_a":            meta_a["pages"],
        "pages_b":            meta_b["pages"],
        "identical_pages":    identical_pages,
        "changed_pages":      changed_pages,
    }


# ── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 3:
        print("Usage: python pdf_comparator.py <a.pdf> <b.pdf> [output.html]")
        sys.exit(1)
    out = sys.argv[3] if len(sys.argv) > 3 else None
    result = compare_pdfs(sys.argv[1], sys.argv[2], out)
    print(json.dumps(result, indent=2))
