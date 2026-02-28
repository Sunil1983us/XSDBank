"""
PDF Merger / Splitter
  - Merge multiple PDFs into one
  - Split a PDF by page ranges, fixed chunk size, or bookmarks
  - Extract specific pages
"""

import os
import re
from pathlib import Path
from typing import Union

from pypdf import PdfReader, PdfWriter


# ── Merge ────────────────────────────────────────────────────────────────────

def merge_pdfs(input_paths: list[str], output_path: str) -> dict:
    """
    Merge a list of PDFs into a single PDF.

    Parameters
    ----------
    input_paths : list of file paths (str or Path)
    output_path : destination .pdf path

    Returns
    -------
    dict  {output_file, total_pages, files_merged}
    """
    output_path = Path(output_path)
    writer = PdfWriter()
    total_pages = 0
    files_merged = []

    for path in input_paths:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)
        total_pages += len(reader.pages)
        files_merged.append({"file": path.name, "pages": len(reader.pages)})

    with open(output_path, "wb") as f:
        writer.write(f)

    return {
        "output_file":  str(output_path),
        "total_pages":  total_pages,
        "files_merged": files_merged,
    }


# ── Split helpers ────────────────────────────────────────────────────────────

def _parse_ranges(range_str: str, max_page: int) -> list[tuple[int, int]]:
    """
    Parse a range string like "1-5,8,10-12" into list of (start, end) tuples
    (1-indexed, inclusive).
    """
    ranges = []
    for part in range_str.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(\d+)(?:\s*-\s*(\d+))?$", part)
        if not m:
            raise ValueError(f"Invalid range specification: '{part}'")
        start = int(m.group(1))
        end   = int(m.group(2)) if m.group(2) else start
        if start < 1 or end > max_page or start > end:
            raise ValueError(
                f"Range {start}-{end} is out of bounds (document has {max_page} pages)"
            )
        ranges.append((start, end))
    return ranges


def _write_range(reader: PdfReader, start: int, end: int, output_path: Path):
    """Write pages [start..end] (1-indexed) to output_path."""
    writer = PdfWriter()
    for i in range(start - 1, end):
        writer.add_page(reader.pages[i])
    with open(output_path, "wb") as f:
        writer.write(f)
    return end - start + 1


# ── Split ────────────────────────────────────────────────────────────────────

def split_pdf(
    input_path: str,
    output_dir: str,
    mode: str = "pages",           # "pages" | "ranges" | "chunks"
    ranges: str | None = None,     # e.g. "1-5,8,10-12" – used when mode="ranges"
    chunk_size: int = 1,           # used when mode="chunks" or mode="pages"
    prefix: str | None = None,     # output filename prefix
) -> dict:
    """
    Split a PDF.

    Parameters
    ----------
    input_path  : source PDF
    output_dir  : directory to write output files into
    mode        :
        "pages"  – one file per page  (chunk_size=1)
        "chunks" – fixed-size chunks  (chunk_size pages each)
        "ranges" – custom page ranges (provide `ranges` string)
    ranges      : comma-separated page ranges like "1-5,8,10-12"
    chunk_size  : pages per file when mode="chunks"
    prefix      : filename prefix; defaults to source stem

    Returns
    -------
    dict  {output_dir, files_created: [...]}
    """
    input_path  = Path(input_path)
    output_dir  = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    prefix    = prefix or input_path.stem
    reader    = PdfReader(str(input_path))
    total_pgs = len(reader.pages)
    files_created = []

    if mode == "ranges":
        if not ranges:
            raise ValueError("mode='ranges' requires a `ranges` string")
        parsed = _parse_ranges(ranges, total_pgs)
        for idx, (s, e) in enumerate(parsed, start=1):
            out = output_dir / f"{prefix}_range{idx:03d}_p{s}-p{e}.pdf"
            pages_written = _write_range(reader, s, e, out)
            files_created.append({
                "file": out.name, "pages": pages_written,
                "range": f"{s}-{e}"
            })

    elif mode in ("pages", "chunks"):
        size = 1 if mode == "pages" else max(1, chunk_size)
        for start in range(1, total_pgs + 1, size):
            end = min(start + size - 1, total_pgs)
            if size == 1:
                out = output_dir / f"{prefix}_page{start:04d}.pdf"
            else:
                out = output_dir / f"{prefix}_p{start:04d}-p{end:04d}.pdf"
            pages_written = _write_range(reader, start, end, out)
            files_created.append({
                "file": out.name, "pages": pages_written,
                "range": f"{start}-{end}"
            })
    else:
        raise ValueError(f"Unknown mode: {mode!r}. Use 'pages', 'chunks', or 'ranges'.")

    return {
        "output_dir":    str(output_dir),
        "source":        input_path.name,
        "total_pages":   total_pgs,
        "files_created": files_created,
    }


# ── Extract pages ─────────────────────────────────────────────────────────────

def extract_pages(input_path: str, page_range: str, output_path: str) -> dict:
    """
    Convenience wrapper: extract a page range from a PDF to a new file.

    Parameters
    ----------
    input_path  : source PDF
    page_range  : e.g. "2-10" or "5"
    output_path : destination .pdf
    """
    input_path  = Path(input_path)
    output_path = Path(output_path)
    reader      = PdfReader(str(input_path))
    total_pgs   = len(reader.pages)

    parsed = _parse_ranges(page_range, total_pgs)
    if len(parsed) != 1:
        raise ValueError("extract_pages expects a single range, e.g. '2-10'")
    start, end = parsed[0]

    pages_written = _write_range(reader, start, end, output_path)
    return {
        "output_file": str(output_path),
        "pages":       pages_written,
        "range":       f"{start}-{end}",
    }


# ── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, json, argparse

    parser = argparse.ArgumentParser(description="PDF Merger / Splitter")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # merge
    m = sub.add_parser("merge", help="Merge multiple PDFs")
    m.add_argument("inputs", nargs="+")
    m.add_argument("-o", "--output", required=True)

    # split
    s = sub.add_parser("split", help="Split a PDF")
    s.add_argument("input")
    s.add_argument("-d", "--outdir",  default="split_output")
    s.add_argument("--mode",          default="pages",
                   choices=["pages", "chunks", "ranges"])
    s.add_argument("--ranges",        default=None)
    s.add_argument("--chunk-size",    type=int, default=1)
    s.add_argument("--prefix",        default=None)

    # extract
    e = sub.add_parser("extract", help="Extract page range")
    e.add_argument("input")
    e.add_argument("range",  help='e.g. "2-10"')
    e.add_argument("-o", "--output", required=True)

    args = parser.parse_args()

    if args.cmd == "merge":
        result = merge_pdfs(args.inputs, args.output)
    elif args.cmd == "split":
        result = split_pdf(
            args.input, args.outdir,
            mode=args.mode, ranges=args.ranges,
            chunk_size=args.chunk_size, prefix=args.prefix,
        )
    else:
        result = extract_pages(args.input, args.range, args.output)

    print(json.dumps(result, indent=2))
