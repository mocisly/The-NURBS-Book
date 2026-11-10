"""Fig4.3: three equal-scale panels for the basis of the Fig4.2 family."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,cubic_path
from surface_geometry import extraction,weights
from rational_geometry import approximate,graph_controls,project,evaluate
from nurbs41_data import K,control_weights,rational

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_03.tex';assert not target.exists()
cases=(F(1),F(3,10),F(0));panels=[];paths=checks=0;maximum=F(0)
lines=['% Fig4.3: the exact basis of Fig4.2 for w3=1,3/10,0; other weights1.',
       '% Equal11cm horizontal/3cm vertical scales in all three panels.',
       '% Positive denominator>=1/3, including w3=0 where R3 is identically zero.',
       '% Native cubic paths certified within0.0001cm, from rational equations, no image contours.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-1.1,-1.5) rectangle (12.6,16.5);']
for index,w3 in enumerate(cases):
    w=control_weights(w3);shift=12-6*index;local_paths=0;partition=0;graph_checks=0;denmin=F(1)
    lines += [r'\begin{scope}[yshift='+str(shift)+'cm]',
              r'\draw[book axis] (0,0)--(12,0) node[right] {$u$};',
              r'\draw[book axis] (0,0)--(0,4);',
              r'\draw[book grid] (-.08,3)--(.08,3);',r'\node[left=5pt] at (0,3) {$1$};']
    for x,label in [(0,'0'),(F(11,4),r'\frac14'),(F(11,2),r'\frac12'),(F(33,4),r'\frac34'),(11,'1')]:
        lines += [r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';',r'\node[below=5pt] at '+point((x,0))+' {$'+label+'$};']
    for basis_index in range(7):
        for span in range(3,7):
            B=extraction(K,3,span);A=tuple(w[basis_index]*row[basis_index] for row in B)
            D=tuple(sum(row[j]*w[j] for j in range(7)) for row in B);denmin=min(denmin,*D)
            assert min(D)>=F(1,3)
            if not any(A):continue
            G=graph_controls(K[span],K[span+1],A,D,F(11),F(3))
            for j in range(11):
                t=F(j,10);u=K[span]+(K[span+1]-K[span])*t;_,rr=rational(u,w3)
                assert project(evaluate(G,t))==(11*u,3*rr[basis_index]);graph_checks+=1
            for a in approximate(G):
                lines.append(cubic_path(a));local_paths+=1;maximum=max(maximum,a['certified_l1_error'])
        if basis_index in (0,6):
            x,anchor=(F(1,10),'above right') if basis_index==0 else (F(109,10),'above left')
            lines.append(r'\node['+anchor+'=4pt] at '+point((x,F(16,5)))+' {$R_{'+str(basis_index)+',3}$};')
        elif w[basis_index]:
            # A rational sample only locates the label; curves are equation-based.
            candidates=[(rational(F(j,100),w3)[1][basis_index],F(j,100)) for j in range(101)]
            peak,u=max(candidates)
            lines.append(r'\node[above=5pt] at '+point((11*u,3*peak))+' {$R_{'+str(basis_index)+',3}$};')
    for j in range(101):
        u=F(j,100);_,rr=rational(u,w3);partition+=1
        if w3==1:assert rr==tuple(weights(K,3,u))
        if w3==0:assert rr[3]==0
    for x in (F(-2,25),F(-1,25),F(1,25),F(2,25),F(273,25),F(274,25),F(276,25),F(277,25)):
        lines.append(r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';')
    wlabel=r'\frac3{10}' if w3==F(3,10) else str(w3)
    lines += [r'\node at (5.5,-1.1) {('+chr(97+index)+r')\quad $w_3='+wlabel+'$};',r'\end{scope}']
    panels.append({'w3':str(w3),'native_paths':local_paths,'rational_partition_points':partition,'exact_graph_checks':graph_checks,'denominator_lower_bound':str(denmin)})
    paths+=local_paths;checks+=graph_checks
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nurbs-basis-weight-panels-check.json').write_text(json.dumps({
    'figure':'4.3','knots':list(map(str,K)),'panels':panels,'all_other_weights':1,
    'w3_one_basis_equals_polynomial_basis':True,'w3_zero_R3_identically_zero':True,
    'native_cubic_paths':paths,'exact_basis_graph_checks':checks,'maximum_certified_l1_error_cm':str(maximum),
    'equal_panel_scales':{'x_cm':11,'y_cm':3}},indent=2)+'\n')
print(f'PASS:303 rational partitions,{checks} exact graph comparisons,{paths} native cubic paths; equal scales, R=N atw3=1, R3=0 atw3=0; maximum error{float(maximum):.8f}cm.')
