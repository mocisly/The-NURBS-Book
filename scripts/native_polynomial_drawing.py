"""Certified native cubic rendering of exact polynomial Bezier segments.

This operates on mathematical Bezier coefficients, never on image pixels.
Unit homogeneous weights allow rational_geometry's exact Bernstein residual bound
to certify higher-degree polynomial curves as well as rational curves.
"""
from fractions import Fraction as F
from rational_geometry import approximate
from native_bspline import cubic_path

def paths(segs,style='book line',tolerance=F(1,10000)):
    lines=[];maximum=F(0);count=0
    for seg in segs:
        if len(seg['bern'])<=4:
            lines.append(cubic_path(seg,style));count+=1
        else:
            H=tuple(tuple(pt)+(F(1),) for pt in seg['bern'])
            for piece in approximate(H,tolerance):
                lines.append(cubic_path(piece,style));maximum=max(maximum,piece['certified_l1_error']);count+=1
    return lines,{'native_cubic_paths':count,'maximum_certified_L1_error_cm':str(maximum),'requested_tolerance_cm':str(tolerance)}
