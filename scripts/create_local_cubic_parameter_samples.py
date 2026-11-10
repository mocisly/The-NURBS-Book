"""9.30: exact Renner cubic with actual equal-parameter samples on a winding curve."""
from pathlib import Path
from fractions import Fraction as F
import json
from renner_exact_geometry import construct
from local_quadratic_interpolator import dot,add
from native_bspline import de_boor,cubic_path,point
from bspline_math import derivative,evaluate
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_36.tex')['applied']
T=tuple(tuple(map(F,t)) for t in [('-3/5','4/5'),('3/5','4/5'),('3/5','-4/5'),('3/5','-4/5'),('12/13','5/13'),('3/5','4/5'),('-12/13','5/13')])
MID=tuple(tuple(map(F,t)) for t in [('3/5','4/5'),('1','0'),('-3/5','-4/5'),('1','0'),('12/13','5/13'),('-3/5','4/5')])
ALPHA=tuple(map(F,['2','3','2','3/2','4','2']))
Q,params,U,P,ss,proof=construct(T,MID,ALPHA)
samples=tuple(de_boor(U,P,3,F(j,58)) for j in range(59))
assert all(u*58==int(u*58) for u in params)
assert all(samples[int(u*58)]==q for u,q in zip(params,Q))
witness=[]
for s in ss:
    u=(3*s['a']+s['b'])/4;D=tuple(evaluate(derivative(c),u) for c in s['power']);witness.append(dot(D,D))
assert any(v!=sum(ALPHA)**2 for v in witness)
dist2=[dot(add(a,b,-1),add(a,b,-1)) for a,b in zip(samples,samples[1:])];assert min(dist2)>0
out=['% Chosen exact unit directions produce six true Renner cubics;uniform samplesu=j/58.',r'\begin{tikzpicture}[book line,x=2.8cm,y=2.8cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (8.8,3.9);']
out.extend(cubic_path(s) for s in ss)
for q in samples:
    xy=point(q);out.extend([r'\draw '+xy+r' ++(-1.8pt,0)--++(3.6pt,0);',r'\draw '+xy+r' ++(0,-1.8pt)--++(0,3.6pt);'])
out.extend(r'\draw '+point(q)+r' circle[radius=2.7pt];' for q in Q)
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_36.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/local-cubic-parameter-samples-check.json').write_text(json.dumps(dict(figure='9.30',representative_data=[list(map(str,q)) for q in Q],unit_tangents=[list(map(str,q)) for q in T],chosen_midpoint_unit_directions=[list(map(str,q)) for q in MID],local_alpha=list(map(str,ALPHA)),parameters=list(map(str,params)),construction=proof,uniform_parameter_samples=59,sample_parameters=[str(F(j,58)) for j in range(59)],sample_points=[list(map(str,q)) for q in samples],all7data_on_sample_grid_exact=True,quarter_interval_speed_squared_witnesses=list(map(str,witness)),sampling_is_uniform_parameter_not_exact_arc_length=True,maximum_over_minimum_adjacent_chord_length=float(max(dist2)/min(dist2))**.5),indent=2)+'\n')
print('PASS9.30:6exact Renner cubics,7interpolated data,5zero-error removals,C1andendpoint/midpoint speed29/2exact;59actual uniform-u samples;chord spacing ratio',float(max(dist2)/min(dist2))**.5)
