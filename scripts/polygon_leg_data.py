"""Common representative11-vertex polygon for Fig5.3 and5.4."""
from fractions import Fraction as F
P=tuple(tuple(F(str(x)) for x in p) for p in [(1.5,0),(0,2.3),(1.5,5),(4.4,5.5),(6,3.1),(5.2,1.7),(6.3,0),(9,0),(11,1.8),(10.2,4.2),(7.2,5.2)])
K=tuple(map(F,[0,0,0,0,1,2,3,4,4,5,6,7,7,7,7]))
NONUNIFORM=tuple(F(str(x)) for x in [0,0,0,0,1,1.5,2.3,3.9,4.3,5,6.5,7,7,7,7])
