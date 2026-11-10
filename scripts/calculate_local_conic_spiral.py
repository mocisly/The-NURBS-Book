"""Calculateallfour9.54spiral fits with printedE/Kmax settings."""
from pathlib import Path
from fractions import Fraction as F
import json
from log_spiral_data import Q,DIRECTIONS,THETA
from local_conic_approximation import approximate,PARAMS
root=Path(__file__).resolve().parents[1];panels=[]
for letter,E,Kmax in [('a',F(1,100),50),('b',F(1,1000),50),('c',F(1,10),6),('d',F(1,10),10)]:
    U,H,pieces,report=approximate(E,Kmax)
    report.update(letter=letter,U=list(map(str,U)),homogeneous_controls=[list(map(str,p)) for p in H],pieces=[{k:([list(map(str,p)) for p in value] if k=='H' else list(map(str,value)) if k in ('R','projection_parameters','squared_distances') else str(value) if isinstance(value,F) else value) for k,value in piece.items()} for piece in pieces])
    panels.append(report)
    (root/'image_tex/build/local-conic-spiral-data.json').write_text(json.dumps(dict(figure='9.54',formula='r=exp(theta/5)/2',theta_range='0..3pi',analytic_sample_count=51,theta_values=THETA,data=[list(map(str,p)) for p in Q],analytic_tangent_directions=[list(map(str,p)) for p in DIRECTIONS],common_chord_parameters=list(map(str,PARAMS)),panels=panels),indent=2)+'\n',encoding='utf-8')
    print('PASS9.54'+letter,'E',E,'Kmax',Kmax,'segments',report['segments'],'maxdistance',report['maximum_exact_checked_datum_distance'],flush=True)
