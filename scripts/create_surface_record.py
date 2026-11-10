from pathlib import Path
from fractions import Fraction as F
from memory_diagram import grid
root=Path(__file__).resolve().parents[1]
out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1,-4.8) rectangle (29,7.6);',r'\node at (14,7) {\texttt{sur : SURFACE}};']
out+=grid(F(0),F(63,10),(F(28,5),)*5,[(r'\texttt{net}',r'$p$',r'$q$',r'\texttt{knu}',r'\texttt{knv}')],F(9,10))
out+=grid(F(0),F(18,5),(F(11,5),)*3,[(r'$n$',r'$m$',r'\texttt{Pw}')],F(9,10))
for x,idx,k in[(F(35,2),'r','U'),(F(231,10),'s','V')]:out+=grid(x,F(18,5),(F(21,10),)*2,[('$'+idx+'$',r'\texttt{'+k+'}')],F(9,10))
out.extend([r'\draw[book grid,book axis] (2.8,5.4)--(2.8,4.4)--(3.3,4.4)--(3.3,3.6);',r'\draw[book grid,book axis] (19.6,5.4)--(19.6,3.6);',r'\draw[book grid,book axis] (25.2,5.4)--(25.2,3.6);',r'\draw[book grid,book axis] (5.5,2.7)--(5.5,.7);',r'\draw[book grid,book axis] (20.65,2.7)--(20.65,.7);',r'\draw[book grid,book axis] (26.25,2.7)--(26.25,.7);'])
out+=grid(F(22,5),F(7,10),(F(11,5),),[(r'\texttt{Pw[0]}',),(r'$\vdots$',),(r'\texttt{Pw[n]}',)],F(9,10))
out.extend([r'\draw[book grid,book axis] (6.6,.25)--(9,.25);',r'\draw[book grid,book axis] (6.6,-1.55)--(7.8,-1.55)--(7.8,-2.45)--(9,-2.45);'])
rows=[]
for i,j in[('0','0'),('0','m'),('...','...'),('n','0'),('n','m')]:
    if i=='...':rows.append((r'$\vdots$',)*4);continue
    sub='{'+i+','+j+'}';rows.append(tuple('$w_'+sub+x+'_'+sub+'$'if x else'$w_'+sub+'$'for x in('x','y','z','')))
out+=grid(F(9),F(7,10),(F(19,10),)*4,rows,F(9,10))
for x,k,end in[(F(197,10),'u','r'),(F(253,10),'v','s')]:out+=grid(x,F(7,10),(F(19,10),),[('$'+k+'_0$',),('$'+k+'_1$',),(r'$\vdots$',),('$'+k+'_'+end+'$',)],F(9,10))
out.append(r'\end{tikzpicture}');(root/'image_tex/ch13/fig_13_05.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/fig1306-caption.txt').write_text('图 13.6. 曲面数据结构。\\\\\n'+r'\texttt{SURFACE}包含控制网指针\texttt{net}、次数$p,q$及两个节点向量指针\texttt{knu,knv}；控制网和节点数组的索引分别为$n,m$与$r,s$。'+'\\\\\n'+r'$r=n+p+1$，$s=m+q+1$；\texttt{Pw[i][j]}为齐次控制点，两个节点数组分别存储$u_0,\ldots,u_r$和$v_0,\ldots,v_s$。'+'\n',encoding='utf-8');print('PASS SURFACE net/p/q/knu/knv, CNET andtwoKNOTVECTORobjects; homogeneouscontrolnet/twonodearrays indexed n,m,r,s.')
