"""Certified native rational isocurves,verified against their actual tensor surface."""
from fractions import Fraction as F
from native_bspline import segments,check,de_boor,cubic_path
from rational_geometry import approximate
from surface_geometry import isocurve,surface
def grid(U,V,p,q,NET,camera,u_values,v_values,interior='book grid'):
    lines=[];iso=nc=0;errors=[]
    for variable,values in [('u',tuple(v_values)),('v',tuple(u_values))]:
        for i,fixed in enumerate(values):
            K,degree,Q=isocurve(U,V,p,q,NET,variable,fixed);ss=segments(K,Q,degree);nc+=check(K,Q,degree,ss)
            for j in range(21):
                t=K[degree]+(K[-degree-1]-K[degree])*F(j,20)
                assert de_boor(K,Q,degree,t)==(surface(U,V,p,q,NET,t,fixed) if variable=='u' else surface(U,V,p,q,NET,fixed,t));iso+=1
            hh=tuple(camera(h[:3])+(h[-1],) for h in Q)
            parts=[part for seg in segments(K,hh,degree) for part in approximate(seg['bern'],F(1,100000))]
            style='book line' if i in (0,len(values)-1) else interior
            lines.extend(cubic_path(part,style) for part in parts);errors.append(str(max(part['certified_l1_error'] for part in parts)))
    return lines,{'exact_isocurve_vs_surface_checks':iso,'native_curve_checks':nc,'u_values':list(map(str,u_values)),'v_values':list(map(str,v_values)),'native_screen_L1_error_bounds_cm':errors}
