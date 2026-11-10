from pathlib import Path
from fractions import Fraction as F
from memory_diagram import grid
from native_bspline import point
root=Path(__file__).resolve().parents[1]
out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1,-7.2) rectangle (27,6.4);',r'\node at (12,5.8) {\texttt{stacks : STACKS}};']
out+=grid(F(0),F(5),(F(4),)*6,[(r'\texttt{i1d}',r'\texttt{i2d}',r'\texttt{r1d}',r'\texttt{r2d}',r'$\ldots$',r'\texttt{knt}')],F(9,10))
for x in(6,10):
    out+=grid(F(x)-F(4,5),F(14,5),(F(8,5),),[(r'\texttt{NULL}',)],F(9,10));out.append(r'\draw[book grid,book axis] '+point((x,F(41,10)))+'--'+point((x,F(14,5)))+';')
for x,count,prefix in[(2,2,'I'),(14,3,'R'),(22,1,'K')]:
    out.append(r'\draw[book grid,book axis] '+point((x,F(41,10)))+'--'+point((x,F(3,2)))+';')
    for j in range(count):
        y=F(3,2)-3*j;left=F(x)-1
        out+=grid(left,y,(F(2),),[(r'\texttt{ptr}',),(r'\texttt{next}'if j<count-1 else r'\texttt{NULL}',)],F(9,10))
        out+=grid(F(x)+F(9,5),y,(F(14,5),),[('$'+prefix+'_{'+str(j+1)+'}$',)],F(9,10))
        out.append(r'\draw[book grid,book axis] '+point((x+1,y-F(9,20)))+'--'+point((F(x)+F(9,5),y-F(9,20)))+';')
        if j<count-1:out.append(r'\draw[book grid,book axis] '+point((x,y-F(9,5)))+'--'+point((x,y-3))+';')
out.append(r'\end{tikzpicture}');(root/'image_tex/ch13/fig_13_06.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/fig1307-caption.txt').write_text('图 13.7. 按内存类型分别维护的链式内存栈示例。\\\\\n'+r'\texttt{STACKS}保存各类链表的头指针；此例中\texttt{i1d,r2d,knt}非空，\texttt{i2d,r1d}为空，其余类型以省略号表示。'+'\\\\\n'+r'每个节点保存已分配内存的\texttt{ptr}及链指针\texttt{next}；右侧小框$I_j,R_j,K_j$代表相应类型的内存块，空栈和链尾均为\texttt{NULL}。'+'\n',encoding='utf-8');print('PASS typedstack heads,2/3/1nodes, explicitptr/next/NULL, distinct allocation blocks; semantic linked lists.')
