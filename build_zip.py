"""Build the Claude.ai upload zips into dist/: one per skill.

Usage: python build_zip.py
"""
import pathlib
import zipfile

root = pathlib.Path(__file__).parent
dist = root / "dist"
dist.mkdir(exist_ok=True)
for skill in (root / "skills").iterdir():
    if not (skill / "SKILL.md").exists():
        continue
    out = dist / f"{skill.name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, pathlib.Path(skill.name) / f.relative_to(skill))
    print(f"built {out}")

# Plugin zip for Customize > Plugins > Add > Upload plugin (.claude-plugin/plugin.json at the root).
PLUGIN_PARTS = [".claude-plugin", "agents", "skills", "hooks", "LICENSE", "README.md", "README.he.md", "requirements.txt"]
out = dist / "rezumatch-plugin.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for part in PLUGIN_PARTS:
        p = root / part
        files = [p] if p.is_file() else sorted(p.rglob("*"))
        for f in files:
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, f.relative_to(root).as_posix())
print(f"built {out}")
