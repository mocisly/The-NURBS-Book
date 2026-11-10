"""Apply the same final refit/remove verification to existing9.52solves."""
from pathlib import Path
from fractions import Fraction as F
import json
from bounded_surface_approximation import final_refit_removals,actual_errors,maximum,grid
from bounded_surface_example_data import Q
root=Path(__file__).resolve().parents[1];path=root/'image_tex/build/bounded-surface-comparison-data.json'
d=json.loads(path.read_text());assert len(d['panels'])==4
for r in d['panels'][1:]:
    assert 'final_refit_removals' not in r
    net=(tuple(map(F,r['U'])),tuple(map(F,r['V'])),*r['degrees'],tuple(tuple(tuple(map(F,p)) for p in row) for row in r['controls']))
    net,history=final_refit_removals(net,F(r['tolerance']));U,V,p,q,P=net;err=maximum(actual_errors(net));assert err<=F(r['tolerance'])
    squares=tuple(sum((a-b)**2 for a,b in zip(x,y)) for row,data in zip(grid(net),Q) for x,y in zip(row,data))
    r.update(U=list(map(str,U)),V=list(map(str,V)),controls=[[[str(x) for x in point] for point in row] for row in P],control_shape=[len(P),len(P[0])],final_refit_removals=history,maximum_actual_L1_error=float(err),certified_accumulated_L1_bound=float(err),maximum_actual_Euclidean_error=float(max(squares))**.5)
    print(r['letter'],'shape',r['control_shape'],'finalrefitremovals',len(history),'maxL1',float(err),'maxEuclidean',r['maximum_actual_Euclidean_error'])
path.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
