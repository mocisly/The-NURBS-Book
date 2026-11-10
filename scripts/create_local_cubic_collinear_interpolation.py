"""9.31: same13points as9.7, actual local cubic preserves every collinear run."""
from pathlib import Path
from fractions import Fraction as F
import json
from renner_interpolation import interpolate
from native_bspline import cubic_path,point
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_37.tex')['applied']
prior=json.loads((root/'image_tex/build/collinear-data-interpolation-check.json').read_text(encoding='utf-8'))
Q=tuple(tuple(map(F,q)) for q in prior['representative_data']);assert len(Q)==13
source=(root/'image_tex/ch09/fig_9_07.tex').read_text(encoding='utf-8')
assert all(r'\draw '+point(q)+r' circle' in source for q in Q)
U,P,ss,params,proof=interpolate(Q)
for ids,dim,value in [(range(3),0,F(0)),(range(6,8),0,F(3)),(range(9,12),1,-F(3,5))]:
    for i in ids:assert all(q[dim]==value for q in ss[i]['bern'])
out=['% Actual local cubic on EXACT SAME13data as globally solved9.7;collinear spans verified coefficientwise.',r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-.9,-3.7) rectangle (8,2.6);']
out.extend(cubic_path(s) for s in ss)
out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in Q)
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_37.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/local-cubic-collinear-interpolation-check.json').write_text(json.dumps(dict(figure='9.31',same_data_as_9_7_exact=True,data=[list(map(str,q)) for q in Q],parameters=list(map(str,params)),knots=list(map(str,U)),construction=proof,straight_spans_checked_coefficientwise={'left_x_zero':[0,1,2],'middle_x_three':[6,7],'right_y_minus_three_fifths':[9,10,11]},common_geometry_scale_as_9_7='5/2cm'),indent=2)+'\n')
print('PASS9.31:same13data as9.7,actual Akima/Renner cubics,certified positive roots,exact13interpolations/C1joins/knotremovals;all8collinear intervals coefficientwise straight.')
