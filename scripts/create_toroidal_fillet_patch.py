"""8.13: genuine biquadratic90x90degree toroidal fillet and its3x3net."""
from pathlib import Path
from fractions import Fraction as F
import json
from revolved_surface_data import camera,w
from native_bspline import point
from rational_geometry import project
from surface_geometry import surface,verify_tensor
from native_rational_surface_grid import grid
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_17.tex')['applied']
R,r,z0=F(2),F(3,5),F(6,5);U=V=(F(0),F(0),F(0),F(1),F(1),F(1))
CIRCLE=((F(1),F(0),F(1)),(w,w,w),(F(0),F(1),F(1)))
PROFILE=((R-r,z0,F(1)),((R-r)*w,(z0-r)*w,w),(R,z0-r,F(1)))
NET=tuple(tuple((x*rho,y*rho,a*z,a*b) for rho,z,b in PROFILE) for x,y,a in CIRCLE)
tc=verify_tensor(U,V,2,2,NET);maxres=F(0)
for i in range(21):
    for j in range(21):
        u,v=F(i,20),F(j,20);p=project(surface(U,V,2,2,NET,u,v));x,y,z=p
        residual=abs((x*x+y*y+(z-z0)**2+R*R-r*r)**2-4*R*R*(x*x+y*y));assert residual<F(1,10**35);maxres=max(maxres,residual)
        assert x>=0 and y>=0 and z0-r<=z<=z0
# The profile meets the inner cylinder vertically and the lower plane horizontally.
assert project(PROFILE[0])==(R-r,z0) and project(PROFILE[-1])==(R,z0-r)
assert project(PROFILE[1])[0]==project(PROFILE[0])[0]
assert project(PROFILE[1])[1]==project(PROFILE[-1])[1]
lines=['% Torus fillet,R2,r3/5,zcenter6/5;theta0..90deg,phi180..270deg;true3x3 product-weight net.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-10,-8) rectangle (11,10);']
for j in range(3):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(NET[i][j]))) for i in range(3))+';')
for row in NET:
    lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(h))) for h in row)+';')
    lines.extend(r'\fill '+point(camera(project(h)))+r' circle[radius=1.5pt];' for h in row)
paths,report=grid(U,V,2,2,NET,camera,tuple(F(i,4) for i in range(5)),tuple(F(j,24) for j in range(25)))
lines+=paths
for end,name,anchor in [((F(5,2),0,0),'x','below left'),((0,F(5,2),0),'y','right'),((0,0,F(11,5)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_17.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/toroidal-fillet-patch-check.json').write_text(json.dumps({'figure':'8.13','major_radius':str(R),'minor_radius':str(r),'torus_axis_center_height':str(z0),'circumferential_angle_degrees':[0,90],'profile_angle_degrees':[180,270],'degrees':[2,2],'control_dimensions':[3,3],'exact_tensor_checks':tc,'torus_implicit_checks':441,'torus_residual_grid_max':str(maxres),'vertical_tangent_at_inner_cylinder':True,'horizontal_tangent_at_lower_plane':True,'weights_product_rule':True,'native_grid':report,'display':'transparent wireframe'},indent=2)+'\n')
print('PASS:441tensor/torus checks,residual<1e-35;actual3x3net,630isocurve identities and exact vertical/horizontal fillet tangent directions.')
