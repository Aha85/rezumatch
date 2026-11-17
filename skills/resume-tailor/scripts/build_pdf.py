"""Export an HTML document (cover letter, or a resume that is already fitted) to PDF.

Usage: python build_pdf.py work/cover-letter.html "Out/Jane Doe Cover Letter.pdf" [--pages 1]
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import copy_out, pdf_stats, render_pdf  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("html")
ap.add_argument("pdf")
ap.add_argument("--pages", type=int, default=1)
a = ap.parse_args()

tmp = render_pdf(a.html, None)
pages, free, text = pdf_stats(tmp)
if pages > a.pages:
    sys.exit(f"FAIL: {pages} pages, target is {a.pages}. Shorten the text and try again.")
if len(text.split()) < 30:
    sys.exit("FAIL: almost no text could be extracted from the PDF. Check that fonts loaded.")
out = copy_out(tmp, a.pdf)
print(f"OK pages={pages} words={len(text.split())} -> {out}")
