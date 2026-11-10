"""One exact representative curve satisfying BOTH printed11.15/16 targets."""
from fractions import Fraction as F
from native_bspline import de_boor
from rational_geometry import project
U=(F(0),)*4+tuple(map(F,('.2','.35','.5','.71','.878')))+(F(1),)*4
GRE=tuple(sum(U[i+1:i+4])/3 for i in range(9));assert (GRE[4]+GRE[5])/2==F(76,125)
P=[tuple(map(F,p)) for p in [(0,0),('.2',0),('.3','.18'),('.15','.33'),('.4','.6'),('.75','.46'),('.85','.2'),('.6',0),('.45','.15')]]
OLD=tuple(F(1,20) if i in (4,5) else F(1) for i in range(9))
CASES={15:(F(76,125),tuple(F(123,100) if i in(4,5) else F(1) for i in range(9)),(F(192,1033),F(1015,1033))),16:(F(153,250),tuple(F(189,100) if i==4 else F(12,25) if i==5 else F(1) for i in range(9)),(-F(8,17),F(15,17)))}
def basis(u,W):
    N=[de_boor(U,tuple((F(i==k),) for i in range(9)),3,u)[0] for k in range(9)];den=sum(n*w for n,w in zip(N,W));return tuple(n*w/den for n,w in zip(N,W))
rows=[];rhs=[[],[]]
for fig,(u,W,D) in CASES.items():
    assert sum(x*x for x in D)==1
    old,new=basis(u,OLD),basis(u,W);delta=tuple(b-a for a,b in zip(old,new));rows.append((delta[4],delta[5]))
    for axis in range(2):rhs[axis].append(F(11,125)*D[axis]-sum(delta[i]*P[i][axis] for i in range(9) if i not in(4,5)))
a,b=rows[0];c,d=rows[1];det=a*d-b*c;assert det
for i in(4,5):P[i]=tuple((rhs[axis][0]*d-b*rhs[axis][1])/det if i==4 else (a*rhs[axis][1]-rhs[axis][0]*c)/det for axis in range(2))
P=tuple(P)
def homogeneous(W):return tuple(tuple(w*v for v in p)+(w,) for w,p in zip(W,P))
def curve(u,W):return project(de_boor(U,homogeneous(W),3,u))
def case(fig):
    u,W,D=CASES[fig];A,Z=curve(u,OLD),curve(u,W);R=curve(u,tuple(F(0) if i in(4,5) else F(1) for i in range(9)));N=basis(u,OLD);a,b=N[4:6];Q=tuple((a*x+b*y)/(a+b) for x,y in zip(P[4],P[5]))
    assert tuple(y-x for x,y in zip(A,Z))==tuple(F(11,125)*v for v in D)
    cross=lambda x,y:x[0]*y[1]-x[1]*y[0]
    sub=lambda x,y:tuple(a-b for a,b in zip(x,y))
    if fig==15:assert cross(sub(Q,R),sub(Z,A))==0 and W[4]==W[5]
    else:assert cross(sub(Q,R),sub(Z,A))!=0 and W[4]!=W[5]
    return dict(figure=fig,parameter=u,old_weights=OLD,new_weights=W,controls=P,knots=U,greville=GRE,unit_direction=D,exact_displacement=tuple(F(11,125)*v for v in D),exact_distance_squared=F(11,125)**2,old_point=A,new_point=Z,R=R,Q=Q,ratio_preserved=fig==15)
