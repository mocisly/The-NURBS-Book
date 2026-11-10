"""11.13 equal selected-point increments on the SAME11.11/12 curve."""
from pathlib import Path
from fractions import Fraction as F
import json
from weight_pull_data import U,P,W0,homogeneous,curve,modified_weight,DIRECTIONS
from native_bspline import segments,check,cubic_path,point,number
from rational_geometry import approximate
root=Path(__file__).resolve().parents[1];u=F(13,25);delta=F(11,500);W=[modified_weight(u,j*delta) for j in range(5)];A=curve(u,W0)
lines=['% Same representative curve as11.11/12; four EXACT distance increments.022.',r'\begin{tikzpicture}[book line,x=20cm,y=20cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.05,-.18) rectangle (.92,.69);',r'\draw[book grid] '+'--'.join(point(p) for p in P)+';'];proof=[];nc=0
for j,w in enumerate(W):
    ss=segments(U,homogeneous(w),3);nc+=check(U,homogeneous(w),3,ss,steps=7);paths=[p for s in ss for p in approximate(s['bern'],F(1,2000000))];lines.extend(cubic_path(p,'' if j==0 else 'dashed') for p in paths);Z=curve(u,w)
    assert tuple(z-a for a,z in zip(A,Z))==tuple(j*delta*v for v in DIRECTIONS[u]);lines.append(r'\draw '+point(Z)+r' circle[radius=1.6pt];')
    proof.append(dict(step=j,weight=w,point=Z,exact_distance_squared=(j*delta)**2,certified_screen_error_cm=max(p['certified_l1_error'] for p in paths)*20))
for j in range(1,30):
    v=F(1,5)+F(7,10)*F(j,30);x,y=curve(v,W0),curve(v,W[-1]);assert (y[0]-x[0])*(P[4][1]-x[1])==(y[1]-x[1])*(P[4][0]-x[0])
    if sum((a-b)**2 for a,b in zip(x,y))>F(1,1000000):lines.append(r'\draw[book grid] '+point(x)+'--'+point(y)+';')
for p in P:lines.append(r'\draw '+point(p)+r' circle[radius=1.4pt];')
lines.extend([r'\node[above=10pt] at '+point(P[4])+r' {$P_4$};',r'\draw[book axis] '+point(A)+'--'+point(curve(u,W[-1]))+';',r'\node[anchor=west] at (.04,.64) {$\Delta d=0.022,\quad j=0,\ldots,4$};',r'\draw[book axis] (0,-.10)--(.84,-.10) node[right=6pt] {$w_4$};'])
for j,w in enumerate(W):
    x=F(4,5)*w/6;lines.append(r'\draw[book grid] '+point((x,-F(21,200)))+'--'+point((x,-F(19,200)))+';')
    lines.append(r'\node['+('below' if j%2==0 else 'above')+r'=7pt] at '+point((x,-F(1,10)))+' {$'+f'{float(w):.3f}'.rstrip('0').rstrip('.')+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_15.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/incremental-weight-pull-check.json').write_text(json.dumps(dict(knots=U,controls=P,parameter=u,increment=delta,weights=W,native_checks=nc,steps=proof,exact_equal_distance_increments=True,all_unmodified_control_points=True,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.13',nc,'native checks; four equal distance increments; weights',list(map(float,W)))
