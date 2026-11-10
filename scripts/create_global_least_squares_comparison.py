"""9.37: actual7/9/11control least-squares fits, common data and true parameter rulers."""
from pathlib import Path
from fractions import Fraction as F
import json
from least_squares_curve_data import Q,PARAMS,BOUNDS,fit
from native_bspline import cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (44,45):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex')['applied']
reports=[];panels=[]
for idx,count in enumerate((7,9,11)):
    U,P,ss,report=fit(count);reports.append(report)
    out=[r'\begin{scope}[xshift='+str(18 if idx==2 else 0)+r'cm]',r'\path[use as bounding box] (-.7,-1.7) rectangle (7.9,5.5);',r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
    out.extend(cubic_path(s) for s in ss)
    out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in Q)
    y=-F(4,5);out.append(r'\draw[book grid] (0,-.8)--(7,-.8);')
    for t in U[4:-4]:
        x=7*t;out.append(r'\draw[book grid] '+point((x,y-F(7,100)))+'--'+point((x,y+F(7,100)))+';')
    for t in (F(0),F(1)):
        for j in range(4):
            x=7*t+F(1,25)*(F(j)-F(3,2));out.append(r'\draw[book grid] '+point((x,y-F(7,100)))+'--'+point((x,y+F(7,100)))+';')
    for t in PARAMS:out.append(r'\draw '+point((7*t,y))+r' circle[radius=1.6pt];')
    out.extend([r'\node at (3.5,-1.35) {('+chr(97+idx)+')};',r'\end{scope}']);panels.append(out)
    report['control_hull_bounds']=[[float(min(p[i] for p in P)),float(max(p[i] for p in P))] for i in range(2)]
    assert all(-F(7,10)<p[0]<F(79,10) and -F(4,5)<p[1]<F(11,2) for p in P),report['control_hull_bounds']
assert reports[0]['sum_squared_residual_decimal']>reports[1]['sum_squared_residual_decimal']>reports[2]['sum_squared_residual_decimal']
header=['% Actual endpoint-constrained cubic least-squares fits on18chosen data,7/9/11controls;Eq9.68/69knots.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm]']
for n,body in [(44,panels[0]),(45,panels[1]+panels[2])]:
    (root/f'image_tex/ch09/fig_9_{n:02}.tex').write_text('\n'.join(header+body+[r'\end{tikzpicture}'])+'\n',encoding='utf-8')
(root/'image_tex/build/global-least-squares-comparison-check.json').write_text(json.dumps(dict(figure='9.37',representative_data=[list(map(str,q)) for q in Q],data_count=len(Q),common_chord_parameters=list(map(str,PARAMS)),chord_parameter_enclosures=[list(map(str,b)) for b in BOUNDS],parameter_enclosure_width_less_than='1e-11',variants=reports,three_same_parameter_squared_errors_strictly_decrease=True,actual_data_parameter_circles_and_knot_ticks=True,common_coordinate_scale_cm='2'),indent=2)+'\n')
print('PASS9.37:3actual endpoint-constrained least-squares solves,exact zero gradients/positiveLDLpivots/C2native curves,Eq9.68/69knots;SSE:',[r['sum_squared_residual_decimal'] for r in reports])
