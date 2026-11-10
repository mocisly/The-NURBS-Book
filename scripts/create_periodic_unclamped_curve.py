from pathlib import Path
import json
from fractions import Fraction as F
from periodic_curve_data import K,P,POLYGON
from unclamped_geometry import verified_segments
from native_bspline import cubic_path,point,de_boor
from bspline_math import derivative,evaluate
root=Path(__file__).resolve().parents[1];ss,n=verified_segments(K,P,3);closure=[]
for a,b in zip(ss[0]['power'],ss[-1]['power']):
    c=[]
    for order in range(3):
        x,y=evaluate(a,F(3)),evaluate(b,F(8));assert x==y;c.append(x);a,b=derivative(a),derivative(b)
    closure.append(c)
out=[r'\begin{tikzpicture}[book line,x=4cm,y=4cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-2.4,-2.3) rectangle (2.4,2.1);',r'\draw[book grid,dashed] '+'--'.join(point(q)for q in POLYGON)+'--cycle;'];out.extend(cubic_path(s)for s in ss)
for i,q in enumerate(POLYGON):
    anchor={0:'above left=7pt',1:'left=7pt',2:'below=7pt',3:'right=7pt',4:'above=7pt'}[i]
    label='P_'+str(i)+(('=P_'+str(i+5))if i<3 else'');out.append(r'\draw[book grid] '+point(q)+r' circle[radius=1.6pt] node['+anchor+r'] {$'+label+'$};')
for u in range(3,8):out.append(r'\draw[book grid] '+point(de_boor(K,P,3,F(u)))+r' node[rectangle,draw,inner sep=1.5pt] {};')
out.append(r'\end{tikzpicture}');(root/'image_tex/ch12/fig_12_02.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/periodic-unclamped-curve-check.json').write_text(json.dumps(dict(knots=K,degree=3,controls=P,wrapped_controls=3,domain=(3,8),exact_C2_endpoint_position_and_derivatives=closure,native_checks=n,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS printedU2/wrap3; exactC2closure position+2derivatives; nativechecks',n)
