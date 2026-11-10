"""Explicit representative periodic pentagon, printed U2 and p=3 wrapping."""
from fractions import Fraction as F
K=tuple(F(i)for i in range(12))
POLYGON=tuple(tuple(F(str(x))for x in p)for p in[(-1,1.5),(-1.8,0),(0,-1.8),(1.8,0),(1,1.5)])
P=POLYGON+POLYGON[:3]
