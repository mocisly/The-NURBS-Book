"""The exact same representative seven-point data used in9.5 and9.6."""
from fractions import Fraction as F
Q=tuple(tuple(map(F,p)) for p in [('0','0'),('7/25','24/25'),('67/25','49/25'),('82/25','29/25'),('97/25','9/25'),('157/25','53/50'),('339/50','-7/50')])
LENGTHS=tuple(map(F,['1','13/5','1','1','5/2','13/10']))
assert all(sum((b-a)**2 for a,b in zip(A,B))==ell**2 for A,B,ell in zip(Q,Q[1:],LENGTHS))
PARAMS=(F(0),)+tuple(sum(LENGTHS[:i])/sum(LENGTHS) for i in range(1,7))
