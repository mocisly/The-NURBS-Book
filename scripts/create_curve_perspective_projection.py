"""6.6: closed spatial cubic projected by exact homogeneous control transformation."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate,project

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_06.tex'
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_06.tex')['applied']
U=(F(0),)*4+(F(1,3),F(2,3))+(F(1),)*4
xz=((F(7,5),F(2)),(F(7,5),F(3,5)),(-F(7,5),F(3,5)),
    (-F(7,5),F(17,5)),(F(7,5),F(17,5)),(F(7,5),F(2)))
P=tuple((x,F(4)+x/4+(z-2)/5,z) for x,z in xz)
E=(F(0),F(9),F(0));Q=(-F(4),F(0),F(8));N=(F(0),F(1),F(0))
def homogeneous(a):
    x,y,z=a;return (9*x,F(0),9*z,9-y)
def perspective(a):return project(homogeneous(a))
H=tuple(map(homogeneous,P));B=tuple(map(project,H));weights=tuple(h[-1] for h in H)
assert min(weights)>0 and len(set(weights))>1
ss=segments(U,P,3);hs=segments(U,H,3)
checks=check(U,P,3,ss)+check(U,H,3,hs)
for i in range(101):
    t=F(i,100);a=de_boor(U,P,3,t);b=project(de_boor(U,H,3,t))
    assert b==perspective(a) and b[1]==0
    ratio=(E[1]-b[1])/(E[1]-a[1])
    assert tuple(e+ratio*(p-e) for p,e in zip(a,E))==b
assert P[0]==P[-1] and B[0]==B[-1]
assert tuple(P[1][i]-P[0][i] for i in range(3))==tuple(P[-1][i]-P[-2][i] for i in range(3))
native=[];bounds=[]
for s in hs:
    for piece in approximate(s['bern'],F(1,10000)):
        native.append(cubic_path(piece,'book line,dashed'));bounds.append(piece['certified_l1_error'])
lines=['% Closed spatial cubic in tilted plane; source weights one, projected weights9-y_i.',
       '% Perspective controls exactly transformed in homogeneous coordinates.',
       '% Projected rational curve rendered with certified mathematical cubic error <1e-4cm.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-4.4,-3.6) rectangle (9.4,11.1);',
       r'\begin{scope}[x={(-.85cm,-.5cm)},y={(.9cm,-.3cm)},z={(0cm,1.05cm)}]',
       r'\draw[book grid] (4,0,-.5)--(-4,0,-.5)--(-4,0,8)--(4,0,8)--cycle;']
for i in range(5):lines.append(r'\draw[book grid,densely dotted] '+point(E)+'--'+point(B[i])+';')
lines += [r'\draw[book grid] '+'--'.join(map(point,P))+';',
          r'\draw[book grid,dashed] '+'--'.join(map(point,B))+';']
lines.extend(cubic_path(s) for s in ss);lines.extend(native)
for p,label,anchor in [(P[2],r'\mathbf P_2','right'),(B[2],r'\overline{\mathbf P}_2','below left'),(E,r'\mathbf E','below right'),(Q,r'\mathbf Q','above left')]:
    lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=5pt] {$'+label+'$};')
lines += [r'\draw[book axis] '+point(Q)+'--'+point(tuple(q+F(5,2)*n for q,n in zip(Q,N)))+r' node[right=4pt] {$\mathbf N$};',
          r'\draw[book axis] (0,0,0)--(4.8,0,0) node[below left=4pt] {$x$};',
          r'\draw[book axis] (0,0,0)--(0,9.8,0) node[right=4pt] {$y$};',
          r'\draw[book axis] (0,0,0)--(0,0,9.8) node[above=4pt] {$z$};',r'\end{scope}',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-perspective-projection-check.json').write_text(json.dumps({
    'figure':'6.6','source_controls':[[str(x) for x in p] for p in P],
    'projected_controls':[[str(x) for x in p] for p in B],
    'projected_weights':list(map(str,weights)),'eye':list(map(str,E)),
    'native_checks':checks,'exact_curve_and_ray_identities':101,
    'closed_curve_with_matching_endpoint_derivatives':True,
    'native_rational_paths':len(native),'maximum_certified_L1_error_cm':str(max(bounds))},indent=2)+'\n')
print(f'PASS:{checks} native checks,101 exact perspective/ray identities, positive varying weights;{len(native)} certified native paths.')
