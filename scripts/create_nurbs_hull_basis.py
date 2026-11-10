"""Fig4.1: rational cubic local convex hull and its seven weighted basis functions."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,de_boor,point,cubic_path
from surface_geometry import weights,extraction
from rational_geometry import approximate,graph_controls,evaluate,project

root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch04/fig_4_01.tex';assert not target.exists()
K=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
P=tuple(tuple(map(F,p)) for p in [(0,0),(1,3),(5,F(17,5)),(3,-2),(9,-2),(8,F(8,5)),(11,2)])
w=(F(1),F(1),F(1),F(3),F(1),F(1),F(1))
H=tuple((w[i]*p[0],w[i]*p[1],w[i]) for i,p in enumerate(P))
segs=segments(K,H,3);exact_checks=check(K,H,3,segs)
def rational(u):
    n=weights(K,3,u);d=sum(a*b for a,b in zip(n,w));r=tuple(n[i]*w[i]/d for i in range(7))
    assert min(r)>=0 and sum(r)==1
    val=tuple(sum(r[i]*P[i][j] for i in range(7)) for j in range(2))
    assert val==project(de_boor(K,H,3,u))
    return val,r
for i in range(101):rational(F(i,100))
E=extraction(K,3,4)
assert all(E[r][i]==0 for r in range(4) for i in (0,5,6))
assert all(min(row)>=0 and sum(row)==1 for row in E)
lines=['% Fig4.1: stated cubic knots and weights(1,1,1,3,1,1,1).',
       '% Representative seven control coordinates; convex hull uses P1,P2,P3,P4 on[1/4,1/2].',
       '% Rational functions evaluated from exact homogeneous B-spline pieces.',
       '% Native cubic Hermite paths have certified L1 error <=0.0001cm via Bernstein residual bounds.',
       '% No scan contours, extracted outlines, or raster wrappers.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-1.3,-1.4) rectangle (12.7,12.3);',
       r'\begin{scope}[yshift=8cm]']
for i,p in enumerate(P):lines.append(r'\coordinate(P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5)--(P6);')
lines.append(r'\draw[dashed,book grid] (P1)--(P2)--(P4)--(P3)--cycle;')
paths=0;bounds=[];curve_paths=0
for i,seg in enumerate(segs):
    pieces=approximate(seg['bern']);curve_paths+=len(pieces)
    for s in pieces:
        bounds.append(s['certified_l1_error']);paths+=1
        lines.append(cubic_path(s,'dashed' if i==1 else ''))
for seg in segs[:-1]:lines.append(r'\fill '+point(project(seg['bern'][-1]))+' circle[radius=1.6pt];')
for i,pos in enumerate(['below left','above left','above','below left','below right','above left','above right']):
    lines.extend([r'\node[book point] at (P'+str(i)+') {};',r'\node['+pos+'=5pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};'])
lines += [r'\node at (5.5,-3) {(a)};',r'\end{scope}',
          r'\draw[book axis] (0,0)--(12,0) node[right] {$u$};',
          r'\draw[book axis] (0,0)--(0,4);']
for x,label in [(0,'0'),(F(11,4),r'\frac14'),(F(11,2),r'\frac12'),(F(33,4),r'\frac34'),(11,'1')]:
    lines.extend([r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';',
                  r'\node[below=5pt] at '+point((x,0))+' {$'+label+'$};'])
for x in (F(11,4),F(11,2)):lines.append(r'\draw[book grid] '+point((x,0))+'--'+point((x,F(17,5)))+';')
lines += [r'\draw[book grid] (-.08,3)--(.08,3);',r'\node[left=5pt] at (0,3) {$1$};']
basis_pieces=0;graph_checks=0
for index in range(7):
    for span in range(3,7):
        B=extraction(K,3,span)
        A=tuple(w[index]*row[index] for row in B)
        D=tuple(sum(row[j]*w[j] for j in range(7)) for row in B)
        if not any(A):continue
        G=graph_controls(K[span],K[span+1],A,D,F(11),F(3))
        for j in range(11):
            t=F(j,10);u=K[span]+(K[span+1]-K[span])*t
            val=project(evaluate(G,t));_,rr=rational(u)
            assert val==(11*u,3*rr[index]);graph_checks+=1
        pieces=approximate(G);basis_pieces+=len(pieces)
        for s in pieces:
            bounds.append(s['certified_l1_error']);paths+=1
            lines.append(cubic_path(s,'dashed' if span==4 else ''))
for x in (F(-2,25),F(-1,25),F(1,25),F(2,25),F(273,25),F(274,25),F(276,25),F(277,25)):
    lines.append(r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';')
for pos,anchor,label in [((F(1,10),F(16,5)),'above right',0),((F(109,10),F(16,5)),'above left',6),
                         ((F(11,10),F(21,10)),'above',1),((F(99,10),F(21,10)),'above',5),
                         ((F(29,5),F(29,10)),'above right',3)]:
    lines.append(r'\node['+anchor+'=3pt] at '+point(pos)+' {$R_{'+str(label)+',3}$};')
for index,u,pos in [(2,F(1,4),(F(16,5),F(11,5))),(4,F(7,10),(F(77,10),F(11,5)))]:
    _,rr=rational(u)
    lines.append(r'\node(R'+str(index)+') at '+point(pos)+' {$R_{'+str(index)+',3}$};')
    lines.append(r'\draw[book grid] (R'+str(index)+'.south)--'+point((11*u,3*rr[index]))+';')
lines += [r'\node at (5.5,-1.1) {(b)};',r'\end{tikzpicture}']
target.parent.mkdir(exist_ok=True)
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nurbs-hull-basis-check.json').write_text(json.dumps({
    'figure':'4.1','representative_controls':[[str(v) for v in p] for p in P],
    'knots':list(map(str,K)),'weights':list(map(str,w)),
    'exact_homogeneous_piece_checks':exact_checks,'partition_nonnegative_projection_points':101,
    'exact_basis_graph_checks':graph_checks,'curve_cubic_paths':curve_paths,'basis_cubic_paths':basis_pieces,
    'all_native_cubic_paths':paths,'maximum_certified_l1_error_cm':str(max(bounds)),
    'tolerance_cm':'1/10000','convex_hull_active_controls':[1,2,3,4],
    'full_span_convex_hull_proof':'Nonnegative homogeneous Bezier extraction rows sum1 and vanish outside1..4; positive weights preserve convex projection',
    'chapter_integration':'Tracked separately in manifest and chapter layout review'},indent=2)+'\n')
print(f'PASS:{exact_checks} homogeneous checks,101 rational partitions,{graph_checks} exact graph comparisons;{paths} certified native cubic paths, maximum error{float(max(bounds)):.8f}cm.')
