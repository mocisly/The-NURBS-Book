"""Fig5.6: exact cubic bases before/after three insertions at1."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,cubic_path,de_boor
from surface_geometry import extraction,weights
from rational_geometry import evaluate
from knot55_data import K,states

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_07.tex';assert not target.exists()
lines=['% Fig5.6: basis functions of the EXACT knot vectors in Fig5.5.',
       '% Native exact polynomial cubic Bezier graphs, equal axes in both panels.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',r'\path[use as bounding box] (-.8,-1.6) rectangle (12.4,11.7);']
reports=[];graphchecks=0;nativepaths=0
for index,knots in enumerate((K,states[-1][0])):
    n=len(knots)-4;shift=7 if index==0 else 0
    unit=tuple(tuple(F(i==j) for j in range(n)) for i in range(n))
    for j in range(101):
        u=F(3*j,100);rr=weights(knots,3,u)
        assert min(rr)>=0 and sum(rr)==1 and tuple(rr)==de_boor(knots,unit,3,u)
    lines += [r'\begin{scope}[yshift='+str(shift)+'cm]',r'\draw[book axis] (0,0)--(11.8,0) node[right=4pt] {$u$};',r'\draw[book axis] (0,0)--(0,4.35);',r'\draw[book grid] (-.08,3.2)--(.08,3.2) node[left=5pt] {$1$};']
    paths=0
    for s in range(3,n):
        a,b=knots[s:s+2]
        if a==b:continue
        B=extraction(knots,3,s)
        for i in range(n):
            if not any(row[i] for row in B):continue
            controls=tuple((F(18,5)*(a+(b-a)*F(r,3)),F(16,5)*B[r][i]) for r in range(4))
            for j in range(11):
                t=F(j,10);u=a+(b-a)*t
                assert evaluate(controls,t)==(F(18,5)*u,F(16,5)*weights(knots,3,u)[i]);graphchecks+=1
            lines.append(cubic_path({'bern':controls}));paths+=1
    for i in range(n):
        label=('N_' if index==0 else r'\bar N_')+str(i)
        if i in (0,n-1):x,y,anchor=(F(1,10),F(17,5),'above right') if i==0 else (F(107,10),F(17,5),'above left')
        else:
            peak,u=max((weights(knots,3,F(3*j,200))[i],F(3*j,200)) for j in range(201));x,y,anchor=F(18,5)*u,F(16,5)*peak,'above'
        lines.append(r'\node['+anchor+'=5pt] at '+point((x,y))+' {$'+label+'$};')
    for u in sorted(set(knots)):
        m=knots.count(u)
        for j in range(m):
            x=F(18,5)*u+F(3,50)*(F(j)-F(m-1,2));lines.append(r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';')
        anchor='below left' if index==1 and u==1 else 'below'
        lines.append(r'\node['+anchor+'=5pt] at '+point((F(18,5)*u,0))+' {$'+str(u)+'$};')
    if index==1:lines.append(r'\draw[book axis] (3.6,-.95)--(3.6,-.12);')
    lines += [r'\node at (5.4,-1.4) {('+chr(97+index)+')};',r'\end{scope}']
    nativepaths+=paths;reports.append({'knots':list(map(str,knots)),'basis_count':n,'partition_and_deboor_points':101,'native_cubic_paths':paths})
at1=weights(states[-1][0],3,F(1));assert at1[3]==1 and sum(at1)==1 and sum(v!=0 for v in at1)==1
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/repeated-insertion-bases-check.json').write_text(json.dumps({'figure':'5.6','panels':reports,'exact_native_graph_vs_basis_points':graphchecks,'native_paths':nativepaths,'shared_basis_at1':list(map(str,at1)),'same_horizontal_and_vertical_scales_cm':['10.8','3.2']},indent=2)+'\n')
print(f'PASS:202 partition/deBoor points,{graphchecks} exact graph checks,{nativepaths} native cubic paths; only barN3(1)=1.')
