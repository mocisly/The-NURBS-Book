"""7.20: exact insertion replaces the infinite control by two finite controls."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,de_boor,point
from rational_geometry import project
from knot51_data import insert
from native_rational_basis import graphs

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_23.tex')['applied']
K=(F(0),)*3+(F(1),)*3;H=((F(1),F(0),F(1)),(F(0),F(1),F(0)),(-F(1),F(0),F(1)))
U,QH,alphas=insert(K,H,2,F(1,2));assert all(v==F(1,2) for v in alphas.values())
assert QH==(H[0],(F(1,2),F(1,2),F(1,2)),(-F(1,2),F(1,2),F(1,2)),H[2])
Q=tuple(project(h) for h in QH);W=tuple(h[-1] for h in QH);assert Q==((1,0),(1,1),(-1,1),(-1,0))
old,new=segments(K,H,2),segments(U,QH,2);assert all(s['power']==old[0]['power'] for s in new)
nativechecks=check(U,QH,2,new)
for i in range(101):
    u=F(i,100);h=de_boor(U,QH,2,u);assert h==de_boor(K,H,2,u) and h[-1]>=F(1,2)
    R=[de_boor(U,tuple((w*F(k==j),) for k,w in enumerate(W)),2,u)[0]/h[-1] for j in range(4)]
    assert min(R)>=0 and sum(R)==1 and project(h)==tuple(sum(r*q[d] for r,q in zip(R,Q)) for d in range(2))
    x,y=project(h);assert x*x+y*y==1 and y>=0
lines=['% Exact Ex7.5 insertion into H=(1,0,1),(0,1,0),(-1,0,1).',
       '% Q1H=(+1/2,1/2,1/2),Q2H=(-1/2,1/2,1/2); OCR signs must match this insertion.',
       r'\begin{tikzpicture}[book line]',r'\begin{scope}[x=4cm,y=4cm]',
       r'\path[use as bounding box] (-1.85,-.9) rectangle (1.95,1.6);',
       r'\draw[book axis,book grid] (-1.5,0)--(1.5,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-.35)--(0,1.35) node[above=4pt] {$y$};',
       r'\draw[book grid] '+'--'.join(map(point,Q))+';']
for i in range(1,40):
    C=project(de_boor(U,QH,2,F(i,40)));assert C==project(de_boor(K,H,2,F(i,40)))
    lines += [r'\begin{scope}[shift={'+point(C)+'}]',r'\draw (-1.5pt,0)--(1.5pt,0) (0,-1.5pt)--(0,1.5pt);',r'\end{scope}']
for i,(q,anchor) in enumerate(zip(Q,('below right','above right','above left','below left'))):
    label=r'\mathbf Q_0=\mathbf P_0' if i==0 else r'\mathbf Q_3=\mathbf P_2' if i==3 else r'\mathbf Q_'+str(i)
    lines.append(r'\draw '+point(q)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};')
lines += [r'\node at (0,-.65) {(a)};',r'\end{scope}',r'\begin{scope}[xshift=10.2cm,yshift=-.2cm]',
          r'\path[use as bounding box] (-.6,-1.9) rectangle (13.1,5.1);',
          r'\draw[book axis] (-.1,0)--(12.7,0) node[right=4pt] {$u$};',
          r'\draw[book axis] (0,0)--(0,4.7);',r'\node[left=5pt] at (0,4) {$1$};']
basis,proofs=graphs(U,W);lines+=basis
for i,u,anchor in [(0,F(0),'above right'),(1,F(3,8),'above'),(2,F(5,8),'above'),(3,F(1),'above left')]:
    h=de_boor(U,QH,2,u);v=de_boor(U,tuple((w*F(k==i),) for k,w in enumerate(W)),2,u)[0]/h[-1]
    lines.append(r'\node['+anchor+r'=6pt] at '+point((12*u,4*v))+' {$R_{'+str(i)+r',2}$};')
for u,label,m in [(F(0),'0',3),(F(1,2),r'\tfrac12',1),(F(1),'1',3)]:
    for k in range(m):
        x=12*u+F(7,100)*(F(k)-F(m-1,2));lines.append(r'\draw[book grid] '+point((x,-F(1,10)))+'--'+point((x,F(1,10)))+';')
    lines.append(r'\node[below=6pt] at '+point((12*u,-F(1,10)))+' {$'+label+'$};')
lines += [r'\node at (6,-1.55) {(b)};',r'\end{scope}',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_23.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/four-control-semicircle-check.json').write_text(json.dumps({'figure':'7.20','knots':list(map(str,U)),'homogeneous_controls':[[str(x) for x in h] for h in QH],'controls':[[str(x) for x in q] for q in Q],'weights':list(map(str,W)),'exact_original_homogeneous_polynomial_coefficients_unchanged':True,'global_denominator_lower_bound':'1/2','native_checks':nativechecks,'exact_circle_insertion_partition_checks':101,'all39_interior_markers_unchanged':True,'OCR_Q1_Q2_x_signs_verified_by_insertion':True,'native_basis_graph_certificates':proofs},indent=2)+'\n')
print('PASS:exact insertion and homogeneous coefficient identity;101circle/partition checks;Q1xpositive,Q2xnegative;4certified rational bases.')
