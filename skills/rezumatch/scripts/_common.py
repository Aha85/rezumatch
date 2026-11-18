"""Shared helpers: find a Chromium browser, render HTML to PDF, read PDFs."""
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

logging.getLogger("pdfminer").setLevel(logging.ERROR)

CANDIDATES = [
    os.environ.get("RESUME_HELPER_CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]
NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "msedge", "chrome"]


def find_browser():
    for c in CANDIDATES:
        if c and pathlib.Path(c).exists():
            return c
    for n in NAMES:
        p = shutil.which(n)
        if p:
            return p
    return None


def render_pdf(html_path, out_pdf):
    """Render HTML to a temp PDF with headless Chromium. Returns the temp path."""
    html_path = pathlib.Path(html_path).resolve()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="rh_")) / "out.pdf"
    browser = find_browser()
    if browser:
        subprocess.run(
            [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             "--virtual-time-budget=10000", f"--print-to-pdf={tmp}", html_path.as_uri()],
            capture_output=True, timeout=120,
        )
    else:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            sys.exit("No Chrome, Edge or Chromium found, and Playwright is not installed. "
                     "Install Chrome, or run: pip install playwright && playwright install chromium")
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page()
            page.goto(html_path.as_uri(), wait_until="networkidle")
            page.pdf(path=str(tmp), prefer_css_page_size=True, print_background=True)
            b.close()
    if not tmp.exists() or tmp.stat().st_size == 0:
        sys.exit(f"PDF rendering failed for {html_path}")
    return tmp


def copy_out(tmp_pdf, target):
    """Copy the rendered PDF to target. If target is open/locked, write next to it and say so."""
    target = pathlib.Path(target)
    try:
        shutil.copy(tmp_pdf, target)
        return target
    except PermissionError:
        alt = target.with_name(target.stem + " (new)" + target.suffix)
        shutil.copy(tmp_pdf, alt)
        print(f"NOTE: {target.name} is open in another program. Saved as {alt.name}. "
              f"Close the file and run again to overwrite it.")
        return alt


def pdf_stats(pdf_path):
    """Pages, free space at the bottom of the last page (0-1), full text."""
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        pages = len(pdf.pages)
        text = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
        last = pdf.pages[-1]
        words = last.extract_words()
        bottom = max((w["bottom"] for w in words), default=0)
        free = (last.height - bottom) / last.height
    return pages, free, text


def layout_flags(pdf):
    """(has_real_table, multi_column) for an open pdfplumber PDF.
    Rules under headings are not tables; right-aligned dates are not a second column."""
    has_table = False
    for pg in pdf.pages:
        for t in pg.extract_tables():
            rows = [r for r in t if sum(1 for c in r if c and c.strip()) >= 2]
            if len(rows) >= 3:
                has_table = True
    pg = pdf.pages[0]
    words = pg.extract_words()
    covered = [0] * 100
    for w in words:
        for b in range(int(w["x0"] / pg.width * 100), min(99, int(w["x1"] / pg.width * 100)) + 1):
            covered[b] += 1
    multi = False
    run = 0
    for b in range(20, 70):
        run = run + 1 if covered[b] == 0 else 0
        if run >= 2:
            left = sum(1 for w in words if w["x1"] / pg.width * 100 <= b - run + 1)
            right = sum(1 for w in words if w["x0"] / pg.width * 100 >= b)
            if left >= 8 and right >= 15 and left >= 0.1 * len(words):  # a narrow sidebar is still a second column
                multi = True
                break
    if not multi:
        multi = _sidebar_lines(pg, words)
    return has_table, multi


def _sidebar_lines(pg, words):
    """Second check for a sidebar: the page has a second left margin (main column) at 25-70%
    of the width, and 3+ lines on the left side that all end before that margin."""
    from collections import defaultdict
    rows = defaultdict(list)
    for w in words:
        rows[round(w["top"] / 3)].append(w)
    lines = []  # text segments: a row split wherever the gap between words is wide
    for ws in rows.values():
        ws.sort(key=lambda w: w["x0"])
        seg = [ws[0]]
        for a, b in zip(ws, ws[1:]):
            if (b["x0"] - a["x1"]) / pg.width > 0.015:
                lines.append((seg[0]["x0"] / pg.width, seg[-1]["x1"] / pg.width))
                seg = []
            seg.append(b)
        lines.append((seg[0]["x0"] / pg.width, seg[-1]["x1"] / pg.width))
    starts = defaultdict(int)
    for x0, _ in lines:
        starts[round(x0 * 50)] += 1
    for b, n in starts.items():
        m = b / 50
        if n < 3 or not 0.25 <= m <= 0.7:
            continue
        left = [x1 for x0, x1 in lines if x0 < m - 0.05]
        if len(left) >= 3 and all(x1 < m for x1 in left):
            return True
    return False
