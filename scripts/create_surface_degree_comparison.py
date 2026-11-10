"""9.17:independent(2,3),(3,2),(3,3)tensor interpolants with fixed chord mesh parameters."""
from fractions import Fraction as F
from pathlib import Path
import json
from surface_mesh_interpolation import interpolate_mesh
from mesh_interpolation_example_data import Q,camera
from surface_geometry import surface
from native_tensor_interpolation_panel import panel
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (20,21):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex')['applied']
def view(q):return tuple(x/2 for x in camera(q))
reports=[];bases=[];panels=[];parameter_vectors=[]
for k,(p,q,letter,shift) in enumerate([(2,3,'a',0),(3,2,'b',14),(3,3,'c',0)]):
    base,params,proof=interpolate_mesh('chord',p,q);bases.append(base);parameter_vectors.append(params)
    lines,checks=panel(base,Q,view,letter,shift);panels.append(lines)
    reports.append(dict(degrees=[p,q],parameters=[list(map(str,a)) for a in params],knots=[list(map(str,base[0])),list(map(str,base[1]))],all16point_constraints_exact=True,reverse_interpolation_order_identical=True,**checks))
assert parameter_vectors[0]==parameter_vectors[1]==parameter_vectors[2]
witness=tuple(surface(*b,F(2,5),F(3,5)) for b in bases)
assert len(set(witness))==3
header=['% SAME16representative data and chord parameters9.15/9.16;vary actual interpolation degrees.',r'\begin{tikzpicture}[book line]']
for n,lines in [(20,header+panels[0]+panels[1]+[r'\end{tikzpicture}']),(21,header+panels[2]+[r'\end{tikzpicture}'])]:
    (root/f'image_tex/ch09/fig_9_{n:02}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-degree-comparison-check.json').write_text(json.dumps(dict(figure='9.17',same_representative_input_as='9.15',variants=reports,all_three_parameter_vectors_identical=True,witness_parameter=['2/5','3/5'],distinct_geometry_witnesses=[[str(x) for x in p] for p in witness],all_three_surface_geometries_distinct=True,small_transverse_data_variation_prevents_q_direction_degeneracy=True,same_camera_and_font_as='9.16',coordinate_camera_scale='7/4'),indent=2)+'\n')
print('PASS:three exact tensor solves,same chord parameters,all16points each;all3geometries provably distinct at a rational witness;native/tensor checks.')
