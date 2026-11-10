"""7.30: correct Ex7.8 by exact elevation of its actual240degree circle."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import elevate,project,approximate,evaluate
from polynomial_native import multiply
from bspline_math import add
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_38.tex')['applied']
# Use X/a for a fully exact circle certificate, with a^2=3/4.
oldS=((F(1),F(1,2),F(1)),(F(0),-F(1),-F(1,2)),(-F(1),F(1,2),F(1)))
HS=elevate(oldS);assert tuple(h[-1] for h in HS)==(1,0,0,1)
K=(F(0),)*3+(F(1),)*3;U=(F(0),)*4+(F(1),)*4
before,after=segments(K,oldS,2)[0],segments(U,HS,3)[0]
assert all(tuple(a)+(F(0),)==tuple(b) for a,b in zip(before['power'],after['power']))
X,Y,Z=after['power'];res=add(add(tuple(F(3,4)*x for x in multiply(X,X)),multiply(Y,Y)),tuple(-x for x in multiply(Z,Z)));assert all(x==0 for x in res)
D=10**40;n=isqrt(3*D*D);lo,hi=F(n,2*D),F(n+1,2*D);assert lo*lo<F(3,4)<hi*hi;a=(lo+hi)/2
old=tuple((a*x,y,w) for x,y,w in oldS);H=elevate(old);assert H[1]==(a/3,-F(1,2),F(0)) and H[2]==(-a/3,-F(1,2),F(0))
for i in range(101):
    u=F(i,100);h=de_boor(U,H,3,u);assert h==de_boor(K,old,2,u) and h[-1]>=F(1,4)
    x,y=project(h);assert abs(x*x+y*y-1)<F(1,10**38)
assert project(evaluate(H,F(1,2)))==(0,-1)
# Counterexample to the previous printed finite-control data, independent of a.
wrong=((a,F(1,2),F(1)),(a/3,-F(1,2),F(1,6)),(-a/3,-F(1,2),F(1,6)),(-a,F(1,2),F(1)))
wrongmid=project(evaluate(wrong,F(1,2)));assert wrongmid==(0,-F(2,3)) and sum(x*x for x in wrongmid)==F(4,9)
fifth=elevate(elevate(H));assert tuple(h[-1] for h in fifth)==(1,F(2,5),F(1,10),F(1,10),F(2,5),1)
nc=check(U,H,3,segments(U,H,3));paths=approximate(H,F(1,200000))
lines=['% Correct Ex7.8: exact degree elevation gives weights1,0,0,1, not1,1/6,1/6,1.',
       '% Nonzero infinite vectors v1=(a/3,-1/2),v2=(-a/3,-1/2); same exact240degree curve and parameter.',
       '% Previous finite data has C(1/2)=(0,-2/3), squared radius4/9, so is not the prescribed unit circle.',
       r'\begin{tikzpicture}[book line,x=4cm,y=4cm]',r'\path[use as bounding box] (-2.3,-1.6) rectangle (2.5,1.3);',
       r'\draw[book axis,book grid] (-2.05,0)--(2.1,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-1.3)--(0,1.05) node[above=4pt] {$y$};']
lines.extend(cubic_path(s) for s in paths)
for idx,v,base,anchor in [(1,H[1][:2],project(H[0]),'below right'),(2,H[2][:2],project(H[3]),'below left')]:
    end=tuple(p+3*q for p,q in zip(base,v));lines.append(r'\draw[book axis,book grid] '+point(base)+'--'+point(end)+r' node['+anchor+r'=7pt] {$\overrightarrow{\mathbf Q}_'+str(idx)+'$};')
for idx,base,anchor in [(0,project(H[0]),'above right'),(3,project(H[3]),'above left')]:lines.append(r'\draw '+point(base)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$\mathbf Q_'+str(idx)+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch07/fig_7_38.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/cubic-240-arc-check.json').write_text(json.dumps({'figure':'7.30','homogeneous_controls':[[str(x) for x in h] for h in H],'weights':['1','0','0','1'],'exact_scaled_circle_identity_coefficients':list(map(str,res)),'all_original_homogeneous_coefficients_unchanged':True,'exact_same_parameter_checks':101,'native_checks':nc,'correct_midpoint':['0','-1'],'previous_finite_control_data_midpoint':list(map(str,wrongmid)),'previous_midpoint_squared_radius':'4/9','previous_data_contradicts_unit_circle':True,'subsequent_degree5_weights':[str(h[-1]) for h in fifth],'denominator_lower_bound':'1/4','native_L1_error':str(max(s['certified_l1_error'] for s in paths))},indent=2)+'\n')
print('PASS:exact240circle elevation,W>=1/4,weights1/0/0/1. Previous1/6finite data disproved at midpoint(0,-2/3); correct midpoint(0,-1).')
