"""Fig5.38: exact directional elevation of one cubic-by-quadratic surface.

Uses the same documented representative translation surface as5.9, whose
printed knot vectors match this example. Control nets, not sampled isocurves,
are drawn. Both generating curves have exact polynomial identities after
elevation, certifying unchanged tensor geometry over the entire domain.
"""
from pathlib import Path
from fractions import Fraction as F
import json
from knot59_data import U,V,xs,ys,zu,zv,P
from degree_elevation_geometry import elevate_spline
from native_bspline import segments,check,point
from surface_geometry import surface,verify_tensor

root=Path(__file__).resolve().parents[1]
R=tuple(zip(ys,zu));S=tuple(zip(xs,zv));base=(U,V,3,2,P)
camera=r'x={(-.75cm,-.75cm)},y={(.85cm,-.3cm)},z={(0cm,.7cm)}'
states=[base];reports=[]
for tu,tv in [(0,0),(1,1),(2,2),(3,4),(6,7)]:
    if tu:
        A,r,pu=elevate_spline(U,R,3,tu);B,s,pv=elevate_spline(V,S,2,tv)
        Q=tuple(tuple((x,y,z+zz) for x,zz in s) for y,z in r);net=(A,B,3+tu,2+tv,Q)
        states.append(net)
    else:A,B,r,s,pu,pv=U,V,R,S,{},{}
    net=states[-1];a,b,p,q,Q=net
    native=check(a,r,p,segments(a,r,p))+check(b,s,q,segments(b,s,q))
    count=verify_tensor(*net,steps=10);comparisons=0
    for i in range(11):
        for j in range(11):
            u,v=F(i,10),F(j,10);assert surface(*net,u,v)==surface(*base,u,v);comparisons+=1
    us=[(-F(3,10)*(yy-y)+F(7,10)*(zz-z))/(F(17,20)*(yy-y)) for (y,z),(yy,zz) in zip(r,r[1:])]
    vs=[(-F(3,4)*(xx-x)+F(7,10)*(zz-z))/(-F(3,4)*(xx-x)) for (x,z),(xx,zz) in zip(s,s[1:])]
    assert all(yy>y for (y,z),(yy,zz) in zip(r,r[1:])) and all(xx<x for (x,z),(xx,zz) in zip(s,s[1:]))
    assert max(us)<min(vs)
    reports.append({'degrees':[p,q],'counts':[len(Q),len(Q[0])],
                    'U':list(map(str,a)),'V':list(map(str,b)),
                    'controls':[[list(map(str,pt)) for pt in row] for row in Q],
                    'u_elevation':pu,'v_elevation':pv,'native_generating_curve_checks':native,
                    'independent_tensor_checks':count,'exact_original_surface_comparisons':comparisons,
                    'projection_tangent_slopes_strictly_separated':[str(max(us)),str(min(vs))]})
assert [r['counts'] for r in reports]==[[4,4],[5,6],[6,8],[7,12],[10,18]]

def net_lines(Q,style,markers):
    lines=[]
    for row in Q:lines.append(r'\draw['+style+'] '+'--'.join(map(point,row))+';')
    for j in range(len(Q[0])):lines.append(r'\draw['+style+'] '+'--'.join(point(row[j]) for row in Q)+';')
    if markers:
        for row in Q:
            for pt in row:lines.append(r'\fill '+point(pt)+r' circle[radius=1pt];')
    return lines
for pair,indices in enumerate([(0,1),(2,3),(4,)]):
    target=root/f'image_tex/ch05/fig_5_{54+pair}.tex';assert not target.exists()
    lines=['% Semantic tensor degree elevation, same geometry and camera for every net.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-5.6,-4.9) rectangle ('+('18.8' if len(indices)==2 else '5.8')+',5.5);']
    for col,i in enumerate(indices):
        a,b,p,q,Q=states[i]
        lines.extend([r'\begin{scope}[xshift='+str(13*col)+r'cm]',r'\begin{scope}['+camera+']'])
        if i:lines+=net_lines(P,'book grid,dashed',False)
        lines+=net_lines(Q,'book line',True)
        lines += [r'\draw[book axis] (0,0,0)--(5.3,0,0) node[below left=4pt] {$x$};',
                  r'\draw[book axis] (0,0,0)--(0,6.1,0) node[right=4pt] {$y$};',
                  r'\draw[book axis] (0,0,0)--(0,0,6.6) node[above=4pt] {$z$};',r'\end{scope}',
                  r'\node at (0,-4.35) {('+chr(97+i)+r') $(p,q)=('+str(p)+','+str(q)+r'),\quad '+str(len(Q))+r'\times'+str(len(Q[0]))+'$};',r'\end{scope}']
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-degree-comparisons-check.json').write_text(json.dumps({
    'figure':'5.38','representative_data_source':'knot59_data.py; same printed knot vectors',
    'entire_surface_equality_certified_by_exact_generating_curve_power_identities':True,
    'all_projected_nets_have_tangent_cone_separation':True,'states':reports},indent=2)+'\n')
print('PASS:5 exact tensor representations,605 tensor checks+605 original comparisons; degrees(3,2)/(4,3)/(5,4)/(6,6)/(9,9).')
