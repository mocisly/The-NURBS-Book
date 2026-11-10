"""8.8: meridian,circular parallel,rotated meridian and corresponding control row."""
from pathlib import Path
from fractions import Fraction as F
import json
from revolved_surface_data import P,V,PROFILE,U,CIRCLE,NET,camera,lo,hi,w
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor
from bspline_math import add,compose_affine
from polynomial_native import multiply
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_12.tex')['applied']
tc=verify_tensor(U,V,2,2,NET);nc=check(V,PROFILE,2,segments(V,PROFILE,2));bounds=[]
for s in segments(U,CIRCLE,2):
    X,Y,W=s['power'];res=add(add(multiply(X,X),multiply(Y,Y)),tuple(-x for x in multiply(W,W)))
    bound=sum(map(abs,compose_affine(res,s['a'],s['b']-s['a'])))/w**2;assert bound<F(1,10**38);bounds.append(str(bound))
for i in range(21):
    u=F(i,20);cx,cy=project(de_boor(U,CIRCLE,2,u))
    for j in range(21):
        v=F(j,20);r,_,z=project(de_boor(V,PROFILE,2,v));h=surface(U,V,2,2,NET,u,v)
        assert project(h)==(r*cx,r*cy,z) and h[-1]>=w
assert project(de_boor(V,PROFILE,2,F(1,3)))==P[2]
assert project(de_boor(U,CIRCLE,2,F(1,4)))==(0,1)
row=tuple(project(NET[i][2]) for i in range(9));r,_,z=P[2]
assert row[0]==row[8]==P[2]
assert all(p[2]==z and max(abs(p[0]),abs(p[1]))==r for p in row)
lines=['% Semantic revolution diagram,exact quadratic six-control meridian;vbar=1/3 interpolatesP2.',
       '% ubar=1/4 is a90deg rotation; square control row2 is not the circle itself.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-16,-7) rectangle (16,20);',
       r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in P)+';',
       r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in row)+';']
anchors=['below right','below left','left','right','right','above left']
for i,p in enumerate(P):
    lines.append(r'\fill '+point(camera(p))+r' circle[radius=1.5pt];')
    if i!=2:lines.append(r'\node['+anchors[i]+r'=7pt] at '+point(camera(p))+r' {$\mathbf P_{'+str(i)+'}$};')
rowanchors={1:'below right',2:'below right',3:'right',4:'above right',5:'above left',6:'above left',7:'above left'}
for i,p in enumerate(row[:-1]):
    lines.append(r'\fill '+point(camera(p))+r' circle[radius=1.5pt];')
    if i:lines.append(r'\node['+rowanchors[i]+r'=7pt] at '+point(camera(p))+r' {$\mathbf P_{'+str(i)+',2}$};')
for rotated in (False,True):
    pp=tuple(camera((F(0),r,z) if rotated else (r,F(0),z)) for r,_,z in P)
    lines.extend(cubic_path(s) for s in segments(V,pp,2))
HH=tuple(camera((r*x,r*y,z*a))+(a,) for x,y,a in CIRCLE)
paths=[part for s in segments(U,HH,2) for part in approximate(s['bern'],F(1,100000))];lines.extend(cubic_path(part) for part in paths)
for end,name,anchor in [((F(14,5),0,0),'x','below left'),((0,F(14,5),0),'y','right'),((0,0,F(9,2)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
lines.append(r'\node[anchor=west] (p2label) at (-15.5,1) {$\mathbf P_{8,2}=\mathbf P_{0,2}=\mathbf P_2$};')
lines.append(r'\draw[book grid] (p2label.east)--'+point(camera(P[2]))+';')
v=F(4,5);pt=project(de_boor(V,PROFILE,2,v));lines.append(r'\node[anchor=east] (meridian) at (-10,13) {$\mathbf C(v)$};')
lines.append(r'\draw[book grid] (meridian.east)--'+point(camera(pt))+';')
u=F(3,8);pt=project(surface(U,V,2,2,NET,u,F(1,3)))
lines.append(r'\node[anchor=west] (parallel) at (12.6,3.5) {$\mathbf S(u,\bar v)$};');lines.append(r'\draw[book grid] (parallel.west)--'+point(camera(pt))+';')
pt=project(surface(U,V,2,2,NET,F(1,4),F(3,25)))
lines.append(r'\node[anchor=west] (rotated) at (10.5,-.5) {$\mathbf S(\bar u,v)$};');lines.append(r'\draw[book grid] (rotated.west)--'+point(camera(pt))+';')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_12.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/revolution-definition-check.json').write_text(json.dumps({'figure':'8.8','profile_controls':[[str(x) for x in p] for p in P],'profile_knots':list(map(str,V)),'degrees':[2,2],'weights_product_rule':True,'vbar':'1/3','ubar':'1/4','exact_tensor_checks':tc,'exact_revolution_identities':441,'profile_checks':nc,'circle_whole_span_residual_bounds':bounds,'vbar_exactly_interpolates_controlP2':True,'control_row2_square_half_width':'9/5','closed_row0_equals8_equals_profileP2':True,'circle_weight_enclosure':list(map(str,(lo,hi))),'native_circle_screen_L1_error_cm':str(max(part['certified_l1_error'] for part in paths))},indent=2)+'\n')
print('PASS:441 tensor/revolution identities,exactvbar=P2 and90deg rotated meridian;9-point square row and product weights;circle residual<1e-38.')
