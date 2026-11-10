"""One printed figure11.2 or11.3, actual single-control relocation and vectors."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
from point_relocation_example_data import U,P,GRE,relocate
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('number',type=int,choices=(2,3));a=parser.parse_args();t=F(37,100) if a.number==2 else F(43,100);k=3
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']==f'image_tex/ch11/fig_11_{a.number:02}.tex')['applied']
Q,r=relocate(U,P,k,t);assert min(range(len(P)),key=lambda i:abs(GRE[i]-t))==k
out=['% Actual relocation constrained at the printed parameter; shared input curve and requested movement.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (8.7,3.8);'];nc=lines=0
out.append(r'\draw[book grid] '+'--'.join(point(p) for p in P)+';');out.append(r'\draw[book grid,dashed] '+point(P[k-1])+'--'+point(Q[k])+'--'+point(P[k+1])+';')
for v in (U[k]+(U[k+4]-U[k])*F(i,36) for i in range(1,36)):
    x,y=de_boor(U,P,3,v),de_boor(U,Q,3,v)
    if sum((a-b)**2 for a,b in zip(x,y))<F(1,10000):continue
    assert (y[0]-x[0])*r['unit_direction'][1]==(y[1]-x[1])*r['unit_direction'][0]
    out.append(r'\draw[book grid] '+point(x)+'--'+point(y)+';');lines+=1
for C,style in [(P,''),(Q,'dashed')]:
    ss=segments(U,C,3);nc+=check(U,C,3,ss,steps=7);out.extend(cubic_path(s,style) for s in ss)
for p in P:out.append(r'\draw '+point(p)+r' circle[radius=1.4pt];')
out.extend([r'\node[above left=7pt] at '+point(P[k])+r' {$P_3$};',r'\draw[book axis] '+point(P[k])+'--'+point(Q[k])+';',r'\draw '+point(Q[k])+r' circle[radius=1.6pt] node[below=7pt] {$\widehat P_3$};'])
out.extend([r'\draw '+point(r['selected_point'])+r' circle[radius=2.1pt] node[above right=8pt] {$P$};',r'\draw '+point(r['new_selected_point'])+r' circle[radius=2.1pt] node[right=8pt] {$\widehat P$};',r'\end{tikzpicture}'])
(root/f'image_tex/ch11/fig_11_{a.number:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8');r.update(native_curve_checks=nc,actual_parallel_displacement_segments=lines,no_contour_tracing=True,native_curve_error=0)
(root/f'image_tex/build/single-point-relocation-{a.number}-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.'+str(a.number),nc,'nativechecks/',lines,'actualparallelvectors;48poweridentities;targetdistanceexact;maximumratio',float(r['maximum_to_requested_ratio']))
