"""Mathematical sparse isoparametric comparison grid for5.30-5.34."""
from fractions import Fraction as F
from surface_geometry import surface,isocurve
from native_bspline import segments,check,cubic_path,de_boor
U_VALUES=tuple(F(t) for t in ('0','.3','.7','1'))
V_VALUES=tuple(F(t) for t in ('0','.42','.81','1'))

def sparse(net,style):
    lines=[];checks=points=0
    for variable,values in [('u',V_VALUES),('v',U_VALUES)]:
        for fixed in values:
            K,p,Q=isocurve(*net,variable,fixed);ss=segments(K,Q,p);checks+=check(K,Q,p,ss)
            for i in range(21):
                t=F(i,20);assert de_boor(K,Q,p,t)==(surface(*net,t,fixed) if variable=='u' else surface(*net,fixed,t));points+=1
            for s in ss:lines.append(cubic_path(s,style))
    return lines,{'exact_native_isocurve_checks':checks,'isocurve_vs_surface_points':points,
                  'u_parameters':list(map(str,U_VALUES)),'v_parameters':list(map(str,V_VALUES))}
