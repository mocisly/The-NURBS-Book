"""Solve9.51withE.08and a protected,exactly interpolated apex corner."""
from pathlib import Path
from fractions import Fraction as F
import json
from bounded_corner_profile_data import Q,CORNER,PIECES,COUNTS
from bounded_curve_approximation import approximate
root=Path(__file__).resolve().parents[1]
U,P,params,report=approximate(Q,F(8,100),hard_indices=(CORNER,))
report.update(figure='9.51',representative_data=True,data=[list(map(str,p)) for p in Q],data_generator_pieces=[[[str(x) for x in p] for p in row] for row in PIECES],data_samples_per_piece=COUNTS,protected_corner_index=CORNER,corner_position_exact=True,corner_knot_multiplicity=3,knots=list(map(str,U)),controls=[list(map(str,p)) for p in P])
(root/'image_tex/build/bounded-corner-profile-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.51:',len(P),'controls,bound',report['certified_maximum_accumulated_L1_bound'],'exactprotectedcorner',CORNER)
