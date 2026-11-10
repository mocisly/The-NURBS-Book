"""Certified native graphs for positive-weight B-spline rational basis functions."""
from fractions import Fraction as F
from native_bspline import segments,cubic_path,point
from rational_geometry import graph_controls,approximate,split

def positive_paths(H,depth=0):
    """Certify a positive denominator even when its original controls have signs."""
    assert H[0][-1]>0 and H[-1][-1]>0
    if min(pt[-1] for pt in H)>=0:return approximate(H,F(1,100000))
    assert depth<20,'Denominator did not acquire a positive Bernstein certificate'
    left,right=split(H)
    return positive_paths(left,depth+1)+positive_paths(right,depth+1)

def graphs(U,W,p=2,width=F(12),height=F(4),allow_signed=False):
    assert (min(W)>0 or allow_signed) and U[p]==0 and U[len(W)]==1
    lines=[];proofs=[]
    for i in range(len(W)):
        C=tuple((w*F(j==i),w) for j,w in enumerate(W));pieces=segments(U,C,p);paths=[]
        for s in pieces:
            numerator=tuple(q[0] for q in s['bern']);denominator=tuple(q[1] for q in s['bern'])
            if not any(numerator):continue
            H=graph_controls(s['a'],s['b'],numerator,denominator,xscale=width,yscale=height)
            paths.extend(positive_paths(H))
        lines.extend(cubic_path(s) for s in paths)
        proofs.append({'index':i,'native_paths':len(paths),'certified_screen_L1_error_cm':str(max(s['certified_l1_error'] for s in paths))})
    return lines,proofs
