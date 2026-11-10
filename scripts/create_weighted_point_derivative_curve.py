"""9.41: preserve all8hard constraints while raising weights5and15to100."""
from fractions import Fraction as F
from pathlib import Path
import json
from weighted_constrained_curve_data import Q,fit
from constrained_curve_example_data import POINTS,DERIVATIVES
from constrained_curve_native import drawing
from native_bspline import point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_49.tex')['applied']
P,ss,proof=fit({5:100,15:100},POINTS,DERIVATIVES)
prior=json.loads((root/'image_tex/build/point-derivative-constrained-curve-check.json').read_text(encoding='utf-8'))['fit']
before=sum(F(prior['point_squared_residuals'][k]) for k in (5,15));after=sum(F(proof['point_squared_residuals'][k]) for k in (5,15));assert after<before
out=['% Same4position+4derivativehardconstraintsas9.40;ONLYw5andw15change1to100.']+drawing(P,ss,POINTS,DERIVATIVES,[((F(11,5),F(21,10)),r'w_5^q=100'),((F(11,2),F(7,20)),r'w_{15}^q=100')])
out[-1:-1]=[r'\draw[book grid,shorten >=4pt] (2.2,2.32)--'+point(Q[5])+';',r'\draw[book grid,shorten >=4pt] (5.5,.12)--'+point(Q[15])+';']
(root/'image_tex/ch09/fig_9_49.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/weighted-point-derivative-curve-check.json').write_text(json.dumps(dict(figure='9.41',same_data_parameters_knots_control_count_constraints_as='9.40',only_weights_changed={'5':100,'15':100},fit=proof,selected_group_squared_error_before=float(before),selected_group_squared_error_after=float(after),selected_group_error_strictly_reduced=True,all8hard_constraints_unchanged_exact=True,common_arrow_scale='1/10',control_hull_bounds=[[float(min(p[i] for p in P)),float(max(p[i] for p in P))] for i in range(2)]),indent=2)+'\n')
print('PASS9.41:same8hardconstraints exact,KKTgradient exact,onlyw5/w15=100;selectedSSE',float(before),'->',float(after),';controlbounds',[[float(min(p[i] for p in P)),float(max(p[i] for p in P))] for i in range(2)])
