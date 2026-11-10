"""7.11: actual rational quadratic barycentric/oblique vector decomposition."""
from pathlib import Path
from fractions import Fraction as F
import json
from rational_geometry import approximate,evaluate,project
from native_bspline import cubic_path,point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_11.tex')['applied']
P=((F(0),F(0)),(F(4),F(5)),(F(8),F(0)));W=(F(1),F(1,2),F(1))
H=tuple(tuple(w*x for x in pt)+(w,) for pt,w in zip(P,W));S=tuple(x-y for x,y in zip(P[0],P[1]));T=tuple(x-y for x,y in zip(P[2],P[1]));k=W[0]*W[2]/(W[1]*W[1])
assert S[0]*T[1]-S[1]*T[0]!=0
for i in range(101):
    u=F(i,100);BB=((1-u)**2,2*u*(1-u),u*u);den=sum(w*b for w,b in zip(W,BB));R=tuple(w*b/den for w,b in zip(W,BB))
    alpha,beta=R[0],R[2];C=project(evaluate(H,u))
    assert C==tuple(p+alpha*s+beta*t for p,s,t in zip(P[1],S,T))
    assert alpha*beta==k*(1-alpha-beta)**2/4 and min(R)>=0 and sum(R)==1
u=F(2,5);alpha,beta=F(9,19),F(4,19)
B=tuple(p+alpha*s for p,s in zip(P[1],S));C=tuple(b+beta*t for b,t in zip(B,T));assert C==project(evaluate(H,u))
paths=approximate(H,F(1,100000))
lines=['% Representative P0(0,0),P1(4,5),P2(8,0),W1,1/2,1; true rational curve.',
       '% u2/5 gives alpha9/19,beta4/19; exact P1+alpha*S+beta*T=C(u).',
       r'\begin{tikzpicture}[book line,x=1.3cm,y=1.3cm]',r'\path[use as bounding box] (-1,-1) rectangle (9,6);',
       r'\draw[book axis,book grid] '+point(P[1])+'--'+point(P[0])+r' node[pos=.7,left=7pt] {$\mathbf S$};',
       r'\draw[book axis,book grid] '+point(P[1])+'--'+point(P[2])+r' node[pos=.65,right=7pt] {$\mathbf T$};']
lines.extend(cubic_path(s) for s in paths)
lines += [r'\draw[book axis] '+point(P[1])+'--'+point(B)+r' node[pos=.4,left=8pt] {$\alpha(u)\mathbf S$};',
          r'\draw[book axis] '+point(B)+'--'+point(C)+r' node[midway,right=8pt] {$\beta(u)\mathbf T$};']
for i,(pt,anchor) in enumerate(zip(P,('below left','above right','below right'))):
    lines.append(r'\draw '+point(pt)+r' circle[radius=2pt] node['+anchor+r'=6pt] {$\mathbf P_'+str(i)+'$};')
lines += [r'\draw '+point(C)+r' circle[radius=2pt] node[below=8pt] {$\mathbf C(u)$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_11.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/oblique-conic-frame-check.json').write_text(json.dumps({'figure':'7.11','representative_controls':[[str(x) for x in pt] for pt in P],'weights':list(map(str,W)),'chosen_u':str(u),'alpha':str(alpha),'beta':str(beta),'S':list(map(str,S)),'T':list(map(str,T)),'intermediate_point':list(map(str,B)),'curve_point':list(map(str,C)),'exact_decomposition_and_oblique_implicit_checks':101,'native_paths':len(paths),'certified_native_L1_error':str(max(s['certified_l1_error'] for s in paths))},indent=2)+'\n')
print('PASS:101 exact barycentric decompositions and Eq7.26 identities; alpha9/19,beta4/19 arrows are actual vector lengths.')
