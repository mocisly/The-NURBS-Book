"""10.15actual swept skins with an exactly certified transverse self-intersection."""
from fractions import Fraction as F
from math import comb
from moving_frame_sweep_data import section
from bspline_math import evaluate,derivative
from native_bspline import segments,de_boor
from knot51_data import insert
from inverse_knot_projection import solve
from global_interpolation_data import interpolate
from bounded_curve_approximation import chord_parameters
from surface_geometry import weights,isocurve,surface,verify_tensor
U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4;C=section(True)
assert all(s['power'][1]==(-F(2),F(4),F(0),F(0)) for s in segments(U,C,3))
POWER=((-F(4,3),F(0),F(8),-F(16,3)),(F(2),-F(8),F(8),F(0)),(F(0),)*4)
T_K=(F(0),)*4+(F(1),)*4
T_P=tuple(tuple(sum(POWER[d][k]*F(comb(i,k),comb(3,k)) for k in range(i+1)) for d in range(3)) for i in range(4))
for t in tuple(F(i,8) for i in range(1,8)):T_K,T_P,_=insert(T_K,T_P,3,t)
assert all(s['power']==POWER for s in segments(T_K,T_P,3))
U_STAR=F(151,192);OFFSET=F(55,48);V_PAIR=(F(1,4),F(3,4))
def trajectory(v):return tuple(evaluate(p,v) for p in POWER)
def normal(v):
    t=2*v-1;n=1+t*t
    return(-2*t/n,(1-t*t)/n,F(0))
def placed(v):
    T=trajectory(v);N=normal(v)
    return tuple(tuple(T[d]+p[1]*N[d]+(p[2] if d==2 else 0) for d in range(3)) for p in C)
Z_STAR=de_boor(U,C,3,U_STAR)[2];I=(F(0),F(19,16),Z_STAR)
assert de_boor(U,C,3,U_STAR)[1]==OFFSET
assert all(de_boor(U,placed(v),3,U_STAR)==I for v in V_PAIR)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dcurve(K,P,p,t):
    ss=segments(K,P,p);s=next((s for s in ss if s['a']<=t<s['b']),ss[-1])
    return tuple(evaluate(derivative(c),t) for c in s['power'])
def view(P):
    x,y,z=P;return(F(9,5)*(F(4,5)*x+F(3,5)*y),F(9,5)*(-F(9,25)*x+F(12,25)*y+F(4,5)*z))
def construct(mode):
    assert mode in ('free','trajectory')
    if mode=='trajectory':V=T_K;vhat=tuple(sum(V[i+1:i+4])/3 for i in range(11));VP=vhat;paramerr=0
    else:vhat=tuple(map(F,('0','1/8','1/4','1/2','3/4','7/8','1')))
    rows=tuple(placed(v) for v in vhat)
    if mode=='free':
        results=[chord_parameters(tuple(row[i] for row in rows)) for i in range(7)]
        VP=tuple(sum(p[0][k] for p in results)/7 for k in range(7));paramerr=max(p[1] for p in results)
    net=[]
    if mode=='trajectory':
        A=tuple(tuple(weights(V,3,v)) for v in VP)
        for i in range(7):net.append(solve(A,tuple(row[i] for row in rows)))
    else:
        for i in range(7):V,P=interpolate(tuple(row[i] for row in rows),VP,3);net.append(P)
    net=tuple(net);base=(U,V,3,3,net)
    for row,v in zip(rows,VP):
        w=weights(V,3,v)
        assert all(tuple(sum(a*p[d] for a,p in zip(w,column)) for d in range(3))==row[i] for i,column in enumerate(net))
    assert all(p[2]==C[i][2] for i,row in enumerate(net) for p in row)
    w1,w2=(VP[vhat.index(v)] for v in V_PAIR);assert w1<w2
    assert surface(*base,U_STAR,w1)==surface(*base,U_STAR,w2)==I
    loopK,loopp,loopC=isocurve(*base,'v',U_STAR);d1,d2=(dcurve(loopK,loopC,loopp,w) for w in (w1,w2))
    tangent_cross=sum(x*x for x in cross(d1,d2));assert tangent_cross>0
    normals=[]
    for w,dv in zip((w1,w2),(d1,d2)):
        K,p,P=isocurve(*base,'u',w);du=dcurve(K,P,p,U_STAR);normals.append(cross(du,dv))
    normal_cross=sum(x*x for x in cross(*normals));assert normal_cross>0
    K,p,P=isocurve(*base,'v',F(1,2))
    if mode=='trajectory':assert K==T_K and P==T_P
    report=dict(method='A10.2' if mode=='free' else 'A10.1',instance_count=len(rows),spine_placement_parameters=list(map(str,vhat)),interpolation_parameters=list(map(str,VP)),parameter_error_bound=paramerr,u_knots=list(map(str,U)),v_knots=list(map(str,V)),placed_section_controls=[[[str(x) for x in p] for p in row] for row in rows],surface_controls=[[[str(x) for x in p] for p in row] for row in net],all_whole_placed_sections_interpolated=True,section_control_vector_identities=7*len(rows),whole_trajectory_exact_origin_isocurve=(mode=='trajectory'),intersection_u=str(U_STAR),intersection_v_parameters=list(map(str,(w1,w2))),actual_3D_intersection_point=list(map(str,I)),intersection_point_equalities_exact=True,loop_tangent_cross_squared=str(tangent_cross),surface_normal_cross_squared=str(normal_cross),genuine_transverse_surface_self_intersection=True,tensor_checks=verify_tensor(*base,steps=3))
    return base,VP,rows,report
