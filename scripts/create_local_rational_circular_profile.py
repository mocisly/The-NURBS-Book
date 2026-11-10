"""9.27: computed local rational profile, four-point circles and two corners."""
from pathlib import Path
from fractions import Fraction as F
import json
from local_quadratic_interpolator import interpolate,add,mul,cross,dot
from native_bspline import cubic_path,point,segments
from rational_geometry import approximate,evaluate,project
from polynomial_native import multiply
from bspline_math import add as polyadd
from revolved_surface_data import w
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_33.tex')['applied']
Q=tuple(tuple(map(F,q)) for q in [('0','0'),('0','2'),('0','5'),('1.5','6.5'),('5','6.5'),('8.5','6.5'),('8.5','4'),('6','4'),('3.5','4'),('2.5','3'),('2.5','1'),('2.5','0'),('1.25','0'),('0','0')])
outer,proof=interpolate(Q,'akima',corners=True,closed=True)
assert proof['flagged_corner_indices']==[0,11] and sum(not x['G1'] for x in proof['joins'])==2
circle_checks=[];out=['% Computed periodic Akima rational interpolation;representative circular mechanical profile.',r'\begin{tikzpicture}[book line,x=2.7cm,y=2.7cm]',r'\path[use as bounding box] (-.5,-.5) rectangle (10.3,7);']
K=(F(0),)*3+(F(1),)*3
def rational_arc(tri):
    A,R,B=tri;va=add(R,A,-1);vb=add(R,B,-1)
    if cross(va,vb)==0:
        out.append(cubic_path(dict(bern=tri)));return
    assert dot(va,va)==dot(vb,vb) and dot(va,vb)==0
    # Every curved triangle in this representative example is a right isosceles
    # triangle. Eq7.33 gives w=cos45=sqrt2/2; w has certified40digit enclosure.
    H=tuple(tuple(ww*x for x in p)+(ww,) for p,ww in zip(tri,(F(1),w,F(1))))
    O=add(add(A,B),R,-1);r2=dot(add(A,O,-1),add(A,O,-1))
    power=segments(K,H,2)[0]['power'];W=power[2]
    X=polyadd(power[0],tuple(-O[0]*a for a in W));Y=polyadd(power[1],tuple(-O[1]*a for a in W))
    residual=polyadd(polyadd(multiply(X,X),multiply(Y,Y)),tuple(-r2*a for a in multiply(W,W)))
    bound=sum(map(abs,residual));assert bound<F(1,10**36)
    parts=approximate(H,F(1,100000));out.extend(cubic_path(s) for s in parts)
    for j in range(41):
        p=project(evaluate(H,F(j,40)));assert abs(dot(add(p,O,-1),add(p,O,-1))-r2)<F(1,10**36)
    circle_checks.append(dict(center=list(map(str,O)),radius_squared=str(r2),weight='sqrt2/2',whole_polynomial_circle_residual=str(bound),sample_checks=41,native_pieces=len(parts),certified_native_l1_error='1e-5'))
for s in outer:rational_arc(s['bern'])
for C in ((F(3,2),F(5)),(F(17,2),F(21,4))):
    r=F(3,4);P=tuple(add(C,p,r) for p in ((1,0),(0,1),(-1,0),(0,-1),(1,0)))
    pieces,rep=interpolate(P,'akima',closed=True)
    assert len(pieces)==4 and all(x['G1'] for x in rep['joins'])
    for s in pieces:rational_arc(s['bern'])
    out.extend(r'\draw '+point(p)+r' circle[radius=2.4pt];' for p in P[:-1])
out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in Q[:-1]);out.append(r'\end{tikzpicture}')
assert len(circle_checks)==12
(root/'image_tex/ch09/fig_9_33.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/local-rational-circular-profile-check.json').write_text(json.dumps(dict(figure='9.27',outer_construction=proof,outer_distinct_data_points=len(Q)-1,two_four_point_circles=True,closed_outer_boundary=True,exact_corner_indices=[0,11],rational_weight_formula='cos45=sqrt2/2',certified_weight_precision_digits=40,circular_pieces=circle_checks,straight_segments_exact=True),indent=2)+'\n')
print('PASS9.27:periodic Akima13outer data,exact two corners and straight runs;12rational quartercircles,whole circle identities<1e-36,2holes from4points each,certified native paths.')
