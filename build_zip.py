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
