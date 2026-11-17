"""Stop hook: when a resume-helper hand-over folder is marked ready, its files must have clean names.

Looks for resume-helper.json with "handover": true in the session folder (and one level down).
Exit 2 blocks Claude from finishing and lists what to rename. Runs once per stop to avoid loops.
"""
import json
import os
import pathlib
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

root = pathlib.Path(data.get("cwd") or ".")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "skills" / "resume-tailor" / "scripts"))
from check_filenames import check  # noqa: E402

problems = []
for dirpath, dirnames, filenames in os.walk(root):
    depth = len(pathlib.Path(dirpath).relative_to(root).parts)
    # The application folder is created in the session folder, so look only one level down (fast for everyone).
    dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in ("node_modules", "work") and depth < 1]
    if "resume-helper.json" in filenames:
        try:
            state = json.loads((pathlib.Path(dirpath) / "resume-helper.json").read_text(encoding="utf-8"))
        except Exception:
            continue
        if state.get("handover"):
            problems += [f"{dirpath}: {p}" for p in check(dirpath)]

if problems:
    msg = "Hand-over files need clean names before you finish:\n" + "\n".join("  - " + p for p in problems)
    msg += "\nRename to '<Full Name> Resume.pdf' / '<Full Name> Cover Letter.pdf' and delete old versions."
    print(msg, file=sys.stderr)
    sys.exit(0 if data.get("stop_hook_active") else 2)
sys.exit(0)
