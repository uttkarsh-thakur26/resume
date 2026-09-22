# Build both resume variants. `make` builds everything; `make sde` or
# `make aiml` builds one. Requires pdfLaTeX (see README for packages).

VARIANTS := sde aiml
PDFS     := $(addprefix resume-,$(addsuffix .pdf,$(VARIANTS)))
SOURCES  := preamble.tex $(wildcard sections/*.tex)

.PHONY: all sde aiml ats clean

all: $(PDFS)

resume-%.pdf: resume-%.tex $(SOURCES)
	pdflatex -interaction=nonstopmode -halt-on-error $<

sde: resume-sde.pdf
aiml: resume-aiml.pdf

clean:
	rm -f *.aux *.log *.out *.fls *.fdb_latexmk *.synctex.gz

ats: $(PDFS)
	python3 tools/ats_check.py $(PDFS)
