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

`resume-sde.tex` pulls in `preamble.tex` and the files in `sections/`, so
uploading that one file on its own fails with **`File 'preamble.tex' not
found`**. Two ways round it.

**Option A, upload the project (keeps the shared structure):**

```bash
make overleaf          # writes dist/resume-overleaf.zip
```

In Overleaf: **New Project > Upload Project**, pick that zip. The files sit at
the zip root, so the relative `\input` paths resolve as-is. Then set the main
document (**Menu > Main document**) to `resume-sde.tex` or `resume-aiml.tex`.

**Option B, upload a single file (simplest):**

```bash
make standalone        # writes dist/resume-*-standalone.tex
```

Each is one self-contained file with every `\input` already inlined. Drag one
into a blank Overleaf project and compile. Nothing else needed.

These are **generated** files. Edit the modular sources and re-run the command;
never edit `dist/` by hand. `make` regenerates them as part of a normal build.

## Editing

- **Contact details, education, certifications, achievements** — edit the file
  in `sections/`. Both resumes update together.
- **Skills and projects** — edit the variant root file. These are deliberately
  not shared, since the whole point is that they differ.
- **Fonts, margins, spacing** — edit `preamble.tex`. Applies to both.

After any edit, rebuild and check the log for `Overfull \hbox`: that warning
means a line is bleeding past the right margin, which looks broken in print
even though the PDF still compiles.

## ATS checks

```bash
make ats
```

Runs `tools/ats_check.py`, which parses the built PDFs exactly as an applicant
tracking system would (text layer only) and reports what it can and cannot
find. Run it after editing the header or section headings.

There is no universal "ATS score". Real scores come from matching a CV against
one specific job description, so this checks the mechanical things that are
objectively right or wrong:

- contact fields recovered from the text layer (email, phone, LinkedIn, GitHub)
- junk characters introduced by icon fonts
- standard section headings the parser recognises
- date formats
- word count and bullet structure

Current state: all four contact fields extract cleanly. Both PDFs are single
column, carry no images, embed every font, and set `\pdfgentounicode=1` so the
text layer copies correctly.

### Known limitation

The FontAwesome icons in the header have no Unicode mapping, so they extract as
three stray characters next to the contact details. They are separated by
spaces and every field still parses, so the risk is low. To remove them
entirely, delete the `\faPhone*`, `\faEnvelope`, `\faLinkedin` and `\faGithub`
commands from `sections/header.tex`.

### Link text must be the URL

Parsers read the text layer, not the PDF's link annotations. So the visible
text has to be the address itself (`github.com/uttkarsh-thakur26`), not a label
like `github/uttkarsh-thakur26`. Keep it that way when editing.
