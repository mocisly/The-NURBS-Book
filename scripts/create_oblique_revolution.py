"""8.12:150degree rotation about an explicitly specified non-coordinate axis."""
from pathlib import Path
from fractions import Fraction as F
import json
from revolved_surface_data import P,V,camera
from certified_trig import cos_sin
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor,isocurve
from polynomial_native import multiply
from bspline_math import add,compose_affine
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_16.tex')['applied']
S=(F(4,5),-F(1),-F(6,5));T=(F(0),F(3,5),F(4,5));X=(F(1),F(0),F(0));Y=(F(0),F(4,5),-F(3,5))
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
assert all(dot(a,b)==F(i==j) for i,a in enumerate((X,Y,T)) for j,b in enumerate((X,Y,T)))
PROFILE=tuple((F(11,20)*r,F(2,5)+F(9,10)*z) for r,_,z in P)
w=cos_sin(F(75,2))[0];H=[]
for i in range(2):
    angle=F(15+75*i);c0,s0=cos_sin(angle);c1,s1=cos_sin(angle+F(75,2));c2,s2=cos_sin(angle+75)
    if not i:H.append((c0,s0,F(1)))
    H.extend(((c1,s1,w),(c2,s2,F(1))))
H=tuple(H);U=(F(0),)*3+(F(1,2),)*2+(F(1),)*3
NET=tuple(tuple(tuple(a*(s+t*h)+r*(x*ex+y*ey) for s,t,ex,ey in zip(S,T,X,Y))+(a,) for r,h in PROFILE) for x,y,a in H)
tc=verify_tensor(U,V,2,2,NET);bounds=[]
for seg in segments(U,H,2):
    A,B,W=seg['power'];res=add(add(multiply(A,A),multiply(B,B)),tuple(-z for z in multiply(W,W)))
    bound=sum(map(abs,compose_affine(res,seg['a'],seg['b']-seg['a'])))/w**2;assert bound<F(1,10**27);bounds.append(str(bound))
for i in range(21):
    u=F(i,20);cx,cy=project(de_boor(U,H,2,u))
    for j in range(21):
        v=F(j,20);r,h=de_boor(V,PROFILE,2,v);p=project(surface(U,V,2,2,NET,u,v))
        assert p==tuple(s+t*h+r*(cx*ex+cy*ey) for s,t,ex,ey in zip(S,T,X,Y))
        assert dot(tuple(p[k]-S[k] for k in range(3)),T)==h
        radial=tuple(p[k]-S[k]-h*T[k] for k in range(3));assert abs(dot(radial,radial)-r*r)<F(1,10**27)
lines=['% Semantic partial revolution: orthonormal frameX,Y,T; axisS+tT,angle15..165deg.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-12,-9) rectangle (11,11);'];nc=iso=0;cert=[]
for variable,values in [('u',[F(i,10) for i in range(11)]),('v',[F(i,16) for i in range(17)])]:
    for index,fixed in enumerate(values):
        K,p,Q=isocurve(U,V,2,2,NET,variable,fixed);ss=segments(K,Q,p);nc+=check(K,Q,p,ss)
        for j in range(21):
            t=F(j,20);assert de_boor(K,Q,p,t)==(surface(U,V,2,2,NET,t,fixed) if variable=='u' else surface(U,V,2,2,NET,fixed,t));iso+=1
        style='book line' if index in (0,len(values)-1) else 'book grid'
        if variable=='v':
            assert len(set(h[-1] for h in Q))==1
            lines.extend(cubic_path(part,style) for part in segments(K,tuple(camera(project(h)) for h in Q),p))
        else:
            hh=tuple(camera(h[:3])+(h[-1],) for h in Q)
            parts=[part for seg in segments(K,hh,p) for part in approximate(seg['bern'],F(1,100000))]
            lines.extend(cubic_path(part,style) for part in parts);cert.append(str(max(part['certified_l1_error'] for part in parts)))
for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(5,2),0),'y','right'),((0,0,F(12,5)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
axispoint=lambda t:tuple(s+t*v for s,v in zip(S,T))
lines.extend([r'\draw[book grid,dashed] '+point(camera(S))+'--'+point(camera(axispoint(F(24,5))))+';',
              r'\draw[book axis] '+point(camera(axispoint(F(19,5))))+'--'+point(camera(axispoint(F(24,5))))+r' node[above right=6pt] {$\mathbf T$};',
              r'\fill '+point(camera(S))+r' circle[radius=1.8pt];',r'\node[below left=7pt] at '+point(camera(S))+r' {$\mathbf S$};',r'\end{tikzpicture}'])
(root/'image_tex/ch08/fig_8_16.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/oblique-revolution-check.json').write_text(json.dumps({'figure':'8.12','axis_point':list(map(str,S)),'axis_unit_direction':list(map(str,T)),'orthonormal_radial_frame':[list(map(str,X)),list(map(str,Y))],'start_end_angles_degrees':[15,165],'angle_degrees':150,'profile_from8_8':'radius11/20 times original,height2/5+9/10 times original','degrees':[2,2],'control_dimensions':[5,6],'exact_tensor_checks':tc,'exact_rotation_frame_and_axial_height_checks':441,'circle_whole_span_residual_bounds':bounds,'exact_isocurve_checks':iso,'native_curve_checks':nc,'arc_parameters':'v=j/10','meridian_parameters':'u=i/16','native_arc_screen_L1_error_bounds_cm':cert,'axis_arrow_segment_physical_length':1,'common_camera_as8_8':True},indent=2)+'\n')
print('PASS:orthonormal tilted-axis frame,441tensor/rotation/axial-height identities,588isocurve checks;150deg arc and actual unit direction arrow.')

