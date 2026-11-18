"""AI-slop check for resumes, cover letters and short texts (English and Hebrew).

Usage:
  python slop_check.py <file.html | file.txt | file.md> [--warn-only]

Finds the mechanical signs of AI-written text: stock words, translated-sounding Hebrew,
X-versus-Y punchlines, empty openers, dashes inside sentences. Exit 2 = found something
(the build hook blocks), exit 0 = clean. It can't judge meaning: the three human tests
in references/anti-slop.md still apply.

A phrase the user insists on, in their own words, goes in work/slop_allow.json next to the
file: {"allow": ["exact phrase"]}. Those are skipped.
"""
import html as htmlmod
import json
import pathlib
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

EN_WORDS = [
    "leverage", "leveraged", "leveraging", "spearhead", "spearheaded", "synergy", "synergies",
    "cutting-edge", "passionate", "dynamic", "results-driven", "seamless", "seamlessly", "robust",
    "delve", "tapestry", "testament", "transformative", "innovative", "visionary", "holistic",
    "empower", "empowered", "empowering", "elevate", "elevated", "foster", "fostered", "fostering",
    "landscape", "journey", "realm", "unlock", "unlocked", "game-changer", "game changer", "thrive",
    "thrived", "go-getter", "world-class", "revolutionized", "revolutionised", "best-in-class",
    "detail-oriented", "self-starter", "hard-working", "hardworking", "proactive",
]
EN_PHRASES = [
    "proven track record", "wear many hats", "think outside the box", "outside the box",
    "i am writing to express", "i am excited to apply", "i believe i would be a great fit",
    "i would be a great fit", "excited to bring", "hit the ground running", "fast-paced environment",
    "team player", "strong communication skills", "excellent communication skills",
    "in today's", "ever-evolving", "ever-changing", "drive results", "add value",
]
EN_CONTRAST = [
    r"\bnot (just|only|merely) (a |an |the )?\w+[,.]? (but |a |an |it'?s )",
    r"\bit'?s not about\b", r"\bisn'?t just\b", r"\bmore than just\b",
]
HE_PHRASES = [
    "לייצר ערך", "להניע תהליכים", "הנעת תהליכים", "ליצור תוצרים", "מוכוון תוצאות", "מוכוונת תוצאות",
    "עם דגש על", "ברמה הגבוהה ביותר", "לקחת חלק פעיל", "יכולת הובלה מוכחת", "ניסיון מוכח",
    "חדשני", "חדשנית", "פורץ דרך", "פורצת דרך", "סינרגיה", "תשוקה", "יוצא דופן", "יוצאת דופן",
    "ראש גדול", "ראייה רחבה", "יכולות בין-אישיות", "יכולות בין אישיות", "יכולת למידה עצמית",
    "מוטיבציה גבוהה", "סביבה דינמית", "מחוץ לקופסה", "שחקן צוות", "שחקנית צוות",
    "ברצוני להגיש", "אשמח להזדמנות", "להוכיח את עצמי", "אודה על התייחסותכם",
    "בעל/ת", "בעל.ת", "מנהל/ת", "יכולת עבודה תחת לחץ", "סדר עדיפויות גבוה",
]
HE_CONTRAST = [r"לא רק\b[^.!?\n]{0,60}\bאלא", r"זה לא עניין של", r"לא עוד\b[^.!?\n]{0,30}[,.]"]

DASH = re.compile(r"(?<=[^\d\s])\s*[—–]\s*(?=\D)|(?<=\D)\s[—–]\s(?=\D)|—")


def visible_text(path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in (".html", ".htm"):
        raw = re.sub(r"(?s)<!--.*?-->", " ", raw)
        raw = re.sub(r"(?is)<(style|script|svg|head)\b.*?</\1>", " ", raw)
        raw = re.sub(r"(?i)<br\s*/?>|</(p|li|h\d|div|tr)>", "\n", raw)
        raw = htmlmod.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    return raw


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 0
    path = pathlib.Path(argv[0])
    warn_only = "--warn-only" in argv
    text = visible_text(path)
    allow = []
    af = path.parent / "slop_allow.json"
    if af.exists():
        try:
            allow = [a.lower() for a in json.loads(af.read_text(encoding="utf-8")).get("allow", [])]
        except Exception:
            pass

    hits = []
    for line in [l.strip() for l in text.splitlines() if l.strip()]:
        low = line.lower()
        if any(a in low for a in allow):
            continue
        for w in EN_WORDS:
            if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low):
                hits.append(("stock AI word", w, line))
        for p in EN_PHRASES + HE_PHRASES:
            if p in low:
                hits.append(("stock or translated phrase", p, line))
        for r in EN_CONTRAST + HE_CONTRAST:
            m = re.search(r, low)
            if m:
                hits.append(("X-versus-Y punchline", m.group(0), line))
        if DASH.search(line):
            hits.append(("dash inside a sentence (use a comma, period or colon)", "—/–", line))

    if not hits:
        print("slop_check: OK, no mechanical AI-text patterns found. Still read it against the three tests.")
        return 0
    print(f"STOP: AI-text patterns in {path.name}:", file=sys.stderr)
    seen = set()
    for kind, what, line in hits:
        key = (kind, what, line)
        if key in seen:
            continue
        seen.add(key)
        short = line if len(line) <= 110 else line[:107] + "..."
        print(f"  - {kind}: '{what}' in: {short}", file=sys.stderr)
    print("Rewrite each line with the fact behind it (references/anti-slop.md). If the user insists on "
          "their own wording, add the exact phrase to work/slop_allow.json.", file=sys.stderr)
    return 0 if warn_only else 2


if __name__ == "__main__":
    sys.exit(main())
