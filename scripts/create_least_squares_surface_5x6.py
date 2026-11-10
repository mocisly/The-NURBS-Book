"""9.45: actual5x6tensor fit and pointwise residual mesh, no tracing."""
from pathlib import Path
from fractions import Fraction as F
import json
from surface_least_squares_data import fit,sqrt_bounds,UP,VP
from surface_approximation_example_data import Q,X,Y
from surface_geometry import isocurve,surface,verify_tensor
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch09/fig_9_53.tex')['applied']
base,squares,report=fit(5,6)
def view(p):
    x,y,z=p;return (2*(-F(4,5)*x+F(9,10)*y),2*(-F(2,5)*x-F(7,20)*y+z))
error=tuple(tuple((X[i],Y[j],2*sum(sqrt_bounds(squares[i][j]))) for j in range(9)) for i in range(9))
out=['% Exact A9.7degree(2,3)5x6fit; same81data as9.44; actual 3Dpointwise residuals.',r'\begin{tikzpicture}[book line]']
native=iso=0
for letter,shift in [('a',0),('b',F(33,2))]:
    out.extend([r'\begin{scope}[xshift='+str(float(shift))+r'cm]',r'\path[use as bounding box] (-7.6,-4) rectangle (7.6,9);'])
    if letter=='a':
        fixed=tuple(sorted(set(tuple(F(i,32) for i in range(33))+VP)))
        for v in fixed:
            K,p,C=isocurve(*base,'u',v);ss=segments(K,C,p);native+=check(K,C,p,ss,steps=4)
            for u in (F(0),F(1,3),F(2,3),F(1)):
                assert de_boor(K,C,p,u)==surface(*base,u,v);iso+=1
            out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in ss)
        out.extend(r'\fill '+point(view(p))+r' circle[radius=.95pt];' for row in Q for p in row)
    else:
        for lines in (error,tuple(zip(*error))):
            for row in lines:out.append(r'\draw[book grid] '+'--'.join(point(view(p)) for p in row)+';')
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(7,2)),'z' if letter=='a' else '4e','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend([r'\node at (0,-3.55) {('+letter+')};',r'\end{scope}'])
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_53.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report.update(figure='9.45',same_data_as='9.44',native_curve_checks=native,isocurve_tensor_crosschecks=iso,tensor_checks=verify_tensor(*base,steps=3),displayed_isocurves=len(fixed),error_mesh='9x9polyline of Euclidean 3Dsame-parameter residuals; NOT continuous error surface or nearest distance',error_vertical_magnification=4,error_sqrt_enclosure_width='1e-12',camera_scale=2,font_rescaling=False,common_comparison_camera=True)
(root/'image_tex/build/least-squares-surface-5x6-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.45:',native,'native checks;41or fewer actual isocurves; exact order commutation; RMS/max',report['RMS_same_parameter_3D_error'],report['maximum_same_parameter_3D_error'])
