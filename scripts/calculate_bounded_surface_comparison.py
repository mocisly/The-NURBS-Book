"""Solve9.52b-e on exactly the same169data and common mesh parameters."""
from pathlib import Path
from fractions import Fraction as F
import json
from bounded_surface_example_data import Q,X,Y
from bounded_surface_approximation import initial_interpolant,approximate,UP,VP,PARAM_ERROR,grid
root=Path(__file__).resolve().parents[1];base=initial_interpolant();panels=[]
for letter,E,p in [('b',F(0),2),('c',F(1,2),2),('d',F(1),2),('e',F(1),3)]:
    if not E:net=base;proof=dict(tolerance='0',degrees=[2,2],control_shape=[13,13],all169interpolation_residuals_exactly_zero=True)
    else:net,proof=approximate(base,E,p)
    U,V,p,q,P=net
    squares=tuple(sum((a-b)**2 for a,b in zip(x,y)) for row,data in zip(grid(net),Q) for x,y in zip(row,data));assert max(squares)<=E*E
    proof.update(letter=letter,U=list(map(str,U)),V=list(map(str,V)),controls=[[[str(x) for x in point] for point in row] for row in P],maximum_actual_Euclidean_error=float(max(squares))**.5)
    panels.append(proof)
    (root/'image_tex/build/bounded-surface-comparison-data.json').write_text(json.dumps(dict(figure='9.52',representative_data=True,shape=[13,13],data=[[[str(x) for x in point] for point in row] for row in Q],height_formula='3*(2-x)^4/((2-x)^4+(2+x)^4)+(1-x*x/4)^2*(1-y*y/4)/10',X=list(map(str,X)),Y=list(map(str,Y)),u_parameters=list(map(str,UP)),v_parameters=list(map(str,VP)),common_mesh_chord_parameter_error_bounds=PARAM_ERROR,panels=panels),indent=2)+'\n',encoding='utf-8')
    print('PASS9.52'+letter,'shape',proof['control_shape'],'maxEuclidean',proof['maximum_actual_Euclidean_error'],'<=',E,flush=True)
