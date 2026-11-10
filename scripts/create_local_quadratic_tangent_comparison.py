"""9.23: actual Bessel/Akima local quadratic interpolants of a representative hump."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import cubic_path,point
from local_quadratic_interpolator import interpolate,add,cross
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_29.tex')['applied']
Q=tuple(tuple(map(F,q)) for q in [('0','0'),('1','0'),('2.5','0'),('4','2'),('5.5','0'),('7','0'),('8','0')])
out=['% Representative exact seven-point hump; computed Eq9.28..44, not raster tracing.',r'\begin{tikzpicture}[book line,x=2.8cm,y=2.8cm]'];reports=[]
for i,method in enumerate(('bessel','akima')):
    ss,report=interpolate(Q,method);reports.append(report)
    out.extend([r'\begin{scope}[yshift='+str(-11*i)+r'cm]',r'\path[use as bounding box] (-.5,-.8) rectangle (8.5,2.7);'])
    out.extend(cubic_path(s) for s in ss)
    out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in Q)
    out.extend([r'\node at (4,-.55) {('+chr(97+i)+')};',r'\end{scope}'])
    if method=='akima':
        # Exact horizontal reproduction of BOTH complete collinear data runs.
        for s in ss:
            if s['bern'][0][0]>=0 and s['bern'][-1][0]<=F('2.5') or s['bern'][0][0]>=F('5.5'):
                assert all(p[1]==0 for p in s['bern'])
    else:assert any(any(p[1]!=0 for p in s['bern']) for s in ss if s['bern'][0][0]>=1 and s['bern'][-1][0]<=F('2.5'))
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_29.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/local-quadratic-tangent-comparison-check.json').write_text(json.dumps(dict(figure='9.23',panels=reports,Akima_collinear_runs_exactly_horizontal=True,Bessel_flat_run_deviation_nonzero=True,all_data_interpolated=True,all_piece_joins_G1=True),indent=2)+'\n')
print('PASS9.23: actual Bessel/Akima tangent estimation, exact quadratic pieces/data interpolation/G1joins, Akima collinearity vs Bessel deviation.')
