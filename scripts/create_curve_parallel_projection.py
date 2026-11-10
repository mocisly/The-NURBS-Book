"""6.5: exact affine control-point and whole-curve parallel projection."""
from pathlib import Path
from fractions import Fraction as F
import json
from projection_curve_data import U,P,Q,N,W,dot,parallel
from native_bspline import segments,check,cubic_path,point,de_boor

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_05.tex'
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_05.tex')['applied']
B=tuple(map(parallel,P));ss=segments(U,P,3);bs=segments(U,B,3)
checks=check(U,P,3,ss)+check(U,B,3,bs)
for i in range(101):
    u=F(i,100);a=de_boor(U,P,3,u);b=de_boor(U,B,3,u)
    assert parallel(a)==b and dot(N,tuple(x-q for x,q in zip(b,Q)))==0
for a,b in zip(P,B):
    assert dot(N,tuple(x-q for x,q in zip(b,Q)))==0
    assert tuple((b[i]-a[i])/W[i] for i in range(3))==(a[1],)*3
lines=['% Exact affine projection onto y=0 along W=(3/20,-1,3/5).',
       '% Source and projected NURBS use identical knots and unit weights.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-5.3,-4.8) rectangle (6.9,12.8);',
       r'\begin{scope}[x={(-.9cm,-.6cm)},y={(.95cm,-.35cm)},z={(0cm,1.4cm)}]',
       r'\draw[book grid] (4.8,0,0)--(-3.5,0,0)--(-3.5,0,7)--(4.8,0,7)--cycle;',
       r'\node[above right=3pt] at (-3.5,0,7) {$\mathbf N\cdot(\mathbf X-\mathbf Q)=0$};',
       r'\draw[book grid] '+'--'.join(map(point,P))+';',
       r'\draw[book grid,dashed] '+'--'.join(map(point,B))+';']
lines.extend(cubic_path(s) for s in ss);lines.extend(cubic_path(s,'book line,dashed') for s in bs)
lines += [r'\draw[book axis] '+point(P[3])+'--'+point(B[3])+r' node[midway,left=6pt] {$\mathbf W$};',
          r'\draw '+point(P[3])+r' circle[radius=2pt] node[below right=5pt] {$\mathbf P_3$};',
          r'\draw '+point(B[3])+r' circle[radius=2pt] node[above right=6pt] {$\overline{\mathbf P}_3$};',
          r'\draw '+point(Q)+r' circle[radius=2pt] node[left=5pt] {$\mathbf Q$};',
          r'\draw[book axis] '+point(Q)+'--'+point(tuple(q+F(5,2)*n for q,n in zip(Q,N)))+r' node[right=5pt] {$\mathbf N$};',
          r'\draw[book axis] (0,0,0)--(5.5,0,0) node[below left=4pt] {$x$};',
          r'\draw[book axis] (0,0,0)--(0,7,0) node[right=4pt] {$y$};',
          r'\draw[book axis] (0,0,0)--(0,0,8.7) node[above=4pt] {$z$};',r'\end{scope}',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-parallel-projection-check.json').write_text(json.dumps({
    'figure':'6.5','source_controls':[[str(x) for x in p] for p in P],
    'projected_controls':[[str(x) for x in p] for p in B],'direction':list(map(str,W)),
    'plane_normal':list(map(str,N)),'plane_reference':list(map(str,Q)),
    'exact_projected_curve_commutation_checks':101,'native_checks':checks,
    'all_weights_unchanged_and_equal_to_one':True},indent=2)+'\n')
print(f'PASS:{checks} native checks,101 exact affine curve/projection identities; all projected controls on plane.')
