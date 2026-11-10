from pathlib import Path
from fractions import Fraction as F
from memory_diagram import grid
root=Path(__file__).resolve().parents[1]
out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1,-7.6) rectangle (19,5.4);',r'\node at (3.3,4.8) {\texttt{net : CNET}};']
out+=grid(F(0),F(41,10),(F(11,5),)*3,[(r'$n$',r'$m$',r'\texttt{Pw}')],F(9,10))
out+=grid(F(22,5),F(3,2),(F(11,5),),[(r'\texttt{Pw[0]}',),(r'$\vdots$',),(r'\texttt{Pw[n]}',)],F(9,10))
out.extend([r'\draw[book grid,book axis] (5.5,3.2)--(5.5,1.5);',r'\draw[book grid,book axis] (6.6,1.05)--(10,1.05);',r'\draw[book grid,book axis] (6.6,-.75)--(8,-.75)--(8,-3.75)--(10,-3.75);'])
for i,y in[('0',F(3,2)),('n',-F(33,10))]:
    rows=[]
    for j in('0','1','...', 'm'):
        if j=='...':rows.append((r'$\vdots$',)*4);continue
        sub='{'+i+','+j+'}';rows.append(tuple('$w_'+sub+x+'_'+sub+'$'if x else'$w_'+sub+'$'for x in('x','y','z','')))
    out+=grid(F(10),y,(F(19,10),)*4,rows,F(9,10));out.append(r'\node at (13.8,'+str(float(y+F(1,2)))+') {$i='+i+'$};')
out.append(r'\end{tikzpicture}');(root/'image_tex/ch13/fig_13_04.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/fig1305-caption.txt').write_text('图 13.5. 控制网数据结构。\\\\\n'+r'\texttt{CNET}包含两个最高索引$n,m$和指针\texttt{Pw}；\texttt{Pw}指向$n+1$个列指针，每个\texttt{Pw[i]}指向包含$m+1$个齐次控制点的第$i$列。'+'\\\\\n'+r'\texttt{Pw[i][j]}访问该列第$j$项；图中展开第0列和第$n$列，其余列以省略号表示，每项均有四个齐次分量。'+'\n',encoding='utf-8');print('PASS CNET n/m/Pw, n+1column pointers to m+1four-component controls, indices i/j explicit.')
