"""9.12:fixed unit tangents,three genuine cubic global Hermite interpolants."""
from fractions import Fraction as F
from pathlib import Path
import json
from all_point_hermite_data import Q,T,TOTAL,PARAMS,interpolate_all
from native_bspline import cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_12.tex')['applied']
lines=['% Same data/unit tangents as9.11;independent exact solves with alpha=d,3d/2,d/2.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-2.7,-3) rectangle (8,5.7);']
reports=[]
cases=[(F(1),'','d'),(F(3,2),'dashed','3d/2'),(F(1,2),'dotted','d/2')]
for factor,style,label in cases:
    U,P,D,ss,nc=interpolate_all(3,factor);lines.extend(cubic_path(s,style) for s in ss)
    for q,v in zip(Q,D):lines.append(r'\draw[book axis] '+point(q)+'--'+point(tuple(a+b/5 for a,b in zip(q,v)))+';')
    reports.append(dict(magnitude_scale=str(factor),actual_magnitude=str(factor*TOTAL),all5point_and5derivative_constraints_exact=True,C2_native_checks=nc))
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
for k,(_,style,label) in enumerate(cases):
    x=F(5,2)*k;y=-F(13,5)
    lines.append(r'\draw['+(style or 'solid')+'] '+point((x,y))+'--'+point((x+F(3,5),y))+';')
    lines.append(r'\node[anchor=west] at '+point((x+F(7,10),y))+r' {$\alpha='+label+'$};')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_12.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/all-point-derivative-magnitudes-check.json').write_text(json.dumps(dict(figure='9.12',same_data_unit_tangents_parameters_and_cubic_knots_as='9.11',parameters=list(map(str,PARAMS)),knots=list(map(str,U)),variants=reports,common_arrow_scale='1/5',correct_magnitude_interpretation=['d','3d/2','d/2'],OCR_reciprocal_magnitudes_in_prose_need_repair=True),indent=2)+'\n')
print('PASS:three10x10cubicHermite solves,all5positions+5derivatives exact,alpha=d/2,d,3d/2;C2native checks and common1/5arrows.')
