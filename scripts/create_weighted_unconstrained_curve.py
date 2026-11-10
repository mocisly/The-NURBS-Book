"""9.39: same unconstrained fit as9.38, with only point weights4..7raised to100."""
from pathlib import Path
from fractions import Fraction as F
import json
from weighted_constrained_curve_data import Q,PARAMS,COUNT,U,fit
from native_bspline import point,cubic_path
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_47.tex')['applied']
baseline=json.loads((root/'image_tex/build/unconstrained-least-squares-curve-check.json').read_text(encoding='utf-8'))
assert baseline['representative_data']==[list(map(str,q)) for q in Q] and baseline['knots']==list(map(str,U))
P,ss,proof=fit({k:100 for k in range(4,8)});assert P[0]!=Q[0] and P[-1]!=Q[-1]
before=sum(F(baseline['fit']['point_squared_residuals'][i]) for i in range(4,8));after=sum(F(proof['point_squared_residuals'][i]) for i in range(4,8));assert after<before
out=['% Same21data,10controls,parameters/knotsas9.38;ONLYw4..w7change1to100.',r'\begin{tikzpicture}[book line,x=2.6cm,y=2.6cm]',r'\path[use as bounding box] (-.8,-1.7) rectangle (8.6,4.6);',r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
out.extend(cubic_path(s) for s in ss);out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in Q)
out.extend([r'\node at (2.4,4.05) {$w_4^q=\cdots=w_7^q=100$};',r'\end{tikzpicture}'])
(root/'image_tex/ch09/fig_9_47.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/weighted-unconstrained-curve-check.json').write_text(json.dumps(dict(figure='9.39',same_data_parameters_knots_control_count_as='9.38',data_count=len(Q),control_count=COUNT,fit=proof,selected_indices=[4,5,6,7],selected_group_unweighted_squared_error_before=float(before),selected_group_unweighted_squared_error_after=float(after),selected_group_error_strictly_reduced=True,both_endpoint_residuals_exactly_nonzero=True,common_coordinate_scale_cm='13/5'),indent=2)+'\n')
print('PASS9.39:exactweightedLSgradient/C2native,ONLY4weightschanged;selectedgroupSSE',float(before),'->',float(after),';freeendpointresiduals',proof['endpoint_residual_lengths'])
