"""6.13: exact knot/weight transforms and actual equal-parameter sample distributions."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,cubic_path,de_boor
from rational_geometry import project,approximate
from mobius_reparameterization import transform

root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in ('fig_6_14.tex','fig_6_15.tex'):
    assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/'+name)['applied']
U=(F(0),)*4+(F(3,10),F(7,10))+(F(1),)*4
P=((F(1),F(0)),(F(0),F(3)),(F(4),F(6)),(F(5),-F(2)),(F(10),F(0)),(F(8),F(3,2)))
cases=[('a',(2,1,3,2),(F(1),)*6,r'g(u)=\frac{2u+1}{3u+2}'),
       ('b',(2,0,3,1),(F(1),)*6,r'g(u)=\frac{2u}{3u+1}'),
       ('c',(2,-1,3,2),(F(1),F(1,2),F(2),F(3),F(1,2),F(1)),r'g(u)=\frac{2u-1}{3u+2}')]
panels=[];reports=[]
for letter,coeff,weights,formula in cases:
    H=tuple(tuple(w*x for x in pt)+(w,) for w,pt in zip(weights,P))
    K,Q,g,inverse,proof=transform(U,H,3,coeff)
    assert tuple(map(project,Q))==P
    checks=check(U,H,3,segments(U,H,3),steps=11)+check(K,Q,3,segments(K,Q,3),steps=11)
    old=[project(de_boor(U,H,3,F(i,20))) for i in range(21)]
    new=[project(de_boor(K,Q,3,K[0]+(K[-1]-K[0])*F(i,20))) for i in range(21)]
    lines=[r'\begin{scope}[x=.9cm,y=.9cm]',r'\draw[book grid] '+'--'.join(map(point,P))+';']
    for a in old:
        lines += [r'\begin{scope}[shift={'+point(a)+'}]',r'\draw[book grid] (-1.8pt,0)--(1.8pt,0) (0,-1.8pt)--(0,1.8pt);',r'\end{scope}']
    for a in new:lines.append(r'\node[rectangle,draw,line width=.35pt,inner sep=1.4pt] at '+point(a)+' {};')
    for a in P:lines.append(r'\draw '+point(a)+r' circle[radius=1.7pt];')
    lines += [r'\end{scope}',r'\begin{scope}[xshift=6.3cm,yshift=3.2cm,x=3cm,y=2.7cm]',
              r'\draw[book axis] (0,0)--(1.12,0) node[right=3pt] {$u$};',
              r'\draw[book axis] (0,'+('-.57' if letter=='c' else '0')+r')--(0,1.08) node[above=3pt] {$s$};',
              r'\node[below left=3pt] at (0,0) {$0$};',
              r'\draw[book grid] (1,-.025)--(1,.025) node[below=4pt] {$1$};',
              r'\draw[book grid] (-.025,1)--(.025,1) node[left=4pt] {$1$};']
    # The Mobius function is degree1 rational; its graph(u,g(u)) is degree2.
    # Numerator of u*mu(u) is degree2; represent it in degree2 homogeneous form.
    a,b,c,d=map(F,coeff)
    graph=((F(0),b,d),(d/2,b+a/2,d+c/2),(c+d,a+b,c+d))
    bound=F(0);count=0
    for piece in approximate(graph,F(1,100000)):
        lines.append(cubic_path(piece));bound=max(bound,piece['certified_l1_error']);count+=1
    lines += [r'\node[right=4pt] at '+point((F(1),g(F(1))))+r' {$g(u)$};',r'\end{scope}',
              r'\node at (4.8,-2.35) {('+letter+')};',r'\node at (4.8,-2.95) {$'+formula+'$};']
    panels.append(lines);proof.update({'panel':letter,'original_weights':list(map(str,weights)),
                                     'new_knots':list(map(str,K)),'new_weights':[str(row[-1]) for row in Q],
                                     'old_marker_points':[[str(x) for x in pt] for pt in old],
                                     'new_marker_points':[[str(x) for x in pt] for pt in new],
                                     'native_basis_checks':checks,'mapping_graph_native_paths':count,
                                     'mapping_graph_certified_L1_error':str(bound)})
    reports.append(proof);print(f'Panel{letter}:exact mapped knots and weights,{checks}native basis checks,101 exact projected identities.',flush=True)
for group,name in [(panels[:1],'fig_6_14.tex'),(panels[1:],'fig_6_15.tex')]:
    right='10.9' if len(group)==1 else '22.9'
    lines=['% Exact given Mobius mappings and original weights; explicit representative six controls.',
           '% Markers evaluate actual old/new NURBS on uniform grids in their OWN parameter intervals.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.6,-3.5) rectangle ('+right+',6.5);']
    for j,panel in enumerate(group):
        lines.append(r'\begin{scope}[xshift='+str(12*j)+'cm]');lines.extend(panel);lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');(root/'image_tex/ch06'/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/rational-reparameterization-check.json').write_text(json.dumps({
    'figure':'6.13','representative_control_points':[[str(x) for x in pt] for pt in P],
    'original_knots':list(map(str,U)),'parameter_grid_divisions':20,'panels':reports},indent=2)+'\n')
print('PASS:all three exact degree-preserving reparameterizations; controls unchanged, weights/knots transformed.')
