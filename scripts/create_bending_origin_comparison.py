from pathlib import Path
from fractions import Fraction as F
import json
from circular_bending_data import U,P,C,US,UE,bend
from native_bspline import segments,check,cubic_path,point
root=Path(__file__).resolve().parents[1];origins=(C,(F(0),F(6,5)),(-F(1),F(2)));cases=[bend(F(2),o)for o in origins];xmin=min(-F(4),min(x for Q,r in cases for x,y in Q))-F(3,5);xmax=max(F(4),max(x for Q,r in cases for x,y in Q))+F(6,5);bottom=min(-F(1),min(y for Q,r in cases for x,y in Q))-F(4,5)
lines=['% SAME curve/circle/lambda, only origin changes; actual projective/rigid maps.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] '+point((xmin,bottom-F(1,5)))+' rectangle '+point((xmax,F(18,5)))+';',r'\draw[book grid,dashed] (-2,3) arc[start angle=180,end angle=360,radius=2];',r'\node[above right=8pt] at (2,3) {$B(w)$};'];nc=0;reports=[]
for j,(Q,r)in enumerate(cases):
    style=('','dashed','dotted')[j];ss=segments(U,Q,3);nc+=check(U,Q,3,ss,steps=2);lines.extend(cubic_path(s,style)for s in ss);o=origins[j];lines.append(r'\draw '+point(o)+r' circle[radius=1.8pt] node[above left=8pt] {$O_'+str(j+1)+'$};')
    x=-F(3)+3*j;lines.extend([r'\draw['+style+'] '+point((x,bottom))+'--'+point((x+F(1,2),bottom))+';',r'\node[anchor=west] at '+point((x+F(3,5),bottom))+r' {$\widehat C(O_'+str(j+1)+')$};']);r.update(controls=Q);reports.append(r)
lines.extend(cubic_path(s,'book grid')for s in segments(U,P,3));lines.extend([r'\node[below right=7pt] at '+point(P[-1])+r' {$C(u)$};',r'\end{tikzpicture}']);(root/'image_tex/ch11/fig_11_36.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/bending-origin-comparison-check.json').write_text(json.dumps(dict(knots=U,original_controls=P,lambda_value=2,origins=origins,cases=reports,native_checks=nc,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.30',nc,'nativechecks, samecircle/curve/lambda2,3insideorigins; exactcrossratios and numericalcircle/rigidchecks.')
