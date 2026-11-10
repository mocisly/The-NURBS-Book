"""10.11explicit closed B section and spatial trajectory; exact sum tensor product."""
from fractions import Fraction as F
U=(F(0),)*4+(F(1,3),)*3+(F(2,3),)*3+(F(1),)*4
Q=tuple(tuple(map(F,p)) for p in [(0,0,'-1.2'),(0,'1.4','-1.2'),(0,'1.4',0),(0,0,0),(0,'1.4',0),(0,'1.4','1.2'),(0,0,'1.2'),(0,'-.35','1.2'),(0,'-.35','-1.2'),(0,0,'-1.2')])
V=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
T=tuple(tuple(map(F,p)) for p in [(-4,-1,0),(-2,-1,1),(-2,1,-1),(1,2,-1),(3,2,0),(3,2,4),(1,2,4)])
NET=tuple(tuple(tuple(a+b for a,b in zip(q,t)) for t in T) for q in Q)
def view(P):
    x,y,z=P
    return(F(8,5)*(F(4,5)*x+F(3,5)*y),F(8,5)*(-F(9,25)*x+F(12,25)*y+F(4,5)*z))
