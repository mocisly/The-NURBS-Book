"""8.11: exact product-weight sphere construction,including collapsed polar rows."""
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
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_15.tex')['applied']
a=F(3,2);P=[(0,0,-a),(a,0,-a),(a,0,0),(a,0,a),(0,0,a)]
PROFILE=tuple(tuple(F(x)*b for x in p)+(b,) for i,p in enumerate(P) for b in [w if i%2 else F(1)])
V=(F(0),)*3+(F(1,2),)*2+(F(1),)*3
NET=tuple(tuple((x*rh,y*rh,b*zh,b*c) for rh,_,zh,c in PROFILE) for x,y,b in CIRCLE)
tc=verify_tensor(U,V,2,2,NET);bounds=[]
for s in segments(V,PROFILE,2):
    X,_,Z,W=s['power'];res=add(add(multiply(X,X),multiply(Z,Z)),tuple(-a*a*x for x in multiply(W,W)))
    bound=sum(map(abs,compose_affine(res,s['a'],s['b']-s['a'])))/w**2;assert bound<F(1,10**37);bounds.append(str(bound))
maxres=F(0)
for i in range(21):
    u=F(i,20);cx,cy=project(de_boor(U,CIRCLE,2,u))
    for j in range(21):
        v=F(j,20);rho,_,z=project(de_boor(V,PROFILE,2,v));h=surface(U,V,2,2,NET,u,v);p=project(h)
        assert p==(rho*cx,rho*cy,z) and h[-1]>=w*w
        residual=abs(sum(x*x for x in p)-a*a);maxres=max(maxres,residual);assert residual<F(1,10**36)
        if j in (0,20):assert p==(0,0,-a if j==0 else a)
assert NET[0]==NET[-1]
distinct={project(h) for row in NET for h in row};assert len(distinct)==26
lines=['% Quadratic sphere: radius3/2,full9pointcircle x5point semicircle,paired product weights.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-12,-13) rectangle (13,14);']
for j in (1,2,3):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(NET[i][j]))) for i in range(9))+';')
for row in NET[:-1]:lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(h))) for h in row)+';')
lines.extend(r'\fill '+point(camera(p))+r' circle[radius=1.3pt];' for p in sorted(distinct))
iso=nc=0;cert=[]
for variable,values in [('u',[F(i,12) for i in range(1,12)]),('v',[F(i,12) for i in range(12)])]:
    for fixed in values:
        K,p,Q=isocurve(U,V,2,2,NET,variable,fixed);ss=segments(K,Q,p);nc+=check(K,Q,p,ss)
        for j in range(21):
            t=F(j,20);assert de_boor(K,Q,p,t)==(surface(U,V,2,2,NET,t,fixed) if variable=='u' else surface(U,V,2,2,NET,fixed,t));iso+=1
        hh=tuple(camera(h[:3])+(h[-1],) for h in Q)
        parts=[part for s in segments(K,hh,p) for part in approximate(s['bern'],F(1,100000))]
        lines.extend(cubic_path(part) for part in parts);cert.append(str(max(part['certified_l1_error'] for part in parts)))
for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','right'),((0,0,F(16,5)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_15.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/sphere-revolution-check.json').write_text(json.dumps({'figure':'8.11','radius':str(a),'degrees':[2,2],'control_dimensions':[9,5],'distinct_controls':26,'weights_product_rule':True,'poles_collapsed_for_every_u':True,'exact_tensor_checks':tc,'exact_revolution_and_sphere_checks':441,'sphere_residual_grid_bound':str(maxres),'semicircle_whole_span_residual_bounds':bounds,'exact_isocurve_vs_surface_checks':iso,'native_curve_checks':nc,'parallels':'v=i/12,i=1..11','meridian_halfcircles':'u=i/12,i=0..11','native_isocurve_screen_L1_error_bounds_cm':cert,'display':'transparent wireframe','polar_partial_u':'identically zero since projected polar row is constant','polar_geometric_normals':'(0,0,-1),(0,0,1)'},indent=2)+'\n')
print('PASS:441 tensor/revolution/sphere checks,residual<1e-36;483isocurve identities,26distinct controls and both collapsed poles.')
