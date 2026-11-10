"""9.51: actual error-controlled cubic with exact protected apex corner."""
from pathlib import Path
from fractions import Fraction as F
import json
from bounded_corner_profile_data import Q,CORNER
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_59.tex')['applied']
r=json.loads((root/'image_tex/build/bounded-corner-profile-data.json').read_text())
U=tuple(map(F,r['knots']));P=tuple(tuple(map(F,p)) for p in r['controls']);params=tuple(map(F,r['parameters']))
ss=segments(U,P,3);native=check(U,P,3,ss,steps=9)
squares=tuple(sum((x-y)**2 for x,y in zip(q,de_boor(U,P,3,t))) for q,t in zip(Q,params))
assert max(squares)<=F(8,100)**2 and squares[CORNER]==0 and U.count(params[CORNER])==3
left=next(s for s in ss if s['b']==params[CORNER]);right=next(s for s in ss if s['a']==params[CORNER])
a=tuple(left['bern'][-1][d]-left['bern'][-2][d] for d in range(2));b=tuple(right['bern'][1][d]-right['bern'][0][d] for d in range(2));det=a[0]*b[1]-a[1]*b[0];assert det!=0
out=['% Actual85point bounded cubic,explicit apex interpolation constraint and retained triple knot;no tracing.',r'\begin{tikzpicture}[book line,x=2.4cm,y=2.4cm]',r'\path[use as bounding box] (-.6,-1.4) rectangle (11.5,6.2);']
out.extend(cubic_path(s) for s in ss)
for i,q in enumerate(Q):
    if i!=CORNER:out.append(r'\draw '+point(q)+r' circle[radius=2pt];')
out.extend([r'\draw '+point(Q[CORNER])+r' ++(-2.8pt,-2.8pt) rectangle ++(5.6pt,5.6pt);',r'\node (apex) at (6.4,5.8) {$\mathbf Q_{'+str(CORNER)+r'}$};',r'\draw[book grid,shorten >=4pt] (apex)--'+point(Q[CORNER])+';',r'\end{tikzpicture}'])
(root/'image_tex/ch09/fig_9_59.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_cubic_checks=native,all85datum_errors_certified_below_008=True,actual_maximum_Euclidean_same_parameter_error=float(max(squares))**.5,corner_interpolation_exact=True,corner_one_sided_tangents_nonparallel_exact=True,corner_tangent_determinant=str(det),native_coordinate_scale='2.4cm',font_rescaling=False)
(root/'image_tex/build/bounded-corner-profile-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print('PASS9.51native:',native,'exact checks;maxEuclidean',r['actual_maximum_Euclidean_same_parameter_error'],'<=.08;apex exact andnonparallelone-sidedtangents.')
