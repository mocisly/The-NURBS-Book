"""Fig5.36: exact threefold knot removal after quartic-to-quintic elevation."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,de_boor
from native_polynomial_drawing import paths
from rational_geometry import elevate
from inverse_knot_projection import remove_to

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_51.tex';assert not target.exists()
U=(F(0),)*5+(F('.5'),)+(F(1),)*5
P=tuple(tuple(F(str(t)) for t in q) for q in [(-5,0),(-4,-1),(-2,-3),(2,5),(6,4),(5,-4)])
ss=segments(U,P,4);checks=check(U,P,4,ss)
E=[elevate(s['bern']) for s in ss]
K=(F(0),)*6+(F('.5'),)*5+(F(1),)*6;Q=E[0]+E[1][1:]
stages=[(K,Q)];proofs=[]
for j in range(3):
    K,Q,proof=remove_to(K,Q,5,[F('.5')]);assert proof['curve_exactly_unchanged']
    stages.append((K,Q));proofs.append(proof)
assert [len(q) for k,q in stages]==[11,10,9,8]
comparisons=0
for K,Q in stages:
    segs=segments(K,Q,5);checks+=check(K,Q,5,segs)
    for a,b in zip(ss,segs):assert all(tuple(x)+(F(0),)==tuple(y) for x,y in zip(a['power'],b['power']))
    for i in range(201):
        u=F(i,200);assert de_boor(K,Q,5,u)==de_boor(U,P,4,u);comparisons+=1
R=[q for k,q in stages];mid=lambda a,b:tuple((x+y)/2 for x,y in zip(a,b))
# The inward equations verify the shortcuts; no coordinate fitting is involved.
assert R[0][5]==mid(R[1][4],R[1][5])
assert R[1][4]==mid(R[2][3],R[2][4]) and R[1][5]==mid(R[2][4],R[2][5])
assert all(R[2][i]==mid(R[3][i-1],R[3][i]) for i in (3,4,5))
drawing,certificate=paths(ss)
lines=['% Representative quartic, elevated exactly to quintic; 3 zero-residual removals.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-6.4,-5.3) rectangle (8,6);',
       r'\draw[book grid] '+'--'.join(map(point,R[0]))+';']
for state,start,end,style in [(1,3,7,'dashed'),(2,2,6,'densely dotted'),(3,2,5,'dashed')]:
    lines.append(r'\draw[book grid,'+style+'] '+'--'.join(map(point,R[state][start:end+1]))+';')
lines+=drawing
for q in R[0]:lines.append(r'\draw '+point(q)+r' circle[radius=1.8pt];')
for q in (R[2][3],R[3][3],R[3][4]):
    x,y=q;d=F(7,100);lines.append(r'\draw '+point((x-d,y-d))+' rectangle '+point((x+d,y+d))+';')
labels=[(R[0][5],r'\mathbf P_k^0','below=8pt'),
        (R[1][4],r'\mathbf P_{k-1}^1','above left=8pt'),
        (R[1][5],r'\mathbf P_k^1','above right=8pt'),
        (R[2][3],r'\mathbf P_{k-1}^2','below left=12pt'),
        (R[3][3],r'\mathbf P_{k-1}^3','below left=8pt'),
        (R[3][4],r'\mathbf P_k^3','above=8pt')]
for q,label,where in labels:lines.append(r'\node['+where+'] at '+point(q)+' {$'+label+'$};')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/elevated-knot-removal-check.json').write_text(json.dumps({
    'figure':'5.36','original_degree':4,'elevated_degree':5,'original_U':list(map(str,U)),
    'representative_controls':[[str(t) for t in q] for q in P],
    'stage_knots':[list(map(str,k)) for k,q in stages],
    'stage_controls':[[[str(t) for t in q] for q in controls] for k,controls in stages],
    'three_exact_removal_proofs':proofs,'inward_midpoint_identities_exact':True,
    'native_checks':checks,'invariance_comparisons':comparisons,'native_render_certificate':certificate},indent=2)+'\n')
print(f'PASS: {checks} native checks, {comparisons} invariance points; all inward identities and three removals exact.')
