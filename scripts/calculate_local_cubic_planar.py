"""9.57three actual planar cubic approximations with printedE/Kmax."""
from pathlib import Path
from fractions import Fraction as F
import json
from local_cubic_planar_data import Q,D,PIECES,COUNTS
from local_cubic_approximation import approximate_planar
root=Path(__file__).resolve().parents[1];panels=[]
def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x
for letter,E,Kmax in [('a',F(1,10),11),('b',F(1,10),8),('c',F(1,100),11)]:
    U,P,pieces,r=approximate_planar(Q,D,E,Kmax);r.update(letter=letter,U=U,controls=P,pieces=pieces);panels.append(r)
    data=dict(figure='9.57',representative_data=True,data=Q,data_generator_pieces=PIECES,samples_per_piece=COUNTS,known_analytic_tangent_directions=D,panels=panels)
    (root/'image_tex/build/local-cubic-planar-data.json').write_text(json.dumps(serial(data),indent=2)+'\n',encoding='utf-8')
    print('PASS9.57'+letter,'segments',r['segments'],'C1controls',r['control_count'],'maxdistance',r['maximum_exact_checked_datum_distance'],'E',E,flush=True)
