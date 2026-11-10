"""7.12: five prescribed weights, actual shoulders and the complementary negative arc."""
from pathlib import Path
from fractions import Fraction as F
import json
from rational_geometry import approximate,evaluate,project,split
from native_bspline import cubic_path,point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_12.tex')['applied']
P=((F(8),F(0)),(F(4),F(5)),(F(0),F(0)));weights=(F(3),F(1),F(3,10),F(0),-F(3,10));M=(F(4),F(0))
lines=['% Prescribed w1=3,1,3/10,0,-3/10; same symmetric representative triangle for all curves.',
       '% Negative interior homogeneous weight is subdivided to positive-weight patches before certification.',
       r'\begin{tikzpicture}[book line,x=1.2cm,y=1.2cm]',r'\path[use as bounding box] (-1,-3.1) rectangle (9,6);',
       r'\draw[book grid] '+point(P[0])+'--'+point(P[1])+'--'+point(P[2])+';',
       r'\draw[book grid] (4,5)--(4,-2.6);']
proofs=[];shoulders=[]
for w in weights:
    H=tuple(tuple(ww*x for x in pt)+(ww,) for pt,ww in zip(P,(F(1),w,F(1))))
    minimum=min(F(1),(1+w)/2);assert minimum>0
    for i in range(101):
        u=F(i,100);bb=((1-u)**2,2*u*(1-u),u*u);den=bb[0]+w*bb[1]+bb[2];assert den>=minimum
        alpha,beta=bb[0]/den,bb[2]/den
        assert 4*w*w*alpha*beta==(1-alpha-beta)**2
        C=project(evaluate(H,u));assert C==tuple((bb[0]*p+w*bb[1]*q+bb[2]*r)/den for p,q,r in zip(*P))
    S=project(evaluate(H,F(1,2)));s=w/(1+w)
    assert S==tuple((1-s)*m+s*p for m,p in zip(M,P[1]))
    dh=tuple(tuple(2*(y-x) for x,y in zip(a,b)) for a,b in zip(H,H[1:]));d=evaluate(dh,F(1,2));hm=evaluate(H,F(1,2))
    tangent=tuple((d[k]*hm[-1]-hm[k]*d[-1])/(hm[-1]**2) for k in range(2));assert tangent[1]==0 and tangent[0]!=0
    if w==0:
        lines.append(r'\draw '+point(P[0])+'--'+point(P[2])+';');paths=[]
    else:
        chunks=split(H) if w<0 else (H,)
        assert all(min(pt[-1] for pt in chunk)>0 for chunk in chunks)
        paths=[p for chunk in chunks for p in approximate(chunk,F(1,100000))]
        lines.extend(cubic_path(p) for p in paths)
    label={F(3):'3',F(1):'1',F(3,10):r'\frac3{10}',F(0):r'w_1=0',-F(3,10):r'-\frac3{10}'}[w]
    anchor='below right' if w<0 else 'above right'
    lines.append(r'\draw '+point(S)+r' circle[radius=1.8pt] node['+anchor+r'=7pt] {$'+label+'$};')
    proofs.append({'w1':str(w),'global_denominator_lower_bound':str(minimum),'native_paths':len(paths),'certified_native_L1_error':str(max((p['certified_l1_error'] for p in paths),default=F(0))),'shoulder':list(map(str,S)),'shoulder_parameter_s':str(s),'shoulder_tangent':list(map(str,tangent))})
for i,(pt,anchor) in enumerate(zip(P,('above right','above right','above left'))):
    lines.append(r'\draw '+point(pt)+r' circle[radius=2pt] node['+anchor+r'=6pt] {$\mathbf P_'+str(i)+'$};')
lines += [r'\node[below left=7pt] at (4,0) {$\mathbf M$};',
          r'\node[above left=7pt] at '+point((F(4),F(15,13)))+r' {$\mathbf S$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_12.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/conic-weight-family-check.json').write_text(json.dumps({'figure':'7.12','representative_controls':[[str(x) for x in pt] for pt in P],'prescribed_weights':list(map(str,weights)),'exact_oblique_implicit_and_geometry_checks':505,'shoulder_formulas_and_horizontal_tangents_exact':True,'proofs':proofs},indent=2)+'\n')
print('PASS:505 exact geometry/implicit checks; all five shoulders and horizontal tangents exact; negative arc certified after positive-weight subdivision.')
