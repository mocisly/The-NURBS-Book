from pathlib import Path
from fractions import Fraction as F
import json
from circular_bending_data import U,P,C,US,UE,bend
from native_bspline import segments,check,cubic_path,point,number
root=Path(__file__).resolve().parents[1];cases=[(l,*bend(l))for l in(F(1,2),F(1),F(2),F(5))];xmin=min(x for _,Q,_ in cases for x,y in Q)-F(3,5);xmax=max(x for _,Q,_ in cases for x,y in Q)+F(6,5);ymin=min(-F(1),min(y for _,Q,_ in cases for x,y in Q))-F(3,5)
lines=['% Actual circular projective bends and rigidly repositioned exterior controls, not traces.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] '+point((xmin,ymin))+' rectangle '+point((xmax,F(18,5)))+';',r'\draw[book grid,dotted] (0,-1.4)--(0,3.2) node[above right=4pt] {$L$};',r'\draw[book grid,dashed] (-2,3) arc[start angle=180,end angle=360,radius=2];',r'\draw (0,3) circle[radius=1.8pt] node[above left=8pt] {$O$};',r'\node[above left=14pt] at (2,3) {$B(w)$};'];nc=0;reports=[]
for l,Q,r in cases:
    ss=segments(U,Q,3);nc+=check(U,Q,3,ss,steps=2);lines.extend(cubic_path(s)for s in ss);label=r'\frac12'if l==F(1,2)else str(l);lines.append(r'\node[right=8pt] at '+point(Q[-1])+r' {$\lambda='+label+'$};');r.update(controls=Q);reports.append(r)
lines.extend(cubic_path(s,'book grid,dotted')for s in segments(U,P,3));lines.extend([r'\node[below right=7pt] at '+point(P[-1])+r' {$C(u)$};',r'\end{tikzpicture}']);(root/'image_tex/ch11/fig_11_35.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/circular-bending-family-check.json').write_text(json.dumps(dict(knots=U,original_controls=P,interval=(US,UE),cases=reports,native_checks=nc,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.29',nc,'nativechecks; four specified lambdas, circle residual<1e-14 and rigid exterior error<1e-10; endpoints',[(str(l),list(map(float,Q[-1])))for l,Q,_ in cases])
