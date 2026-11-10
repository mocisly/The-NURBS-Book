"""8.18:exact circular inversion controls,planar2x1patch and lifted great-circle edges."""
from pathlib import Path
from fractions import Fraction as F
import json
from projected_spherical_triangle_data import ARC,K,T,PLANAR_NET,C1,C2,C3
from stereographic_geometry import lift
from revolved_surface_data import camera
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor
from polynomial_native import multiply
from bspline_math import add
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_23.tex')['applied']
A,P,B=map(project,ARC);M=tuple((a+b)/2 for a,b in zip(A,B));O=(F(0),F(0));N=(F(0),F(0),F(2));r=F(2)
assert sum(x*y for x,y in zip(M,P))==r*r
alpha=r*r/sum(x*x for x in M);assert alpha==F(25,9) and tuple(alpha*x for x in M)==P
assert sum(x*x for x in M)/r**2==F(9,25)
ss=segments(K,ARC,2);U,V,W=ss[0]['power'];res=add(add(multiply(U,U),multiply(V,V)),tuple(-4*x for x in multiply(W,W)));assert all(x==0 for x in res)
assert W==(F(1),-F(4,5),F(4,5))
tc=verify_tensor(K,T,2,1,PLANAR_NET);checks=0
for i in range(21):
    s=F(i,20);uv=project(de_boor(K,ARC,2,s));assert uv[0]*uv[0]+uv[1]*uv[1]==4
    for j in range(21):
        t=F(j,20);p=project(surface(K,T,2,1,PLANAR_NET,s,t));assert p==(t*uv[0],t*uv[1],0)
        if t==0:assert p==(0,0,0)
for i in range(101):
    t=F(i,100);assert project(de_boor(K,C1,2,t))==lift(t*A[0],t*A[1])
    assert project(de_boor(K,C3,2,t))==lift(t*B[0],t*B[1])
    u,v=project(de_boor(K,ARC,2,t));assert project(de_boor(K,C2,2,t))==lift(u,v);checks+=3
lines=['% Exact projected radius2 circle arc with normalized middle weight3/5,all rational controls.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-12,-10) rectangle (13,14);'];cert=[];nc=0
for endpoint in (A,B):lines.append(r'\draw[book grid,dashed] '+point(camera(N))+'--'+point(camera(endpoint+(F(0),)))+';')
for endpoint in (A,B):lines.append(r'\draw[book grid] (0,0)--'+point(camera(endpoint+(F(0),)))+';')
lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(p+(F(0),))) for p in (A,P,B))+';')
lines.append(r'\draw[book grid,dashed] '+point(camera(A+(F(0),)))+'--'+point(camera(B+(F(0),)))+';')
lines.append(r'\draw[book grid,dashed] (0,0)--'+point(camera(P+(F(0),)))+';')
for H in (tuple((u,v,F(0),a) for u,v,a in ARC),C1,C2,C3):
    ss=segments(K,H,2);nc+=check(K,H,2,ss)
    # Every spherical boundary is a great circle of the sphere centered(0,0,1).
    if H in (C1,C2,C3):
        X,Y,Z,W=ss[0]['power'];zbar=add(Z,tuple(-x for x in W));res=add(add(multiply(X,X),multiply(Y,Y)),add(multiply(zbar,zbar),tuple(-x for x in multiply(W,W))))
        assert all(x==0 for x in res)
    hh=tuple(camera(h[:3])+(h[-1],) for h in H);parts=[part for s in segments(K,hh,2) for part in approximate(s['bern'],F(1,100000))]
    lines.extend(cubic_path(part) for part in parts);cert.append(str(max(part['certified_l1_error'] for part in parts)))
for end,name,anchor in [((F(7,2),0,0),'x','below left'),((0,F(3),0),'y','right'),((0,0,F(3)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
for p,label,anchor in [(A,r'\mathbf P_{0,1}','above left'),(P,r'\mathbf P_{1,1}','below right'),(B,r'\mathbf P_{2,1}','above right'),(M,r'\mathbf M','below left')]:
    lines.extend([r'\fill '+point(camera(p+(F(0),)))+r' circle[radius=1.5pt];',r'\node['+anchor+r'=7pt] at '+point(camera(p+(F(0),)))+' {$'+label+'$};'])
for H in (C1,C3):lines.append(r'\fill '+point(camera(project(H[-1])))+r' circle[radius=1.5pt];')
lines.extend([r'\fill '+point(camera(N))+r' circle[radius=1.5pt];',r'\node[right=7pt] at '+point(camera(N))+r' {$(0,0,2R)$};',r'\node[above left=7pt] at (0,0) {$\mathbf O$};',r'\node at (-1.4,-2.8) {$\mathbf S_2$};'])
for H,t,xy,name,anchor in [(C1,F(3,5),(-4.2,.8),'1','east'),(C2,F(1,2),(1.5,4.5),'2','south'),(C3,F(3,5),(5.7,1.5),'3','west')]:
    label='edge'+name;lines.append(r'\node[anchor='+anchor+'] ('+label+') at '+point(tuple(F(str(x)) for x in xy))+r' {$\mathbf C_'+name+'$};')
    lines.append(r'\draw[book grid] ('+label+'.'+anchor+')--'+point(camera(project(de_boor(K,H,2,t))))+';')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_23.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/projected-spherical-triangle-check.json').write_text(json.dumps({'figure':'8.18','R':1,'projected_arc_center':['0','0'],'projected_arc_radius':2,'projected_arc_controls':[list(map(str,p)) for p in (A,P,B)],'projected_arc_weights':['1','3/5','1'],'mid_chord':list(map(str,M)),'inversion_alpha':str(alpha),'OM_dot_OP_equals_r_squared':True,'complete_circle_power_identity_exact':True,'planar_patch_degrees':[2,1],'exact_tensor_checks':tc,'exact_radial_planar_patch_checks':441,'exact_lifted_boundary_checks':checks,'spherical_boundary_full_power_identities_exact':True,'native_curve_checks':nc,'native_boundary_screen_L1_error_bounds_cm':cert,'collapsed_t0_boundary':True},indent=2)+'\n')
print('PASS:exact radius2circle/inversion identities,441planar tensor/radial and303lifted-boundary checks;three full great-circle power identities and true2x1plane patch.')
