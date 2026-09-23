#!/usr/bin/env python3
"""Build dist/resume-overleaf.zip for Overleaf's "Upload Project".

Files sit at the zip root with no wrapping folder, because Overleaf makes the
archive's top level the project root: a wrapping folder would nest every file
one level deeper and break the relative \input paths.
"""
import pathlib, zipfile

ROOT = pathlib.Path.cwd()
OUT = ROOT / "dist" / "resume-overleaf.zip"

MEMBERS = ["resume-sde.tex", "resume-aiml.tex", "preamble.tex", "README.md"] + \
          [f"sections/{n}.tex" for n in
           ("header", "education", "certifications", "achievements")]

OUT.parent.mkdir(exist_ok=True)
missing = [m for m in MEMBERS if not (ROOT / m).is_file()]
if missing:
    raise SystemExit(f"missing source files: {missing}")

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for m in MEMBERS:
        z.write(ROOT / m, arcname=m)

print(f"  {OUT}  ({OUT.stat().st_size // 1024} KB)")
for n in zipfile.ZipFile(OUT).namelist():
    print(f"    {n}")
