"""8.4: open240degree ellipse arc extruded normally, with a true two-row NURBS net."""
from pathlib import Path
from fractions import Fraction as F
import json
from certified_trig import cos_sin
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor
from bspline_math import add,compose_affine
from polynomial_native import multiply
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_04.tex')['applied']
def camera(p):
    x,y,z=p;return (4*(-F(39,50)*x+F(24,25)*y),4*(-x/2-F(3,10)*y+z))
axis1,axis2=F(1),F(3,2);w=cos_sin(F(40))[0];H=[]
for i in range(3):
    first=F(120-80*i);mid=first-40;last=first-80
    c0,s0=cos_sin(first);c1,s1=cos_sin(mid);c2,s2=cos_sin(last)
    if i==0:H.append((axis1*c0,-F(3,2),axis2*s0,F(1)))
    H.extend(((axis1*c1,-F(3,2)*w,axis2*s1,w),(axis1*c2,-F(3,2),axis2*s2,F(1))))
H=tuple(H);P=tuple(map(project,H));U=(F(0),)*3+(F(1,3),)*2+(F(2,3),)*2+(F(1),)*3;V=(F(0),F(0),F(1),F(1));net=tuple((h,(h[0],h[1]+3*h[-1],h[2],h[-1])) for h in H)
ss=segments(U,H,2);nc=check(U,H,2,ss);tensorchecks=verify_tensor(U,V,2,1,net);bounds=[]
for s in ss:
    X,_,Z,T=s['power'];res=add(add(multiply(X,X),tuple(z/axis2**2 for z in multiply(Z,Z))),tuple(-x for x in multiply(T,T)))
    bound=sum(map(abs,compose_affine(res,s['a'],s['b']-s['a'])))/w**2;assert bound<F(1,10**27);bounds.append(str(bound))
for i in range(21):
    u=F(i,20);base=project(de_boor(U,H,2,u))
    for j in range(21):
        v=F(j,20);h=surface(U,V,2,1,net,u,v);p=project(h)
        assert p==(base[0],-F(3,2)+3*v,base[2]) and h[-1]>=w
        assert abs(p[0]*p[0]+p[2]*p[2]/axis2**2-1)<F(1,10**27)
assert project(de_boor(U,H,2,F(1,2)))==(1,-F(3,2),0)
lines=['% Representative open ellipse arc inXZ plane: radii1,3/2; angles120->-120 clockwise240deg,3equal80deg spans.',
       '% Paired control weights and normal extrusion delta(0,3,0); shared camera with8.1-8.3.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-11.5,-10) rectangle (12,11);'];cert=[]
for shift in (F(0),F(3)):
    pp=tuple((x,y+shift,z) for x,y,z in P);lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in pp)+';')
    lines.extend(r'\fill '+point(camera(p))+r' circle[radius=1.5pt];' for p in pp)
    hh=tuple(camera((h[0],h[1]+shift*h[-1],h[2]))+(h[-1],) for h in H)
    paths=[p for s in segments(U,hh,2) for p in approximate(s['bern'],F(1,100000))];lines.extend(cubic_path(p) for p in paths)
    cert.append({'translation_y':str(shift),'screen_L1_error_cm':str(max(p['certified_l1_error'] for p in paths)),'native_paths':len(paths)})
for i,(x,y,z) in enumerate(P):lines.append(r'\draw['+('book line' if i in (0,len(P)-1) else 'book grid,dashed')+'] '+point(camera((x,y,z)))+'--'+point(camera((x,y+3,z)))+';')
for end,label,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','right'),((0,0,F(12,5)),'z','above')]:lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+label+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_04.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/elliptic-cylinder-patch-check.json').write_text(json.dumps({'figure':'8.4','representative_radii':['1','3/2'],'start_angle_degrees':120,'end_angle_degrees':-120,'equal_angular_spans':3,'profile_homogeneous_controls':[[str(v) for v in h] for h in H],'translation':['0','3','0'],'degrees':[2,1],'native_curve_checks':nc,'exact_homogeneous_tensor_checks':tensorchecks,'exact_extrusion_and_ellipse_checks':441,'whole_span_ellipse_residual_bounds':bounds,'trig_coordinate_error_bound':'1e-29','native_rational_certificates':cert,'open_patch_boundary_generators_at_both_arc_ends':True},indent=2)+'\n')
print('PASS:open3span240deg ellipse,441tensor/extrusion/ellipse identities,paired weights,unit-normal sweep and actual boundary generators certified.')
