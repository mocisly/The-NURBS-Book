"""51representative3Ddata:twohorizontal planar arcs and a skewconnector."""
from fractions import Fraction as F
from local_cubic_planar_data import casteljau
PIECES=tuple(tuple(tuple(map(F,p)) for p in row) for row in [
 [('0','2','0'),('3','2','0'),('3','-2','0'),('0','-2','0')],
 [('0','-2','0'),('-1','-2','0'),('-1','-3','3'),('0','-2','3')],
 [('0','-2','3'),('2','0','3'),('2','2','3'),('0','2','3')]])
COUNTS=(16,18,16);Q=[];D=[];LOCAL=[]
for index,(P,n) in enumerate(zip(PIECES,COUNTS)):
    derivative=tuple(tuple(3*(b-a) for a,b in zip(A,B)) for A,B in zip(P,P[1:]))
    for j in range(n):Q.append(casteljau(P,F(j,n)));D.append(casteljau(derivative,F(j,n)));LOCAL.append((index,F(j,n)))
Q.append(PIECES[-1][-1]);D.append(tuple(3*(b-a) for a,b in zip(PIECES[-1][-2],PIECES[-1][-1])));LOCAL.append((2,F(1)))
Q=tuple(Q);D=tuple(D);LOCAL=tuple(LOCAL);assert len(Q)==len(D)==51
assert all(p[2]==0 for p in Q[:17]) and all(p[2]==3 for p in Q[34:])
