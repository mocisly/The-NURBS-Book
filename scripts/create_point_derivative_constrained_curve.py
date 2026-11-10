"""9.40: solve all hard point and first-derivative constraints with exactKKT."""
from pathlib import Path
from fractions import Fraction as F
import json
from weighted_constrained_curve_data import Q,PARAMS,COUNT,U,fit
from constrained_curve_example_data import POINTS,DERIVATIVES
from constrained_curve_native import drawing
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_48.tex')['applied']
P,ss,proof=fit(point_constraints=POINTS,derivative_constraints=DERIVATIVES)
assert all(F(proof['point_squared_residuals'][k])==0 for k in POINTS)
assert all(-F(4,5)<p[0]<F(43,5) and -F(2)<p[1]<F(24,5) for p in P)
(root/'image_tex/ch09/fig_9_48.tex').write_text('\n'.join(['% Exact18x18KKT system:10controls,4point+4derivativeconstraints;allunconstrainedweights1.']+drawing(P,ss,POINTS,DERIVATIVES))+'\n',encoding='utf-8')
(root/'image_tex/build/point-derivative-constrained-curve-check.json').write_text(json.dumps(dict(figure='9.40',same_data_parameters_knots_control_count_as='9.38',point_constraint_indices=list(POINTS),derivative_constraints={str(k):list(map(str,D)) for k,D in DERIVATIVES.items()},scalar_KKT_dimension=18,all8constraints_exact=True,fit=proof,arrow_common_scale='1/10',coordinate_scale_cm='13/5'),indent=2)+'\n')
print('PASS9.40:18x18exactKKT,4positions+4derivatives exact,positiveGramLDL/C2native,arrowscommon1/10;unconstrainedSSE',proof['weighted_objective_decimal'])
