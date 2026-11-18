"""Anti-invention check. Every fact in a draft must come from the user.

Checks the draft HTML against work/source.txt (the user's resume and any pages they pointed to)
and work/confirmed_facts.json (answers the user gave and approved during the interview):
  - every number (counts, money, percentages, years) in the draft
  - every company name (class "role-org") and job title (class "role-title")
  - scope words that change what a role means (guest, founder, director, head, ...)

Usage: python verify_facts.py work/resume.html
Exit 0 = clean. Exit 2 = unmatched facts, listed on stderr (the build must stop and Claude must ask).

work/confirmed_facts.json:
  {"facts": ["Led a team of 6 at Acme", "Cut onboarding time from 3 weeks to 1 week", ...]}
Write each confirmed answer in the user's own terms, including its numbers.
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

SCOPE_WORDS = ["guest", "visiting", "assistant", "assisted", "intern", "junior", "senior", "lead",
               "head", "director", "vp", "vice president", "chief", "founder", "co-founder",
               "owner", "partner", "principal", "manager", "managed", "supervised", "phd", "doctor",
               "certified", "award", "winner", "patent"]


def strip_html(raw):
    raw = re.sub(r"(?s)<!--.*?-->", " ", raw)
    raw = re.sub(r"(?is)<(style|script|svg)\b.*?</\1>", " ", raw)
    return htmlmod.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))


def norm(s):
    s = s.replace("&", " and ")
    s = re.sub(r"[,.;:](?=\s|$)", " ", s)
    return " " + re.sub(r"\s+", " ", re.sub(r"[^\w$%+.,/-]+", " ", s.lower())).strip() + " "


def numbers(s):
    out = set()
    for m in re.finditer(r"\$?\d[\d,]*(?:\.\d+)?\s?(?:%|k|m|\+)?", s, re.I):
        tok = m.group(0).strip().lower()
        core = re.sub(r"[^\d.]", "", tok)
        if core:
            out.add(core.rstrip("."))
    return out


def main():
    html_path = pathlib.Path(sys.argv[1])
    work = html_path.parent
    src_file = work / "source.txt"
    if not src_file.exists():
        print(f"verify_facts: {src_file} is missing. Save the user's resume text there first "
              "(extract_resume.py --out work/source.txt).", file=sys.stderr)
        return 2
    raw = html_path.read_text(encoding="utf-8")
    draft = strip_html(raw)
    source = src_file.read_text(encoding="utf-8", errors="replace")
    cf = work / "confirmed_facts.json"
    confirmed = ""
    if cf.exists():
        confirmed = " ".join(json.loads(cf.read_text(encoding="utf-8")).get("facts", []))
    allowed_text = norm(source + " " + confirmed)
    allowed_nums = numbers(source + " " + confirmed)
    # Contact details are the user's own and change often (phone formats): skip the contact line.
    # Contact details and the letter date are not claims about the user's career: skip them.
    draft_body = re.sub(r"(?is)<p class=\"(contact|date)\".*?</p>", " ", raw)
    draft_body = strip_html(draft_body)

    problems = []
    for n in sorted(numbers(draft_body)):
        if n not in allowed_nums:
            problems.append(f"number '{n}' is not in the source or confirmed facts")
    for cls in ("role-org", "role-title"):
        for m in re.finditer(rf'class="{cls}"[^>]*>(.*?)</', raw, re.S):
            val = strip_html(m.group(1)).strip()
            val_core = re.sub(r"\s*\([^)]*\)", "", val).strip()  # "(Director level)" checked as scope word
            pieces = [x.strip() for x in re.split(r",| \| | - ", val_core) if x.strip()]
            if val_core and any(norm(x) not in allowed_text for x in pieces):
                problems.append(f"{cls.replace('role-', '')} '{val}' is not in the source or confirmed facts")
    dn = norm(draft_body)
    for w in SCOPE_WORDS:
        if f" {w} " in dn and f" {w} " not in allowed_text:
            problems.append(f"scope word '{w}' is not in the source or confirmed facts")

    if problems:
        print("STOP: possible invented facts in " + html_path.name + ":", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        print("Ask the user about each item, one question at a time. Add confirmed answers to "
              "work/confirmed_facts.json, or remove the item from the draft.", file=sys.stderr)
        return 2
    print("verify_facts: OK, every checked fact traces to the user.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
