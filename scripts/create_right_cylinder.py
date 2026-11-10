"""8.3: prescribed nine-point circle extruded along its plane normal."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor
from polynomial_native import multiply
from bspline_math import add,compose_affine,derivative,evaluate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_03.tex')['applied']
def camera(p):
    x,y,z=p;return (4*(-F(39,50)*x+F(24,25)*y),4*(-x/2-F(3,10)*y+z))
D=10**40;n=isqrt(2*D*D);lo,hi=F(n,2*D),F(n+1,2*D);assert lo*lo<F(1,2)<hi*hi;w=(lo+hi)/2
circle=tuple(tuple(map(F,p)) for p in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)])
P=tuple((x,-F(3,2),z) for x,z in circle);delta=(F(0),F(3),F(0));W=tuple(F(1) if i%2==0 else w for i in range(9))
H=tuple(tuple(a*x for x in p)+(a,) for p,a in zip(P,W));net=tuple((h,(h[0],h[1]+3*h[-1],h[2],h[-1])) for h in H)
U=(F(0),)*3+(F(1,4),)*2+(F(1,2),)*2+(F(3,4),)*2+(F(1),)*3;V=(F(0),F(0),F(1),F(1));tensorchecks=verify_tensor(U,V,2,1,net);ss=segments(U,H,2);nc=check(U,H,2,ss)
bounds=[]
for s in ss:
    X,_,Z,T=s['power'];res=add(add(multiply(X,X),multiply(Z,Z)),tuple(-x for x in multiply(T,T)))
    bound=sum(map(abs,compose_affine(res,s['a'],s['b']-s['a'])))/w**2;assert bound<F(1,10**38);bounds.append(str(bound))
for i in range(21):
    u=F(i,20);base=project(de_boor(U,H,2,u))
    for j in range(21):
        v=F(j,20);h=surface(U,V,2,1,net,u,v);p=project(h)
        assert p==(base[0],-F(3,2)+3*v,base[2]) and h[-1]>=w
        assert abs(p[0]**2+p[2]**2-1)<F(1,10**38)
def tangent(s,u):
    h=[evaluate(p,u) for p in s['power']];dh=[evaluate(derivative(p),u) for p in s['power']]
    return tuple((dh[k]*h[-1]-h[k]*dh[-1])/h[-1]**2 for k in range(3))
for l,r in zip(ss,ss[1:]):assert tangent(l,l['b'])==tangent(r,r['a'])
assert tangent(ss[-1],1)==tangent(ss[0],0)
lines=['% Eq8.3: Ex7.2 nine-point circular control polygon embedded in XZ plane and translated alongY.',
       '% Unitradius,distance3,paired circle weights; common affine camera as8.1/8.2.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-11.5,-9.5) rectangle (12,10.5);']
for shift in (F(0),F(3)):
    pp=tuple((x,y+shift,z) for x,y,z in P);lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in pp)+';')
    lines.extend(r'\fill '+point(camera(p))+r' circle[radius=1.5pt];' for p in pp[:-1])
for x,y,z in P[:-1]:lines.append(r'\draw[book grid,dashed] '+point(camera((x,y,z)))+'--'+point(camera((x,y+3,z)))+';')
cert=[]
for shift in (F(0),F(3)):
    hh=tuple(camera((h[0],h[1]+shift*h[-1],h[2]))+(h[-1],) for h in H)
    paths=[p for s in segments(U,hh,2) for p in approximate(s['bern'],F(1,100000))];lines.extend(cubic_path(p) for p in paths)
    cert.append({'translation_y':str(shift),'screen_L1_error_cm':str(max(p['certified_l1_error'] for p in paths)),'native_paths':len(paths)})
# True silhouette generators: the projected circular tangent is parallel to delta.
M=10**40;nn=isqrt(39761*M*M);slo,shi=F(nn,M),F(nn+1,M);assert slo*slo<39761<shi*shi;r=(slo+shi)/2
for sign in (-1,1):
    x,z=sign*(-F(119)/r),sign*(F(160)/r);a=(x,-F(3,2),z);b=(x,F(3,2),z)
    assert abs(x*x+z*z-1)<F(1,10**38)
    tangent2=camera((-z,F(0),x));direction=camera(delta);assert direction[0]*tangent2[1]-direction[1]*tangent2[0]==0
    lines.append(r'\draw '+point(camera(a))+'--'+point(camera(b))+';')
for end,label,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','right'),((0,0,F(12,5)),'z','above')]:lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+label+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_03.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/right-cylinder-check.json').write_text(json.dumps({'figure':'8.3','circle_controls':[[str(x) for x in p] for p in circle],'profile_plane':'y=-3/2','translation':['0','3','0'],'weights_enclosure':list(map(str,(lo,hi))),'degrees':[2,1],'exact_homogeneous_tensor_checks':tensorchecks,'exact_extrusion_and_cylinder_checks':441,'whole_span_unit_radius_residual_bounds':bounds,'paired_weights_identical':True,'closedC1_cross_section_exact_for_common_enclosed_weight':True,'native_checks':nc,'true_projected_silhouette_generator_directions':'(-119,160)/sqrt39761 and antipode','native_rational_certificates':cert},indent=2)+'\n')
print('PASS:prescribed9point circle,441tensor/extrusion/cylinder checks,whole-span unitradius<1e-38,C1closure and exact projected silhouette directions.')
