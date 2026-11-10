"""Fig6.2: real closest-point fibres, endpoint cones and a C0 corner cone."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from rational_geometry import evaluate
from projection_certificate import certify

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_02.tex'
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch06/fig_6_02.tex')['applied']
pieces=[tuple(tuple(F(str(x)) for x in p) for p in pts) for pts in
        [[(0,0),(2,6),(5,3),(7,1)],[(7,1),(8,2.5),(8.5,5),(9,7)]]]
U=(F(0),)*4+(F('.7'),)*3+(F(1),)*4;P=pieces[0]+pieces[1][1:]
ss=segments(U,P,3);checks=check(U,P,3,ss)
assert [s['bern'] for s in ss]==pieces
fibres=[];rays=[];reductions=0

def add(foot,direction,length,anchors,kind,parameter):
    global reductions
    normal=tuple(x/sum(map(abs,direction)) for x in direction);used=length
    for attempt in range(10):
        Q=tuple(x+used*d for x,d in zip(foot,normal));proof=certify(pieces,Q,foot,anchors)
        if proof is not None:break
        used/=2
    else:raise AssertionError((kind,parameter,direction))
    reductions+=attempt
    rays.append({'kind':kind,'parameter':str(parameter),'target':list(map(str,Q)),
                 'foot':list(map(str,foot)),'signed_L1_offset':str(used),'certificate':proof})
    return Q

for index,divisions in [(0,32),(1,15)]:
    Q=pieces[index];derivatives=tuple(tuple(3*(b-a) for a,b in zip(x,y)) for x,y in zip(Q,Q[1:]))
    for i in range(1,divisions):
        t=F(i,divisions);foot=evaluate(Q,t);dx,dy=evaluate(derivatives,t);normal=(dy,-dx)
        plus=add(foot,normal,F(7,5),{index:t},'smooth',t)
        minus=add(foot,tuple(-x for x in normal),F(19,20),{index:t},'smooth',t)
        assert sum(a*b for a,b in zip((dx,dy),normal))==0
        fibres.append((plus,minus))
# Rational directions cover the global outward cones at the two endpoints.
directions=[(F(-1),F(i,10)) for i in range(2,-11,-1)]+[(F(i,10),F(-1)) for i in range(-9,2)]
for d in directions:
    foot=pieces[0][0];Q=add(foot,d,F(7,5),{0:F(0)},'start_endpoint',F(0));fibres.append((Q,foot))
directions=[(F(1),F(i,10)) for i in range(-2,11)]+[(F(i,10),F(1)) for i in range(9,-3,-1)]
for d in directions:
    foot=pieces[1][-1];Q=add(foot,d,F(7,5),{1:F(1)},'end_endpoint',F(1));fibres.append((Q,foot))
# The left tangent(6,-6), right tangent(3,4.5) define an exterior normal cone.
# Each proposed corner point is independently certified against BOTH full pieces.
directions=[(F(-1)+F(i,10),F(-1)) for i in range(25)]
for d in directions:
    if 6*d[0]-6*d[1]<0 or 3*d[0]+F(9,2)*d[1]>0:continue
    foot=pieces[0][-1];Q=add(foot,d,F(5,2),{0:F(1),1:F(0)},'C0_corner',F('.7'));fibres.append((Q,foot))
lines=['% Explicit representative two-span cubic with a C0 turn at u=.7.',
       '% EVERY fibre endpoint has an exact global distance-minimum certificate.',
       '% Smooth fibres are normal; endpoint/corner fans lie in their outward cones.',
       r'\begin{tikzpicture}[book line,x=1.5cm,y=1.5cm]',r'\path[use as bounding box] (-1.8,-1.8) rectangle (10.8,8.8);']
for a,b in fibres:lines.append(r'\draw[book grid] '+point(a)+'--'+point(b)+';')
for s in ss:lines.append(cubic_path(s))
lines.append(r'\end{tikzpicture}');target.parent.mkdir(exist_ok=True);target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-projection-set-check.json').write_text(json.dumps({
    'figure':'6.2','representative_controls':[[str(x) for x in p] for p in P],'knots':list(map(str,U)),
    'native_checks':checks,'projection_points':len(rays),'drawn_fibres':len(fibres),
    'offset_halvings_required_for_valid_global_projections':reductions,
    'smooth_normals_exact':True,'corner_is_explicitly_C0':True,
    'every_drawn_point_has_whole_curve_projection_certificate':True,'rays':rays},indent=2)+'\n')
print(f'PASS:{checks} native checks,{len(rays)} exact global projection certificates;{len(fibres)} fibres,endpoint/C0 cones distinguished.')
