from pathlib import Path
from fractions import Fraction as F
from memory_diagram import grid
root=Path(__file__).resolve().parents[1]
out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1,-4.2) rectangle (9,3.8);',r'\node at (3.8,3.4) {\texttt{CPOLYGON}};']
out+=grid(F(17,10),F(29,10),(F(21,10),)*2,[(r'$n$',r'\texttt{Pw}')],F(9,10))
out.append(r'\draw[book grid,book axis] (4.85,2)--(4.85,0);')
rows=[(r'$w_0x_0$',r'$w_0y_0$',r'$w_0z_0$',r'$w_0$'),(r'$w_1x_1$',r'$w_1y_1$',r'$w_1z_1$',r'$w_1$'),(r'$\vdots$',)*4,(r'$w_nx_n$',r'$w_ny_n$',r'$w_nz_n$',r'$w_n$')]
out+=grid(F(0),F(0),(F(19,10),)*4,rows,F(9,10));out.append(r'\end{tikzpicture}');(root/'image_tex/ch13/fig_13_01.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
print('PASS CPOLYGON fields n/Pw, pointer to n+1 homogeneous four-component controls; semantic record cells.')
