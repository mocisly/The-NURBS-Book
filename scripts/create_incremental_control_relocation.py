"""Printed11.7: identical control increments and exact equal selected-point steps."""
from pathlib import Path
from fractions import Fraction as F
import json
from point_relocation_example_data import U,P,DIRECTION,peak
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch11/fig_11_07.tex')['applied']
t=F(3,5);step=F(2,5);B=tuple((F(i==4),) for i in range(9));N=de_boor(U,B,3,t)[0];deltaalpha=step/N;delta=tuple(deltaalpha*v for v in DIRECTION)
curves=[P];points=[de_boor(U,P,3,t)];proof=[];old=segments(U,P,3);basis=segments(U,B,3)
for n in range(1,5):
    Q=tuple(tuple(x+n*y for x,y in zip(p,delta)) if i==4 else p for i,p in enumerate(P));A=de_boor(U,Q,3,t);assert tuple(a-b for a,b in zip(A,points[-1]))==tuple(step*v for v in DIRECTION)
    assert tuple(a-b for a,b in zip(Q[4],curves[-1][4]))==delta
    identities=0
    for a,b,c in zip(old,segments(U,Q,3),basis):
        for axis in (0,1):assert all(y-x==n*delta[axis]*w for x,y,w in zip(a['power'][axis],b['power'][axis],c['power'][0]));identities+=4
        if a['b']<=U[4] or a['a']>=U[8]:assert a['power']==b['power']
    curves.append(Q);points.append(A);proof.append(dict(step=n,controls=Q,selected_point=A,exact_total_selected_distance=n*step,whole_power_coefficient_identities=identities))
out=['% Actual four equal point-distance increments by fixed delta-alpha and delta-P4; no tracing.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (8.7,3.8);'];nc=lines=0
out.append(r'\draw[book grid] '+'--'.join(point(p) for p in P)+';')
for Q in curves[1:]:out.append(r'\draw[book grid,dashed] '+point(P[3])+'--'+point(Q[4])+'--'+point(P[5])+';')
for v in (U[4]+(U[8]-U[4])*F(i,40) for i in range(1,40)):
    a,b=de_boor(U,P,3,v),de_boor(U,curves[-1],3,v)
    if sum((x-y)**2 for x,y in zip(a,b))<F(1,10000):continue
    assert (b[0]-a[0])*DIRECTION[1]==(b[1]-a[1])*DIRECTION[0]
    out.append(r'\draw[book grid] '+point(a)+'--'+point(b)+';');lines+=1
for n,Q in enumerate(curves):
    ss=segments(U,Q,3);nc+=check(U,Q,3,ss,steps=7)
    out.extend(cubic_path(s,'' if n==0 else 'dashed') for s in ss if n==0 or U[4]<=s['a'] and s['b']<=U[8])
for p in P:out.append(r'\draw '+point(p)+r' circle[radius=1.4pt];')
for Q in curves[1:-1]:out.append(r'\draw '+point(Q[4])+r' circle[radius=1.3pt];')
out.extend([r'\node[above=8pt] at '+point(P[4])+r' {$P_4$};',r'\draw[book axis] '+point(P[4])+'--'+point(curves[-1][4])+';',r'\draw '+point(curves[-1][4])+r' circle[radius=1.8pt] node[below=8pt] {$\widehat P_4$};',r'\draw[book grid] '+point(points[0])+'--'+point(points[-1])+';'])
for a in points:out.append(r'\draw '+point(a)+r' circle[radius=1.8pt];')
out.extend([r'\node[above right=8pt] at '+point(points[0])+r' {$P$};',r'\node[right=9pt] at '+point(points[-1])+r' {$\widehat P$};',r'\end{tikzpicture}'])
(root/'image_tex/ch11/fig_11_07.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r=dict(ubar=t,moved_control=4,unit_direction=DIRECTION,delta_selected_distance=step,delta_alpha=deltaalpha,delta_control=delta,basis_value_unchanged=N,stages=proof,all_successive_selected_displacements_exactly_equal=True,all_successive_control_displacements_exactly_equal=True,native_curve_checks=nc,actual_final_parallel_displacement_segments=lines,native_curve_error=0,no_contour_tracing=True)
(root/'image_tex/build/incremental-control-relocation-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.7:',nc,'nativechecks/',sum(a['whole_power_coefficient_identities'] for a in proof),'wholecoef;4equalexactpointstepsandcontrolsteps;deltaalpha',deltaalpha)
