"""PreToolUse hook: before any resume-helper build command runs, check the draft for invented facts.

Triggers only on shell commands that call fit_page.py, build_pdf.py or build_docx.py.
Exit 2 blocks the command and sends the list of unmatched facts back to Claude.
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

BUILD = ("fit_page.py", "build_pdf.py", "build_docx.py")

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""
if not any(b in cmd for b in BUILD):
    sys.exit(0)

cwd = pathlib.Path(data.get("cwd") or ".")
paths = re.findall(r'"([^"]+\.html?)"|\'([^\']+\.html?)\'|(\S+\.html?)', cmd)
htmls = [next(p for p in grp if p) for grp in paths]
if not htmls:
    sys.exit(0)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "skills" / "rezumatch" / "scripts"))
import verify_facts  # noqa: E402

status = 0
for h in htmls:
    p = pathlib.Path(h)
    if not p.is_absolute():
        p = cwd / p
    if not p.exists():
        continue
    sys.argv = ["verify_facts.py", str(p)]
    if verify_facts.main() != 0:
        status = 2
sys.exit(status)
