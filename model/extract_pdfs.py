"""Phase 1: extract the OWASP source PDFs into a clean, tracked knowledge store.

The raw PDFs under ``docs/owasp-pdfs/`` are large binaries kept out of git. This
script converts each one into a lightweight Markdown file under ``model/knowledge/``
that is committed and reviewable, and which doubles as the runtime RAG corpus for
the hybrid "Nora" assistant (facts live here, not baked into the 0.5B weights).

What it does per PDF:
  * extracts text page-by-page with PyMuPDF (``fitz``);
  * removes recurring header/footer lines (page furniture that repeats across the
    document) and bare page numbers;
  * promotes OWASP-style section identifiers (LLM01, ASI01, T01, numbered headings,
    ALL-CAPS titles) to Markdown headings so the text is section-navigable;
  * writes ``model/knowledge/<slug>.md`` with a small provenance header.

It also writes ``model/knowledge/README.md`` indexing every extracted document.

Usage:
    python model/extract_pdfs.py
    python model/extract_pdfs.py --src docs/owasp-pdfs --out model/knowledge
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
from collections import Counter
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "PyMuPDF (fitz) is required: pip install pymupdf"
    ) from exc

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = ROOT / "docs" / "owasp-pdfs"
DEFAULT_OUT = ROOT / "model" / "knowledge"

# Section identifiers used across the OWASP GenAI/LLM/Agentic material.
_SECTION_ID = re.compile(
    r"^(LLM\d{1,2}|ASI\d{1,2}|T\d{1,3}|DSGAI\d{1,2}|AITG[-\w]*|MC\d{1,2})\b[:.\s-]",
    re.IGNORECASE,
)
_NUMBERED_HEADING = re.compile(r"^\d{1,2}(\.\d{1,2}){0,3}\s+[A-Z]")
_PAGE_NUMBER = re.compile(r"^\s*(page\s+)?\d{1,4}(\s*/\s*\d{1,4})?\s*$", re.IGNORECASE)


def _slug(name: str) -> str:
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem)
    return stem.strip("-")


def _page_lines(page: "fitz.Page") -> list[str]:
    text = page.get_text("text")
    return [ln.rstrip() for ln in text.splitlines()]


def _find_repeating_furniture(pages: list[list[str]], min_fraction: float = 0.4) -> set[str]:
    """Lines that appear on >= min_fraction of pages are treated as header/footer."""
    if len(pages) < 4:
        return set()
    counts: Counter[str] = Counter()
    for lines in pages:
        # only the first/last few lines of each page can be furniture
        candidates = {ln.strip() for ln in (lines[:3] + lines[-3:]) if ln.strip()}
        for ln in candidates:
            counts[ln] += 1
    threshold = max(3, int(len(pages) * min_fraction))
    return {ln for ln, c in counts.items() if c >= threshold and len(ln) < 120}


def _clean_lines(lines: list[str], furniture: set[str]) -> list[str]:
    out: list[str] = []
    blank = False
    for ln in lines:
        s = ln.strip()
        if not s:
            if not blank and out:
                out.append("")
            blank = True
            continue
        blank = False
        if s in furniture or _PAGE_NUMBER.match(s):
            continue
        out.append(s)
    return out


def _promote_headings(lines: list[str]) -> list[str]:
    out: list[str] = []
    for ln in lines:
        if not ln:
            out.append(ln)
            continue
        is_id = bool(_SECTION_ID.match(ln))
        is_num = bool(_NUMBERED_HEADING.match(ln))
        is_caps = ln.isupper() and 3 <= len(ln) <= 80 and any(c.isalpha() for c in ln)
        if is_id or is_num:
            out.append(f"## {ln}")
        elif is_caps:
            out.append(f"### {ln.title()}")
        else:
            out.append(ln)
    return out


def extract_pdf(path: Path) -> tuple[str, int]:
    doc = fitz.open(path)
    pages = [_page_lines(p) for p in doc]
    page_count = len(pages)
    furniture = _find_repeating_furniture(pages)

    body: list[str] = []
    for idx, lines in enumerate(pages, start=1):
        cleaned = _clean_lines(lines, furniture)
        if not any(cleaned):
            continue
        cleaned = _promote_headings(cleaned)
        body.append(f"<!-- page {idx} -->")
        body.extend(cleaned)
        body.append("")
    doc.close()

    title = _guess_title(pages)
    header = (
        f"# {title}\n\n"
        f"> Source: `{path.name}` ({page_count} pages). "
        f"Extracted {_dt.date.today().isoformat()} for the Nora knowledge store.\n"
        f"> Raw PDF is gitignored; this Markdown is the tracked, reviewable copy.\n"
    )
    text = header + "\n" + "\n".join(body).strip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, page_count


def _guess_title(pages: list[list[str]]) -> str:
    for lines in pages[:2]:
        for ln in lines:
            s = ln.strip()
            if len(s) >= 8 and any(c.isalpha() for c in s):
                return s
    return "OWASP source document"


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract OWASP PDFs into the Nora knowledge store")
    ap.add_argument("--src", default=str(DEFAULT_SRC), help="directory of source PDFs")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output directory for Markdown")
    args = ap.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    if not src.is_dir():
        raise SystemExit(f"source directory not found: {src}")
    out.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(src.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"no PDFs found in {src}")

    index: list[tuple[str, str, int]] = []
    for pdf in pdfs:
        try:
            text, pages = extract_pdf(pdf)
        except Exception as exc:  # keep going on a single bad file
            print(f"  FAILED {pdf.name}: {exc}")
            continue
        slug = _slug(pdf.name)
        dest = out / f"{slug}.md"
        dest.write_text(text, encoding="utf-8")
        words = len(text.split())
        index.append((slug, pdf.name, pages))
        print(f"  {pdf.name} -> {dest.name} ({pages} pages, {words} words)")

    _write_index(out, index)
    print(f"\nExtracted {len(index)} documents to {out}")


def _write_index(out: Path, index: list[tuple[str, str, int]]) -> None:
    lines = [
        "# Nora knowledge store",
        "",
        "Markdown extracted from the OWASP source PDFs (`docs/owasp-pdfs/`, gitignored).",
        "This is the tracked, reviewable RAG corpus for the Nora assistant. Regenerate with",
        "`python model/extract_pdfs.py`.",
        "",
        "| Document | Source PDF | Pages |",
        "| --- | --- | --- |",
    ]
    for slug, src_name, pages in sorted(index):
        lines.append(f"| [{slug}]({slug}.md) | `{src_name}` | {pages} |")
    lines.append("")
    (out / "README.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
