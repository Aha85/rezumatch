"""Estimated ATS match score (0-100) for a resume against a job listing.

Usage:
  python ats_score.py --resume "Out/Jane Doe Resume.pdf" --keywords work/jd_keywords.json [--judgment work/judgment.json] [--json]

work/jd_keywords.json (Claude writes it from the listing):
  {"title": "Director of GenAI Operations",
   "keywords": [{"term": "python", "aliases": ["py"], "weight": 2}, {"term": "change management", "weight": 1}]}
  weight: 2 = required / repeated in the listing, 1 = mentioned once.

work/judgment.json (Claude's judgment, things a script can't measure):
  {"experience": 13, "soft": 8}      # experience/seniority out of 15, soft skills out of 10

The script measures keywords, title, format and measurable results. It is an estimate: real ATS
products differ, and many only rank and filter for a human. Always present it as "estimated".
"""
import argparse
import html as htmlmod
import json
import logging
import pathlib
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.getLogger("pdfminer").setLevel(logging.ERROR)

ap = argparse.ArgumentParser()
ap.add_argument("--resume", required=True)
ap.add_argument("--keywords", required=True)
ap.add_argument("--judgment")
ap.add_argument("--json", action="store_true")
a = ap.parse_args()

rp = pathlib.Path(a.resume)
pages, has_table, columns = 1, False, False
if rp.suffix.lower() == ".pdf":
    import pdfplumber
    with pdfplumber.open(rp) as pdf:
        pages = len(pdf.pages)
        text = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
        sys.path.insert(0, str(pathlib.Path(__file__).parent))
        from _common import layout_flags
        has_table, columns = layout_flags(pdf)
elif rp.suffix.lower() in (".html", ".htm"):
    raw = rp.read_text(encoding="utf-8")
    has_table = "<table" in raw.lower()
    raw = re.sub(r"(?is)<(style|script)\b.*?</\1>", " ", raw)
    text = htmlmod.unescape(re.sub(r"(?s)<[^>]+>", "\n", raw))
else:
    text = rp.read_text(encoding="utf-8", errors="replace")

def _norm(s):
    s = re.sub(r"[,.;:!?](?=\s|$)", " ", s.lower())
    return " " + re.sub(r"\s+", " ", re.sub(r"[^\w$%+#./-]+", " ", s)).strip() + " "


norm = _norm(text)
kw = json.loads(pathlib.Path(a.keywords).read_text(encoding="utf-8"))


def present(term):
    """Whole-word match. Most ATS also match simple plurals, so "expansion" finds "expansions"
    and "QBRs" finds "QBR"."""
    t = _norm(term).strip()
    if not t:
        return False
    forms = {t, t + "s", t + "es"}
    if t.endswith("es"):
        forms.add(t[:-2])
    if t.endswith("s"):
        forms.add(t[:-1])
    return any(" " + f + " " in norm for f in forms)


# Keywords: 40
total_w = found_w = 0
found, missing = [], []
for k in kw.get("keywords", []):
    w = k.get("weight", 1)
    total_w += w
    terms = [k["term"]] + k.get("aliases", [])
    if any(present(t) for t in terms):
        found_w += w
        found.append(k["term"])
    else:
        missing.append(k["term"])
kw_score = round(40 * found_w / total_w) if total_w else 0

# Title: 15
title = kw.get("title", "")
tw = [w for w in re.findall(r"\w+", title.lower()) if w not in {"of", "and", "the", "for", "&"}]
# Full points only when the title is in the headline (top lines) or on a role line.
# Mentioned elsewhere ("ready for a Customer Success Manager role") counts as partial.
_lines = [l for l in text.splitlines() if l.strip()]
_top = _norm(" ".join(_lines[:4]))
_roleish = [_norm(l) for l in _lines if re.search(r"(19|20)\d{2}", l) and len(l.split()) <= 14]
if title and (_norm(title) in _top or any(_norm(title) in l for l in _roleish)):
    title_score = 15
elif title and present(title):
    title_score = 11
elif tw:
    ratio = sum(1 for w in tw if present(w)) / len(tw)
    title_score = round(11 * ratio)
else:
    title_score = 0

# Format: 15
fmt = {}
fmt["text extracts cleanly"] = 3 if len(text.split()) > 150 else 0  # very little text usually means images, text boxes or a thin resume
fmt["length (1-2 pages)"] = 2 if pages <= 2 else 0
fmt["no tables"] = 0 if has_table else 2
fmt["single column"] = 0 if columns else 2
heads = ["experience", "education", "skills", "summary", "ניסיון", "השכלה", "כישורים", "תקציר"]
hits = sum(1 for h in heads if h in text.lower())
fmt["standard headings"] = 2 if hits >= 3 else (1 if hits >= 2 else 0)
has_email = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text))
has_phone = bool(re.search(r"\+?\d[\d\s().-]{7,}\d", text))
has_li = "linkedin.com" in text.lower()
fmt["contact details"] = 2 if has_email and (has_phone or has_li) else (1 if has_email else 0)
fmt["years in dates"] = 2 if len(re.findall(r"\b(19|20)\d{2}\b", text)) >= 4 else 0
fmt_score = sum(fmt.values())

# Measurable results: 5
lines = [l for l in text.splitlines() if len(l.split()) >= 5]
def _result_digits(l):
    # years, date ranges, phone numbers and emails are not results
    l = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", " ", l)
    l = re.sub(r"\+?\d[\d\s().-]{7,}\d", " ", l)
    l = re.sub(r"(19|20)\d{2}", " ", l)
    return re.search(r"\d", l)
with_num = sum(1 for l in lines if _result_digits(l))
ratio = with_num / len(lines) if lines else 0
meas_score = 5 if ratio >= 0.35 else 4 if ratio >= 0.25 else 3 if ratio >= 0.15 else 2 if ratio > 0 else 0

judg = {}
if a.judgment and pathlib.Path(a.judgment).exists():
    judg = json.loads(pathlib.Path(a.judgment).read_text(encoding="utf-8"))
exp_score = judg.get("experience")
soft_score = judg.get("soft")

parts = {
    "keywords (40)": kw_score,
    "title (15)": title_score,
    "experience and seniority (15)": exp_score,
    "soft skills (10)": soft_score,
    "format (15)": fmt_score,
    "measurable results (5)": meas_score,
}
known = sum(v for v in parts.values() if v is not None)
complete = all(v is not None for v in parts.values())

result = {"estimated_total": known if complete else None, "partial_total": known, "parts": parts,
          "format_checks": fmt, "keywords_found": found, "keywords_missing": missing, "pages": pages}
if a.json:
    print(json.dumps(result, ensure_ascii=False, indent=2))
else:
    sys.stdout.reconfigure(encoding="utf-8")
    for k, v in parts.items():
        print(f"{k:32} {'needs judgment' if v is None else v}")
    print(f"{'ESTIMATED TOTAL':32} {known if complete else str(known) + ' (without judgment parts)'}")
    if missing:
        print("missing keywords: " + ", ".join(missing))
    weak = [k for k, v in fmt.items() if v == 0]
    print("format problems: " + (", ".join(weak) if weak else "none"))
