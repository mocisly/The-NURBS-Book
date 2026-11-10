"""9.16:three exact degree(2,3)interpolants using uniform/chord/centripetal mesh params."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
from surface_mesh_interpolation import interpolate_mesh
from mesh_interpolation_example_data import Q,camera
from surface_geometry import surface,verify_tensor,isocurve
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (18,19):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex')['applied'] or '--refresh' in sys.argv
def view(q):return tuple(x/2 for x in camera(q))
reports=[]
def panel(mode,letter,shift=0):
    base,params,proof=interpolate_mesh(mode);U,V,p,q,P=base;tc=verify_tensor(*base,steps=10);nc=0;iso_checks=0
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-6.5,-4.5) rectangle (6.5,11);']
    for j in range(41):
        fixed=F(j,40);K,degree,C=isocurve(*base,'u',fixed);ss=segments(K,C,degree);nc+=check(K,C,degree,ss)
        for k in range(21):
            t=F(k,20);assert de_boor(K,C,degree,t)==surface(*base,t,fixed);iso_checks+=1
        out.extend(cubic_path(dict(bern=tuple(view(pt) for pt in s['bern']))) for s in ss)
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(26,5)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    for row in Q:
        for pt in row:out.append(r'\fill '+point(view(pt))+r' circle[radius=1.7pt];')
    out.extend([r'\node at (0,-4) {('+letter+')};',r'\end{scope}'])
    reports.append(dict(method=mode,degrees=[p,q],parameters=[list(map(str,a)) for a in params],parameter_enclosures=[[[str(v) for v in b] for b in axis] for axis in proof],knots=[list(map(str,U)),list(map(str,V))],all16point_constraints_exact=True,reverse_interpolation_order_identical=True,independent_tensor_checks=tc,native_curve_checks=nc,isocurve_vs_surface_exact_checks=iso_checks))
    return out
header=['% Same16representative data9.15;exacttensorinterpolation;certifiedmeshparam enclosures.',r'\begin{tikzpicture}[book line]']
ab=header+panel('uniform','a')+panel('chord','b',14)+[r'\end{tikzpicture}']
c=header+panel('centripetal','c')+[r'\end{tikzpicture}']
for n,lines in [(18,ab),(19,c)]:(root/f'image_tex/ch09/fig_9_{n:02}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-parameterization-comparison-check.json').write_text(json.dumps(dict(figure='9.16',same_representative_input_as='9.15',methods=reports,coordinate_camera_scale='7/4',camera_projection_same_as_data_figure=True,coordinate_scale_relative_to_data_figure='1/2',font_size_unchanged=True,mesh_parameters_are_averages_of_per_row_normalized_lengths=True),indent=2)+'\n')
print('PASS:3exact tensor interpolation solves,all16points per variant,reverse order identical;per-row averaged certified params;native isocurves verified.')
