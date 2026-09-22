#!/usr/bin/env python3
"""Mechanical ATS parse checks. Every result is derived from the PDF, not estimated."""
import re, subprocess, sys, unicodedata

STANDARD_HEADINGS = ["EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT", "EDUCATION",
                     "SKILLS", "PROJECTS", "CERTIFICATIONS", "ACHIEVEMENTS",
                     "AWARDS", "SUMMARY", "PUBLICATIONS"]

def text(pdf, layout=False):
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [pdf, "-"]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def check(pdf):
    raw = text(pdf)
    print(f"\n{'='*66}\n  {pdf}\n{'='*66}")

    # --- 1. Contact block -------------------------------------------------
    print("\n[1] CONTACT FIELD EXTRACTION")
    tests = {
        "Email":      r"[\w.+-]+@[\w-]+\.[\w.]+",
        "Phone":      r"\+?\d[\d\s\-()]{8,}\d",
        "LinkedIn URL": r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+",
        "GitHub URL":   r"(?:https?://)?(?:www\.)?github\.com/[\w-]+",
    }
    for label, pat in tests.items():
        m = re.search(pat, raw)
        print(f"    {'PASS' if m else 'FAIL'}  {label:<14} {m.group(0) if m else 'not found as parseable text'}")

    # --- 2. Junk characters ----------------------------------------------
    print("\n[2] NON-ASCII / JUNK CHARACTERS IN TEXT LAYER")
    junk = {}
    for ch in raw:
        if ord(ch) > 127 and ch not in "–—‘’“”•·₹":
            junk[ch] = junk.get(ch, 0) + 1
    # private-use + stray punctuation adjacent to contact info
    contact_line = next((l for l in raw.splitlines() if "@" in l), "")
    stray = re.findall(r"(?<![\w])[#§ïÒ¶](?=\s)", contact_line)
    if junk:
        for ch, n in sorted(junk.items(), key=lambda x: -x[1]):
            try: nm = unicodedata.name(ch)
            except ValueError: nm = "UNNAMED / PRIVATE USE"
            print(f"    WARN  U+{ord(ch):04X} {ch!r} x{n}  ({nm})")
    else:
        print("    PASS  none")
    if stray:
        print(f"    WARN  {len(stray)} stray glyph(s) inside the contact line: {stray}")

    # --- 3. Section headings ---------------------------------------------
    print("\n[3] SECTION HEADINGS RECOGNISED")
    upper = raw.upper()
    found = [h for h in STANDARD_HEADINGS if re.search(rf"^\s*{h}\s*$", upper, re.M)]
    print(f"    Found: {', '.join(found)}")
    for critical in ["EDUCATION", "SKILLS"]:
        print(f"    {'PASS' if critical in found else 'FAIL'}  {critical} present")
    has_exp = any(h in found for h in ["EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT"])
    print(f"    {'PASS' if has_exp else 'WARN'}  Experience-type heading present")

    # --- 4. Dates ---------------------------------------------------------
    print("\n[4] DATE PARSEABILITY")
    dates = re.findall(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}", raw)
    years = re.findall(r"\b(?:19|20)\d{2}\b", raw)
    print(f"    {len(dates)} month-year dates, {len(years)} bare years")
    print(f"    Month-year samples: {dates[:4]}")

    # --- 5. Structure -----------------------------------------------------
    print("\n[5] STRUCTURE")
    words = len(raw.split())
    bullets = raw.count("•")
    print(f"    Word count: {words}   (600-800 is the usual sweet spot for 1 page)")
    print(f"    Bullet points: {bullets}")
    blanks = len(re.findall(r"\n\s*\n", raw))
    print(f"    Paragraph breaks mid-bullet: {blanks} (high counts can split bullets on ingest)")

def keywords(pdf, name, kws):
    raw = text(pdf).lower()
    hit = [k for k in kws if k.lower() in raw]
    miss = [k for k in kws if k.lower() not in raw]
    pct = 100 * len(hit) / len(kws)
    print(f"\n  {name}: {len(hit)}/{len(kws)} matched ({pct:.0f}%)")
    if miss:
        print(f"    Missing: {', '.join(miss)}")

if __name__ == "__main__":
    for pdf in sys.argv[1:]:
        check(pdf)
