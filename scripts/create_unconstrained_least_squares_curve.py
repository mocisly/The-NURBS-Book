"""9.38: actual unconstrained fit, including both free endpoint controls."""
from pathlib import Path
import json
from weighted_constrained_curve_data import Q,PARAMS,BOUNDS,COUNT,U,fit
from native_bspline import cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_46.tex')['applied']
P,ss,proof=fit();assert P[0]!=Q[0] and P[-1]!=Q[-1]
out=['% Actual unweighted unconstrained LSfit on21chosen data;all10controls includingendpoints solved.',r'\begin{tikzpicture}[book line,x=2.6cm,y=2.6cm]',r'\path[use as bounding box] (-.8,-1.7) rectangle (8.6,4.6);',r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
out.extend(cubic_path(s) for s in ss);out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in Q);out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_46.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/unconstrained-least-squares-curve-check.json').write_text(json.dumps(dict(figure='9.38',representative_data=[list(map(str,q)) for q in Q],data_count=len(Q),control_count=COUNT,common_parameters=list(map(str,PARAMS)),chord_parameter_enclosures=[list(map(str,b)) for b in BOUNDS],knots=list(map(str,U)),fit=proof,both_endpoint_residuals_exactly_nonzero=True,all_weights_one=True),indent=2)+'\n')
print('PASS9.38:unconstrained all10control LSsolve,exact gradients/positiveLDL/C2native,both endpoint residuals nonzero:',proof['endpoint_residual_lengths'],';SSE',proof['weighted_objective_decimal'])
