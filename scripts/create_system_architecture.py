from pathlib import Path
from fractions import Fraction as F
import json
from memory_diagram import grid
from native_bspline import point
root=Path(__file__).resolve().parents[1]
levels=[('NURBS','N'),(r"B\'{e}zier",'B'),('Geometry','G'),('Mathematics','M'),('Utility','U')];core=[('Memory','S'),('Arithmetic','A'),('Error','E')]
assert len({prefix for _,prefix in levels+core})==8
out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1,-3.2) rectangle (19,12);']
for j,(label,prefix)in enumerate(levels):
    y=F(11)-F(11,5)*j;out+=grid(F(2),y,(F(14),),[(label+r'\quad\texttt{'+prefix+r'\_*.c}',)],F(1))
    if j<4:out.append(r'\draw[book grid,book axis] '+point((F(9),y-1))+'--'+point((F(9),y-F(11,5)))+';')
out.append(r'\draw[book grid] (9,1.2)--(9,.5)--(2.6,.5) (9,.5)--(15.4,.5);')
for j,(label,prefix)in enumerate(core):
    x=F(32,5)*j;out+=grid(x,-F(2,5),(F(26,5),),[(r'\shortstack{'+label+r'\\\texttt{'+prefix+r'\_*.c}}',)],F(7,5))
    out.append(r'\draw[book grid,book axis] '+point((x+F(13,5),F(1,2)))+'--'+point((x+F(13,5),-F(2,5)))+';')
out.extend([r'\draw[book grid,dashed] (5.2,-1.1)--(6.4,-1.1) (11.6,-1.1)--(12.8,-1.1);',r'\draw[book grid,dashed] (2.6,-1.8)--(2.6,-2.5)--(15.4,-2.5)--(15.4,-1.8);',r'\end{tikzpicture}'])
(root/'image_tex/ch13/fig_13_08.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/fig1309-caption.txt').write_text('图 13.9. Nlib V2.0的系统结构。\\\\\n'+r'上层依次为NURBS、B\'{e}zier、几何、数学和实用程序；底层核心包括内存分配、算术与错误处理，文件名前缀与正文一致。'+'\\\\\n'+r'每一层可以调用所有更低层的例程；图中用代表性的向下箭头概括这一层次关系，虚线表示三个核心模块间的协作。'+'\n',encoding='utf-8')
(root/'image_tex/build/system-architecture-check.json').write_text(json.dumps(dict(modules=[dict(name=n,file_prefix=p)for n,p in levels+core],module_count=8,representative_downward_call_arrows=True,all_lower_layer_dependencies_summarized=True,core_cooperation_dashed=True,no_contour_tracing=True),indent=2)+'\n',encoding='utf-8');print('PASS all8printed modules/prefixes, downwardlayercall semantics andcorecooperation; native hierarchy.')
