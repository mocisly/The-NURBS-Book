"""8.6: a genuine quadratic-by-linear rational right-cone patch."""
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
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_09.tex')['applied']
def camera(p):
    x,y,z=p;return (4*(-F(39,50)*x+F(24,25)*y),4*(-x/2-F(3,10)*y+z))
w=cos_sin(F(45))[0];height=F(23,10);H=[]
for i in range(3):
    a=F(135+90*i);c0,s0=cos_sin(a);c1,s1=cos_sin(a+45);c2,s2=cos_sin(a+90)
    if not i:H.append((c0,s0,F(0),F(1)))
    H.extend(((c1,s1,F(0),w),(c2,s2,F(0),F(1))))
H=tuple(H);P=tuple(map(project,H));A=(F(0),F(0),height)
U=(F(0),)*3+(F(1,3),)*2+(F(2,3),)*2+(F(1),)*3;V=(F(0),F(0),F(1),F(1))
net=tuple((h,(F(0),F(0),height*h[-1],h[-1])) for h in H)
ss=segments(U,H,2);nc=check(U,H,2,ss);tc=verify_tensor(U,V,2,1,net);bounds=[]
for s in ss:
    X,Y,_,T=s['power'];res=add(add(multiply(X,X),multiply(Y,Y)),tuple(-x for x in multiply(T,T)))
    bound=sum(map(abs,compose_affine(res,s['a'],s['b']-s['a'])))/w**2
    assert bound<F(1,10**27);bounds.append(str(bound))
for i in range(21):
    u=F(i,20);base=project(de_boor(U,H,2,u))
    for j in range(21):
        v=F(j,20);h=surface(U,V,2,1,net,u,v);p=project(h)
        assert p==tuple((1-v)*x+v*y for x,y in zip(base,A)) and h[-1]>=w
        assert abs(p[0]**2+p[1]**2-(1-p[2]/height)**2)<F(1,10**27)
        if v==1:assert p==A
lines=['% Semantic right cone: unit circular arc135..405deg,apex(0,0,23/10).',
       '% Seven paired weights; collapsed second control row. Same affine camera as8.1-8.4.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-7.5,-5) rectangle (8.7,11);',
       r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in P)+';']
for p in P:
    lines.append(r'\draw[book grid,dashed] '+point(camera(p))+'--'+point(camera(A))+';')
    lines.append(r'\fill '+point(camera(p))+r' circle[radius=1.5pt];')
for u in (F(0),F(1,2),F(1)):
    lines.append(r'\draw '+point(camera(project(de_boor(U,H,2,u))))+'--'+point(camera(A))+';')
hh=tuple(camera(h[:3])+(h[-1],) for h in H)
paths=[p for s in segments(U,hh,2) for p in approximate(s['bern'],F(1,100000))]
lines.extend(cubic_path(p) for p in paths)
for end,label,anchor in [((F(2),0,0),'x','below left'),((0,F(2),0),'y','right'),((0,0,F(27,10)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+label+'$};')
lines.extend([r'\fill '+point(camera(A))+r' circle[radius=1.5pt];',r'\node[right=7pt] at '+point(camera(A))+r' {$\mathbf P$};',r'\end{tikzpicture}'])
(root/'image_tex/ch08/fig_8_09.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/right-cone-patch-check.json').write_text(json.dumps({'figure':'8.6','base_radius':1,'base_angles_degrees':[135,405],'height':str(height),'degrees':[2,1],'control_net_dimensions':[7,2],'paired_weights_identical':True,'collapsed_second_row_at_apex':True,'native_curve_checks':nc,'exact_tensor_checks':tc,'exact_affine_ruling_and_cone_checks':441,'whole_span_circle_residual_bounds':bounds,'trig_coordinate_error_bound':'1e-29','native_curve_screen_L1_error_cm':str(max(p['certified_l1_error'] for p in paths)),'view':'transparent control net; solid arc,patch boundary rays and central ruling'},indent=2)+'\n')
print('PASS:441 exact affine cone/tensor evaluations,collapsed apex row,same paired weights;whole-span circle/cone residual<1e-27.')
