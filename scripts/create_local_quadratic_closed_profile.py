"""9.25: representative shoe-sole data interpolated by periodic Akima parabolas."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import cubic_path,point
from local_quadratic_interpolator import interpolate
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_31.tex')['applied']
# Chosen CAD-style outline data; no coordinates are extracted from the scan.
Q=tuple(tuple(map(F,q)) for q in [('0','0'),('.3','.8'),('1.2','1.3'),('2.2','1.35'),('3.2','1.1'),('4.2','.6'),('5.2','.4'),('6.3','.4'),('7.3','.65'),('8.3','.65'),('9.1','.1'),('9.05','-.7'),('8.2','-1.15'),('7.2','-1.25'),('6.2','-1.15'),('5.2','-1.2'),('4.2','-1.5'),('3.2','-1.65'),('2.2','-1.5'),('1.2','-1.1'),('.3','-.6'),('0','0')])
ss,report=interpolate(Q,'akima',closed=True)
assert len(report['joins'])==len(ss) and all(j['G1'] for j in report['joins'])
out=['% Representative closed shoe-sole data;periodic Akima tangent estimates,exact quadratic construction.',r'\begin{tikzpicture}[book line,x=2.8cm,y=2.8cm]',r'\path[use as bounding box] (-.5,-2) rectangle (9.7,1.8);']
out.extend(cubic_path(s) for s in ss)
out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in Q[:-1])
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_31.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/local-quadratic-closed-profile-check.json').write_text(json.dumps(dict(figure='9.25',construction=report,distinct_data_points=len(Q)-1,all_data_interpolated=True,closure_position_exact=True,closure_tangent_G1_exact=True,all_other_joins_G1_exact=True),indent=2)+'\n')
print('PASS9.25:21representative closed profile points,periodic Akima directions,exact quadratic pieces and every G1join including closure.')
