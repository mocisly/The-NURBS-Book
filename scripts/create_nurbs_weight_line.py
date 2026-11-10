"""Fig4.6: fixed-parameter points move on the exact line from B toward P3."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from rational_geometry import approximate,project
from surface_geometry import weights
from nurbs46_data import K,P,homogeneous,rational

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_06.tex';assert not target.exists()
family=(F(0),F(1),F(3));u0=F(5,8)
marks=[rational(u0,w)[0] for w in family]
lines=['% Fig4.6: representative SIX-control cubic, not the seven-control Fig4.1 polygon.',
       '% U=(0,0,0,0,1/3,2/3,1,1,1,1), other weights1, w3=0,1,3.',
       '% Fixed u=5/8; B=C(u;0), N=C(u;1), B3=C(u;3).',
       '% C=(1-alpha)B+alpha P3, alpha=w3*N3/(1-N3+w3*N3); exact collinearity.',
       '% Native cubic paths from mathematical homogeneous pieces, certified error<=0.0001cm.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-1.1,-4.1) rectangle (11,5.4);']
for i,p in enumerate(P):lines.append(r'\coordinate(P'+str(i)+') at '+point(p)+';')
lines += [r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5);',
          r'\draw[book grid,dashed] '+point(marks[0])+'--(P3);']
checks=paths=identities=0;maximum=F(0);minimum=F(1)
for w3 in family:
    segs=segments(K,homogeneous(w3),3);checks+=check(K,homogeneous(w3),3,segs)
    minimum=min(minimum,min(c[-1] for s in segs for c in s['bern']))
    assert minimum>0
    for s in segs:
        for a in approximate(s['bern']):
            lines.append(cubic_path(a));paths+=1;maximum=max(maximum,a['certified_l1_error'])
    for s in segs[:-1]:lines.append(r'\fill '+point(project(s['bern'][-1]))+' circle[radius=1.4pt];')
    for j in range(101):
        u=F(j,100);actual,_=rational(u,w3);B,_=rational(u,0);n=weights(K,3,u)
        alpha=w3*n[3]/(1-n[3]+w3*n[3])
        assert actual==tuple((1-alpha)*B[d]+alpha*P[3][d] for d in range(2));identities+=1
prev=None;fixed=[];B=marks[0];n=weights(K,3,u0)[3]
for w3 in (F(0),F(1,100),F(1,10),F(3,10),F(1),F(3),F(10),F(100)):
    c,_=rational(u0,w3);a=w3*n/(1-n+w3*n)
    assert 0<=a<1 and c==tuple((1-a)*B[d]+a*P[3][d] for d in range(2))
    assert (c[0]-B[0])*(P[3][1]-B[1])-(c[1]-B[1])*(P[3][0]-B[0])==0
    distance=sum((c[d]-P[3][d])**2 for d in range(2))
    assert prev is None or distance<prev;prev=distance
    fixed.append({'w3':str(w3),'point':list(map(str,c)),'alpha':str(a)})
for i,pos in enumerate(['below left','below','above left','above right','right','below']):
    lines += [r'\node[book point] at (P'+str(i)+') {};',r'\node['+pos+'=5pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};']
for c,label,anchor,gap in [(marks[0],r'\mathbf B','below left','6pt'),(marks[1],r'\mathbf N','left','12pt'),(marks[2],r'\mathbf B_3','above','12pt')]:
    lines += [r'\node[book point] at '+point(c)+' {};',r'\node['+anchor+'='+gap+'] at '+point(c)+' {$'+label+'$};']
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nurbs-weight-line-check.json').write_text(json.dumps({
    'figure':'4.6','representative_controls':[[str(v) for v in p] for p in P],
    'knots':list(map(str,K)),'fixed_parameter':str(u0),'family_weights':list(map(str,family)),
    'exact_homogeneous_checks':checks,'rational_partition_and_weight_line_identity_points':identities,
    'denominator_lower_bound_from_exact_bezier_controls':str(minimum),
    'native_cubic_paths':paths,'maximum_certified_l1_error_cm':str(maximum),'fixed_parameter_collinearity_and_monotonicity':fixed,
    'all_positive_weight_proof':'alpha=w3*N3/(1-N3+w3*N3) increases from0 to1 for fixed u with0<N3<1; C=(1-alpha)B+alpha*P3'},indent=2)+'\n')
print(f'PASS:{checks} homogeneous checks,{identities} weight-line identities,8 exact fixed-u collinearity/monotonicity cases,{paths} certified paths.')
