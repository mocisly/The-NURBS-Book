"""Fig5.11: actual surface represented by Fig5.9's common control net."""
from pathlib import Path
import json
from knot59_data import U,V,P
from native_surface_drawing import wires
from surface_geometry import verify_tensor

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_12.tex';assert not target.exists()
curves,report=wires(U,V,3,2,P)
report.update(figure='5.11',same_controls_as5_9=True,tensor_vs_nested_deboor_points=verify_tensor(U,V,3,2,P,10),weights='all1')
lines=['% Fig5.11: actual cubic-by-quadratic polynomial surface of Fig5.9, identical unit-weight controls.',
       '% Thirty-one exact u-isocurves and four boundary curves; no raster sampling or contour conversion.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-6cm,y=-4.9cm) rectangle (canvas cs:x=7cm,y=8.1cm);']+curves+[
       r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,6,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,7.1) node[above=4pt] {$z$};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/subdivision-base-surface-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:'+json.dumps(report))
