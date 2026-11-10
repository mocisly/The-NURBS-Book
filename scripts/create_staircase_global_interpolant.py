"""9.47: exact tensor interpolation of the SAME81staircase points."""
from pathlib import Path
from fractions import Fraction as F
import json
from surface_least_squares_data import UP,VP,PARAMETER_PROOF
from surface_approximation_example_data import Q
from global_interpolation_data import interpolate
from surface_geometry import surface,verify_tensor
from surface_comparison_native import draw
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_56.tex')['applied']
cols=[]
for j in range(9):
    U,C=interpolate(tuple(Q[i][j] for i in range(9)),UP,2);cols.append(C)
temp=tuple(tuple(cols[j][i] for j in range(9)) for i in range(9));P=[]
for row in temp:
    V,C=interpolate(row,VP,3);P.append(C)
P=tuple(P);base=(U,V,2,3,P)
other=tuple(interpolate(row,VP,3)[1] for row in Q)
reverse_cols=tuple(interpolate(tuple(other[i][j] for i in range(9)),UP,2)[1] for j in range(9))
assert P==tuple(tuple(reverse_cols[j][i] for j in range(9)) for i in range(9))
assert all(surface(*base,u,v)==Q[i][j] for i,u in enumerate(UP) for j,v in enumerate(VP))
tex,checks=draw(base)
(root/'image_tex/ch09/fig_9_56.tex').write_text('% Actual degree(2,3)tensor interpolation of all81shared points;average knots/chord mesh parameters.\n'+tex,encoding='utf-8')
report=dict(figure='9.47',same81data_parameters_as=['9.44','9.45','9.46'],control_shape=[9,9],degrees=[2,3],knots_u=list(map(str,U)),knots_v=list(map(str,V)),common_parameter_proof=PARAMETER_PROOF,all81interpolation_residuals_exactly_zero=True,reverse_direction_order_exactly_identical=True,tensor_checks=verify_tensor(*base,steps=3),native_checks=checks)
(root/'image_tex/build/staircase-global-interpolant-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.47:all81interpolation residuals exactly0;reverse order exactly equal;',checks)
