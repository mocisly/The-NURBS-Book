"""7.13: exact3-4-5 circular arc and its angle-bisector weight construction."""
from pathlib import Path
from fractions import Fraction as F
import json
from rational_geometry import approximate,evaluate,project
from native_bspline import cubic_path,point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_13.tex')['applied']
P=((F(3),F(0)),(F(0),F(4)),(-F(3),F(0)));w=F(3,5)
H=tuple(tuple(ww*x for x in pt)+(ww,) for pt,ww in zip(P,(F(1),w,F(1))))
S=project(evaluate(H,F(1,2)));M=(F(0),F(0));assert S==(F(0),F(3,2))
center=(F(0),-F(9,4));radius=F(15,4)
for i in range(101):
    x,y=project(evaluate(H,F(i,100)));assert x*x+(y-center[1])**2==radius**2
assert sum((x-y)**2 for x,y in zip(P[0],P[1]))==sum((x-y)**2 for x,y in zip(P[2],P[1]))==25
assert S[1]/(P[1][1]-S[1])==F(3,5)==w
# At P2, normalized ray directions toward M and P1 are (1,0),(3/5,4/5).
# Their sum is exactly parallel to the ray P2->S, proving the angle bisector.
bisector=(F(8,5),F(4,5));ray=tuple(x-y for x,y in zip(S,P[2]));assert bisector[0]*ray[1]==bisector[1]*ray[0]
assert F(3,5)==sum(x*y for x,y in zip((F(1),F(0)),(F(3,5),F(4,5))))
paths=approximate(H,F(1,100000))
lines=['% Exact circle with center(0,-9/4),radius15/4,representative3-4-5 control triangle.',
       '% e3/f5=MS/SP1=3/5=cos(theta); P2S is the exact angle bisector.',
       r'\begin{tikzpicture}[book line,x=1.5cm,y=1.5cm]',r'\path[use as bounding box] (-4.8,-1) rectangle (5.4,5.2);',
       r'\draw[book grid] '+point(P[2])+'--'+point(P[1])+'--'+point(P[0])+'--cycle;',
       r'\draw[book grid] (0,4)--(0,0);',r'\draw[book grid] (-3,0)--(1,2);',
       r'\node[left=7pt] at (-1.5,2) {$f$};',r'\node[below=7pt] at (-1.5,0) {$e$};']
lines.extend(cubic_path(p) for p in paths)
for i,(pt,anchor) in enumerate(zip(P,('below right','above','below left'))):
    lines.append(r'\draw '+point(pt)+r' circle[radius=2pt] node['+anchor+r'=6pt] {$\mathbf P_'+str(i)+'$};')
lines += [r'\draw (0,0) circle[radius=1.8pt] node[below=7pt] {$\mathbf M$};',
          r'\draw '+point(S)+r' circle[radius=1.8pt] node[below right=8pt] {$\mathbf S$};',
          r'\node[above right=8pt] at (3,0) {$w_0=1$};',
          r'\node[above left=8pt] at (-3,0) {$w_2=1$};',
          r'\node[anchor=west] at (1,3.9) {$w_1=e/f$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_13.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/circular-arc-weight-check.json').write_text(json.dumps({'figure':'7.13','representative_controls':[[str(x) for x in pt] for pt in P],'weights':['1',str(w),'1'],'circle_center':list(map(str,center)),'radius':str(radius),'exact_circle_checks':101,'e':'3','f':'5','MS_over_SP1_equals_e_over_f_equals_cos_theta':True,'angle_bisector_certified_by_normalized_ray_sum':True,'shoulder':list(map(str,S)),'certified_native_L1_error':str(max(p['certified_l1_error'] for p in paths))},indent=2)+'\n')
print('PASS:101 exact circle identities; MS/SP1=e/f=cos(theta)=3/5 and P2S angle bisector exact.')
