from pathlib import Path
from fractions import Fraction as F
from memory_diagram import grid
root=Path(__file__).resolve().parents[1]
out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-4,-1.8) rectangle (14,5.8);']
for y,label in[(F(5),r'\texttt{Err=5 in N\_capreb}'),(F(5,2),r'\texttt{Err=7 in N\_clqapr}'),(F(0),r'\texttt{Err=1 in M\_ludcmp}')]:out+=grid(F(3),y,(F(10),),[(label,)],F(11,10))
out+=grid(-F(3,2),F(5),(F(11,10),),[('',)],F(11,10))
out.extend([r'\draw[book grid,book axis] (-.4,4.45)--(3,4.45);',r'\node at (-.95,3.2) {\texttt{calling routine}};',r'\draw[book grid,book axis] (8,0)--(8,1.4);',r'\draw[book grid,book axis] (8,2.5)--(8,3.9);',r'\end{tikzpicture}'])
(root/'image_tex/ch13/fig_13_07.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/fig1308-caption.txt').write_text('图 13.8. 错误栈示例。\\\\\n'+r'底层\texttt{M\_ludcmp}的错误逐层返回，\texttt{N\_clqapr}与\texttt{N\_capreb}依次补充本层错误；上层调用者获得包含各层信息的错误栈。'+'\\\\\n'+r'箭头表示错误向上返回的路径，错误码和例程名与原图一致；正文随后说明Nlib V2.0采用单一错误标志的选择。'+'\n',encoding='utf-8');print('PASS exact original codes5/7/1 androutine names, explicit upwarderrorpropagation andcalleraccess.')
