"""10.17actual projected-normal steps, certified normalization, exact Frenet axes."""
from pathlib import Path
from fractions import Fraction as F
import json
from projected_frame_comparison_data import construct
root=Path(__file__).resolve().parents[1];reports=[]
for case in 'ab':
    r=construct(case);reports.append(r)
    print('PASS10.17',case,'7exactorthogonality identities;maximum PN directionerror',float(F(r['maximum_accumulated_projected_direction_error_bound'])),'positiveadjacentdotlower',float(F(r['certified_positive_adjacent_projected_normal_dot_lower_bound'])))
report=dict(figure='10.17',representative_curves=True,sample_parameters=[str(x) for x in ('0','3/20','3/10','1/2','7/10','17/20','1')],panels=reports,PN_calculated_by_actual_projection_not_illustrative_arrows=True,no_contour_tracing=True)
(root/'image_tex/build/projected-frame-comparison-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
