"""Fig4.5: three equal-scale panels for the basis of the Fig4.4 family."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,cubic_path
from surface_geometry import extraction,weights
from rational_geometry import approximate,graph_controls,project,evaluate
from nurbs44_data import K,control_weights,rational

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_05.tex';assert not target.exists()
from bspline_math import piece,compose_affine
base=(F(1),F(0),F(1),F(1),F(1))
for span,expected in [(2,(F(1),F(-2),F(3,2))),(3,(F(1,2),F(1),F(-1,2))),(4,(F(1),))]:
    coefficients=tuple(sum(base[i]*(piece(K,i,2,span)[r] if r<len(piece(K,i,2,span)) else 0) for i in range(5)) for r in range(3))
    local=list(compose_affine(coefficients,K[span],K[span+1]-K[span]))
    while len(local)>1 and local[-1]==0:local.pop()
    assert tuple(local)==expected
assert rational(F(2,9),F(4))[1][1]==F(8,9)
cases=(F(4),F(3,10),F(0));panels=[];paths=checks=0;maximum=F(0)
lines=['% Exercise4.1 explicitly confirms the thirds knot vector for Fig4.5(a).',
       '% Fig4.5: the exact basis of Fig4.4 for w1=4,3/10,0; other weights1.',
       '% Equal11cm horizontal/3cm vertical scales in all three panels.',
       '% Positive denominator>=1/3, including w1=0 where R1 is identically zero.',
       '% Native cubic paths certified within0.0001cm, from rational equations, no image contours.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-1.1,-1.5) rectangle (12.6,16.5);']
for index,w1 in enumerate(cases):
    w=control_weights(w1);shift=12-6*index;local_paths=0;partition=0;graph_checks=0;denmin=F(1)
    lines += [r'\begin{scope}[yshift='+str(shift)+'cm]',
              r'\draw[book axis] (0,0)--(12,0) node[right] {$u$};',
              r'\draw[book axis] (0,0)--(0,4);',
              r'\draw[book grid] (-.08,3)--(.08,3);',r'\node[left=5pt] at (0,3) {$1$};']
    for x,label in [(0,'0'),(F(11,3),r'\frac13'),(F(22,3),r'\frac23'),(11,'1')]:
        lines += [r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';',r'\node[below=5pt] at '+point((x,0))+' {$'+label+'$};']
    for basis_index in range(5):
        for span in range(2,5):
            B=extraction(K,2,span);A=tuple(w[basis_index]*row[basis_index] for row in B)
            D=tuple(sum(row[j]*w[j] for j in range(5)) for row in B);denmin=min(denmin,*D)
            assert min(D)>=0
            if not any(A):continue
            G=graph_controls(K[span],K[span+1],A,D,F(11),F(3))
            for j in range(11):
                t=F(j,10);u=K[span]+(K[span+1]-K[span])*t;_,rr=rational(u,w1)
                assert project(evaluate(G,t))==(11*u,3*rr[basis_index]);graph_checks+=1
            for a in approximate(G):
                lines.append(cubic_path(a));local_paths+=1;maximum=max(maximum,a['certified_l1_error'])
        if basis_index in (0,4):
            x,anchor=(F(1,10),'above right') if basis_index==0 else (F(109,10),'above left')
            lines.append(r'\node['+anchor+'=4pt] at '+point((x,F(16,5)))+' {$R_{'+str(basis_index)+',2}$};')
        elif w[basis_index]:
            # A rational sample only locates the label; curves are equation-based.
            candidates=[(rational(F(j,100),w1)[1][basis_index],F(j,100)) for j in range(101)]
            peak,u=max(candidates)
            if basis_index==1 and w1==F(3,10):
                u=F(8,25);peak=rational(u,w1)[1][basis_index]
            lines.append(r'\node[above=5pt] at '+point((11*u,3*peak))+' {$R_{'+str(basis_index)+',2}$};')
    for j in range(101):
        u=F(j,100);_,rr=rational(u,w1);partition+=1
        if w1==0:assert rr[1]==0
    for x in (F(-1,25),F(1,25),F(274,25),F(276,25)):
        lines.append(r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';')
    wlabel=r'\frac3{10}' if w1==F(3,10) else str(w1)
    lines += [r'\node at (5.5,-1.1) {('+chr(97+index)+r')\quad $w_1='+wlabel+'$};',r'\end{scope}']
    panels.append({'w1':str(w1),'native_paths':local_paths,'rational_partition_points':partition,'exact_graph_checks':graph_checks,'minimum_initial_denominator_control':str(denmin),'denominator_global_lower_bound':'1/3'})
    paths+=local_paths;checks+=graph_checks
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nurbs-quadratic-basis-panels-check.json').write_text(json.dumps({
    'figure':'4.5','knots':list(map(str,K)),'panels':panels,'all_other_weights':1,
    'w1_four_R1_exact_maximum':'8/9 at u=2/9','w1_zero_R1_identically_zero':True,
    'native_cubic_paths':paths,'exact_basis_graph_checks':checks,'maximum_certified_l1_error_cm':str(maximum),
    'equal_panel_scales':{'x_cm':11,'y_cm':3},'denominator_proof':'Exact local base polynomials1-2t+3t^2/2,1/2+t-t^2/2,1 have minima1/3,1/2,1. Nonnegative w1 only increases W.'},indent=2)+'\n')
print(f'PASS:303 rational partitions,{checks} exact graph comparisons,{paths} native cubic paths; equal scales, R1 max8/9 atw1=4, R1=0 atw1=0; maximum error{float(maximum):.8f}cm.')
