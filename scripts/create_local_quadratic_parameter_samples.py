"""9.21:same quadratic geometry,uniform parameter samples under C1and chord G1knots."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
from local_parabolic_interpolation_data import Q,R,FULL,C1PARAMS,UC,MINIMAL,knots
from native_bspline import segments,check,de_boor,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (25,26):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex')['applied']
squares=tuple(sum((b-a)**2 for a,b in zip(A,B)) for A,B in zip(Q,Q[1:]));scale=10**12
lo=tuple(F(isqrt(x.numerator*scale**2//x.denominator),scale) for x in squares);hi=tuple(x+F(1,scale) for x in lo)
assert all(a*a<=s<b*b for a,b,s in zip(lo,hi,squares))
chord=(F(0),)+tuple(sum(lo[:i])/sum(lo) for i in range(1,5))+(F(1),)
bounds=tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,5))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(chord[1:-1],bounds))
KG=knots(chord);reports=[]
for n,K,P,params,letter in [(25,UC,MINIMAL,C1PARAMS,'a'),(26,KG,FULL,chord,'b')]:
    ss=segments(K,P,2);nc=check(K,P,2,ss)
    assert all(s['bern']==(Q[i],R[i],Q[i+1]) for i,s in enumerate(ss))
    samples=tuple(de_boor(K,P,2,F(i,40)) for i in range(41))
    jumps=[]
    for i in range(1,5):
        incoming=tuple(2*(Q[i][j]-R[i-1][j])/(params[i]-params[i-1]) for j in range(2))
        outgoing=tuple(2*(R[i][j]-Q[i][j])/(params[i+1]-params[i]) for j in range(2))
        jumps.append(tuple(b-a for a,b in zip(incoming,outgoing)))
    assert all(not any(j) for j in jumps) if letter=='a' else any(any(j) for j in jumps)
    lines=['% Actual quadratic spline evaluations at u=i/40;same five Bezier geometries as9.20.',r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-.9,-1.2) rectangle (9.3,5.7);',r'\draw[book grid,dashed] '+'--'.join(map(point,MINIMAL))+';']
    for pt in samples[1:-1]:
        xy=point(pt);lines.append(r'\draw '+xy+r' ++(-1.8pt,0)--++(3.6pt,0);')
        lines.append(r'\draw '+xy+r' ++(0,-1.8pt)--++(0,3.6pt);')
    for i,(q,anchor) in enumerate(zip(Q,['right','right','below right','below left','left','left'])):
        lines.extend([r'\draw '+point(q)+r' circle[radius=2.4pt];',r'\fill '+point(q)+r' circle[radius=1pt];',r'\node['+anchor+r'=8pt] at '+point(q)+r' {$\mathbf Q_'+str(i)+'$};'])
    for i,(r,anchor) in enumerate(zip(R,['left','above left','above','above right','right']),1):
        lines.extend([r'\draw '+point(r)+r' circle[radius=2.4pt];',r'\node['+anchor+r'=8pt] at '+point(r)+r' {$\mathbf R_'+str(i)+'$};'])
    lines.extend([r'\node at (4.2,-.85) {('+letter+')};',r'\end{tikzpicture}'])
    (root/f'image_tex/ch09/fig_9_{n:02}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    reports.append(dict(panel=letter,parameterization='C1' if letter=='a' else 'chordG1',data_parameters=list(map(str,params)),knots=list(map(str,K)),same5Bezier_geometries_exact=True,native_curve_checks=nc,uniform_parameter_sample_count=41,interior_plus_marker_count=39,sample_parameters=[str(F(i,40)) for i in range(41)],sample_points=[[str(x) for x in pt] for pt in samples],exact_derivative_jumps=[[str(x) for x in row] for row in jumps]))
(root/'image_tex/build/local-quadratic-parameter-samples-check.json').write_text(json.dumps(dict(figure='9.21',same_representative_geometry_as='9.20',panels=reports,chord_parameter_enclosures=[[str(x) for x in b] for b in bounds],chord_enclosure_width_less_than='1e-11',sampling_is_uniform_parameter_not_arc_length=True),indent=2)+'\n')
print('PASS:same5Beziergeometries exactly,C1zero derivative jumps/chordG1nonzero jumps;41actual uniform-u evaluations each,certified chord params.')
