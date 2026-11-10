"""7.32: exact quartic elevation, common homogeneous scaling and clockwise rotation."""
from fractions import Fraction as F
from pathlib import Path
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import elevate,project,approximate
from polynomial_native import multiply
from bspline_math import add,derivative,evaluate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_40.tex')['applied']
old=tuple(tuple(map(F,h)) for h in [(3,0,3),(0,3,0),(-3,0,1),(0,-3,0),(3,0,3)])
H=tuple((F(5,3)*y,-F(5,3)*x,F(5,3)*w) for x,y,w in elevate(old))
assert H==tuple(tuple(map(F,h)) for h in [(0,-5,5),(4,-1,1),(2,3,1),(-2,3,1),(-4,-1,1),(0,-5,5)])
Q=tuple(map(project,H));W=tuple(h[-1] for h in H);assert min(W)>0 and Q==((0,-1),(4,-1),(2,3),(-2,3),(-4,-1),(0,-1))
U=(F(0),)*6+(F(1),)*6;K=(F(0),)*5+(F(1),)*5;ss=segments(U,H,5);X,Y,Z=ss[0]['power']
res=add(add(multiply(X,X),multiply(Y,Y)),tuple(-v for v in multiply(Z,Z)));assert all(v==0 for v in res)
def velocity(u):
    h=[evaluate(p,u) for p in (X,Y,Z)];dh=[evaluate(derivative(p),u) for p in (X,Y,Z)]
    return tuple((dh[k]*h[-1]-h[k]*dh[-1])/h[-1]**2 for k in range(2))
assert velocity(F(0))==velocity(F(1))==(4,0)
for i in range(401):
    u=F(i,400);h=de_boor(U,H,5,u);before=de_boor(K,old,4,u)
    assert h==(F(5,3)*before[1],-F(5,3)*before[0],F(5,3)*before[2]) and h[-1]>=F(5,4)
    x,y=project(h);assert x*x+y*y==1
    R=[de_boor(U,tuple((ww*F(k==j),) for k,ww in enumerate(W)),5,u)[0]/h[-1] for j in range(6)];assert min(R)>=0 and sum(R)==1
nc=check(U,H,5,ss);paths=approximate(H,F(1,200000))
lines=['% Exact Ex7.10 six homogeneous controls, all positive weights5,1,1,1,1,5.',
       '% Obtain by degree-elevating Ex7.9, multiplying every H by5/3 and rotating XY clockwise90degrees.',
       r'\begin{tikzpicture}[book line,x=4cm,y=4cm]',r'\path[use as bounding box] (-4.6,-1.7) rectangle (4.6,3.6);',
       r'\draw[book axis,book grid] (-1.5,0)--(4.35,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-1.35)--(0,3.4) node[above=4pt] {$y$};',r'\draw[book grid] '+'--'.join(map(point,Q))+';']
lines.extend(cubic_path(s) for s in paths)
for i,(q,anchor) in enumerate(zip(Q[:5],['below right','below right','above right','above left','below left'])):
    label=r'\mathbf R_0=\mathbf R_5' if i==0 else r'\mathbf R_'+str(i)
    lines.append(r'\draw '+point(q)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch07/fig_7_40.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/quintic-circle-check.json').write_text(json.dumps({'figure':'7.32','homogeneous_controls':[[str(v) for v in h] for h in H],'finite_controls':[[str(v) for v in q] for q in Q],'weights':list(map(str,W)),'exact_degree_elevation_common_scale_and_rotation_verified':True,'common_scale':'5/3','rotation_degrees':-90,'exact_circle_polynomial_identity':list(map(str,res)),'same_parameter_elevation_and_circle_partition_checks':401,'global_denominator_lower_bound':'5/4','closure_derivative':['4','0'],'native_checks':nc,'native_L1_error':str(max(s['certified_l1_error'] for s in paths))},indent=2)+'\n')
print('PASS:given quintic controls exactly equal elevated/rotated/scaled quartic,401circle/partition checks,all positive finite controls,closedC1,W>=5/4.')
