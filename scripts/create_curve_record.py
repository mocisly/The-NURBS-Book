from pathlib import Path
from fractions import Fraction as F
from memory_diagram import grid
root=Path(__file__).resolve().parents[1]
out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1,-3.8) rectangle (16,7.1);',r'\node at (8.6,6.6) {\texttt{cur : CURVE}};']
out+=grid(F(29,10),F(59,10),(F(19,5),)*3,[(r'\texttt{pol}',r'$p$',r'\texttt{knt}')],F(9,10))
out+=grid(F(17,10),F(18,5),(F(21,10),)*2,[(r'$n$',r'\texttt{Pw}')],F(9,10))
out+=grid(F(103,10),F(18,5),(F(21,10),)*2,[(r'$m$',r'\texttt{U}')],F(9,10))
out.extend([r'\draw[book grid,book axis] (4.8,5)--(4.8,4.3)--(3.8,4.3)--(3.8,3.6);',r'\draw[book grid,book axis] (12.4,5)--(12.4,3.6);',r'\draw[book grid,book axis] (4.85,2.7)--(4.85,.7);',r'\draw[book grid,book axis] (13.45,2.7)--(13.45,.7);'])
rows=[tuple('$w_'+str(i)+x+'_'+str(i)+'$'if x else'$w_'+str(i)+'$'for x in('x','y','z',''))for i in(0,1)]
rows+=[(r'$\vdots$',)*4,(r'$w_nx_n$',r'$w_ny_n$',r'$w_nz_n$',r'$w_n$')]
out+=grid(F(0),F(7,10),(F(19,10),)*4,rows,F(9,10));out+=grid(F(25,2),F(7,10),(F(19,10),),[(r'$u_0$',),(r'$u_1$',),(r'$\vdots$',),(r'$u_m$',)],F(9,10));out.append(r'\end{tikzpicture}')
(root/'image_tex/ch13/fig_13_03.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/fig1304-caption.txt').write_text('图 13.4. 曲线数据结构。\\\\\n'+r'\texttt{CURVE}包含控制多边形指针\texttt{pol}、次数$p$和节点向量指针\texttt{knt}；两个子对象分别管理齐次控制点数组和实数节点数组，$m=n+p+1$。'+'\n',encoding='utf-8');print('PASS CURVE pol/p/knt pointers to CPOLYGON and KNOTVECTOR, samefourcomponent/scalar arrays andfieldscale.')
