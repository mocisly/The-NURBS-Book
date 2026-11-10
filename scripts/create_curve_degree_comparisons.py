"""Fig5.37: original cubic and exact quartic/quintic/septic representations."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from degree_elevation_geometry import elevate_spline

root=Path(__file__).resolve().parents[1]
U=(F(0),)*4+(F('.4'),F('.7'))+(F(1),)*4
P=tuple(tuple(F(str(t)) for t in q) for q in [(0,0),(1,6),(4.5,6),(5.7,2.2),(9.4,2.5),(10.3,7.6)])
ss=segments(U,P,3);checks=check(U,P,3,ss);states=[(U,P,3)];proofs=[];comparisons=0
for t in (1,2,4):
    K,Q,proof=elevate_spline(U,P,3,t);r=3+t
    checks+=check(K,Q,r,segments(K,Q,r));states.append((K,Q,r));proofs.append(proof)
    for i in range(201):
        u=F(i,200);assert de_boor(K,Q,r,u)==de_boor(U,P,3,u);comparisons+=1
assert [len(q) for k,q,r in states]==[6,9,12,18]
for pair in range(2):
    target=root/f'image_tex/ch05/fig_5_{52+pair}.tex';assert not target.exists()
    lines=['% Exact degree elevation; common invariant cubic geometry in all panels.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.8,-1.6) rectangle (23.8,8.3);']
    for col in range(2):
        i=2*pair+col;K,Q,r=states[i]
        lines.append(r'\begin{scope}[xshift='+str(12.3*col)+'cm]')
        lines.append(r'\draw[book grid] '+'--'.join(map(point,Q))+';')
        for s in ss:lines.append(cubic_path(s))
        for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=1.7pt];')
        lines.append(r'\node at (5.15,-.7) {('+chr(97+i)+r') $p='+str(r)+r',\quad N='+str(len(Q))+'$};')
        lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-degree-comparisons-check.json').write_text(json.dumps({
    'figure':'5.37','original_knots':list(map(str,U)),
    'representative_original_controls':[[str(t) for t in q] for q in P],
    'degrees':[r for k,q,r in states],'control_counts':[len(q) for k,q,r in states],
    'states':[{'U':list(map(str,k)),'controls':[[str(t) for t in q] for q in controls]} for k,controls,r in states],
    'elevation_proofs':proofs,'native_checks':checks,'exact_parameterization_points':comparisons,
    'all_panels_draw_identical_native_cubic_paths':True},indent=2)+'\n')
print(f'PASS: {checks} native checks, {comparisons} exact parameter comparisons; cubic/quartic/quintic/septic identical.')
