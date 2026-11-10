"""7.3: prescribed a=1,b=5,2,1,1/2 hyperbolas from exact rational functions."""
from pathlib import Path
from fractions import Fraction as F
import json
from polynomial_native import bernstein
from rational_geometry import approximate,evaluate,project
from native_bspline import cubic_path

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_03.tex')['applied']
bs=(F(5),F(2),F(1),F(1,2));limits=(F(1,5),F(2,5),F(3,5),F(7,10))
lines=['% Prescribed hyperbolas; exact Eq7.9, positive denominators on finite display windows.',
       r'\begin{tikzpicture}[book line,x=1.6cm,y=1.6cm]',r'\path[use as bounding box] (-3.5,-2.7) rectangle (5.2,3);',
       r'\draw[book axis] (-3.2,0)--(4.6,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-2.5)--(0,2.7) node[above=4pt] {$y$};']
proofs=[]
for b,h in zip(bs,limits):
    for sign in (-1,1):
        H=bernstein(((F(sign),F(0),F(sign)),(F(0),2*b,F(0)),(F(1),F(0),-F(1))),-h,h)
        assert min(pt[-1] for pt in H)>0
        for i in range(101):
            x,y=project(evaluate(H,F(i,100)));assert x*x-y*y/(b*b)==1
        paths=approximate(H,F(1,100000));lines.extend(cubic_path(s) for s in paths)
        proofs.append({'b':str(b),'branch_sign':sign,'parameter_window':list(map(str,(-h,h))),'native_paths':len(paths),'certified_L1_bound':str(max(s['certified_l1_error'] for s in paths))})
lines += [r'\draw (-1,0) circle[radius=1.8pt] node[below right=6pt] {$(-a,0)$};',
          r'\draw (1,0) circle[radius=1.8pt] node[below left=6pt] {$(a,0)$};',
          r'\node[anchor=north west,align=left] at (2.8,2.5) {$a=1$\\[5pt]$b=5,\ 2,\ 1,\ \frac12$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_03.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/hyperbola-family-check.json').write_text(json.dumps({'figure':'7.3','a':'1','b':list(map(str,bs)),'exact_implicit_equation_checks':808,'native_error_certificates':proofs,'display_tolerance_coordinate_units':'1/100000'},indent=2)+'\n')
print('PASS:808 exact hyperbola identities, positive display denominators, certified native rational approximation.')
