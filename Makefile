a.pdf:main.tex
	xelatex --shell-escape -8bit -synctex=1 -interaction=nonstopmode main.tex
clean:
	rm *.aux  *.fdb_latexmk *.fls *.log *.gz  *.out *.toc *.xdv  *.pdf -rf
