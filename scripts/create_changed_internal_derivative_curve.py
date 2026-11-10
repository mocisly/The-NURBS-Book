"""9.42: same constrained fit as9.40with only two internal derivative vectors changed."""
from pathlib import Path
import json
from weighted_constrained_curve_data import fit
from constrained_curve_example_data import POINTS,DERIVATIVES,HORIZONTAL_DERIVATIVES
from constrained_curve_native import drawing
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_50.tex')['applied']
assert [k for k in DERIVATIVES if DERIVATIVES[k]!=HORIZONTAL_DERIVATIVES[k]]==[7,13]
P,ss,proof=fit(point_constraints=POINTS,derivative_constraints=HORIZONTAL_DERIVATIVES)
(root/'image_tex/ch09/fig_9_50.tex').write_text('\n'.join(['% Same9.40positions/endderivatives/weights/knots;ONLYD7/D13change to(14,0).']+drawing(P,ss,POINTS,HORIZONTAL_DERIVATIVES))+'\n',encoding='utf-8')
(root/'image_tex/build/changed-internal-derivative-curve-check.json').write_text(json.dumps(dict(figure='9.42',same_data_parameters_knots_control_count_point_constraints_as='9.40',only_changed_derivatives={'7':['14','0'],'13':['14','0']},endpoint_derivatives_unchanged=True,all_weights_one=True,all8hard_constraints_exact=True,fit=proof,common_arrow_scale='1/10',control_hull_bounds=[[float(min(p[i] for p in P)),float(max(p[i] for p in P))] for i in range(2)]),indent=2)+'\n')
print('PASS9.42:exact18x18KKT/C2native,all4positions and4derivatives;ONLYtwointernalDchangedto(14,0),allweights1;controlbounds',[[float(min(p[i] for p in P)),float(max(p[i] for p in P))] for i in range(2)])
