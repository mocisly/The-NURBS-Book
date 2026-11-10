"""10.6 separate spine tangents and their parallel control-column derivatives."""
from pathlib import Path
from fractions import Fraction as F
import json
from spine_skinning_example_data import SPINE_P,SECTION_K,view
from spine_skinning_derivatives import construct
from native_bspline import segments,check,cubic_path,point
from rational_geometry import approximate
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in m['images'] if e['tex']=='image_tex/ch10/fig_10_09.tex')['applied']
Q,P,D,C,DV,report=construct();nc=0;scale=F(1,12)
out=['% Spine/control-column derivative construction from actual shared10.4/5 data. All arrows share1/12scale.',r'\begin{tikzpicture}[book line]',r'\begin{scope}',r'\path[use as bounding box] (0,-12.5) rectangle (12.5,5);']
sp=approximate(tuple(view(p)+(F(1),) for p in SPINE_P),F(1,100000));out.extend(cubic_path(s) for s in sp)
out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in P)+';')
for k,row in enumerate(Q):
    ss=segments(SECTION_K,row,3);nc+=check(SECTION_K,row,3,ss,steps=7)
    out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern'])),'book grid') for s in ss)
    a=view(P[k]);b=view(tuple(x+scale*d for x,d in zip(P[k],D[k])))
    out.append(r'\fill '+point(a)+r' circle[radius=1.5pt];')
    out.append((r'\node[above right=5pt] at ' if k==2 else r'\node[above left=5pt] at ')+point(a)+r' {$P_'+str(k)+r'$};')
    out.append(r'\draw[book axis] '+point(a)+'--'+point(b)+r' node[right=5pt] {$D_'+str(k)+r'$};')
for k in (1,3):
    a,b=map(view,(P[k-1],P[k]));mid=tuple((x+y)/2 for x,y in zip(a,b))
    out.append(r'\node[left=7pt] at '+point(mid)+r' {$d_'+str(k)+r'$};')
out.extend([r'\node at (6,4.5) {$P_k=C_s(\widehat v_k),\quad D_k=C_s^\prime(\widehat v_k)$};',r'\node at (6,-12.1) {(a)};',r'\end{scope}',r'\begin{scope}[xshift=14cm]',r'\path[use as bounding box] (-.5,-12.5) rectangle (12.5,5);'])
# Translate the selected section into the clear top half of the second panel.
delta=(F(0),F(2));tr=lambda p:tuple(a+b for a,b in zip(view(p),delta))
row=Q[1]
out.append(r'\draw[book grid,dashed] '+'--'.join(point(tr(p)) for p in row)+';')
out.extend(cubic_path(dict(bern=tuple(tr(p) for p in s['bern']))) for s in segments(SECTION_K,row,3))
for i,p in enumerate(row):
    a=tr(p);end=tr(tuple(x+scale*d for x,d in zip(p,DV[i][1])))
    out.append(r'\fill '+point(a)+r' circle[radius=1.3pt];')
    out.append(r'\draw[book axis] '+point(a)+'--'+point(end)+';')
    if i in (0,3,6):out.append(r'\node[below=5pt] at '+point(end)+r' {$D_{'+str(i)+r',1}$};')
out.extend([r'\node at (6,4.5) {$k=1:\quad P_{i,1},\ D_{i,1}$};',r'\node at (6,-3) {$D_{i,1}=c_{i,1}D_1,\qquad c_{i,1}>0$};',r'\node at (6,-4.1) {$\displaystyle c_{i,1}=\frac{\lVert P_{i,2}-P_{i,1}\rVert+\lVert P_{i,1}-P_{i,0}\rVert}{d_2+d_1}$};',r'\node at (6,-12.1) {(b)};',r'\end{scope}',r'\end{tikzpicture}'])
(root/'image_tex/ch10/fig_10_09.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report.update(figure='10.6',shared_data_from='10.4/10.5',native_checks=nc,common_arrow_display_scale='1/12',all35positive_parallel_vectors=True,no_contour_tracing=True)
(root/'image_tex/build/spine-derivative-construction-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS10.6:',nc,'native checks;all35derivative positive factors/error<1e-10;common1/12arrow scale.')
