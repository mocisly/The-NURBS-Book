"""Exact whole-curve closest-point certificates for polynomial Bezier pieces.

Squared distance minus the proposed minimum is a Bernstein polynomial. Known
foot parameters are split exactly; nonnegative Bernstein coefficients on a
subdivision partition certify the entire curve, not just sampled points.
"""
from fractions import Fraction as F
from math import comb

def split_scalar(B,t=F(1,2)):
    rows=[tuple(B)]
    while len(rows[-1])>1:
        row=rows[-1];rows.append(tuple((1-t)*a+t*b for a,b in zip(row,row[1:])))
    return tuple(row[0] for row in rows),tuple(row[-1] for row in reversed(rows))

def distance_coefficients(controls,point,minimum_squared):
    p=len(controls)-1;D=[tuple(a-b for a,b in zip(pt,point)) for pt in controls]
    B=[]
    for k in range(2*p+1):
        value=F(0)
        for i in range(max(0,k-p),min(p,k)+1):
            j=k-i;value+=F(comb(p,i)*comb(p,j),comb(2*p,k))*sum(a*b for a,b in zip(D[i],D[j]))
        B.append(value-minimum_squared)
    return tuple(B)

def positive_partition(B,depth=0):
    if min(B)>=0:return {'leaves':1,'deepest':depth,'minimum_coefficient':min(B)}
    if max(B)<0 or depth>=9:return None
    left,right=split_scalar(B);a=positive_partition(left,depth+1)
    if a is None:return None
    b=positive_partition(right,depth+1)
    if b is None:return None
    return {'leaves':a['leaves']+b['leaves'],'deepest':max(a['deepest'],b['deepest']),
            'minimum_coefficient':min(a['minimum_coefficient'],b['minimum_coefficient'])}

def certify(pieces,point,foot,anchors):
    minimum=sum((a-b)**2 for a,b in zip(point,foot));proof=[]
    for index,controls in enumerate(pieces):
        B=distance_coefficients(controls,point,minimum);parts=[B]
        if index in anchors and 0<anchors[index]<1:parts=list(split_scalar(B,anchors[index]))
        for part in parts:
            result=positive_partition(part)
            if result is None:return None
            proof.append({'piece':index,'leaves':result['leaves'],'deepest_subdivision':result['deepest'],
                          'minimum_coefficient':str(result['minimum_coefficient'])})
    return {'global_closest_point_certified':True,'distance_squared':str(minimum),
            'nonnegative_distance_difference_partition':proof}
