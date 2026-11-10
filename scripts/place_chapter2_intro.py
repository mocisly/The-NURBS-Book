"""Place the related introductory diagrams immediately after their explanations."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
path=root/'chapter/2.tex'
text=path.read_text(encoding='utf-8')
for number,anchor in [(1,'任何标准多项式形式'),(2,'强加 \\({C}^{1}\\)')]:
    ref=f'\\BookFigure[max width=0.9\\textwidth]{{ch02/fig_2_0{number}.tex}}'
    start=text.index('\\begin{center}\n'+ref)
    caption=text.index(f'图 2.{number}.',start)
    end=text.index('\n',caption)
    caption_text=text[caption:end]
    text=text[:start]+text[end:]
    block=('\\begin{center}\n\\begin{minipage}{14cm}\n\\centering\n'+ref+
           '\n\\par\\smallskip\n'+caption_text+
           '\n\\end{minipage}\n\\end{center}\n\n')
    pos=text.index(anchor)
    text=text[:pos]+block+text[pos:]
path.write_text(text,encoding='utf-8')
