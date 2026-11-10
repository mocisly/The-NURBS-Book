"""10.13printed piecewise-linear scale and same moving-frame sweep data."""
from fractions import Fraction as F
from native_bspline import de_boor
SCALE_K=tuple(map(F,('0','0','3/10','7/10','1','1')))
SCALE_P=tuple(tuple(map(F,row)) for row in [('3/10','3/10','1'),('3/2','3/2','1/2'),('3/10','3/10','1'),('1','1','2')])
assert min(x for row in SCALE_P for x in row)>0
def scaling(v):return de_boor(SCALE_K,SCALE_P,1,v)
assert all(scaling(t)==p for t,p in zip((F(0),F(3,10),F(7,10),F(1)),SCALE_P))
