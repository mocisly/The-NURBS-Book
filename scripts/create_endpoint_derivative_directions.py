"""9.9:independently solve three endpoint-direction variants for9.8's same data."""
from fractions import Fraction as F
from pathlib import Path
import json
from endpoint_hermite_interpolation import Q,PARAMS,U,interpolate_endpoints
from native_bspline import cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_09.tex')['applied']
cases=[('A',(-12,12),(-12,-12),''),('B',(0,16),(-16,0),'dashed'),('C',(12,12),(-12,12),'dotted')]
lines=['% Same seven representative data/parameters/knots as9.8;three exact Hermite solves.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-1.9,-1.6) rectangle (8.8,5.5);']
reports=[]
for name,D0,Dn,style in cases:
    D0=tuple(map(F,D0));Dn=tuple(map(F,Dn));P,ss,nc=interpolate_endpoints(D0,Dn)
    lines.extend(cubic_path(s,style) for s in ss)
    for q,D in [(Q[0],D0),(Q[-1],Dn)]:
        tip=tuple(x+y/8 for x,y in zip(q,D));lines.append(r'\draw[book axis'+(','+style if style else '')+'] '+point(q)+'--'+point(tip)+';')
    reports.append(dict(variant=name,D0=list(map(str,D0)),Dn=list(map(str,Dn)),all7point_and2derivative_constraints_exact=True,C2_native_checks=nc,bezier_hull_bounds=[[float(min(s['bern'][i][dim] for s in ss for i in range(4))),float(max(s['bern'][i][dim] for s in ss for i in range(4)))] for dim in range(2)]))
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
for k,(name,_,__,style) in enumerate(cases):
    x=F(1,2)+F(5,2)*k;y=-F(11,10)
    lines.append(r'\draw['+(style or 'solid')+'] '+point((x,y))+'--'+point((x+F(3,5),y))+';')
    lines.append(r'\node[anchor=west] at '+point((x+F(7,10),y))+' {'+name+'};')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_09.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/endpoint-derivative-directions-check.json').write_text(json.dumps(dict(figure='9.9',same_representative_data_parameters_and_knots_as='9.8',parameters=list(map(str,PARAMS)),knots=list(map(str,U)),variants=reports,derivative_arrow_common_scale='1/8',arrow_styles_match_curves=True),indent=2)+'\n')
print('PASS:three9x9Hermite solves,same7points,different exact endpoint directions;C2checks;arrow styles and1/8scale. Bounds:',[r['bezier_hull_bounds'] for r in reports])
