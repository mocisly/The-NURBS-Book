"""7.19: exact insertion turns7.18's negative-weight arc into positive weights."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import segments,check,de_boor,point
from rational_geometry import project
from knot51_data import insert
from native_rational_basis import graphs

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_22.tex')['applied']
D=10**40;n=isqrt(3*D*D);lo,hi=F(n,2*D),F(n+1,2*D);assert lo*lo<F(3,4)<hi*hi;a=(lo+hi)/2
K=(F(0),)*3+(F(1),)*3;H=((a,F(1,2),F(1)),(F(0),-F(1),-F(1,2)),(-a,F(1,2),F(1)))
U,QH,alphas=insert(K,H,2,F(1,2));assert all(v==F(1,2) for v in alphas.values())
expected=(H[0],(a/2,-F(1,4),F(1,4)),(-a/2,-F(1,4),F(1,4)),H[2]);assert QH==expected
W=tuple(h[-1] for h in QH);Q=tuple(project(h) for h in QH)
assert W==(F(1),F(1,4),F(1,4),F(1)) and Q==((a,F(1,2)),(2*a,-F(1)),(-2*a,-F(1)),(-a,F(1,2)))
before=segments(K,H,2);after=segments(U,QH,2);nativechecks=check(U,QH,2,after)
assert all(s['power']==before[0]['power'] for s in after)
for i in range(101):
    u=F(i,100);h=de_boor(U,QH,2,u);assert h==de_boor(K,H,2,u) and h[-1]>=F(1,4)
    R=[de_boor(U,tuple((w*F(k==j),) for k,w in enumerate(W)),2,u)[0]/h[-1] for j in range(4)]
    assert min(R)>=0 and sum(R)==1 and project(h)==tuple(sum(r*q[d] for r,q in zip(R,Q)) for d in range(2))
    assert abs(float(sum(x*x for x in project(h))-1))<1e-38
lines=['% Exact Ex7.4 insertion u1/2: QH=(H0,(a/2,-1/4,1/4),(-a/2,-1/4,1/4),H2).',
       '% Every global homogeneous polynomial coefficient unchanged; same u=i/40 points as7.18.',
       r'\begin{tikzpicture}[book line]',r'\begin{scope}[x=4cm,y=4cm]',
       r'\path[use as bounding box] (-2.3,-1.75) rectangle (2.5,1.4);',
       r'\draw[book axis,book grid] (-2.1,0)--(2.15,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-1.35)--(0,1.2) node[above=4pt] {$y$};',
       r'\draw[book grid] '+'--'.join(map(point,Q))+';']
for i in range(1,40):
    C=project(de_boor(U,QH,2,F(i,40)));assert C==project(de_boor(K,H,2,F(i,40)))
    lines += [r'\begin{scope}[shift={'+point(C)+'}]',r'\draw (-1.5pt,0)--(1.5pt,0) (0,-1.5pt)--(0,1.5pt);',r'\end{scope}']
for i,(q,anchor) in enumerate(zip(Q,('above right','below right','below left','above left'))):
    label=r'\mathbf Q_0=\mathbf P_0' if i==0 else r'\mathbf Q_3=\mathbf P_2' if i==3 else r'\mathbf Q_'+str(i)
    lines.append(r'\draw '+point(q)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};')
lines += [r'\node at (0,-1.55) {(a)};',r'\end{scope}',r'\begin{scope}[xshift=13.1cm,yshift=-2.3cm]',
          r'\path[use as bounding box] (-.6,-1.9) rectangle (13.1,5.1);',
          r'\draw[book axis] (-.1,0)--(12.7,0) node[right=4pt] {$u$};',
          r'\draw[book axis] (0,0)--(0,4.7);',r'\node[left=5pt] at (0,4) {$1$};']
basis,proofs=graphs(U,W);lines+=basis
q=2*a/3
for i,u,v,anchor in [(0,F(0),F(1),'above right'),(1,1-q,q,'above'),(2,q,q,'above'),(3,F(1),F(1),'above left')]:
    lines.append(r'\node['+anchor+r'=6pt] at '+point((12*u,4*v))+' {$R_{'+str(i)+r',2}$};')
for u,label,m in [(F(0),'0',3),(F(1,2),r'\tfrac12',1),(F(1),'1',3)]:
    for k in range(m):
        x=12*u+F(7,100)*(F(k)-F(m-1,2));lines.append(r'\draw[book grid] '+point((x,-F(1,10)))+'--'+point((x,F(1,10)))+';')
    lines.append(r'\node[below=6pt] at '+point((12*u,-F(1,10)))+' {$'+label+'$};')
lines += [r'\node at (6,-1.55) {(b)};',r'\end{scope}',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_22.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/positive-circle-arc-check.json').write_text(json.dumps({'figure':'7.19','original_knots':list(map(str,K)),'inserted_knots':list(map(str,U)),'homogeneous_controls':[[str(x) for x in h] for h in QH],'positive_weights':list(map(str,W)),'all_global_homogeneous_polynomials_identical':True,'homogeneous_quadratic_smoothness_unchanged':True,'global_denominator_lower_bound':'1/4','native_checks':nativechecks,'exact_homogeneous_curve_partition_checks':101,'all39_interior_sample_points_identical_to_7_18':True,'native_basis_graph_certificates':proofs},indent=2)+'\n')
print('PASS:exact Boehm insertion and ALLglobal homogeneous coefficients unchanged;101identical points and positive partitions;39markers match7.18;4certified bases.')
