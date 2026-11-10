"""169explicit smooth step-profile data for ALL five panels of9.52."""
from fractions import Fraction as F
X=tuple(-F(2)+F(i,3) for i in range(13));Y=X
def height(x,y):
    a,b=(2-x)**4,(2+x)**4
    return 3*a/(a+b)+(1-x*x/4)**2*(1-y*y/4)/10
Q=tuple(tuple((x,y,height(x,y)) for y in Y) for x in X)
