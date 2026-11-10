"""Fig5.5/5.6: representative cubic and the exact three-stage insertion triangle."""
from fractions import Fraction as F
from knot51_data import insert
K=tuple(map(F,[0,0,0,0,2,3,3,3,3]));u=F(1);p=3
P=tuple(tuple(F(str(x)) for x in pt) for pt in [(0,0),(0,2.6),(3.6,5),(9,3.5),(9,0)])
table={(i,0):pt for i,pt in enumerate(P)};ratios={};states=[];U,R=K,P
for r in (1,2,3):
    U,R,unused=insert(U,R,p,u)
    for i in range(r,4):
        a=(u-K[i])/(K[i+p-r+1]-K[i]);ratios[i,r]=a
        table[i,r]=tuple((1-a)*x+a*y for x,y in zip(table[i-1,r-1],table[i,r-1]));assert table[i,r]==R[i]
    states.append((U,R))
assert R==(P[0],table[1,1],table[2,2],table[3,3],table[3,2],table[3,1],P[3],P[4])
