"""9.34: true A9.5doubly-periodic local bicubic interpolation of toroidal data."""
from pathlib import Path
from fractions import Fraction as F
import json
from local_bicubic_surface import construct
from surface_geometry import verify_tensor,surface,isocurve
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_41.tex')['applied']
UV=((1,0),(0,1),(-1,0),(0,-1),(1,0));R,r=F(2),F(3,5)
Q=tuple(tuple(((R+r*c)*x,(R+r*c)*y,r*s) for c,s in UV) for x,y in UV)
base,params,full,patch,proof=construct(Q,True,True)
assert proof['whole_edge_C0_C1_coefficient_equalities']==128 and proof['closed_seam_coefficient_equalities']==32 and proof['mixed_derivatives_nonzero']
tc=verify_tensor(*base,steps=4);native=crosschecks=0
def camera(q):
    x,y,z=q;scale=F(11,5)
    return (scale*(-F(4,5)*x+F(9,10)*y),scale*(-F(2,5)*x-F(7,20)*y+z))
def poly(row):return r'\draw[book grid,dashed] '+'--'.join(point(camera(q)) for q in row)+';'
def mark(q):return r'\draw '+point(camera(q))+r' ++(-2pt,-2pt) rectangle ++(4pt,4pt);'
def panel(letter,shift):
    global native,crosschecks
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-8,-5.5) rectangle (8,8.5);']
    if letter=='a':
        for row in Q[:-1]:out.append(poly(row))
        for j in range(4):out.append(poly(tuple(Q[i][j] for i in range(5))))
    else:
        for variable,count in [('u',32),('v',24)]:
            for j in range(count):
                fixed=F(j,count);K,p,C=isocurve(*base,variable,fixed);ss=segments(K,C,p);native+=check(K,C,p,ss,steps=7)
                for k in range(5):
                    t=F(k,4);assert de_boor(K,C,p,t)==(surface(*base,t,fixed) if variable=='u' else surface(*base,fixed,t));crosschecks+=1
                out.extend(cubic_path(dict(bern=tuple(camera(q) for q in s['bern'])),'book grid' if variable=='u' else '') for s in ss)
    for end,name,anchor in [((F(7,2),0,0),'x','below left'),((0,F(7,2),0),'y','below right'),((0,0,F(10,3)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend(mark(q) for row in Q[:-1] for q in row[:-1]);out.extend([r'\node at (0,-4.9) {('+letter+')};',r'\end{scope}']);return out
out=['% Toroidal16data withmajorradius2,minorradius3/5;actual local polynomial bicubic,not exact rational torus.',r'\begin{tikzpicture}[book line]']+panel('a',0)+panel('b',17)+[r'\end{tikzpicture}']
(root/'image_tex/ch09/fig_9_41.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/two-direction-closed-bicubic-check.json').write_text(json.dumps(dict(figure='9.34',representative_major_radius=str(R),representative_minor_radius=str(r),unique_data_points=16,data=[[[str(x) for x in p] for p in row] for row in Q],construction=proof,independent_tensor_checks=tc,native_curve_checks=native,isocurve_surface_crosschecks=crosschecks,periodic_seams_in_both_directions_C1_exact=True,displayed_parallel_curves=32,displayed_meridian_curves=24,common_camera_scale='11/5',surface_is_local_polynomial_interpolant=True),indent=2)+'\n')
print('PASS9.34:16unique toroidal data,16wholepatch identities,128edgeC1coefficients including32closedseam identities;nonzero mixed derivatives,56actual tensor isocurves,',native,'nativechecks.')
