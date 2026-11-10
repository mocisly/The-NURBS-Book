"""Representative wavy data from an explicit known polynomial spline,not raster."""
from fractions import Fraction as F
from native_bspline import de_boor
K=(F(0),)*4+tuple(t for t in map(F,['.15','.3','.5','.65','.8']) for _ in range(2))+(F('.9'),)+(F(1),)*4
P=tuple(tuple(map(F,p)) for p in [('.3','.1'),('-.3','1.5'),('-.2','3'),('1.5','4'),('2.6','3.8'),('2.7','1'),('3.3','.7'),('4.2','5.8'),('5','6.4'),('5.6','5.5'),('4.5','.1'),('6','-.4'),('6.8','.3'),('6.6','3'),('8','3.3')])
assert len(K)==len(P)+4
Q=tuple(de_boor(K,P,3,F(i,80)) for i in range(81))
