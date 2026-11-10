"""Calculate and certify10.10before native drawing."""
from pathlib import Path
from fractions import Fraction as F
import json
from rational_skin_continuity_data import construct
root=Path(__file__).resolve().parents[1];b,v,r=construct()
(root/'image_tex/build/rational-skin-continuity-data.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print('PASS10.10:all4projectedsectionsC1;20homogeneousconstraints;3actualnormaljumps;VP',list(map(float,v)),'Wlower',float(F(r['global_denominator_positive_lower_bound'])),'weights',[[round(float(F(x)),4) for x in row] for row in r['surface_weight_rows_j_columns_i']])
