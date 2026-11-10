"""Representative horizontal profile with an explicitly flagged apex corner."""
from fractions import Fraction as F
def bezier(P,t):
    Q=P
    for _ in range(3):Q=tuple(tuple((1-t)*a+t*b for a,b in zip(x,y)) for x,y in zip(Q,Q[1:]))
    return Q[0]
PIECES=tuple(tuple(tuple(map(F,p)) for p in row) for row in [
 [('1.5','0'),('0','0'),('0','2.4'),('1.5','2.4')],
 [('1.5','2.4'),('3.1','2.4'),('4.7','2.4'),('6.3','2.4')],
 [('6.3','2.4'),('7.4','2.4'),('7.8','3.3'),('7.8','5.2')],
 [('7.8','5.2'),('10','3.8'),('11','.8'),('5.8','-.6')]])
COUNTS=(16,20,20,28)
Q=tuple(bezier(P,F(j,n)) for P,n in zip(PIECES,COUNTS) for j in range(n))+(PIECES[-1][-1],)
CORNER=sum(COUNTS[:3]);assert Q[CORNER]==(F('7.8'),F('5.2')) and len(Q)==85
