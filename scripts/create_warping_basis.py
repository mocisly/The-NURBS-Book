from pathlib import Path
from fractions import Fraction as F
import json
from warping_basis_data import *
from native_bspline import check,cubic_path,point
from rational_geometry import graph_controls,approximate
root=Path(__file__).resolve().parents[1]
lines=['% Eq11.43-45, exact T and prescribed w3=1/5,1,30; normalized peak1.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1,-1.2) rectangle (18,7);',r'\draw[book axis] (0,0)--(17,0) node[right=5pt] {$t$};',r'\draw[book axis] (0,0)--(0,5.8) node[above=5pt] {$f$};',r'\draw[book grid] (-.12,5)--(.12,5) node[left=10pt] {$1$};'];proof=[];nc=0
for index,(w,style,label) in enumerate([(F(1,5),'dotted',r'1/5'),(F(1),'dashed','1'),(F(30),'','30')]):
    ss=segments(T,homogeneous(w),3);nc+=check(T,homogeneous(w),3,ss,steps=7);paths=[]
    for s in ss:
        H=graph_controls(s['a'],s['b'],tuple(p[0]for p in s['bern']),tuple(p[1]for p in s['bern']),xscale=F(16),yscale=F(5));paths+=approximate(H,F(1,100000))
    lines.extend(cubic_path(p,style) for p in paths)
    x=F(1)+F(11,2)*index;lines.extend([r'\draw['+style+'] '+point((x,F(32,5)))+'--'+point((x+F(4,5),F(32,5)))+';',r'\node[anchor=west] at '+point((x+1,F(32,5)))+r' {$w_3='+label+'$};'])
    proof.append(dict(weight=w,normalizing_peak=2*w/(1+2*w),paths=len(paths),certified_screen_error_cm=max(p['certified_l1_error'] for p in paths),global_range=(0,1),symmetry_exact=True))
for t,label in [(F(0),'0'),(F(1,4),r'\frac14'),(F(1,2),r'\frac12'),(F(3,4),r'\frac34'),(F(1),'1')]:
    for dx in ((-F(9,100),-F(3,100),F(3,100),F(9,100)) if t in(0,1)else(F(0),)):lines.append(r'\draw[book grid] '+point((16*t+dx,-F(1,10)))+'--'+point((16*t+dx,F(1,10)))+';')
    lines.append(r'\node[below=9pt] at '+point((16*t,0))+r' {$'+label+'$};')
lines.extend([r'\fill (8,5) circle[radius=1.6pt];',r'\end{tikzpicture}']);(root/'image_tex/ch11/fig_11_20.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/warping-basis-check.json').write_text(json.dumps(dict(knots=T,degree=3,prescribed_weights=(F(1,5),1,30),global_basis_maximum=F(2,3),native_checks=nc,proofs=proof,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.18',nc,'nativechecks; globalnormalizedmax1 and symmetry exact.')
