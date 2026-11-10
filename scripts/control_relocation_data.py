"""Exact representative cubic relocation, printed11.1; preserves t4=.52/u=.6."""
from fractions import Fraction as F
from native_bspline import segments,de_boor
from bspline_math import evaluate,derivative
U=(F(0),)*4+tuple(map(F,('.2','.35','.5','.71','.9')))+(F(1),)*4
P=tuple(tuple(map(F,p)) for p in [(0,0),(1,0),('1.5','1.3'),('2.5','2.6'),('4.5','3.1'),(6,'2.6'),(7,'1.3'),(7,0),(8,0)])
K=4;DELTA=(F(0),F(-2));UBAR=F(3,5);GRE=tuple(sum(U[i+1:i+4])/3 for i in range(9));assert GRE[4]==F(13,25)
PHAT=tuple(tuple(a+b for a,b in zip(p,DELTA)) if i==K else p for i,p in enumerate(P))
BASIS=tuple((F(i==K),) for i in range(9))
def make():
    old,new,basis=(segments(U,curve,3) for curve in (P,PHAT,BASIS));identities=0
    for a,b,c in zip(old,new,basis):
        for d in range(2):
            assert all(y-x==DELTA[d]*n for x,y,n in zip(a['power'][d],b['power'][d],c['power'][0]));identities+=4
        if a['b']<=U[K] or a['a']>=U[K+4]:assert a['power']==b['power']
    # All derivative Bernstein coefficients nonnegative before the unique peak
    # span, all nonpositive after. In the peak span signs(+,-,-) yield one root:
    # q/(1-t)^2=a+2*b*s+c*s^2 strictly decreases for s=t/(1-t)>=0.
    rising=True;peak=None;signs=[]
    for s in basis:
        coeff=tuple(3*(b[0]-a[0])/(s['b']-s['a']) for a,b in zip(s['bern'],s['bern'][1:]));signs.append(tuple(0 if a==0 else 1 if a>0 else -1 for a in coeff))
        if not any(coeff):continue
        if min(coeff)>=0:assert rising
        elif max(coeff)<=0:rising=False
        else:
            assert peak is None and coeff[0]>0 and coeff[1]<0 and coeff[2]<0 and rising;peak=s;rising=False
    assert peak is not None
    a,b=peak['a'],peak['b'];d=derivative(peak['power'][0])
    for _ in range(64):
        mid=(a+b)/2
        if evaluate(d,mid)>0:a=mid
        else:b=mid
    umax=(a+b)/2;Nmax=de_boor(U,BASIS,3,umax)[0];Nbar=de_boor(U,BASIS,3,UBAR)[0]
    A=de_boor(U,P,3,UBAR);B=de_boor(U,PHAT,3,UBAR);assert tuple(y-x for x,y in zip(A,B))==(0,-2*Nbar)
    assert Nmax>Nbar and a>F(1,2) and b<F(71,100)
    return dict(degree=3,k=K,ubar=UBAR,greville_t4=GRE[4],knots=U,controls=P,modified_controls=PHAT,delta_control=DELTA,selected_point=A,modified_selected_point=B,basis_at_ubar=Nbar,selected_distance=2*Nbar,peak_parameter_bracket=(a,b),peak_parameter=umax,basis_peak_midpoint_value=Nmax,dmax_midpoint_value=2*Nmax,peak_parameter_error_bound=(b-a)/2,peak_distance_error_bound=12*(b-a),exact_whole_power_coefficient_identities=identities,derivative_Bernstein_signs=signs,unique_global_basis_maximum_certified=True,local_support=(U[K],U[K+4]),unchanged_entire_spans_outside_support=True)
