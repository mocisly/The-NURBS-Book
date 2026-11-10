"""8.2: exact rational extrusion, paired control weights and true fixed-u/fixed-v curves."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,de_boor,point,cubic_path
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor
from bspline_math import derivative,evaluate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_02.tex')['applied']
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,t):return tuple(t*x for x in a)
def camera(p):
    x,y,z=p;return (4*(-F(39,50)*x+F(24,25)*y),4*(-x/2-F(3,10)*y+z))
A=(-F(13,10),-F(3,2),F(9,10));B=(F(4,5),-F(3,2),F(3,2));C=(-F(3,10),-F(3,2),-F(8,5))
TA=(-F(3,5),F(0),-F(3,5));TB=(F(1),F(0),-F(1));TC=(-F(1),F(0),F(1,5))
P=(A,add(A,mul(TA,F(1,3))),add(B,mul(TB,-F(1,3))),B,add(B,mul(TB,F(1,3))),add(C,mul(TC,-F(1,3))),C,add(C,mul(TC,F(1,3))),add(A,mul(TA,-F(1,3))),A)
W=tuple(F(1) if i%3==0 else F(2,3) for i in range(10));H=tuple(tuple(w*x for x in p)+(w,) for p,w in zip(P,W))
U=(F(0),)*4+(F(1,3),)*3+(F(2,3),)*3+(F(1),)*4;V=(F(0),F(0),F(1),F(1));delta=(F(0),F(3),F(0));unit=(F(0),F(1),F(0));assert sum(x*x for x in unit)==1
net=tuple((h,tuple(x+w*t for x,t in zip(h[:3],delta))+(w,)) for h,w in zip(H,W));tensorchecks=verify_tensor(U,V,3,1,net)
ss=segments(U,H,3);nativechecks=check(U,H,3,ss)
def tangent(s,u):
    h=[evaluate(p,u) for p in s['power']];dh=[evaluate(derivative(p),u) for p in s['power']]
    return tuple((dh[k]*h[-1]-h[k]*dh[-1])/h[-1]**2 for k in range(3))
for l,r in zip(ss,ss[1:]):assert tangent(l,l['b'])==tangent(r,r['a'])
assert tangent(ss[-1],1)==tangent(ss[0],0)
for i in range(21):
    u=F(i,20);base=project(de_boor(U,H,3,u))
    for j in range(21):
        v=F(j,20);S=project(surface(U,V,3,1,net,u,v));assert S==add(base,mul(delta,v))
        assert S==add(project(surface(U,V,3,1,net,u,0)),mul(delta,v))
        assert surface(U,V,3,1,net,u,v)[-1]>=F(2,3)
lines=['% Representative closedC1 cubic rational profile,3Bezier spans; all paired weights identical.',
       '% Exact extrusion delta=(0,3,0), unitW=(0,1,0), d=3. Same affine camera as8.1.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-12,-10) rectangle (13,11);']
# Dashed polygons are actual control data, not sampled surface contours.
for v in (F(0),F(1)):
    controls=tuple(add(p,mul(delta,v)) for p in P);lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in controls)+';')
    lines.extend(r'\fill '+point(camera(p))+r' circle[radius=1.4pt];' for p in controls[:-1])
for p in P[:-1]:lines.append(r'\draw[book grid,dashed] '+point(camera(p))+'--'+point(camera(add(p,delta)))+';')
certificates=[]
for v in (F(0),F(1,2),F(1)):
    projected=tuple(camera(tuple(x+w*v*t for x,t in zip(h[:3],delta)))+(w,) for h,w in zip(H,W))
    paths=[piece for seg in segments(U,projected,3) for piece in approximate(seg['bern'],F(1,100000))]
    lines.extend(cubic_path(p,'dashed' if v==F(1,2) else '') for p in paths)
    certificates.append({'fixed_v':str(v),'native_paths':len(paths),'screen_L1_error_cm':str(max(p['certified_l1_error'] for p in paths))})
for u in (F(0),F(1,3),F(1,2),F(2,3)):
    base=project(de_boor(U,H,3,u));lines.append(r'\draw[book grid] '+point(camera(base))+'--'+point(camera(add(base,delta)))+';')
for end,label,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','right'),((0,0,F(12,5)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+label+'$};')
# Callouts point to the actual parameter curves named in equation8.2.
def callout(label,start,target,anchor):
    lines.append(r'\draw[book axis,book grid] '+point(start)+r' node['+anchor+r'=5pt] {$'+label+'$}--'+point(camera(target))+';')
def at(u,v):return add(project(de_boor(U,H,3,u)),mul(delta,v))
callout(r'\mathbf C(u)',(-F(21,2),F(1)),at(F(1,2),F(0)),'left')
callout(r'\mathbf C(u)+d\mathbf W',(F(11),-F(15,2)),at(F(1,2),F(1)),'right')
callout(r'u=\bar u', (F(7),F(7)),at(F(1,2),F(3,4)),'above')
callout(r'v=\bar v', (-F(7),F(19,2)),at(F(1,6),F(1,2)),'above')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_02.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/general-cylinder-check.json').write_text(json.dumps({'figure':'8.2','representative_profile_controls':[[str(x) for x in p] for p in P],'profile_knots':list(map(str,U)),'profile_weights':list(map(str,W)),'unit_W':list(map(str,unit)),'distance':'3','translation':list(map(str,delta)),'exact_tensor_evaluation_checks':tensorchecks,'exact_projected_extrusion_identities':441,'exact_closedC1_profile':True,'paired_control_weights_identical':True,'global_denominator_lower_bound':'2/3','native_curve_checks':nativechecks,'projected_rational_curve_certificates':certificates,'wireframe_transparent':True},indent=2)+'\n')
print('PASS:441exact homogeneous tensor and441projected extrusion identities;paired weights,closedC1profile,true fixed-u lines and translated fixed-v curves certified.')
