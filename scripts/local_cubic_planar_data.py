"""51representative planar CAD-profile samples and known analytic directions."""
from fractions import Fraction as F
PIECES=tuple(tuple(tuple(map(F,p)) for p in row) for row in [
 [('1','0'),('-1','0'),('0','3'),('2','3')],
 [('2','3'),('4','3'),('1.5','.2'),('3','.2')],
 [('3','.2'),('5','.2'),('9','1'),('9','4.3')],
 [('9','4.3'),('9','5.3'),('8.2','5.6'),('7.4','5.1')]])
COUNTS=(12,13,16,9)
def casteljau(P,t):
    while len(P)>1:P=tuple(tuple((1-t)*a+t*b for a,b in zip(A,B)) for A,B in zip(P,P[1:]))
    return P[0]
Q=[];D=[]
for P,n in zip(PIECES,COUNTS):
    derivative=tuple(tuple(3*(b-a) for a,b in zip(A,B)) for A,B in zip(P,P[1:]))
    for j in range(n):Q.append(casteljau(P,F(j,n)));D.append(casteljau(derivative,F(j,n)))
Q.append(PIECES[-1][-1]);D.append(tuple(3*(b-a) for a,b in zip(PIECES[-1][-2],PIECES[-1][-1])))
Q=tuple(Q);D=tuple(D);assert len(Q)==len(D)==51
