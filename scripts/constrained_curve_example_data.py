"""Point/derivative constraints shared by the9.40..9.43comparison."""
from fractions import Fraction as F
POINTS=(0,7,13,20)
DERIVATIVES={0:(F(0),F(14)),7:(F(10),-F(10)),13:(F(10),-F(10)),20:(F(0),F(14))}
HORIZONTAL_DERIVATIVES={**DERIVATIVES,7:(F(14),F(0)),13:(F(14),F(0))}
