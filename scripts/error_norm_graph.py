"""Native polyline of a mathematical Bernstein-vector norm, with error bound."""
from fractions import Fraction as F
from math import ceil,sqrt
from rational_geometry import evaluate
from native_bspline import point

def graph(D,x0=F(0),width=F(10),y0=F(-33,10),scale=F(1),tolerance=F(1,200)):
    p=len(D)-1
    L=max(sum(abs(p*(b-a)) for a,b in zip(x,y)) for x,y in zip(D,D[1:]))
    n=max(160,ceil(L*scale/(2*tolerance)));coords=[]
    for i in range(n+1):
        t=F(i,n);d=evaluate(D,t);e=sqrt(sum(float(x)**2 for x in d))
        coords.append(point((x0+width*t,y0+scale*F(str(e)))))
    return r'\draw[book line] '+'--'.join(coords)+';',{
        'degree':p,'segments':n,'norm_Lipschitz_bound_on_unit_interval':str(L),
        'vertical_interpolation_error_cm_bound':str(L*scale/(2*n)),
        'numeric_coordinate_rounding_cm_allowance':'0.00000001',
        'exact_error_Bernstein_controls':[[str(x) for x in d] for d in D]}
