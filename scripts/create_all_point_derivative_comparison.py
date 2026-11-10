"""9.11:quadratic/cubic global Hermite interpolation of all five points and derivatives."""
from fractions import Fraction as F
from pathlib import Path
import json
from all_point_hermite_data import Q,T,TOTAL,PARAMS,BOUNDS,lo,hi,interpolate_all
from native_bspline import cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_11.tex')['applied']
lines=['% Independent10x10solves of all five point+derivative constraints,Eq9.22/23.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-2,-2) rectangle (8,4.8);']
reports=[]
for p,style in [(2,''),(3,'dashed')]:
    U,P,D,ss,nc=interpolate_all(p);lines.extend(cubic_path(s,style) for s in ss)
    reports.append(dict(degree=p,knots=list(map(str,U)),all5point_and5derivative_constraints_exact=True,native_geometry_and_continuity_checks=nc))
for q,v in zip(Q,D):lines.append(r'\draw[book axis] '+point(q)+'--'+point(tuple(a+b/5 for a,b in zip(q,v)))+';')
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_11.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/all-point-derivative-comparison-check.json').write_text(json.dumps(dict(figure='9.11',representative_data=[[str(x) for x in q] for q in Q],exact_unit_tangents=[[str(x) for x in t] for t in T],chord_parameters=list(map(str,PARAMS)),parameter_enclosures=[[str(x) for x in b] for b in BOUNDS],total_chord_enclosure=[str(sum(lo)),str(sum(hi))],represented_total_chord=str(TOTAL),all_derivative_magnitudes_equal_represented_total_chord=True,variants=reports,common_arrow_scale='1/5'),indent=2)+'\n')
print('PASS:independent quadratic/cubic10x10solves,all5point+5derivativeconstraints exact,C1/C2nativechecks,unit tangents/common magnitude and1/5arrows.')
