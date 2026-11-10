"""Fig4.4: quadratic weight family; the last span is drawn only once."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from rational_geometry import approximate,project
from surface_geometry import weights
from nurbs44_data import K,P,homogeneous,rational

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_04.tex';assert not target.exists()
family=(F(0),F(3,10),F(1),F(4))
lines=['% Fig4.4: representative five-control W-shaped quadratic NURBS.',
       '% U=(0,0,0,1/3,2/3,1,1,1), only w1=0,3/10,1,4 varies.',
       '% The scan supplies no numeric control coordinates; data are explicitly representative.',
       '% N1 vanishes on[2/3,1], so all four curves share the final span exactly.',
       '% Certified mathematical rational-to-native cubic paths, <=0.0001cm, never image contours.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-1.2,-3.2) rectangle (13.4,5);']
for i,p in enumerate(P):lines.append(r'\coordinate(P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4);')
exact=paths=identities=0;maximum=F(0);last=None
for w1 in family:
    segs=segments(K,homogeneous(w1),2);exact+=check(K,homogeneous(w1),2,segs)
    if last is not None:assert segs[-1]['bern']==last['bern']
    last=segs[-1]
    for s in segs[:-1]:
        for a in approximate(s['bern']):
            lines.append(cubic_path(a));paths+=1;maximum=max(maximum,a['certified_l1_error'])
    lines.append(r'\fill '+point(project(segs[0]['bern'][-1]))+' circle[radius=1.5pt];')
    for h in range(101):
        u=F(h,100);actual,_=rational(u,w1);B,_=rational(u,0);n=weights(K,2,u)
        alpha=w1*n[1]/(1-n[1]+w1*n[1])
        assert actual==tuple((1-alpha)*B[d]+alpha*P[1][d] for d in range(2));identities+=1
        if u>=F(2,3):assert actual==B
    label=r'\frac3{10}' if w1==F(3,10) else str(w1)
    lines.append(r'\node[above right=5pt] at '+point(rational(F(1,6),w1)[0])+' {$'+label+'$};')
for a in approximate(last['bern']):
    lines.append(cubic_path(a));paths+=1;maximum=max(maximum,a['certified_l1_error'])
lines.append(r'\fill '+point(project(last['bern'][0]))+' circle[radius=1.5pt];')
for i,pos in enumerate(['above left','below','above','below','above right']):
    lines += [r'\node[book point] at (P'+str(i)+') {};',r'\node['+pos+'=5pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};']
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
preflight=json.loads((root/'image_tex/build/nurbs-quadratic-family-preflight.json').read_text(encoding='utf-8'))
preflight.update(status='Native source authored; visual integration tracked in manifest',
                 exact_homogeneous_checks=exact,weight_line_identity_checks=identities,
                 rendered_cubic_pieces=paths,maximum_certified_l1_error_cm=str(maximum),
                 common_final_span_drawn_once=True,weight_support=['0','2/3'])
(root/'image_tex/build/nurbs-quadratic-family-check.json').write_text(json.dumps(preflight,indent=2)+'\n')
print(f'PASS:{exact} homogeneous checks,{identities} weight-line identities,{paths} certified native cubic paths; exact common last span drawn once, max error{float(maximum):.8f}cm.')
