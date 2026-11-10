"""Native tensor-isocurve panel with exact curve/surface cross-checks."""
from fractions import Fraction as F
from surface_geometry import surface,verify_tensor,isocurve
from native_bspline import segments,check,de_boor,cubic_path,point
def panel(base,data,camera,letter,shift=0):
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-6.5,-4.5) rectangle (6.5,11);']
    tensor=verify_tensor(*base,steps=10);native=0;iso=0
    for j in range(41):
        fixed=F(j,40);K,p,C=isocurve(*base,'u',fixed);ss=segments(K,C,p);native+=check(K,C,p,ss)
        for k in range(21):
            t=F(k,20);assert de_boor(K,C,p,t)==surface(*base,t,fixed);iso+=1
        out.extend(cubic_path(dict(bern=tuple(camera(pt) for pt in s['bern']))) for s in ss)
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(26,5)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    for row in data:
        for pt in row:out.append(r'\fill '+point(camera(pt))+r' circle[radius=1.7pt];')
    out.extend([r'\node at (0,-4) {('+letter+')};',r'\end{scope}'])
    return out,dict(independent_tensor_checks=tensor,native_curve_checks=native,isocurve_vs_surface_exact_checks=iso)
