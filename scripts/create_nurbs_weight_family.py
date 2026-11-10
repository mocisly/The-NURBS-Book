"""Fig4.2: four curves from the same polygon, changing only weight3."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from surface_geometry import weights
from rational_geometry import approximate,project
from nurbs41_data import K,P,homogeneous,rational

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_02.tex';assert not target.exists()
family=(F(0),F(3,10),F(1),F(3))
lines=['% Fig4.2: same representative polygon/knots as Fig4.1, only w3 varies.',
       '% Four rational cubic curves, w3=0,3/10,1,3; all other weights1.',
       '% Exact homogeneous extraction and certified cubic error <=0.0001cm.',
       '% Mathematical rational-function rendering, never scan contours.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-1.2,-3.1) rectangle (12.5,4.4);']
for i,p in enumerate(P):lines.append(r'\coordinate(P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5)--(P6);')
exact=paths=partition=line_checks=0;maximum=F(0);denominator_minimum=F(1)
for w3 in family:
    segs=segments(K,homogeneous(w3),3);exact+=check(K,homogeneous(w3),3,segs)
    denominator_minimum=min(denominator_minimum,min(c[-1] for s in segs for c in s['bern']))
    assert min(c[-1] for s in segs for c in s['bern'])>=F(1,3)
    for s in segs:
        for a in approximate(s['bern']):
            lines.append(cubic_path(a));paths+=1;maximum=max(maximum,a['certified_l1_error'])
    for s in segs[:-1]:lines.append(r'\fill '+point(project(s['bern'][-1]))+' circle[radius=1.5pt];')
    for h in range(101):
        u=F(h,100);actual,_=rational(u,w3);partition+=1
        B,_=rational(u,F(0));n=weights(K,3,u);d0=1-n[3];alpha=w3*n[3]/(d0+w3*n[3])
        assert actual==tuple((1-alpha)*B[d]+alpha*P[3][d] for d in range(2));line_checks+=1
    label=r'\frac3{10}' if w3==F(3,10) else str(w3)
    lines.append(r'\node['+('right' if w3==0 else 'above right')+'=5pt] at '+point(rational(F(1,2),w3)[0])+r' {$'+label+'$};')
for i,pos in enumerate(['below left','above left','above','below left','below right','above left','above right']):
    lines += [r'\node[book point] at (P'+str(i)+') {};',r'\node['+pos+'=5pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};']
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nurbs-weight-family-check.json').write_text(json.dumps({
    'figure':'4.2','shared_control_polygon':'nurbs41_data.py; same as Fig4.1',
    'w3_values':list(map(str,family)),'all_other_weights':1,'knots':list(map(str,K)),
    'exact_homogeneous_checks':exact,'partition_nonnegative_projection_points':partition,
    'weight_line_identity_checks':line_checks,'all_u_denominator_lower_bound':str(denominator_minimum),
    'native_cubic_paths':paths,'maximum_certified_l1_error_cm':str(maximum),
    'identity':'C(u;w3)=(1-alpha)B(u)+alpha*P3; alpha=w3*N3/(1-N3+w3*N3)',
    'monotone_weight_effect':'For fixed u, alpha nondecreasing with w3, so distance to P3 decreases; endpoints unchanged'},indent=2)+'\n')
print(f'PASS:{exact} homogeneous checks,{partition} rational partitions,{line_checks} weight-line identities,{paths} native paths; denominator>={denominator_minimum}, max error{float(maximum):.8f}cm.')
