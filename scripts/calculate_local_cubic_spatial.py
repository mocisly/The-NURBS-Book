"""9.58three same-data3Dfits,including exact zero-tolerancepairinterpolation."""
from pathlib import Path
from fractions import Fraction as F
import json
from local_cubic_spatial_data import Q,D,PIECES,COUNTS
from local_cubic_spatial_approximation import approximate
root=Path(__file__).resolve().parents[1];panels=[]
def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x
for letter,E in [('a',F(1,10)),('b',F(1,100)),('c',F(0))]:
    U,P,pieces,r=approximate(E);r.update(letter=letter,U=U,controls=P,pieces=pieces);panels.append(r)
    data=dict(figure='9.58',representative_data=True,data=Q,known_analytic_tangent_directions=D,data_generator_pieces=PIECES,samples_per_piece=COUNTS,planar_sections='first17points z0,last17points z3;middle cubic skew',panels=panels)
    (root/'image_tex/build/local-cubic-spatial-data.json').write_text(json.dumps(serial(data),indent=2)+'\n',encoding='utf-8')
    print('PASS9.58'+letter,'segments',r['segments'],'C1controls',r['control_count'],'max3Ddistance',r['maximum_exact_checked_3D_datum_distance'],'E',E,flush=True)
