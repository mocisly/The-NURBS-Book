"""Fig5.15: actual fixed-u isocurve and the controls obtained by knot insertion."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot59_data import U,V,P
from surface_subdivision import split
from surface_geometry import isocurve,surface
from native_surface_drawing import wires
from native_bspline import segments,check,cubic_path,point,de_boor

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_17.tex';assert not target.exists()
base=(U,V,3,2,P);u0=F(3,4);children,refined=split(base,'u',u0)
k,d,Q=isocurve(*base,'v',u0);assert Q==children[0][-1][-1]==children[1][-1][0]
for j in range(101):
    v=F(j,100);assert de_boor(k,Q,d,v)==surface(*base,u0,v)
for a in range(11):
    for b in range(11):assert surface(*base,F(a,10),F(b,10))==surface(*refined,F(a,10),F(b,10))
ss=segments(k,Q,d);exact=check(k,Q,d,ss);background,report=wires(*base)
lines=['% Fig5.15: actual isocurve C(v)=S(3/4,v), SAME representative surface as5.9/5.11.',
       '% Four extracted controls equal BOTH shared boundary rows after3 insertions ofu=3/4.',
       '% Controls independently computed by tensor-basis contraction; exact native quadratic paths.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-6cm,y=-4.9cm) rectangle (canvas cs:x=7cm,y=8.1cm);']+background
lines += [r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',r'\draw[book axis] (0,0,0)--(0,6,0) node[right=4pt] {$y$};',r'\draw[book axis] (0,0,0)--(0,0,7.1) node[above=4pt] {$z$};',r'\draw[book grid,dashed] '+'--'.join(map(point,Q))+';']
for s in ss:lines.append(cubic_path(s,'book line,line width=.95pt'))
for pt in Q:lines.append(r'\fill '+point(pt)+' circle[radius=1.7pt];')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report.update(figure='5.15',same_controls_as5_9=True,unit_weights=True,fixed_u='3/4',curve_degree=d,curve_knots=list(map(str,k)),
    extracted_controls=[[str(c) for c in pt] for pt in Q],inserted_u_multiplicity=refined[0].count(u0),
    direct_tensor_contraction_equals_inserted_boundary_rows=True,curve_vs_original_surface_points=101,
    full_surface_invariance_points=121,exact_selected_curve_checks=exact,selected_curve_width_pt='.95')
(root/'image_tex/build/isocurve-extraction-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:four extracted controls match direct contraction and both inserted boundary rows;101 curve/surface and121 surface invariance points;82 exact selected curve checks.')
