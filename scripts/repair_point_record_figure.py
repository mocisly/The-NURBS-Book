"""Restore the existing native-but-empty OCR table13.1 from its adjacent typedefs."""
from fractions import Fraction as F
from memory_diagram import grid
from pathlib import Path
root=Path(__file__).resolve().parents[1];f=root/'chapter/13.tex';s=f.read_text(encoding='utf-8');a=s.index('\nP :\n');caption='图 13.1. 点和控制点数据结构。';b=s.index(caption,a)+len(caption)
old=s[a:b];assert old.count(r'\begin{tabular}')==2 and r'\phantom{X}'in old
lines=[r'\begin{center}',r'\begin{minipage}{26cm}',r'\centering',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-2,-1) rectangle (9.2,3.2);',r'\node[left=7pt] at (0,2.05) {$P:$};',r'\node[left=7pt] at (0,.05) {$P^w:$};']
lines+=grid(F(0),F(5,2),(F(21,10),)*3,[(r'$x$',r'$y$',r'$z$')],F(9,10));lines+=grid(F(0),F(1,2),(F(21,10),)*4,[(r'$wx$',r'$wy$',r'$wz$',r'$w$')],F(9,10))
lines.extend([r'\end{tikzpicture}',r'\par\smallskip',caption+r'\\',r'\texttt{POINT}存储欧几里得坐标$(x,y,z)$；\texttt{CPOINT}存储齐次坐标$(wx,wy,wz,w)$。',r'\end{minipage}',r'\end{center}'])
s=s[:a]+'\n'+'\n'.join(lines)+'\n'+s[b:];f.write_text(s,encoding='utf-8');print('Restored13.1 emptyOCRtable to editable POINT/CPOINT cells from adjacent definitions; no original image record added.')
