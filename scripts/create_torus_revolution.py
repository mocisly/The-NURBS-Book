"""8.10: product-weight quadratic torus obtained by revolving an offset circle."""
from pathlib import Path
from fractions import Fraction as F
import json
from revolved_surface_data import U,CIRCLE,camera,w
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor,isocurve
from bspline_math import add,compose_affine
from polynomial_native import multiply
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_14.tex')['applied']
R,r=F(8,5),F(1,2);PROFILE=tuple((R*a+r*x,F(0),r*y,a) for x,y,a in CIRCLE)
NET=tuple(tuple((x*rh,y*rh,a*zh,a*b) for rh,_,zh,b in PROFILE) for x,y,a in CIRCLE)
tc=verify_tensor(U,U,2,2,NET);bounds=[]
for s in segments(U,CIRCLE,2):
    X,Y,W=s['power'];res=add(add(multiply(X,X),multiply(Y,Y)),tuple(-x for x in multiply(W,W)))
    bound=sum(map(abs,compose_affine(res,s['a'],s['b']-s['a'])))/w**2;assert bound<F(1,10**38);bounds.append(str(bound))
maxres=F(0)
for i in range(21):
    u=F(i,20);cx,cy=project(de_boor(U,CIRCLE,2,u))
    for j in range(21):
        v=F(j,20);rho,_,z=project(de_boor(U,PROFILE,2,v));h=surface(U,U,2,2,NET,u,v);x,y,zz=project(h)
        assert (x,y,zz)==(rho*cx,rho*cy,z) and h[-1]>=w*w
        residual=(x*x+y*y+z*z+R*R-r*r)**2-4*R*R*(x*x+y*y)
        maxres=max(maxres,abs(residual));assert abs(residual)<F(1,10**35)
assert NET[0]==NET[-1] and all(row[0]==row[-1] for row in NET)
lines=['% Semantic9x9 product-weight torus,R=8/5,r=1/2,common camera4cm.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-16,-9) rectangle (16,13);']
for j in range(8):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(NET[i][j]))) for i in range(9))+';')
for row in NET[:-1]:
    lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(h))) for h in row)+';')
    lines.extend(r'\fill '+point(camera(project(h)))+r' circle[radius=1.2pt];' for h in row[:-1])
iso=nc=0;cert=[]
for variable in ('u','v'):
    for i in range(12):
        fixed=F(i,12);K,p,Q=isocurve(U,U,2,2,NET,variable,fixed);ss=segments(K,Q,p);nc+=check(K,Q,p,ss)
        for j in range(21):
            t=F(j,20);assert de_boor(K,Q,p,t)==(surface(U,U,2,2,NET,t,fixed) if variable=='u' else surface(U,U,2,2,NET,fixed,t));iso+=1
        hh=tuple(camera(h[:3])+(h[-1],) for h in Q)
        parts=[part for s in segments(K,hh,p) for part in approximate(s['bern'],F(1,100000))]
        lines.extend(cubic_path(part) for part in parts);cert.append(str(max(part['certified_l1_error'] for part in parts)))
for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','right'),((0,0,F(13,5)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_14.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/torus-revolution-check.json').write_text(json.dumps({'figure':'8.10','major_radius':str(R),'minor_radius':str(r),'degrees':[2,2],'control_dimensions':[9,9],'distinct_controls':64,'weights_product_rule':True,'closed_both_directions':True,'exact_tensor_checks':tc,'exact_revolution_checks':441,'torus_implicit_residual_max_grid':str(maxres),'unit_circle_whole_span_residual_bounds':bounds,'exact_isocurve_vs_surface_checks':iso,'native_curve_checks':nc,'parallel_and_meridian_parameters':'i/12,i=0..11','native_isocurve_screen_L1_error_bounds_cm':cert,'display':'transparent wireframe,all controls retained'},indent=2)+'\n')
print('PASS:441 tensor/revolution/torus checks,residual<1e-35;504 isocurve identities,64distinct controls and closed product weights.')
