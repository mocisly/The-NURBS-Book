"""7.29: exact degree elevation of the nonzero-infinite-control semicircle."""
from fractions import Fraction as F
from pathlib import Path
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import elevate,project,approximate
from polynomial_native import multiply
from bspline_math import add
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_37.tex')['applied']
old=((F(1),F(0),F(1)),(F(0),F(1),F(0)),(-F(1),F(0),F(1)));H=elevate(old)
Q=tuple(map(project,H));assert Q==((1,0),(1,2),(-1,2),(-1,0)) and tuple(h[-1] for h in H)==(1,F(1,3),F(1,3),1)
K=(F(0),)*3+(F(1),)*3;U=(F(0),)*4+(F(1),)*4;ss=segments(U,H,3);before=segments(K,old,2)[0]
assert all(tuple(a)+(F(0),)==tuple(b) for a,b in zip(before['power'],ss[0]['power']))
X,Y,Z=ss[0]['power'];res=add(add(multiply(X,X),multiply(Y,Y)),tuple(-x for x in multiply(Z,Z)));assert all(x==0 for x in res)
for i in range(101):
    u=F(i,100);h=de_boor(U,H,3,u);assert h==de_boor(K,old,2,u) and h[-1]>=F(1,2)
    x,y=project(h);assert x*x+y*y==1 and y>=0
nc=check(U,H,3,ss);paths=approximate(H,F(1,200000))
lines=['% Exact Ex7.7 degree elevation: finite controls(1,0),(1,2),(-1,2),(-1,0).',
       '% Positive weights1,1/3,1/3,1; every homogeneous coefficient and original parameter unchanged.',
       r'\begin{tikzpicture}[book line,x=4cm,y=4cm]',r'\path[use as bounding box] (-1.7,-.6) rectangle (1.9,2.6);',
       r'\draw[book axis,book grid] (-1.45,0)--(1.5,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-.35)--(0,2.35) node[above=4pt] {$y$};',r'\draw[book grid] '+'--'.join(map(point,Q))+';']
lines.extend(cubic_path(s) for s in paths)
for i,(q,anchor) in enumerate(zip(Q,['below right','above right','above left','below left'])):lines.append(r'\draw '+point(q)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$\mathbf Q_'+str(i)+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch07/fig_7_37.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/cubic-semicircle-check.json').write_text(json.dumps({'figure':'7.29','homogeneous_controls':[[str(x) for x in h] for h in H],'finite_controls':[[str(x) for x in q] for q in Q],'weights':[str(h[-1]) for h in H],'exact_degree_elevation_and_all_power_coefficients_unchanged':True,'exact_circle_identity_coefficients':list(map(str,res)),'exact_same_parameter_and_circle_checks':101,'denominator_lower_bound':'1/2','native_checks':nc,'native_L1_error':str(max(s['certified_l1_error'] for s in paths))},indent=2)+'\n')
print('PASS:exact homogeneous degree elevation and polynomial identity,101same-parameter/circle checks,W>=1/2,all4controls finite with positive weights.')
