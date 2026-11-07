@echo off
:: Step 1: Generate PDF from main.tex using xelatex
xelatex --shell-escape -8bit -synctex=1 -interaction=nonstopmode main.tex
xelatex --shell-escape -8bit -synctex=1 -interaction=nonstopmode main.tex
