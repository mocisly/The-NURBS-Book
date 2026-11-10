"""Five explicitly defined centreline polylines, exact closest-segment distance.

These are semantic pen strokes for the book's polyline example, not font outlines
or scan traces. The same strokes drive all three panels and the surface heights.
"""
from fractions import Fraction as F
GLYPHS=[[(0,0),(0,1),(1,0),(1,1)],[(0,1),(0,'.25'),('.3',0),('.7',0),(1,'.25'),(1,1)],[(0,0),(0,1),('.7',1),(1,'.85'),(1,'.65'),('.5','.5'),(0,'.5'),('.5','.5'),(1,0)],[(0,0),(0,1),('.7',1),(1,'.85'),(1,'.65'),('.5','.5'),(0,'.5'),('.5','.5'),(1,'.35'),(1,'.15'),('.7',0),(0,0)],[(1,'.85'),('.7',1),('.3',1),(0,'.85'),(0,'.65'),(1,'.35'),(1,'.15'),('.7',0),('.3',0),(0,'.15')]]
STROKES=tuple(tuple((F(3,40)+i*F(9,50)+F(3,25)*F(x),F(3,10)+F(2,5)*F(y))for x,y in glyph)for i,glyph in enumerate(GLYPHS))
SEGMENTS=tuple((a,b)for line in STROKES for a,b in zip(line,line[1:]));RADIUS=F(1,100);DISTANCE=F(3,5)
K=(F(0),)*4+tuple(F(i,64)for i in range(1,64))+(F(1),)*4
G=tuple(sum(K[i+1:i+4])/3 for i in range(67))
def nearest(p):
    best=None
    for a,b in SEGMENTS:
        d=tuple(y-x for x,y in zip(a,b));den=sum(x*x for x in d);assert den>0;t=max(F(0),min(F(1),sum((x-y)*z for x,y,z in zip(p,a,d))/den));q=tuple(x+t*y for x,y in zip(a,d));distance=sum((x-y)**2 for x,y in zip(p,q))
        if best is None or distance<best[0]:best=(distance,q,t,a,b)
    return best
def make():
    selected=[];orthogonal=0;records=[]
    for i,u in enumerate(G):
        for j,v in enumerate(G):
            d2,q,t,a,b=nearest((u,v));assert d2==sum((x-y)**2 for x,y in zip((u,v),q)) and 0<=t<=1
            if 0<t<1:assert sum((x-y)*(z-w)for x,y,z,w in zip((u,v),q,b,a))==0;orthogonal+=1
            if d2<=RADIUS**2:selected.append((i,j));records.append(dict(index=(i,j),distance_squared=d2,projection=q,segment_parameter=t))
    ids=set(selected);P=tuple(tuple((8*u-4,8*v-4,DISTANCE if(i,j)in ids else F(0))for j,v in enumerate(G))for i,u in enumerate(G))
    assert all(P[i][j][2]==0 for i in range(67)for j in range(67)if i in(0,66)or j in(0,66))
    return P,dict(knots=K,degrees=(3,3),controls=P,control_shape=(67,67),strokes=STROKES,radius=RADIUS,distance=DISTANCE,selected_controls=selected,selected_count=len(selected),closest_point_checks=4489,orthogonal_projection_checks=orthogonal,selection_records=records,whole_boundary_curves_unchanged=True,global_z_bounds=(0,DISTANCE))
