"""Extract plain text from a resume (PDF, DOCX, TXT/MD) and flag ATS-unfriendly layout.

Usage: python extract_resume.py resume.pdf [--out work/source.txt]
Prints a short report to stderr and the text to stdout (or --out).
"""
import argparse
import logging
import pathlib
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.getLogger("pdfminer").setLevel(logging.ERROR)

ap = argparse.ArgumentParser()
ap.add_argument("path")
ap.add_argument("--out")
a = ap.parse_args()
p = pathlib.Path(a.path)
notes = []
ext = p.suffix.lower()

if ext == ".pdf":
    import pdfplumber
    with pdfplumber.open(p) as pdf:
        pages = pdf.pages
        text = "\n".join((pg.extract_text() or "") for pg in pages)
        notes.append(f"pages: {len(pages)}")
        # Two-column check: many words start in the right half while the left half also has text.
        sys.path.insert(0, str(pathlib.Path(__file__).parent))
        from _common import layout_flags
        tbl, cols = layout_flags(pdf)
        if cols:
            notes.append("multi-column layout (ATS risk)")
        if tbl:
            notes.append("tables found (ATS risk)")
        if len(text.split()) < 50:
            notes.append("very little extractable text: the PDF may be an image (ATS cannot read it)")
elif ext == ".docx":
    import docx
    d = docx.Document(p)
    parts = [para.text for para in d.paragraphs]
    for t in d.tables:
        notes.append("tables found (ATS risk)")
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
        break
    if d.sections and d.sections[0].header and any(par.text.strip() for par in d.sections[0].header.paragraphs):
        notes.append("text in page header: some ATS skip headers, keep contact details in the body")
    text = "\n".join(parts)
elif ext in (".txt", ".md"):
    text = p.read_text(encoding="utf-8", errors="replace")
else:
    sys.exit(f"Unsupported file type: {ext}. Use PDF, DOCX or TXT.")

words = len(text.split())
notes.append(f"words: {words}")
print("REPORT: " + "; ".join(notes), file=sys.stderr)
if a.out:
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(text, encoding="utf-8")
    print(f"wrote {a.out}", file=sys.stderr)
else:
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)
