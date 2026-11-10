"""9.6:quadratic,cubic,quartic interpolation with fixed chord-length parameters."""
from fractions import Fraction as F
from pathlib import Path
import json
from global_interpolation_data import interpolate
from irregular_interpolation_data import Q,PARAMS
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import approximate
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_06.tex')['applied']
lines=['% Same representative data as9.5;true degree2,3,4 interpolation solves.',
       '% Quartic rendered as mathematically certified native cubic subpieces,error<1e-5 coordinate units.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',
       r'\path[use as bounding box] (-1,-3.6) rectangle (8,3.2);']
reports=[]
for k,(p,style) in enumerate([(2,''),(3,'dashed'),(4,'dash dot')]):
    U,P=interpolate(Q,PARAMS,p);ss=segments(U,P,p);nc=check(U,P,p,ss)
    assert all(de_boor(U,P,p,t)==q for t,q in zip(PARAMS,Q))
    paths=[]
    for s in ss:
        paths.extend(approximate(tuple(q+(F(1),) for q in s['bern']),F(1,100000))) if p==4 else paths.append(s)
    lines.extend(cubic_path(s,style) for s in paths)
    reports.append(dict(degree=p,parameters=list(map(str,PARAMS)),knots=list(map(str,U)),all7interpolation_constraints_exact=True,native_geometry_and_continuity_checks=nc,native_path_count=len(paths),certified_quartic_L1_error_bound=str(max(x['certified_l1_error'] for x in paths)) if p==4 else '0'))
    y=-F(13,10)-F(9,10)*k
    lines.append(r'\draw[book grid] '+point((-F(1,5),y))+'--'+point((F(349,50),y))+';')
    for t in U[p+1:-p-1]:
        x=F(339,50)*t;lines.append(r'\draw[book grid] '+point((x,y-F(3,25)))+'--'+point((x,y+F(3,25)))+';')
    for end in (F(0),F(1)):
        for j in range(p+1):
            x=F(339,50)*end+F(3,50)*(F(j)-F(p,2));lines.append(r'\draw[book grid] '+point((x,y-F(3,25)))+'--'+point((x,y+F(3,25)))+';')
    for t in PARAMS:lines.append(r'\draw '+point((F(339,50)*t,y))+r' circle[radius=2pt];')
    lines.append(r'\draw['+(style or 'solid')+'] '+point((F(1,5),y-F(3,10)))+'--'+point((F(4,5),y-F(3,10)))+';')
    lines.append(r'\node[anchor=west] at '+point((F(9,10),y-F(3,10)))+r' {$p='+str(p)+'$};')
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_06.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/interpolation-degree-comparison-check.json').write_text(json.dumps(dict(figure='9.6',same_representative_data_as='9.5',methods=reports,all_rulers_use_same_chord_parameters_and_degree_specific_average_knots=True),indent=2)+'\n')
print('PASS:degree2/3/4 exact solves for same data and chord parameters;C1/C2/C3 native checks;quartic cubic rendering certified<1e-5.')
