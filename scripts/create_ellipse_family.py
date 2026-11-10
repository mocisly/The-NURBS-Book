"""7.2: the four prescribed ellipses, exact conics with certified native paths."""
from pathlib import Path
from fractions import Fraction as F
import json
from rational_geometry import approximate,evaluate,project
from native_bspline import cubic_path,point,number

root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_02.tex')['applied']
a=F(5,2);bs=(F(5,2),F(2),F(3,2),F(4,5));quarter=((F(1),F(0),F(1)),(F(1),F(1),F(1)),(F(0),F(2),F(2)))
lines=['% Exact prescribed a5/2 and b5/2,2,3/2,4/5; no recovered raster coordinates.',
       '% Rational parametrization Eq7.8 on each quadrant; certified native Hermite cubics.',
       r'\begin{tikzpicture}[book line,x=1.6cm,y=1.6cm]',r'\path[use as bounding box] (-3.8,-3.2) rectangle (5.7,3.5);',
       r'\draw[book axis] (-3.3,0)--(4.9,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-2.9)--(0,3.1) node[above=4pt] {$y$};']
proofs=[]
for b in bs:
    for quadrant in range(4):
        H=[]
        for xx,yy,w in quarter:
            for _ in range(quadrant):xx,yy=-yy,xx
            H.append((a*xx,b*yy,w))
        H=tuple(H)
        for i in range(101):
            x,y=project(evaluate(H,F(i,100)));assert x*x/(a*a)+y*y/(b*b)==1
        paths=approximate(H,F(1,100000))
        lines.extend(cubic_path(s) for s in paths)
        proofs.append({'b':str(b),'quadrant':quadrant,'paths':len(paths),'whole_path_L1_bound':str(max(s['certified_l1_error'] for s in paths))})
lines += [r'\draw (-2.5,0) circle[radius=1.8pt] node[below left=6pt] {$(-a,0)$};',
          r'\draw (2.5,0) circle[radius=1.8pt] node[below right=6pt] {$(a,0)$};',
          r'\node[anchor=north west,align=left] at (3,2.8) {$a=\frac52$\\[5pt]$b=\frac52,\ 2,\ \frac32,\ \frac45$};',
          r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_02.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/ellipse-family-check.json').write_text(json.dumps({'figure':'7.2','a':str(a),'b':list(map(str,bs)),'exact_implicit_equation_checks':1616,'native_error_certificates':proofs,'tolerance_cm':'1/100000, before1.6cm axis scale'},indent=2)+'\n')
print(f'PASS:1616 exact ellipse identities;{sum(p["paths"] for p in proofs)} native paths with certified error below1e-5 coordinate units.')
