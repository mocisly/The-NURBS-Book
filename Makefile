.PHONY: all clean FORCE
all: main.pdf

# Let latexmk track every included chapter, diagram, and index source.
main.pdf: FORCE
	latexmk -xelatex -shell-escape -synctex=1 -interaction=nonstopmode -halt-on-error main.tex

FORCE:

clean:
	latexmk -c main.tex
