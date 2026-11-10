"""6.7: exact tensor-product quadratic surface and its affine projection."""
from pathlib import Path
from fractions import Fraction as F
import json
from surface_geometry import surface,isocurve,verify_tensor
from native_bspline import segments,check,cubic_path,point

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_07.tex'
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_07.tex')['applied']
K=(F(0),)*3+(F(1),)*3
P=tuple(tuple((F(-2+2*i),F(3+2*j),F(1,2)+F(2*(i==1))+F(j==1)) for j in range(3)) for i in range(3))
W=(F(1,10),-F(1),F(3,10));N=(F(0),F(1),F(0));Q=(-F(3),F(0),F(6))
def project(a):return tuple(x+a[1]*w for x,w in zip(a,W))
B=tuple(tuple(map(project,row)) for row in P)
checks=verify_tensor(K,K,2,2,P,steps=10)+verify_tensor(K,K,2,2,B,steps=10)
for i in range(21):
    for j in range(21):
        u,v=F(i,20),F(j,20)
        assert project(surface(K,K,2,2,P,u,v))==surface(K,K,2,2,B,u,v)
lines=['% Independent biquadratic representative; affine projection of all9 controls.',
       '% Every projected isocurve evaluated from projected control net, no trace.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-4.1,-5.4) rectangle (8.2,11.5);',
       r'\begin{scope}[x={(-.9cm,-.6cm)},y={(.95cm,-.35cm)},z={(0cm,1.4cm)}]',
       r'\draw[book grid] (3,0,0)--(-3,0,0)--(-3,0,6)--(3,0,6)--cycle;']
for net,projected in [(P,False),(B,True)]:
    style='book grid,dashed' if projected else 'book grid'
    for row in net:lines.append(r'\draw['+style+'] '+'--'.join(map(point,row))+';')
    for j in range(3):lines.append(r'\draw['+style+'] '+'--'.join(point(row[j]) for row in net)+';')
    for variable in ('u','v'):
        for k in range(5):
            fixed=F(k,4);U,p,C=isocurve(K,K,2,2,net,variable,fixed);ss=segments(U,C,p);checks+=check(U,C,p,ss)
            style=('book line' if k in (0,4) else 'book grid')+(',dashed' if projected else '')
            lines.extend(cubic_path(s,style) for s in ss)
lines += [r'\draw[book axis] '+point(P[2][2])+'--'+point(B[2][2])+r' node[pos=.68,above right=8pt] {$\mathbf W$};']
for pt,label,anchor in [(P[2][2],r'\mathbf P_{2,2}','below right'),(B[2][2],r'\overline{\mathbf P}_{2,2}','left'),(Q,r'\mathbf Q','above left')]:
    gap='12pt' if pt==B[2][2] else '5pt'
    lines.append(r'\draw '+point(pt)+r' circle[radius=2pt] node['+anchor+'='+gap+r'] {$'+label+'$};')
lines += [r'\draw[book axis] '+point(Q)+'--'+point(tuple(q+F(5,2)*n for q,n in zip(Q,N)))+r' node[right=4pt] {$\mathbf N$};',
          r'\draw[book axis] (0,0,0)--(4,0,0) node[below left=4pt] {$x$};',
          r'\draw[book axis] (0,0,0)--(0,8,0) node[right=4pt] {$y$};',
          r'\draw[book axis] (0,0,0)--(0,0,7.7) node[above=4pt] {$z$};',r'\end{scope}',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-parallel-projection-check.json').write_text(json.dumps({
    'figure':'6.7','original_controls':[[list(map(str,pt)) for pt in row] for row in P],
    'projected_controls':[[list(map(str,pt)) for pt in row] for row in B],
    'direction':list(map(str,W)),'native_tensor_and_curve_checks':checks,
    'exact_surface_projection_identities':441,'unit_weights_unchanged':True},indent=2)+'\n')
print(f'PASS:{checks} native tensor/isocurve checks,441 exact surface-affine commutation checks.')
