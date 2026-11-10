"""Persist mathematically solved9.50data before authoring its native figure."""
from pathlib import Path
from fractions import Fraction as F
import json
from bounded_curve_example_data import Q,K,P
from bounded_curve_approximation import approximate
root=Path(__file__).resolve().parents[1]
U,C,params,report=approximate(Q,F(7,100))
report.update(figure='9.50',representative_data=True,data=[list(map(str,p)) for p in Q],data_generator_knots=list(map(str,K)),data_generator_controls=[list(map(str,p)) for p in P],knots=list(map(str,U)),controls=[list(map(str,p)) for p in C])
(root/'image_tex/build/bounded-wavy-curve-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.50bounded computation:',len(C),'cubic controls;L1bound',report['certified_maximum_accumulated_L1_bound'],'multiplicities',report['internal_multiplicities'])
