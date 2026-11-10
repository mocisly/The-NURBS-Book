"""Exact native cubic/quadratic polynomial surface isolines in their global domains."""
from fractions import Fraction as F
from native_bspline import segments,check,cubic_path,de_boor
from surface_geometry import isocurve,surface

def wires(U,V,p,q,P,count=31,boundaries=True,stripe_values=None):
    lines=[];checks=0;tensorchecks=0;paths=0
    a,b=V[q],V[len(P[0])];u0,u1=U[p],U[len(P)]
    values=tuple(a+(b-a)*F(j,count-1) for j in range(count)) if stripe_values is None else tuple(stripe_values)
    assert values[0]==a and values[-1]==b and all(a<=v<=b for v in values)
    count=len(values)
    for j,v in enumerate(values):
        k,d,c=isocurve(U,V,p,q,P,'u',v);ss=segments(k,c,d);checks+=check(k,c,d,ss)
        for n in range(11):
            u=u0+(u1-u0)*F(n,10);assert de_boor(k,c,d,u)==surface(U,V,p,q,P,u,v);tensorchecks+=1
        for s in ss:lines.append(cubic_path(s,'book line' if j in (0,count-1) else 'book grid'));paths+=1
    if boundaries:
        for u in (u0,u1):
            k,d,c=isocurve(U,V,p,q,P,'v',u);ss=segments(k,c,d);checks+=check(k,c,d,ss)
            for s in ss:lines.append(cubic_path(s,'book line'));paths+=1
    return lines,{'exact_isocurve_checks':checks,'curve_vs_surface_points':tensorchecks,'native_paths':paths,'stripe_count':count,'global_u_domain':list(map(str,(u0,u1))),'global_v_domain':list(map(str,(a,b)))}
