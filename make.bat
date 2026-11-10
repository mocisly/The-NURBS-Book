@echo off
:: latexmk also runs MakeIndex and resolves bibliography/index page links.
latexmk -xelatex -shell-escape -synctex=1 -interaction=nonstopmode -halt-on-error main.tex
