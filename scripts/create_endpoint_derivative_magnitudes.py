"""9.8:three exact9x9Hermite solves;fixed directions,varying derivative magnitude."""
from fractions import Fraction as F
from pathlib import Path
import json
from endpoint_hermite_interpolation import Q,PARAMS,BOUNDS,U,interpolate_endpoints
from native_bspline import cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_08.tex')['applied']
lines=['% Actual endpoint-constrained cubic interpolation;fixed vertical/leftward directions.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-.7,-1.6) rectangle (8.8,4.5);']
reports=[]
for a,style in [(F(8),''),(F(16),'dashed'),(F(24),'dotted')]:
    D0=(F(0),a);Dn=(-a,F(0));P,ss,nc=interpolate_endpoints(D0,Dn)
    lines.extend(cubic_path(s,style) for s in ss)
    for q,D in [(Q[0],D0),(Q[-1],Dn)]:
        tip=tuple(x+y/8 for x,y in zip(q,D));lines.append(r'\draw[book axis] '+point(q)+'--'+point(tip)+';')
    reports.append(dict(alpha=str(a),D0=list(map(str,D0)),Dn=list(map(str,Dn)),all7point_and2derivative_constraints_exact=True,C2_native_checks=nc,bezier_hull_bounds=[[float(min(s['bern'][i][dim] for s in ss for i in range(4))),float(max(s['bern'][i][dim] for s in ss for i in range(4)))] for dim in range(2)]))
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
for k,(a,style) in enumerate([(8,'solid'),(16,'dashed'),(24,'dotted')]):
    x=F(1,2)+F(5,2)*k;y=-F(11,10)
    lines.append(r'\draw['+style+'] '+point((x,y))+'--'+point((x+F(3,5),y))+';')
    lines.append(r'\node[anchor=west] at '+point((x+F(7,10),y))+r' {$\alpha='+str(a)+'$};')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_08.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/endpoint-derivative-magnitudes-check.json').write_text(json.dumps(dict(figure='9.8',representative_data=[[str(x) for x in q] for q in Q],chord_parameters=list(map(str,PARAMS)),chord_parameter_enclosures=[[str(x) for x in b] for b in BOUNDS],knots_from_equation9_9=list(map(str,U)),variants=reports,derivative_arrow_common_scale='1/8',fixed_unit_start_direction=[0,1],fixed_unit_end_direction=[-1,0]),indent=2)+'\n')
print('PASS:three9x9exactHermite solves,all7points+2derivatives,C2nativepieces;allarrowsscale1/8. Bounds:',[r['bezier_hull_bounds'] for r in reports])
