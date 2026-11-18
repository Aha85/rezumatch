"""Fill the page: find the largest body font that keeps the target page count,
then add section spacing until the bottom gap is small. Writes the final PDF.

The HTML must define CSS variables --fs (body font, pt) and --gap (section gap, pt) on :root.

Usage: python fit_page.py work/resume.html "Out/Jane Doe Resume.pdf" [--pages 1] [--min 9.5] [--max 11.5]
"""
import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import copy_out, pdf_stats, render_pdf  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("html")
ap.add_argument("pdf")
ap.add_argument("--pages", type=int, default=1)
ap.add_argument("--min", type=float, default=9.5)
ap.add_argument("--max", type=float, default=11.5)
ap.add_argument("--target-free", type=float, default=0.06)
a = ap.parse_args()

html = pathlib.Path(a.html)
src = html.read_text(encoding="utf-8")
if "--fs:" not in src or "--gap:" not in src:
    sys.exit("FAIL: the HTML needs --fs and --gap CSS variables on :root (use a resume-helper template).")


def render(fs, gap):
    txt = re.sub(r"--fs:\s*[\d.]+pt", f"--fs:{fs}pt", src)
    txt = re.sub(r"--gap:\s*[\d.]+pt", f"--gap:{gap}pt", txt)
    html.write_text(txt, encoding="utf-8")
    tmp = render_pdf(html, None)
    pages, free, _ = pdf_stats(tmp)
    return tmp, pages, free


sizes = []
s = a.max
while s >= a.min - 1e-9:
    sizes.append(round(s, 1))
    s -= 0.2

best = None
for fs in sizes:
    tmp, pages, free = render(fs, 7)
    print(f"try font {fs}pt: {pages} page(s), {free:.0%} empty at bottom")
    if pages <= a.pages:
        best = fs
        break

if best is None:
    render(a.min, 7)
    sys.exit(f"FAIL: does not fit {a.pages} page(s) even at {a.min}pt. Cut content: "
             "shorten the summary, merge or drop the weakest bullets, or drop the oldest role.")

gap = 7
while free > a.target_free and gap < 14:
    t2, p2, f2 = render(best, gap + 1)
    if p2 > a.pages:
        break
    gap, tmp, free = gap + 1, t2, f2

tmp, pages, free = render(best, gap)
out = copy_out(tmp, a.pdf)
print(f"OK font={best}pt gap={gap}pt pages={pages} empty_bottom={free:.0%} -> {out}")
