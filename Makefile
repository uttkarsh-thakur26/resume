# Build both resume variants. `make` builds everything; `make sde` or
# `make aiml` builds one. Requires pdfLaTeX (see README for packages).

VARIANTS := sde aiml
PDFS     := $(addprefix resume-,$(addsuffix .pdf,$(VARIANTS)))
SOURCES  := preamble.tex $(wildcard sections/*.tex)

.PHONY: all sde aiml ats standalone overleaf clean

all: $(PDFS) standalone

resume-%.pdf: resume-%.tex $(SOURCES)
	pdflatex -interaction=nonstopmode -halt-on-error $<

sde: resume-sde.pdf
aiml: resume-aiml.pdf

# Single-file copies for Overleaf and portals that take only one file.
standalone:
	python3 tools/flatten.py $(addprefix resume-,$(addsuffix .tex,$(VARIANTS)))

# Zip for Overleaf: New Project > Upload Project.
overleaf:
	python3 tools/make_zip.py

clean:
	rm -f *.aux *.log *.out *.fls *.fdb_latexmk *.synctex.gz dist/*.aux dist/*.log dist/*.out

ats: $(PDFS)
	python3 tools/ats_check.py $(PDFS)
