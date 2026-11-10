"""Printed11.6: exact Eq11.7--11.9 for both gamma values and same target point."""
from pathlib import Path
from fractions import Fraction as F
import json
from point_relocation_example_data import U,P,GRE,DIRECTION,DISTANCE
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import derivative,evaluate
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch11/fig_11_06.tex')['applied']
t=F(43,100);default=(t-GRE[3])/(GRE[4]-GRE[3]);assert default==F(8,17)
out=['% Exact same curve, selected point, direction and distance as11.3; two-control Eq11.7--11.9.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm]'];reports=[]
for letter,gamma,shift in [('a',default,F(21,2)),('b',F(4,5),F(0))]:
    B=tuple((1-gamma if i==3 else gamma if i==4 else F(0),) for i in range(9));w=de_boor(U,B,3,t)[0];alpha=DISTANCE/w
    Q=tuple(tuple(x+(1-gamma if i==3 else gamma if i==4 else F(0))*alpha*v for x,v in zip(p,DIRECTION)) for i,p in enumerate(P))
    A=de_boor(U,P,3,t);Z=de_boor(U,Q,3,t);assert tuple(z-a for a,z in zip(A,Z))==tuple(DISTANCE*v for v in DIRECTION)
    identities=0;found=None;falling=False
    old,new,basis=(segments(U,C,3) for C in (P,Q,B))
    for a,b,c in zip(old,new,basis):
        for axis in (0,1):assert all(y-x==alpha*DIRECTION[axis]*v for x,y,v in zip(a['power'][axis],b['power'][axis],c['power'][0]));identities+=4
        if a['a']>=U[8]:assert a['power']==b['power']
        coeff=tuple(3*(y[0]-x[0])/(c['b']-c['a']) for x,y in zip(c['bern'],c['bern'][1:]))
        if not any(coeff):continue
        if min(coeff)>=0:assert not falling
        elif max(coeff)<=0:falling=True
        else:assert coeff[0]>0 and coeff[-1]<0 and found is None and not falling;found=c;falling=True
    assert found is not None;lo,hi=found['a'],found['b'];der=derivative(found['power'][0])
    for _ in range(64):
        mid=(lo+hi)/2
        if evaluate(der,mid)>0:lo=mid
        else:hi=mid
    peak=(lo+hi)/2;maxratio=de_boor(U,B,3,peak)[0]/w
    out.extend([r'\begin{scope}[yshift='+str(float(shift))+r'cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (8.7,3.95);']);nc=lines=0
    out.append(r'\draw[book grid] '+'--'.join(point(p) for p in P)+';');out.append(r'\draw[book grid,dashed] '+point(P[2])+'--'+point(Q[3])+'--'+point(Q[4])+'--'+point(P[5])+';')
    for u in (U[3]+(U[8]-U[3])*F(i,44) for i in range(1,44)):
        a,b=de_boor(U,P,3,u),de_boor(U,Q,3,u)
        if sum((x-y)**2 for x,y in zip(a,b))<F(1,10000):continue
        assert (b[0]-a[0])*DIRECTION[1]==(b[1]-a[1])*DIRECTION[0]
        out.append(r'\draw[book grid] '+point(a)+'--'+point(b)+';');lines+=1
    for C,style in [(P,''),(Q,'dashed')]:
        ss=segments(U,C,3);nc+=check(U,C,3,ss,steps=7);out.extend(cubic_path(s,style) for s in ss)
    for p in P:out.append(r'\draw '+point(p)+r' circle[radius=1.4pt];')
    for k,anchor in [(3,'below left'),(4,'below right')]:
        clearance=32 if letter=='b' and k==3 else 8
        out.extend([r'\node[above=8pt] at '+point(P[k])+r' {$P_'+str(k)+'$};',r'\draw[book axis] '+point(P[k])+'--'+point(Q[k])+';',r'\draw '+point(Q[k])+r' circle[radius=1.7pt] node['+anchor+'='+str(clearance)+r'pt] {$\widehat P_'+str(k)+'$};'])
    out.extend([r'\draw '+point(A)+r' circle[radius=2.1pt] node[above=16pt] {$P$};',r'\draw '+point(Z)+r' circle[radius=2.1pt] node[below=10pt] {$\widehat P$};',r'\node at (4,3.8) {$\gamma='+(r'8/17\simeq0.47' if letter=='a' else '4/5')+'$};',r'\node at (4,-.6) {('+letter+')};',r'\end{scope}'])
    reports.append(dict(panel=letter,gamma=gamma,alpha=alpha,knots=U,original_controls=P,modified_controls=Q,ubar=t,selected_point=A,modified_selected_point=Z,exact_target_distance=DISTANCE,unit_direction=DIRECTION,whole_power_coefficient_identities=identities,native_curve_checks=nc,actual_parallel_displacement_segments=lines,local_support=(U[3],U[8]),weighted_displacement_peak_parameter_bracket=(lo,hi),weighted_displacement_peak_parameter=peak,maximum_to_requested_ratio=maxratio))
out.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_06.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/two-control-relocation-check.json').write_text(json.dumps(dict(panels=reports,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.6:',sum(r['whole_power_coefficient_identities'] for r in reports),'wholecoef/',sum(r['native_curve_checks'] for r in reports),'nativechecks;twoexacttargets;maximumratios',[float(r['maximum_to_requested_ratio']) for r in reports])
