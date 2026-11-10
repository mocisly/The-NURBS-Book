"""Representative sixteen-point step-profile dataset shared by9.15..9.17."""
from fractions import Fraction as F
X=tuple(map(F,['-2','-.75','.75','2']));Y=tuple(map(F,['-2','-.5','.75','2']))
H=tuple(map(F,['3','3','0','0']));A=tuple(map(F,['1','3/2','1/2','0']));G=tuple(map(F,['0','1/5','1/10','0']))
Q=tuple(tuple((x,y,H[i]+A[i]*G[j]) for j,y in enumerate(Y)) for i,x in enumerate(X))
def camera(q):
    x,y,z=q;s=F(7,2)
    return (s*(-F(4,5)*x+F(9,10)*y),s*(-F(2,5)*x-F(7,20)*y+z))
