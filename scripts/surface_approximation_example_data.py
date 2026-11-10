"""Representative81point staircase mesh shared by9.44..9.47."""
from fractions import Fraction as F
X=tuple(-F(2)+F(i,2) for i in range(9));Y=X
H=tuple(map(F,['1','1','1','1/2','1/2','1/2','0','0','0']))
B=tuple(map(F,[0,0,0,1,1,1,0,0,0]))
Q=tuple(tuple((x,y,H[i]+H[j]+B[i]*B[j]/10) for j,y in enumerate(Y)) for i,x in enumerate(X))
def camera(q):
    x,y,z=q;return (3*(-F(4,5)*x+F(9,10)*y),3*(-F(2,5)*x-F(7,20)*y+z))
