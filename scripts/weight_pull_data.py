"""Representative cubic calibrated to BOTH printed single-weight target pairs.

Unknown original coordinates are not traced. Two controls are solved so that
the specified distances and weights in11.11/12 hold exactly along unit directions.
"""
from fractions import Fraction as F
from control_relocation_data import U,GRE
from native_bspline import de_boor,segments
from rational_geometry import project
W0=F(1,5);K=4
B=tuple((F(i==K),) for i in range(9))
def n(u):return de_boor(U,B,3,u)[0]
def ts(u,w):return w*n(u)/(1-n(u)+w*n(u))
P=[tuple(map(F,p)) for p in [(0,0),('.2',0),('.3','.18'),('.15','.33'),('.4','.6'),('.75','.46'),('.85','.2'),('.6',0),('.45','.15')]]
rows=[];rhs=[[],[]]
DIRECTIONS={F(13,25):(-F(3,5),F(4,5)),F(23,50):(F(3,5),F(4,5))}
for u,w in [(F(13,25),F(49,20)),(F(23,50),F(97,100))]:
    basis=[de_boor(U,tuple((F(i==j),) for i in range(9)),3,u)[0] for j in range(9)]
    rows.append((basis[3],basis[5]));distance=F(3,40)/(ts(u,w)-ts(u,W0))
    target=tuple(p-distance*v for p,v in zip(P[4],DIRECTIONS[u]))
    for axis in range(2):rhs[axis].append((1-basis[4])*target[axis]-sum(basis[i]*P[i][axis] for i in range(9) if i not in (3,4,5)))
a,b=rows[0];c,d=rows[1];det=a*d-b*c;assert det
for i in (3,5):P[i]=tuple((rhs[axis][0]*d-b*rhs[axis][1])/det if i==3 else (a*rhs[axis][1]-rhs[axis][0]*c)/det for axis in range(2))
P=tuple(P)
def homogeneous(w):return tuple(tuple((w if i==4 else 1)*x for x in p)+(w if i==4 else F(1),) for i,p in enumerate(P))
def curve(u,w):return project(de_boor(U,homogeneous(w),3,u))
def modified_weight(u,d):
    old=curve(u,W0);gap=(P[4][1]-old[1])/DIRECTIONS[u][1]
    R=ts(u,W0);return W0*(1+d/(R*(gap-d)))
for u,w in [(F(13,25),F(49,20)),(F(23,50),F(97,100))]:
    old,new=curve(u,W0),curve(u,w);assert tuple(y-x for x,y in zip(old,new))==tuple(F(3,40)*v for v in DIRECTIONS[u]);assert modified_weight(u,F(3,40))==w
