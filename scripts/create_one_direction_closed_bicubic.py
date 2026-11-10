"""9.33: locally interpolated four-ring tube, C1closed in its cross-section."""
from fractions import Fraction as F
from pathlib import Path
import json
from local_translation_surface import construct
from local_quadratic_interpolator import add
from surface_geometry import surface,verify_tensor,isocurve
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_40.tex')['applied']
A=tuple(tuple(map(F,p)) for p in [('-2','0','3'),('-.75','0','3'),('.75','0','0'),('2','0','0')]);r=F(13,20)
B=tuple((F(0),r*y,r*z) for y,z in [(-1,0),(0,1),(1,0),(0,-1),(-1,0)])
base,Q,(UP,VP),proof=construct(A,B,closed_b=True)
tc=verify_tensor(*base,steps=4);native=0;crosschecks=0
def camera(q):
    x,y,z=q;return (3*(-F(4,5)*x+F(9,10)*y),3*(-F(2,5)*x-F(7,20)*y+z))
def poly(row):return r'\draw[book grid,dashed] '+'--'.join(point(camera(q)) for q in row)+';'
def mark(q):return r'\draw '+point(camera(q))+r' ++(-2pt,-2pt) rectangle ++(4pt,4pt);'
def panel(letter,shift):
    global native,crosschecks
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-8,-6) rectangle (8,15);']
    if letter=='a':
        for row in Q:out.append(poly(row))
        for j in range(4):out.append(poly(tuple(Q[i][j] for i in range(4))))
    else:
        #31closed cross-sections plus16finer longitudinal guides;include data lines.
        fixed_u=tuple(UP[l]+(UP[l+1]-UP[l])*F(j,c) for l,c in enumerate((6,18,6)) for j in range(c))+(F(1),)
        for variable,values in [('u',tuple(F(j,16) for j in range(16))),('v',fixed_u)]:
            for fixed in values:
                K,p,C=isocurve(*base,variable,fixed);ss=segments(K,C,p);native+=check(K,C,p,ss,steps=7)
                for j in range(5):
                    t=F(j,4);assert de_boor(K,C,p,t)==(surface(*base,fixed,t) if variable=='v' else surface(*base,t,fixed));crosschecks+=1
                out.extend(cubic_path(dict(bern=tuple(camera(q) for q in s['bern'])),'book grid' if variable=='u' else '') for s in ss)
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(5,2),0),'y','below right'),((0,0,F(9,2)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend(mark(q) for row in Q for q in row[:-1]);out.extend([r'\node at (0,-5.4) {('+letter+')};',r'\end{scope}']);return out
out=['% Four chosen axial stations and four-point cross-sections;actual polynomial local bicubic withC1periodic seam.',r'\begin{tikzpicture}[book line]']+panel('a',0)+panel('b',17)+[r'\end{tikzpicture}']
(root/'image_tex/ch09/fig_9_40.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/one-direction-closed-bicubic-check.json').write_text(json.dumps(dict(figure='9.33',representative_axial_data=[list(map(str,p)) for p in A],cross_section_radius=str(r),cross_section_data=[list(map(str,p)) for p in B],unique_data_points=16,construction=proof,independent_tensor_checks=tc,native_curve_checks=native,isocurve_surface_crosschecks=crosschecks,closed_section_and_seam_C1_exact=True,displayed_ring_curves=31,displayed_longitudinal_curves=16,common_camera_scale='3',cross_section_is_polynomial_cubic_interpolant_not_exact_circle=True),indent=2)+'\n')
print('PASS9.33:16unique data,12whole bicubic patch identities,8x10control net,exact C1closed seam/zero mixedderivatives;47actual tensor isocurves,',native,'native checks.')
