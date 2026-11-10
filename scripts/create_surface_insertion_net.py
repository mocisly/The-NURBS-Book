"""Fig5.9: exact indexed4x4 native control net for the specified surface space."""
from pathlib import Path
import json
from native_bspline import point
from surface_geometry import verify_tensor
from knot59_data import U,V,P

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_10.tex';assert not target.exists()
n=verify_tensor(U,V,3,2,P,10)
lines=['% Fig5.9: representative4x4 cubic-by-quadratic control net, unit weights.',
       '% U=(0,0,0,0,1,1,1,1), V=(0,0,0,1/2,1,1,1).',
       '% Same actual3D coordinates reused for all subsequent insertion/subdivision illustrations.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-6cm,y=-4.9cm) rectangle (canvas cs:x=7cm,y=8.1cm);',
       r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,6,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,7.1) node[above=4pt] {$z$};']
for row in P:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
for j in range(4):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in P)+';')
for row in P:
    for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1.25pt];')
for i,j,anchor in [(0,0,'below left'),(1,0,'below left'),(3,0,'below right'),(0,1,'above left'),(0,3,'above'),(3,3,'right')]:
    lines.append(r'\node['+anchor+'=5pt] at '+point(P[i][j])+r' {$\mathbf P_{'+str(i)+','+str(j)+'}$};')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-insertion-net-check.json').write_text(json.dumps({'figure':'5.9','degrees':[3,2],'U':list(map(str,U)),'V':list(map(str,V)),'representative_controls':[[list(map(str,p)) for p in row] for row in P],'weights':'all1','control_count':[4,4],'tensor_vs_nested_deboor_points':n},indent=2)+'\n')
print(f'PASS:4x4 controls match specified cubic/quadratic knot counts,{n} exact tensor/nested-deBoor points.')
