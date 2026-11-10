"""8.17: actual stereographic point/line map with a certified rational display sphere."""
from pathlib import Path
from fractions import Fraction as F
import json
from stereographic_geometry import lift_h,lift,sphere_net
from revolved_surface_data import camera
from native_bspline import point
from rational_geometry import project
from surface_geometry import surface,verify_tensor
from native_rational_surface_grid import grid
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_22.tex')['applied']
R=F(1);N=(F(0),F(0),2*R);B=(F(1),F(2),F(0));Q=lift(B[0],B[1]);checks=0
for i in range(-10,11):
    for j in range(-10,11):
        u,v=F(i,5),F(j,5);h=lift_h((u,v,F(1)));x,y,z=project(h)
        assert x*x+y*y+(z-R)**2==R*R
        assert (2*R*x/(2*R-z),2*R*y/(2*R-z))==(u,v)
        lam=4*R*R/(u*u+v*v+4*R*R)
        assert (x,y,z)==(lam*u,lam*v,2*R*(1-lam));checks+=1
assert Q==(F(4,9),F(8,9),F(10,9))
U,V,NET=sphere_net(R);tc=verify_tensor(U,V,2,2,NET);maxres=F(0)
for i in range(21):
    for j in range(21):
        x,y,z=project(surface(U,V,2,2,NET,F(i,20),F(j,20)));res=abs(x*x+y*y+(z-R)**2-R*R);assert res<F(1,10**36);maxres=max(maxres,res)
lines=['% Equation8.13 sphere centered(0,0,R),north pole(0,0,2R),R1.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-11,-8) rectangle (13,14);']
paths,report=grid(U,V,2,2,NET,camera,tuple(F(i,8) for i in range(8)),tuple(F(j,16) for j in range(1,16)));lines+=paths
lines.append(r'\draw '+point(camera(N))+'--'+point(camera(B))+';')
for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','right'),((0,0,F(3)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
lines.extend([r'\fill '+point(camera(N))+r' circle[radius=1.5pt];',r'\node[anchor=west] (north) at (1.2,10) {$(0,0,2R)$};',r'\draw[book grid] (north.west)--'+point(camera(N))+';',
              r'\draw '+point(camera(B))+r' circle[radius=1.8pt];',r'\node[below right=7pt] at '+point(camera(B))+r' {$(u,v)$};',
              r'\fill '+point(camera(Q))+r' circle[radius=1.8pt];',r'\node[anchor=west] (mapped) at (7,3) {$(x,y,z)$};',r'\draw[book grid] (mapped.west)--'+point(camera(Q))+';',r'\end{tikzpicture}'])
(root/'image_tex/ch08/fig_8_22.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/stereographic-projection-check.json').write_text(json.dumps({'figure':'8.17','R':str(R),'sphere_center':['0','0','1'],'projection_pole':list(map(str,N)),'plane_point':list(map(str,B)),'mapped_point':list(map(str,Q)),'exact_sphere_inverse_and_collinear_projection_identities':checks,'display_sphere_tensor_checks':tc,'display_sphere_residual_grid_max':str(maxres),'native_grid':report,'map_denominator':'u^2+v^2+4R^2>0 for finite u,v'},indent=2)+'\n')
print('PASS:441exact stereographic sphere/inverse/collinearity identities,actualQ=(4/9,8/9,10/9);441display tensor and483isocurve checks.')
