"""Fig5.28: same8x6 tensor net with actual directional approximate removals."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point
from surface_geometry import surface,verify_tensor
from surface_knot_projection import remove_surface_to,common_basis_error

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (37,38)]
assert not any(p.exists() for p in targets)
U=(F(0),)*4+(F(3,10),)*3+(F(7,10),)+(F(1),)*4
V=(F(0),)*3+(F(1,4),F(1,2),F(3,4))+(F(1),)*3
xs=tuple(F(str(t)) for t in (3,2.5,1.8,.3,-1.8,-3))
ys=tuple(F(str(t)) for t in (-3,-2.6,-2,-.8,.5,1.5,2.6,3))
zu=tuple(F(str(t)) for t in (1.2,1.2,1,-.3,-1.3,-1.3,-1.2,-1.2))
zv=tuple(F(str(t)) for t in (0,0,.7,2.6,2.6,2.6))
P=tuple(tuple((xs[j],ys[i],zu[i]+zv[j]) for j in range(6)) for i in range(8));base=(U,V,3,2,P)
Au,pu=remove_surface_to(base,'u',(F(3,10),)*3)
Av,pv=remove_surface_to(base,'v',(F(1,4),))
Auv,puv=remove_surface_to(Au,'v',(F(1,4),))
Avu,pvu=remove_surface_to(Av,'u',(F(3,10),)*3);assert Auv==Avu
states=(base,Au,Av,Auv);reports=[]
for index,net in enumerate(states):
    A,B,p,q,R=net;assert (len(R),len(R[0]))==((8,6),(5,6),(8,5),(5,5))[index]
    tensor=verify_tensor(*net,steps=10)
    r={'control_count':[len(R),len(R[0])],'U':list(map(str,A)),'V':list(map(str,B)),
       'controls':[[list(map(str,t)) for t in row] for row in R],'exact_tensor_vs_nested_deboor_points':tensor}
    if index:
        E,bound=common_basis_error(base,net,(F(3,10),)*3 if index in (1,3) else (), (F(1,4),) if index in (2,3) else ())
        assert bound>0;maximum=F(0)
        for i in range(11):
            for j in range(11):
                u,v=F(i,10),F(j,10);old=surface(*base,u,v);new=surface(*net,u,v)
                delta=tuple(a-b for a,b in zip(old,new));assert delta==surface(*E,u,v)
                error=sum(map(abs,delta));assert error<=bound;maximum=max(maximum,error)
        r.update(common_basis_error_identity_points=121,certified_whole_domain_L1_surface_error_bound_cm=str(bound),sampled_max_L1_error_cm=str(maximum))
    reports.append(r)

def net_lines(R,style,markers=False):
    lines=[]
    for row in R:lines.append(r'\draw['+style+'] '+'--'.join(map(point,row))+';')
    for j in range(len(R[0])):lines.append(r'\draw['+style+'] '+'--'.join(point(row[j]) for row in R)+';')
    if markers:
        for row in R:
            for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1pt];')
    return lines

panels=[]
for index,net in enumerate(states):
    lines=[r'\begin{scope}[x={(-.75cm,-.5cm)},y={(.85cm,-.28cm)},z={(0cm,.8cm)}]']
    lines+=net_lines(P,'book grid,dashed',index==0)
    if index:lines+=net_lines(net[-1],'book line',True)
    lines += [r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,6.2,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,7.5) node[above=4pt] {$z$};',
              r'\end{scope}',r'\node at (.3,-4.1) {('+chr(97+index)+')};'];panels.append(lines)
for pair,target in enumerate(targets):
    lines=['% Fig5.28: same representative8x6 p3q2 net with exact printed U/V.',
           '% Real inverse-insertion approximations, native control nets; no scan outlines.',
           '% (b)u=.3 removed3times,(c)v=.25 removedonce,(d)both; resulting5x6,8x5,5x5 nets.',
           '% Independent u/v linear operators commute EXACTLY; whole-domain tensor error bounds verified.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-5.5,-4.8) rectangle (18.7,6.8);']
    for panel,shift in [(2*pair,0),(2*pair+1,F(63,5))]:
        lines+=[r'\begin{scope}[xshift='+str(float(shift))+'cm]']+panels[panel]+[r'\end{scope}']
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-knot-removal-examples-check.json').write_text(json.dumps({
    'figure':'5.28','degrees':[3,2],'all_unit_weights':True,'same_original_8x6_net':True,
    'original_U':list(map(str,U)),'original_V':list(map(str,V)),
    'directional_projection_reports':{'u':pu,'v':pv,'uv':puv,'vu':pvu},
    'u_v_removal_orders_produce_identical_controls_exactly':True,'panels':reports},indent=2)+'\n')
print('PASS:484 exact tensor points,363 common-basis surface error identities; actual8x6/5x6/8x5/5x5 nets; both removal orders commute exactly.')
