"""Hand-over check: deliverables have clean human names and no old versions sit next to them.

Usage: python check_filenames.py <output folder>
The output folder has resume-helper.json: {"name": "Jane Doe", "handover": true}
Working files (HTML, source.txt, drafts) live in <output folder>/work/ and are ignored.
Exit 0 = clean, exit 2 = problems listed on stderr.
"""
import json
import pathlib
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ALLOWED_KINDS = ["Resume", "Cover Letter", "קורות חיים", "מכתב פנייה"]
DELIVERABLE_EXT = {".pdf", ".docx"}
BAD = [(r"_", "underscore"), (r"(?i)\bv\d+\b|_v\d+", "version number"), (r"(?i)\bfinal\b", "'final'"),
       (r"(?i)\bcopy\b|עותק", "'copy'"), (r"\(\d+\)|\(new\)", "duplicate marker"), (r"(?i)\bdraft\b|טיוטה", "'draft'")]


def check(folder):
    folder = pathlib.Path(folder)
    state = json.loads((folder / "resume-helper.json").read_text(encoding="utf-8"))
    name = state.get("name", "").strip()
    allowed = {f"{name} {k}" for k in ALLOWED_KINDS}
    problems = []
    for f in sorted(folder.iterdir()):
        if f.is_dir() or f.name == "resume-helper.json" or f.name.startswith("."):
            continue
        if f.suffix.lower() not in DELIVERABLE_EXT:
            problems.append(f"'{f.name}': working file in the hand-over folder, move it to work/")
            continue
        for pat, why in BAD:
            if re.search(pat, f.stem):
                problems.append(f"'{f.name}': {why} in the name")
        if f.stem not in allowed:
            problems.append(f"'{f.name}': expected one of: " + ", ".join(sorted(a + f.suffix for a in allowed)))
    return problems


if __name__ == "__main__":
    probs = check(sys.argv[1])
    if probs:
        print("Hand-over files need clean names:", file=sys.stderr)
        for p in probs:
            print("  - " + p, file=sys.stderr)
        print("Rename to '<Full Name> Resume.pdf' / '<Full Name> Cover Letter.pdf' and delete old versions.",
              file=sys.stderr)
        sys.exit(2)
    print("check_filenames: OK")
