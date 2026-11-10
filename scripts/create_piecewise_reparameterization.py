"""6.11: four given scalar splines, computed control polygons and exact mapping insets."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from polynomial_reparameterization import reparameterize
from bspline_math import derivative,evaluate

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for path in ('ch06/fig_6_11.tex','ch06/fig_6_12.tex'):
    assert not next(e for e in data['images'] if e['tex']=='image_tex/'+path)['applied']
U=(F(0),)*4+(F(1,2),)+(F(1),)*4
P=((F(1),F(0)),(F(0),F(3)),(F(4),F(6)),(F(5),-F(2)),(F(10),F(0)))
cases=[
    ('a',(F(0),F(2,5),F(1)),(F(0),)*3+(F(1),)*3,2,11,r'F=\{0,\frac25,1\}'),
    ('b',(F(0),F(2,5),F(9,10),F(1)),(F(0),)*3+(F(1,2),)+(F(1),)*3,2,16,r'F=\{0,\frac25,\frac9{10},1\}'),
    ('c',(F(0),F(1,2),F(7,10),F(9,10),F(1)),(F(0),)*3+(F(1,2),)*2+(F(1),)*3,2,17,r'F=\{0,\frac12,\frac7{10},\frac9{10},1\}'),
    ('d',(F(0),F(1)),(F(0),)*2+(F(1),)*2,1,5,r'F=\{0,1\}')]
ss=segments(U,P,3);source_checks=check(U,P,3,ss);panels=[];reports=[]
for letter,Fc,S,q,expected,formula in cases:
    K,Q,degree,proof=reparameterize(U,P,3,S,Fc,q);assert len(Q)==expected
    fsegs=segments(S,tuple((x,) for x in Fc),q)
    map_checks=check(S,tuple((x,) for x in Fc),q,fsegs)
    if letter=='d':assert Q==P and K==U
    if letter=='c':
        assert evaluate(derivative(fsegs[0]['power'][0]),F(1,2))==evaluate(derivative(fsegs[1]['power'][0]),F(1,2))==F(4,5)
        proof['retained_given_double_mapping_knot_despite_accidental_C1']=True
    lines=[]
    if letter!='d':lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';')
    lines.append(r'\draw[book grid] '+'--'.join(map(point,Q))+';')
    lines.extend(cubic_path(s) for s in ss)
    for pt in Q:lines.append(r'\draw '+point(pt)+r' circle[radius=1.5pt];')
    lines += [r'\begin{scope}[xshift=7cm,yshift=3.1cm,x=3cm,y=2.6cm]',
              r'\draw[book axis] (0,0)--(1.12,0) node[right=3pt] {$s$};',
              r'\draw[book axis] (0,0)--(0,1.12) node[above=3pt] {$u$};',
              r'\node[below left=3pt] at (0,0) {$0$};',
              r'\draw[book grid] (1,-.025)--(1,.025) node[below=4pt] {$1$};',
              r'\draw[book grid] (-.025,1)--(.025,1) node[left=4pt] {$1$};']
    if F(1,2) in S:
        lines += [r'\draw[book grid] (.5,-.025)--(.5,.025) node[below=4pt] {$\frac12$};']
    for seg in fsegs:
        # Preserve graph coordinates(s,f(s)), not the one-dimensional ordinates.
        from polynomial_native import bernstein
        graph={'bern':bernstein(((F(0),F(1)),seg['power'][0]),seg['a'],seg['b'])}
        lines.append(cubic_path(graph))
    lines += [r'\node[right=4pt] at (1,1) {$f(s)$};',r'\end{scope}',
              r'\node at (5,-2.7) {('+letter+')};',
              r'\node at (5,-3.5) {$'+formula+'$};']
    panels.append(lines);proof.update({'panel':letter,'F':list(map(str,Fc)),'S':list(map(str,S)),
                                     'degree':degree,'mapping_native_checks':map_checks,
                                     'output_knots':list(map(str,K)),
                                     'output_controls':[[str(x) for x in p] for p in Q]})
    reports.append(proof);print(f'Panel{letter}:degree{degree},{len(Q)}controls,whole composition error<{float(F(proof["certified_whole_parameter_L1_composition_error_bound"])):.3g}.',flush=True)
for group,name in [(panels[:2],'fig_6_11.tex'),(panels[2:],'fig_6_12.tex')]:
    lines=['% Figure6.11 representative cubic controls documented in companion generator.',
           '% Given scalar mappings used exactly; inverse-knot rounding is globally certified <1e-24.',
           '% Native displayed control coordinates rounded to10decimal places (<1e-9cm display error).',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.6,-4.05) rectangle (24.5,7);']
    for j,panel in enumerate(group):
        lines.append(r'\begin{scope}[xshift='+str(13*j)+'cm]');lines.extend(panel);lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');(root/'image_tex/ch06'/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/piecewise-reparameterization-check.json').write_text(json.dumps({
    'figure':'6.11','representative_source_controls':[[str(x) for x in pt] for pt in P],
    'source_knots':list(map(str,U)),'source_native_checks':source_checks,'panels':reports},indent=2)+'\n')
print('PASS:all four exact prescribed mappings; four certified computed control nets; no raster geometry.')
