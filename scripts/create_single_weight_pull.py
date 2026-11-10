from pathlib import Path
from fractions import Fraction as F
import argparse,json
from weight_pull_data import U,P,W0,homogeneous,curve,ts,modified_weight,DIRECTIONS
from native_bspline import segments,check,cubic_path,point
from rational_geometry import approximate
a=argparse.ArgumentParser();a.add_argument('figure',type=int,choices=(11,12));arg=a.parse_args();fig=arg.figure;source=fig+2
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']==f'image_tex/ch11/fig_11_{source:02}.tex')['applied']
u,w=(F(13,25),F(49,20)) if fig==11 else (F(23,50),F(97,100))
A,Z=curve(u,W0),curve(u,w);assert sum((y-x)**2 for x,y in zip(A,Z))==F(3,40)**2
lines=['% Representative controls solved from BOTH printed target pairs, not traced.',r'\begin{tikzpicture}[book line,x=20cm,y=20cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.05,-.06) rectangle (.92,.69);',r'\draw[book grid] '+'--'.join(point(p) for p in P)+';'];proof=[];perspective=0
for old,style in [(W0,''),(w,'dashed')]:
    H=homogeneous(old);ss=segments(U,H,3);nc=check(U,H,3,ss,steps=7);paths=[p for s in ss for p in approximate(s['bern'],F(1,2000000))];lines.extend(cubic_path(p,style) for p in paths);proof.append(dict(weight=old,native_checks=nc,native_paths=len(paths),certified_screen_error_cm=max(p['certified_l1_error'] for p in paths)*20))
for j in range(1,40):
    t=F(1,5)+F(7,10)*F(j,40);x,y=curve(t,W0),curve(t,w)
    if sum((a-b)**2 for a,b in zip(x,y))<F(1,1000000):continue
    assert (y[0]-x[0])*(P[4][1]-x[1])==(y[1]-x[1])*(P[4][0]-x[0]);perspective+=1
    lines.append(r'\draw[book grid] '+point(x)+'--'+point(y)+';')
for i,p in enumerate(P):lines.append(r'\draw '+point(p)+r' circle[radius=1.5pt];')
lines.extend([r'\node[above right=10pt] at '+point(P[4])+r' {$P_4$};',r'\draw[book grid,dotted] '+point(A)+'--'+point(P[4])+';',r'\draw '+point(A)+r' circle[radius=2pt] node[below right=8pt] {$P$};',r'\draw '+point(Z)+r' circle[radius=2pt] node[above left=32pt] {$\widehat P$};',r'\draw[book axis] '+point(A)+'--'+point(Z)+';',r'\node[anchor=west] at (.04,.64) {$|P\widehat P|=0.075$};',r'\end{tikzpicture}'])
(root/f'image_tex/ch11/fig_11_{source:02}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/f'image_tex/build/single-weight-pull-{fig}-check.json').write_text(json.dumps(dict(controls=P,knots=U,parameter=u,old_weight=W0,new_weight=w,old_point=A,new_point=Z,exact_displacement=tuple(F(3,40)*v for v in DIRECTIONS[u]),distance_squared=F(3,40)**2,two_printed_target_pairs_exact=True,perspective_lines=perspective,proofs=proof,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8')
print('PASS',fig,'exact printed weight and distance; controls',[[round(float(x),5) for x in p] for p in P],perspective,'exact perspective lines')
