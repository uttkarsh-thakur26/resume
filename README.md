# Resume

Two ATS-optimised LaTeX resumes, built from one shared base so the facts can
never drift apart between them.

| File | Target roles | Leads with |
| --- | --- | --- |
| [`resume-sde.tex`](resume-sde.tex) | Software engineering / backend internships | **BillSync** (Java, Spring Boot) |
| [`resume-aiml.tex`](resume-aiml.tex) | AI/ML internships | **CodeNav AI** (RAG, FAISS) |

Both fit on a single page.

## Layout

```
preamble.tex          styling, fonts and the resume macros — shared
sections/
  header.tex          name and contact details      — shared
  education.tex       degree and coursework          — shared
  certifications.tex  courses and dates              — shared
  achievements.tex    rankings and contests          — shared
resume-sde.tex        SKILLS + PROJECTS, SDE order   — variant-specific
resume-aiml.tex       SKILLS + PROJECTS, ML order    — variant-specific
```

Everything a recruiter checks for consistency (phone number, CGPA, dates)
lives in `sections/` and is written once. Only the pitch — which skills lead
and which project comes first — differs between the two root files.

## Build

```bash
make          # both PDFs
make sde      # just resume-sde.pdf
make aiml     # just resume-aiml.pdf
make clean    # remove .aux/.log build artifacts
```

Or directly:

```bash
pdflatex -interaction=nonstopmode resume-sde.tex
```

### Requirements

pdfLaTeX plus these TeX Live collections:

```bash
sudo apt-get install -y texlive-latex-base texlive-latex-recommended \
  texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra \
  texlive-plain-generic tex-gyre
```

`texlive-plain-generic` supplies `ulem.sty` and `tex-gyre` supplies
`tgheros.sty`; both are easy to miss and the build fails without them.

### Overleaf

Upload the whole folder rather than a single file, then set the main document
to `resume-sde.tex` or `resume-aiml.tex`. The `\input` paths are relative, so
the structure has to come along.

## Editing

- **Contact details, education, certifications, achievements** — edit the file
  in `sections/`. Both resumes update together.
- **Skills and projects** — edit the variant root file. These are deliberately
  not shared, since the whole point is that they differ.
- **Fonts, margins, spacing** — edit `preamble.tex`. Applies to both.

After any edit, rebuild and check the log for `Overfull \hbox`: that warning
means a line is bleeding past the right margin, which looks broken in print
even though the PDF still compiles.

## ATS notes

- `\pdfgentounicode=1` is set, so the PDF carries a correct Unicode text layer
  and copy-paste extraction works. Verify with `pdftotext -layout resume-sde.pdf -`.
- Single-column, no tables for content, no text inside images.
- Keywords are repeated in both the skills list and the project bullets, since
  some parsers weight the two sections differently.
