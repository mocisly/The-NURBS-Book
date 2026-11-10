"""Representative3x2 surface with globally well-posed point projection.

S is a graph z=h(x,y)=2/5(f(y)+g(x)). On its rectangle, |f''|<1,
|g''|<=1, |f'|<=11/13, |g'|<=1. For points in the control-net height
range, the half squared-distance Hessian has eigenvalues in[41/125,2].
Hence the box-constrained objective is strongly convex: projected gradient
with step1/2 converges to the unique GLOBAL closest point. No SciPy required.
"""
from fractions import Fraction as F
from math import sqrt
from knot59_data import U,V,P as OLD

ZETA=F(2,5);P=tuple(tuple((x,y,ZETA*z) for x,y,z in row) for row in OLD)
BASE=(U,V,3,2,P);MU=F(41,125);L=F(2)
FY_SECOND_BOUND=F(66,5)/F(39,10)**2+F(33,10)*F(6,5)/F(39,10)**3
assert FY_SECOND_BOUND<1
HEIGHT_RANGE=F(42,25)
assert 1-HEIGHT_RANGE*ZETA==MU
assert 1+ZETA**2*(1+F(11,13)**2)+HEIGHT_RANGE*ZETA<L
CAMERA=r'x={(-1.08cm,-.72cm)},y={(1.2cm,-.42cm)},z={(0cm,3cm)}'

def partials(u,v):
    """Exact rational Su/Sv when supplied rational parameters."""
    yu=F(21,5)-F(6,5)*u+F(6,5)*u*u
    zu=-F(66,5)*u+F(66,5)*u*u
    if v<=F(1,2):xv,zv=-8+8*v,8*v
    else:xv,zv=-8*v,8-8*v
    return (F(0),yu,ZETA*zu),(xv,F(0),ZETA*zv)

def y_of_u(u):return -2+4.2*u-.6*u*u+.4*u*u*u

def u_of_y(y):
    if y==-2:return 0.
    if y==2:return 1.
    u=(y+2)/4
    for j in range(12):
        change=(y_of_u(u)-y)/(4.2-1.2*u+1.2*u*u)
        u-=change
        if abs(change)<2e-16:break
    assert -1e-14<=u<=1+1e-14 and abs(y_of_u(u)-y)<3e-15
    return min(1.,max(0.,u))

def graph(x,y):
    assert -3-1e-14<=x<=3+1e-14 and -2-1e-14<=y<=2+1e-14
    u=u_of_y(y);yu=4.2-1.2*u+1.2*u*u;yuu=-1.2+2.4*u
    f=1-6.6*u*u+4.4*u*u*u;fu=-13.2*u+13.2*u*u;fuu=-13.2+26.4*u
    if x>=0:
        r=sqrt(1+x);g=5+x-4*r;gx=1-2/r;gxx=1/r**3;v=1-r/2
    else:
        r=sqrt(1-x);g=x-3+4*r;gx=1-2/r;gxx=-1/r**3;v=r/2
    a=float(ZETA)
    return a*(f+g),a*gx,a*fu/yu,a*gxx,a*(fuu*yu-fu*yuu)/yu**3,u,v

def project(point):
    X,Y,Z=map(float,point);assert -.480000000001<=Z<=1.200000000001
    x,y=X,Y;last_value=float('inf')
    for iteration in range(600):
        z,hx,hy,hxx,hyy,u,v=graph(x,y);rz=z-Z
        value=((x-X)**2+(y-Y)**2+rz*rz)/2
        assert value<=last_value+2e-14;last_value=value
        gx=x-X+rz*hx;gy=y-Y+rz*hy
        xx=min(3.,max(-3.,x-gx/2));yy=min(2.,max(-2.,y-gy/2))
        step=sqrt((xx-x)**2+(yy-y)**2)
        if step<2e-14:break
        x,y=xx,yy
    else:raise AssertionError('Projection did not converge.')
    z,hx,hy,hxx,hyy,u,v=graph(x,y)
    gx=x-X+(z-Z)*hx;gy=y-Y+(z-Z)*hy
    residual=sqrt(gx*gx+gy*gy)
    assert residual<2e-12
    return (x,y,z),(u,v),{'iterations':iteration+1,'gradient_norm':residual,
                         'projected_step_norm':step,'strong_convexity_mu':str(MU),
                         'gradient_Lipschitz_upper_bound':str(L),
                         'estimated_xy_position_error_bound_including_roundoff':2*step/float(MU)+1e-11}
