"""Certified chord ratios for10.10/11, exact parallel rational derivative vectors."""
from fractions import Fraction as F
from math import isqrt
from spine_skinning_example_data import V_HAT,U_HAT,positioned,spine,tangent
def length_interval(A,B):
    s=sum((a-b)**2 for a,b in zip(A,B));scale=10**14
    lo=F(isqrt(s.numerator*scale**2//s.denominator),scale);hi=lo+F(1,scale)
    assert lo>0 and lo*lo<=s<hi*hi
    return lo,hi
def construct(vhat=V_HAT,uhat=U_HAT):
    Q=positioned(vhat,uhat);P=tuple(spine(v) for v in vhat);D=tuple(tangent(v) for v in vhat)
    den=[length_interval(a,b) for a,b in zip(P,P[1:])];C=[];DV=[];bounds=[]
    for i in range(7):
        num=[length_interval(a[i],b[i]) for a,b in zip(Q,Q[1:])];coefs=[];row=[];errs=[]
        for k in range(5):
            indices=(0,) if k==0 else (3,) if k==4 else (k-1,k)
            nlo=sum(num[j][0] for j in indices);nhi=sum(num[j][1] for j in indices)
            dlo=sum(den[j][0] for j in indices);dhi=sum(den[j][1] for j in indices)
            lo,hi=nlo/dhi,nhi/dlo;c=F(round((lo+hi)/2*10**12),10**12)
            err=max(abs(c-lo),abs(c-hi));assert c>0 and err<F(1,10**10)
            coefs.append(c);row.append(tuple(c*x for x in D[k]));errs.append(str(err))
        C.append(tuple(coefs));DV.append(tuple(row));bounds.append(errs)
    report=dict(all35derivative_vectors_positive_parallel_to_spine=True,all35chord_ratio_error_bounds=bounds,all35chord_ratio_errors_below='1e-10',chord_square_root_enclosure_width='1e-14',coefficients=[[str(c) for c in row] for row in C],vectors=[[[str(x) for x in v] for v in row] for row in DV],spine_points=[[str(x) for x in p] for p in P],spine_derivatives=[[str(x) for x in p] for p in D])
    return Q,P,D,tuple(C),tuple(DV),report
