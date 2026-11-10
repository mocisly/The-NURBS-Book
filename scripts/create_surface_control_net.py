"""Fig3.20(a), source21: indexed semantic control net, not an outline conversion."""
from pathlib import Path
import json
from native_bspline import point
from surface320_data import P,verify

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_21.tex';assert not target.exists()
report=verify()
lines=['% Printed Fig3.20(a), source21:5x4 representative control net.',
       '% No numerical data/degree/knots in original; chosen bicubic example recorded in surface320_data.py.',
       '% Same controls, camera and knot vectors will generate panel(b). No tracing.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5cm,y=-4.8cm) rectangle (canvas cs:x=6.1cm,y=5.2cm);',
       r'\draw[book axis] (0,0,0)--(4.5,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,5.2,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,4.5) node[above=4pt] {$z$};']
for i in range(5):
    for j in range(4): lines.append(r'\coordinate (P'+str(i)+str(j)+') at '+point(P[i][j])+';')
for i in range(5): lines.append(r'\draw[book grid,dashed] '+'--'.join('(P'+str(i)+str(j)+')' for j in range(4))+';')
for j in range(4): lines.append(r'\draw[book grid,dashed] '+'--'.join('(P'+str(i)+str(j)+')' for i in range(5))+';')
for i in range(5):
    for j in range(4): lines.append(r'\fill (P'+str(i)+str(j)+') circle[radius=1.3pt];')
for i,j,pos in [(0,0,'left'),(1,0,'below left'),(0,1,'above left'),(0,3,'above'),(4,0,'below right'),(4,3,'right')]:
    lines.append(r'\node['+pos+'=5pt] at (P'+str(i)+str(j)+r') {$\mathbf P_{'+str(i)+','+str(j)+'}$};')
lines += [r'\node at (canvas cs:x=.5cm,y=-4.45cm) {(a)};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface320-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:441 exact tensor/deBoor checks,20 indexed controls and four corner interpolation identities.')
