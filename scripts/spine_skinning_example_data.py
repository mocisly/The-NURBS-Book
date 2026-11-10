"""Representative shared data for10.4 onward; exact PH spine and normal frames."""
from fractions import Fraction as F
from math import comb
from native_bspline import de_boor,segments
from bspline_math import evaluate,derivative
SPINE_POWER=((F(0),F(9),F(0),-F(12),F(18),-F(36,5)),(F(3),F(0),-F(18),F(12),F(0),F(0)),(F(0),)*6)
SPINE_K=(F(0),)*6+(F(1),)*6
SPINE_P=tuple(tuple(sum(SPINE_POWER[d][j]*F(comb(i,j),comb(5,j)) for j in range(i+1)) for d in range(3)) for i in range(6))
assert segments(SPINE_K,SPINE_P,5)[0]['power']==SPINE_POWER
V_HAT=tuple(map(F,('0','1/4','1/2','39/50','1')))
U_HAT=(F(1,2),)*5
SECTION_K=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
PROFILE_A=tuple(tuple(map(F,row)) for row in [
    [-1,'-.1','.5','.8','.5','-.1',-1],
    ['-.7','-.4','-1.5','.4','-1.5','-.4','-.7'],
    ['-.6','-.1','.8','-.5',-1,'.1','.6'],
    ['.7','.4','-.3','-.5','-.3','.4','.7'],
    ['-.5','.3','.5','.55','.5','.3','-.5']])
SECTION_P=[]
for values in PROFILE_A:
    P=tuple((a,-2+4*sum(SECTION_K[i+1:i+4])/3) for i,a in enumerate(values))
    mid=de_boor(SECTION_K,P,3,F(1,2));assert mid[1]==0
    SECTION_P.append(tuple((a-mid[0],z) for a,z in P))
SECTION_P=tuple(SECTION_P)
def spine(v):return tuple(evaluate(c,v) for c in SPINE_POWER)
def tangent(v):return tuple(evaluate(derivative(c),v) for c in SPINE_POWER)
def frame(v):
    b=-2*v*(1-v);D=(9*(1-b*b),18*b,F(0));assert D==tangent(v)
    length=9*(1+b*b);assert sum(x*x for x in D)==length*length
    T=tuple(x/length for x in D);N=(-T[1],T[0],F(0));assert sum(x*x for x in N)==1 and sum(a*b for a,b in zip(N,D))==0
    return T,N,(F(0),F(0),F(1))
def positioned(vhat=V_HAT,uhat=U_HAT):
    rows=[]
    for v,u,P in zip(vhat,uhat,SECTION_P):
        center=spine(v);T,N,B=frame(v);anchor=de_boor(SECTION_K,P,3,u)
        # The long coordinate of each local profile lies in the xy normal;
        # its transverse shape bends along z. Both axes span the normal plane.
        Q=tuple(tuple(center[d]+(z-anchor[1])*N[d]+(a-anchor[0])*B[d] for d in range(3)) for a,z in P)
        assert de_boor(SECTION_K,Q,3,u)==center
        assert all(sum((x-c)*t for x,c,t in zip(q,center,T))==0 for q in Q)
        rows.append(Q)
    return tuple(rows)
def view(P):
    x,y,z=P
    return(F(9,5)*(F(4,5)*x+F(3,5)*y),F(9,5)*(-F(9,25)*x+F(12,25)*y+F(4,5)*z))
