"""9.43: preserve9.42horizontal constraints and raise onlyw4=50,w16=20."""
from fractions import Fraction as F
from pathlib import Path
import json
from weighted_constrained_curve_data import Q,fit
from constrained_curve_example_data import POINTS,HORIZONTAL_DERIVATIVES
from constrained_curve_native import drawing
from native_bspline import point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_51.tex')['applied']
P,ss,proof=fit({4:50,16:20},POINTS,HORIZONTAL_DERIVATIVES)
prior=json.loads((root/'image_tex/build/changed-internal-derivative-curve-check.json').read_text(encoding='utf-8'))['fit']
before=[F(prior['point_squared_residuals'][k]) for k in (4,16)];after=[F(proof['point_squared_residuals'][k]) for k in (4,16)]
assert all(a<b for a,b in zip(after,before))
out=['% Same9.42hardpositions/derivatives/knots;ONLYw4=50andw16=20.']+drawing(P,ss,POINTS,HORIZONTAL_DERIVATIVES,[((F(3,2),F(41,10)),r'w_4^q=50'),((F(63,10),F(7,20)),r'w_{16}^q=20')])
out[-1:-1]=[r'\draw[book grid,shorten >=4pt] (1.5,3.86)--'+point(Q[4])+';',r'\draw[book grid,shorten >=4pt] (6.3,.12)--'+point(Q[16])+';']
(root/'image_tex/ch09/fig_9_51.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/weighted-horizontal-derivative-curve-check.json').write_text(json.dumps(dict(figure='9.43',same_data_parameters_knots_control_count_constraints_as='9.42',only_changed_weights={'4':50,'16':20},fit=proof,selected_indices=[4,16],selected_squared_errors_before=list(map(float,before)),selected_squared_errors_after=list(map(float,after)),both_selected_point_errors_strictly_reduced=True,all8hard_constraints_unchanged_exact=True,common_arrow_scale='1/10',control_hull_bounds=[[float(min(p[i] for p in P)),float(max(p[i] for p in P))] for i in range(2)]),indent=2)+'\n')
print('PASS9.43:exactKKT/C2andall8unchangedhardconstraints;ONLYw4=50/w16=20,pointSSE',list(map(float,before)),'->',list(map(float,after)))
