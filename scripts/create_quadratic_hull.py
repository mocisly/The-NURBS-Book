"""Fig3.4: an exact quadratic span lies in its three active controls' hull."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_04.tex'
assert not target.exists()
knots=(F(0),)*3+(F(1,4),F(1,2),F(3,4))+(F(1),)*3
controls=((0,0),(F(-2,5),4),(5,4),(F(23,10),-2),(F(21,2),-2),(F(17,2),2))
segs=segments(knots,controls,2);count=check(knots,controls,2,segs)
def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
active=controls[1:4]
for q in segs[1]['bern']:
    signs=[cross(active[i],active[(i+1)%3],q) for i in range(3)]
    assert all(v>=0 for v in signs) or all(v<=0 for v in signs)
lines=['% Fig3.4: strong convex hull, p=2, active P1,P2,P3 on [u3,u4).',
       '% Representative controls and clamped uniform knot spacing; no numerical data in caption.',
       '% Exact mathematical curve and hull, no raster outline coordinates.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines += [r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5);',
          r'\draw[dashed,book grid] (P1)--(P3);']
for j,seg in enumerate(segs): lines.append(cubic_path(seg,'dashed' if j==1 else ''))
for seg in segs[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
lines += [r'\foreach \i in {0,...,5} \node[book point] at (P\i) {};',
          r'\node at (1.9,2.7) {$u\in[u_3,u_4)$};']
for i,pos in enumerate(['below left','above left','above right','below left','below right','above']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/quadratic-hull-check.json').write_text(json.dumps({'figure':'3.4',
    'knots':list(map(str,knots)),'representative_controls':[[str(v) for v in p] for p in controls],
    'exact_deboor_comparisons':count,'active_indices':[1,2,3],
    'selected_span_bezier_controls_inside_triangle':True},indent=2)+'\n')
print(f'PASS: {count} exact curve checks and full selected Bezier hull containment.')
