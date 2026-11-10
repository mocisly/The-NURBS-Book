"""Exact mathematical checks for the cubic family shown in printed Fig2.9."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import piece,evaluate,basis,derivative

knots=(0,0,0,0,2,4,6,8,8,8,8)
count=0
for span in (3,4,5,6):
    a,b=knots[span:span+2]
    for k in range(41):
        x=F(a)+F(k,41)*(b-a)
        values=[];slopes=[]
        for i in range(7):
            c=piece(knots,i,3,span)
            y=evaluate(c,x)
            assert y==basis(knots,i,3,x)
            values.append(y);slopes.append(evaluate(derivative(c),x));count+=1
        assert min(values)>=0 and sum(values)==1
        assert sum(slopes)==0
for span in (3,4,5):
    u=F(knots[span+1])
    for i in range(7):
        a,b=piece(knots,i,3,span),piece(knots,i,3,span+1)
        for order in range(3):
            assert evaluate(a,u)==evaluate(b,u)
            a,b=derivative(a),derivative(b)
assert evaluate(derivative(piece(knots,0,3,3)),F(0))==-F(3,2)
assert evaluate(derivative(piece(knots,1,3,3)),F(0))==F(3,2)
assert evaluate(derivative(piece(knots,5,3,6)),F(8))==-F(3,2)
assert evaluate(derivative(piece(knots,6,3,6)),F(8))==F(3,2)
report={'knots':knots,'exact_recurrence_comparisons':count,
        'partition_nonnegative_and_derivative_sum_zero':True,
        'C2_at_simple_knots':True,'endpoint_derivatives':[-1.5,1.5,-1.5,1.5]}
root=Path(__file__).resolve().parents[1]
(root/'image_tex/build/cubic-basis-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
