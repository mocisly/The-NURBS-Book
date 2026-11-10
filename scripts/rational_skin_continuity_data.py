"""10.10given positive section weights, C1 projections and actual C0 rational skin."""
from fractions import Fraction as F
from rational_geometry import split,project
from native_bspline import segments
from bspline_math import evaluate,derivative
from bounded_curve_approximation import chord_parameters
from global_interpolation_data import interpolate
from surface_geometry import weights,verify_tensor,isocurve
U=(F(0),)*3+(F(1,2),)*2+(F(1),)*3
W=tuple(tuple(map(F,row)) for row in [(1,2,1,1,1),(1,1,1,3,1),(1,1,1,1,1),(1,4,1,2,1)])
X=tuple(map(F,('-9/2','-3/2','3/2','9/2')));H=tuple(map(F,('0','1','1/2','2')))
P=tuple(((x,-F(2),h-3),(x,-1/w[1],h),(x,F(0),h),(x,1/w[3],h),(x,F(2),h+3)) for x,h,w in zip(X,H,W))
HP=tuple(tuple(tuple(w*x for x in p)+(w,) for p,w in zip(row,ws)) for row,ws in zip(P,W))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def projected_derivative(power,t):
    h=tuple(evaluate(c,t) for c in power);d=tuple(evaluate(derivative(c),t) for c in power)
    return tuple((d[i]*h[-1]-h[i]*d[-1])/h[-1]**2 for i in range(len(h)-1))
def positive_pieces(bern,a=F(0),b=F(1),depth=0):
    if min(p[-1] for p in bern)>0:return[(a,b,bern)]
    assert depth<14,('No strictly positive denominator certificate',a,b)
    L,R=split(bern);mid=(a+b)/2
    return positive_pieces(L,a,mid,depth+1)+positive_pieces(R,mid,b,depth+1)
def construct():
    inputproof=[]
    for k,row in enumerate(HP):
        ss=segments(U,row,2);left,right=ss
        dl=projected_derivative(left['power'],F(1,2));dr=projected_derivative(right['power'],F(1,2));assert dl==dr==(F(0),F(4),F(0))
        HL=tuple(evaluate(derivative(c),F(1,2)) for c in left['power']);HR=tuple(evaluate(derivative(c),F(1,2)) for c in right['power'])
        assert (HL==HR)==(k==2)
        inputproof.append(dict(section=k,Euclidean_C1_derivative=list(map(str,dl)),homogeneous_C1=(HL==HR)))
    param=[chord_parameters(tuple(HP[k][i] for k in range(4))) for i in range(5)]
    VP=tuple(sum(row[0][k] for row in param)/5 for k in range(4));net=[]
    for i in range(5):V,row=interpolate(tuple(HP[k][i] for k in range(4)),VP,3);net.append(row)
    net=tuple(net);base=(U,V,2,3,net);assert V==(F(0),)*4+(F(1),)*4
    for k,v in enumerate(VP):
        w=weights(V,3,v)
        assert all(tuple(sum(a*p[d] for a,p in zip(w,row)) for d in range(4))==HP[k][i] for i,row in enumerate(net))
    positives=[]
    for row in net:positives+=positive_pieces(tuple((p[-1],) for p in row))
    column_lower=min(p[-1] for a,b,bb in positives for p in bb);assert column_lower>0
    # On each quadratic half W=1+2t(1-t)(w_middle(v)-1).
    # The two endpoint weight functions are identically1 and2t(1-t)<=1/2.
    lower=min(F(1),(1+column_lower)/2);assert lower>F(1,2)
    negative=[(i,j) for i,row in enumerate(net) for j,p in enumerate(row) if p[-1]<0];assert negative
    seam=[]
    for v in (F(1,4),F(1,2),F(3,4)):
        K,p,C=isocurve(*base,'u',v);ss=segments(K,C,p)
        dl,dr=[projected_derivative(s['power'],F(1,2)) for s in ss]
        L,q,R=isocurve(*base,'v',F(1,2));sv=projected_derivative(segments(L,R,q)[0]['power'],v)
        nl,nr=cross(dl,sv),cross(dr,sv);turn=cross(nl,nr);sq=sum(x*x for x in turn)
        assert dl!=dr and sq>0
        seam.append(dict(v=str(v),left_du=list(map(str,dl)),right_du=list(map(str,dr)),normal_cross_squared=str(sq),geometric_tangent_plane_jump_exact=True))
    report=dict(figure='10.10',representative_controls=True,section_degrees=[2]*4,u_knots=list(map(str,U)),section_weights=[list(map(str,row)) for row in W],section_controls=[[[str(x) for x in p] for p in row] for row in P],section_continuity=inputproof,v_degree=3,v_parameters=list(map(str,VP)),Eq10_14_4D_chord_parameter_error_bound=max(row[1] for row in param),v_knots=list(map(str,V)),surface_control_shape=[5,4],surface_homogeneous_controls=[[[str(x) for x in p] for p in row] for row in net],surface_weight_rows_j_columns_i=[[str(net[i][j][-1]) for i in range(5)] for j in range(4)],negative_surface_weight_indices_ij=negative,all20homogeneous_section_control_interpolation_identities_exact=True,all4whole_Euclidean_sections_interpolated=True,global_denominator_positive_lower_bound=str(lower),positive_weight_column_subdivision_intervals=len(positives),no_poles_anywhere=True,seam_normal_jump_counterexamples=seam,tensor_checks=verify_tensor(*base,steps=3))
    return base,VP,report
