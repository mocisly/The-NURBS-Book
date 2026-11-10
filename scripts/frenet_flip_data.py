"""10.16true spatial inflection with exact rational Frenet frames on both sides."""
from fractions import Fraction as F
from math import comb
from itertools import combinations
from bspline_math import add,compose_affine,derivative,evaluate
from spatial_frame_sweep_data import mul,dotpoly
from moving_frame_sweep_data import section
from inverse_knot_projection import solve
from bounded_curve_approximation import chord_parameters
from global_interpolation_data import interpolate
from native_bspline import de_boor,segments
from surface_geometry import weights,isocurve,verify_tensor
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def neg(p):return tuple(-x for x in p)
def crosspoly(a,b):return(add(mul(a[1],b[2]),neg(mul(a[2],b[1]))),add(mul(a[2],b[0]),neg(mul(a[0],b[2]))),add(mul(a[0],b[1]),neg(mul(a[1],b[0]))))
# f=t²,t=2v-1. D is a polynomial hodograph numerator with norm N.
D=((F(1),F(0),-F(7,16)),(F(0),F(6,5),-F(6,5)),(F(0),F(8,5),F(9,10)))
N=(F(1),F(0),F(25,16));CF=crosspoly(D,tuple(derivative(p) for p in D))
assert dotpoly(D,D)==mul(N,N) and dotpoly(D,CF)==(F(0),)
assert dotpoly(CF,CF)==tuple(4*x for x in mul(N,N))
POWER_T=((F(0),F(4),F(0),F(0),F(0),-F(7,20)),(F(0),F(0),F(0),F(8,5),F(0),-F(24,25)),(F(0),F(0),F(0),F(32,15),F(0),F(18,25)))
POWER=tuple(tuple(compose_affine(p,-1,2))+(F(0),)*(6-len(compose_affine(p,-1,2))) for p in POWER_T)
def substitute_square(p):return tuple(p[i//2] if i%2==0 else F(0) for i in range(2*len(p)-1))
derivatives=tuple(derivative(p) for p in POWER)
assert all(add(a,neg(tuple(8*x for x in compose_affine(substitute_square(b),-1,2))))==(F(0),) for a,b in zip(derivatives,D))
actualcross=crosspoly(derivatives,tuple(derivative(p) for p in derivatives))
expected=tuple(tuple(256*x for x in compose_affine((F(0),)+substitute_square(p),-1,2)) for p in CF)
assert all(add(a,neg(b))==(F(0),) for a,b in zip(actualcross,expected))
T_K=(F(0),)*6+(F(1),)*6
T_P=tuple(tuple(sum(POWER[d][k]*F(comb(i,k),comb(5,k)) for k in range(i+1)) for d in range(3)) for i in range(6))
U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4;C=section(True)
THAT=tuple(map(F,('-1','-7/10','-2/5','-1/10','1/10','2/5','7/10','1')))
V_HAT=tuple((t+1)/2 for t in THAT)
def trajectory(v):return tuple(evaluate(p,v) for p in POWER)
def frame(v):
    t=2*v-1;assert t
    f=t*t;n=evaluate(N,f);sgn=F(1 if t>0 else -1)
    X=tuple(evaluate(p,f)/n for p in D);B=tuple(sgn*evaluate(p,f)/(2*n) for p in CF);Y=cross(B,X)
    axes=(X,Y,B)
    assert all(sum(a*b for a,b in zip(axis_a,axis_b))==F(i==j) for i,axis_a in enumerate(axes) for j,axis_b in enumerate(axes))
    return X,Y,B
def placed(v):
    X,Y,B=frame(v);T=trajectory(v)
    return tuple(tuple(T[d]+p[1]*Y[d]+p[2]*B[d] for d in range(3)) for p in C)
def view(P):
    x,y,z=P;return(F(11,5)*(-F(4,5)*x+F(3,5)*y),F(11,5)*(-F(9,25)*x-F(12,25)*y+F(4,5)*z))
def construct():
    rows=tuple(placed(v) for v in V_HAT);rigid=0
    assert all(tuple(-x for x in p)==q for row,other in zip(rows,rows[::-1]) for p,q in zip(row,other))
    for row in rows:
        for i,j in combinations(range(7),2):
            assert sum((a-b)**2 for a,b in zip(row[i],row[j]))==sum((a-b)**2 for a,b in zip(C[i],C[j]));rigid+=1
    results=[chord_parameters(tuple(row[i] for row in rows)) for i in range(7)]
    VP=tuple(sum(p[0][k] for p in results)/7 for k in range(8));assert all(a+b==1 for a,b in zip(VP,VP[::-1]))
    net=[]
    for i in range(7):V,P=interpolate(tuple(row[i] for row in rows),VP,3);net.append(P)
    net=tuple(net);base=(U,V,3,3,net)
    for row,v in zip(rows,VP):
        w=weights(V,3,v)
        assert all(tuple(sum(a*p[d] for a,p in zip(w,column)) for d in range(3))==row[i] for i,column in enumerate(net))
    assert all(tuple(-x for x in p)==q for row in net for p,q in zip(row,row[::-1]))
    K,p,P=isocurve(*base,'u',F(1,2));assert P==((F(0),)*3,)*7
    plus=tuple(evaluate(p,F(0))/2 for p in CF);minus=tuple(-x for x in plus);assert plus==(F(0),-F(4,5),F(3,5))
    nonplanar=sum(a*b for a,b in zip(tuple(p[0] for p in D),cross(tuple(p[1] for p in D),tuple(p[2] for p in D))));assert nonplanar
    report=dict(figure='10.16',representative_data=True,trajectory_degree=5,trajectory_global_power=[[str(x) for x in p] for p in POWER],trajectory_controls=[[str(x) for x in p] for p in T_P],trajectory_knots=list(map(str,T_K)),true_spatial_nonplanarity_hodograph_coefficient_determinant=str(nonplanar),trajectory_speed_formula='8*(1+25*(2v-1)^4/16)',global_hodograph_norm_polynomial_identity_exact=True,global_Frenet_cross_product_factorization_exact=True,Frenet_frame_undefined_at_inflection_v='1/2',Frenet_B_left_limit=list(map(str,minus)),Frenet_B_right_limit=list(map(str,plus)),opposite_binormal_limits_exact=True,all_8_frames_exactly_orthonormal=True,instance_parameters=list(map(str,V_HAT)),interpolation_parameters=list(map(str,VP)),interpolation_parameter_symmetry_exact=True,parameter_error_bound=max(p[1] for p in results),surface_controls=[[[str(x) for x in p] for p in row] for row in net],placed_section_controls=[[[str(x) for x in p] for p in row] for row in rows],u_knots=list(map(str,U)),v_knots=list(map(str,V)),local_section_controls=[[str(x) for x in p] for p in C],all56section_control_vector_interpolation_identities_exact=True,all168rigid_control_distance_identities_exact=(rigid==168),all_7_complete_mid_isocurve_controls_zero=True,whole_middle_cross_section_collapses_exactly_to_origin=True,surface_control_columns_antisymmetric_exact=True,tensor_checks=verify_tensor(*base,steps=4),no_contour_tracing=True)
    return base,VP,rows,report
