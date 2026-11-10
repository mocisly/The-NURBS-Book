"""Representative nine-control cubic for the two-weight geometric construction."""
from fractions import Fraction as F
from control_relocation_data import U,GRE
from native_bspline import de_boor
from rational_geometry import project
P=tuple(tuple(map(F,p)) for p in [(0,0),(2,0),(3,'1.8'),('1.5','3.3'),(4,6),('7.5','4.6'),('8.5',2),(6,0),('4.5','1.5')])
def homogeneous(W):return tuple(tuple(w*v for v in p)+(w,) for w,p in zip(W,P))
def curve(u,W):return project(de_boor(U,homogeneous(W),3,u))
def bary(u,W):
    N=[de_boor(U,tuple((F(i==k),) for i in range(9)),3,u)[0] for k in range(9)];den=sum(n*w for n,w in zip(N,W));return N[4]*W[4]/den,N[5]*W[5]/den
def blend(a,b):return tuple((1-a-b)*r+a*x+b*y for r,x,y in zip(R,P[4],P[5]))
UBAR=F(3,5);OLD=tuple(F(1,5) if i in (4,5) else F(1) for i in range(9));NEW=(F(1),)*9
R=curve(UBAR,tuple(F(0) if i in (4,5) else F(1) for i in range(9)))
def edge(t):return tuple((1-t)*a+t*b for a,b in zip(P[4],P[5]))
