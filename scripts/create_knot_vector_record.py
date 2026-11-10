from pathlib import Path
from fractions import Fraction as F
from memory_diagram import grid
root=Path(__file__).resolve().parents[1]
out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1,-4.2) rectangle (9,3.8);',r'\node at (3.8,3.4) {\texttt{knt : KNOTVECTOR}};']
out+=grid(F(17,10),F(29,10),(F(21,10),)*2,[(r'$m$',r'\texttt{U}')],F(9,10));out.append(r'\draw[book grid,book axis] (4.85,2)--(4.85,0);')
out+=grid(F(39,10),F(0),(F(19,10),),[(r'$u_0$',),(r'$u_1$',),(r'$\vdots$',),(r'$u_m$',)],F(9,10));out.append(r'\end{tikzpicture}');(root/'image_tex/ch13/fig_13_02.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/fig1303-caption.txt').write_text('图 13.3. 节点向量数据结构。\\\\\n'+r'$m$为最高节点索引，\texttt{U}指向包含$m+1$个实数的节点数组$u_0,\ldots,u_m$。'+'\n',encoding='utf-8');print('PASS KNOTVECTOR m/U record, scalararray m+1 entries and clear pointer, samefieldscale as13.2.')
