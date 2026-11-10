"""Fig5.24: three sequentially extracted degree4 Bezier control polygons."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point
from native_polynomial_drawing import paths
from knot51_data import insert

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (30,31)]
assert not any(p.exists() for p in targets)
U=(F(0),)*5+(F(1,3),F(2,3))+(F(1),)*5
P=tuple(tuple(F(str(t)) for t in pt) for pt in [(0,0),(3,0),(2.5,4),(5.7,6),(8.5,4),(7.7,0),(11,0)])
ss=segments(U,P,4);checks=check(U,P,4,ss)
K,R=U,P
for t in (F(1,3),F(2,3)):
    for r in range(3):K,R,_=insert(K,R,4,t)
assert len(R)==13 and R==ss[0]['bern']+ss[1]['bern'][1:]+ss[2]['bern'][1:]
for a,b in zip(ss,segments(K,R,4)):assert a['power']==b['power']
checks+=check(K,R,4,segments(K,R,4))
curves,proof=paths(ss);panels=[]
for i,s in enumerate(ss):
    lines=[r'\draw[book grid] '+'--'.join(map(point,P))+';']+curves
    lines += [r'\draw[book grid] '+'--'.join(map(point,s['bern']))+';']
    for pt in P:lines.append(r'\draw '+point(pt)+' circle[radius=1.6pt];')
    for pt in s['bern']:lines.append(r'\fill '+point(pt)+' circle[radius=1.7pt];')
    lines.append(r'\node at (5.5,-.85) {('+chr(97+i)+')};');panels.append(lines)
for index,target in enumerate(targets):
    lines=['% Fig5.24: same representative7-control quartic and three actual Bezier pieces.',
           '% Each view highlights ONLY the current segment controls; complete curve stays fixed.',
           '% Exact U=0five,1/3,2/3,1five. Mathematical native approximation certified<=0.0001cm.',
           r'\begin{tikzpicture}[book line]',
           r'\path[use as bounding box] (-.6,-1.4) rectangle ('+('11.6' if index==0 else '24.6')+',6.8);']
    for panel,shift in ([(0,0)] if index==0 else [(1,0),(2,13)]):
        lines+=[r'\begin{scope}[xshift='+str(shift)+'cm]']+panels[panel]+[r'\end{scope}']
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/on-the-fly-quartic-check.json').write_text(json.dumps({
    'figure':'5.24','degree':4,'U':list(map(str,U)),
    'representative_seven_controls':[[str(t) for t in pt] for pt in P],
    'three_actual_extracted_control_sets':[[list(map(str,pt)) for pt in s['bern']] for s in ss],
    'independent_inserted_thirteen_controls_equal_concatenated_three_bezier_nets':True,
    'all_original_polynomial_spans_identical':True,'native_curve_checks':checks,
    'only_current_control_polygon_highlighted_per_view':True,'analytic_native_rendering':proof},indent=2)+'\n')
print('PASS:246 exact quartic checks;13 inserted controls equal three5-point Bezier nets with shared endpoints. Native bound='+proof['maximum_certified_L1_error_cm'])
