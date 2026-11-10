"""Fig3.5: cubic strong convex hull, paired with the Fig3.4 polygon."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_05.tex'
assert not target.exists()
knots=(F(0),)*4+(F(1,3),F(2,3))+(F(1),)*4
controls=((0,0),(F(-2,5),4),(5,4),(F(23,10),-2),(F(21,2),-2),(F(17,2),2))
segs=segments(knots,controls,3);count=check(knots,controls,3,segs)
def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
hull=[controls[i] for i in (1,2,4,3)]
for q in segs[1]['bern']:
    signs=[cross(hull[i],hull[(i+1)%4],q) for i in range(4)]
    assert all(v>=0 for v in signs) or all(v<=0 for v in signs)
lines=['% Fig3.5: cubic strong convex hull, active P1..P4 on [u4,u5).',
       '% Representative controls match Fig3.4; clamped uniform thirds.',
       '% Exact Cox-de Boor geometry; no tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines += [r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5);',
          r'\draw[dashed,book grid] (P1)--(P3) (P2)--(P4);']
for j,seg in enumerate(segs): lines.append(cubic_path(seg,'dashed' if j==1 else ''))
for seg in segs[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
lines += [r'\foreach \i in {0,...,5} \node[book point] at (P\i) {};',
          r'\node at (6,1) {$u\in[u_4,u_5)$};']
for i,pos in enumerate(['below left','above left','above right','below left','below right','above']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/cubic-hull-check.json').write_text(json.dumps({'figure':'3.5',
    'knots':list(map(str,knots)),'representative_controls':[[str(v) for v in p] for p in controls],
    'exact_deboor_comparisons':count,'active_indices':[1,2,3,4],
    'selected_bezier_controls_inside_quadrilateral':True},indent=2)+'\n')
print(f'PASS: {count} exact curve checks and selected cubic hull containment.')
