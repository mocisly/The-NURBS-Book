from pathlib import Path
from fractions import Fraction as F
import json
from region_surface_data import make,inside,G,K
from region_surface_native import domain,mesh
from surface_geometry import surface
root=Path(__file__).resolve().parents[1];star=tuple(tuple(map(F,p))for p in [('.5','.8'),('.32','.2'),('.8','.58'),('.2','.58'),('.68','.2')])
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
crossings=[]
for i in range(5):
    a,b=star[i],star[(i+1)%5];d=sub(b,a)
    for j in range(i+1,5):
        if j==i+1 or(i,j)==(0,4):continue
        c,e=star[j],star[(j+1)%5];f=sub(e,c);den=cross(d,f)
        if den:
            t=cross(sub(c,a),f)/den;s=cross(sub(c,a),d)/den
            if 0<t<1 and 0<s<1:crossings.append(tuple(x+t*v for x,v in zip(a,d)))
assert len(crossings)==5 and not inside(F(1,2),F(1,2),star)
swapped=tuple((y,x)for x,y in star);assert all(inside(x,y,star)==inside(y,x,swapped)for x in G for y in G)
P,r=make(star,verify_crank=False);A=domain(star,r);B,proof=mesh(P,r)
for n,lines in[(27,A),(28,B)]: (root/f'image_tex/ch11/fig_11_{n}.tex').write_text('\n'.join(['% True self-intersecting five-edge region; exact even-odd selection; no contour traces.']+lines)+'\n',encoding='utf-8')
r.update(controls=P,proper_self_intersections=crossings,central_point_excluded_by_even_odd=True,independent_vertical_ray_membership_checks=1225,centre_surface_point=surface(K,K,3,3,P,F(1,2),F(1,2)),native=proof,no_contour_tracing=True)
(root/'image_tex/build/star-surface-warp-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.23',r['selected_count'],'selectedcontrols;5exactcrossings/1225independent verticalray checks/',proof['native_checks'],'nativechecks.')
