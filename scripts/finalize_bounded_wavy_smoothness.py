"""Finalize the existing81data solve with the documented final C1refit check."""
from pathlib import Path
from fractions import Fraction as F
import json
from bounded_curve_example_data import Q
from bounded_curve_approximation import smooth_triples,point_errors
root=Path(__file__).resolve().parents[1];path=root/'image_tex/build/bounded-wavy-curve-data.json'
d=json.loads(path.read_text());assert len(d['data'])==len(Q)==81 and not d.get('final_smoothness_refits')
U=tuple(map(F,d['knots']));P=tuple(tuple(map(F,p)) for p in d['controls']);params=tuple(map(F,d['parameters']))
U,P,params,history=smooth_triples(Q,params,U,P,F(7,100));assert history
err=point_errors(U,P,3,Q,params);assert max(err)<=F(7,100)
d['prior_greedy_accumulated_bound']=d['certified_maximum_accumulated_L1_bound']
d.update(knots=list(map(str,U)),controls=[list(map(str,p)) for p in P],parameters=list(map(str,params)),final_smoothness_refits=history,actual_same_parameter_L1_errors=list(map(str,err)),actual_maximum_L1_error=float(max(err)),certified_maximum_accumulated_L1_bound=float(max(err)),internal_multiplicities={str(t):U.count(t) for t in sorted(set(U[4:-4]))})
d['variant']+=';final C0join removal/refit accepted only after exact datum L1error check'
path.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('PASS9.50final C1refit:',len(P),'controls,maxL1',float(max(err)),'all internal multiplicities',sorted(set(d['internal_multiplicities'].values())))
