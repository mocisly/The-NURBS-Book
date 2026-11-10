"""51analytic logarithmic-spiral samples,0<=theta<=3pi,certified rounding."""
from decimal import Decimal as D,localcontext
from fractions import Fraction as F
PI='3.14159265358979323846264338327950288419716939937510582097494459230781640628620899'
def sincos(x,pi):
    while x>pi:x-=2*pi
    while x<-pi:x+=2*pi
    sine=x;cosine=D(1);a=x;b=D(1)
    for k in range(1,130):
        a*=-x*x/D((2*k)*(2*k+1));b*=-x*x/D((2*k-1)*(2*k));sine+=a;cosine+=b
        if max(abs(a),abs(b))<D('1e-75'):break
    assert max(abs(a),abs(b))<D('1e-75')
    return sine,cosine
Q=[];DIRECTIONS=[];THETA=[]
with localcontext() as ctx:
    ctx.prec=85;pi=D(PI)
    for i in range(51):
        t=3*pi*D(i)/50;s,c=sincos(t,pi);r=(t/5).exp()/2
        rounded=lambda x:F(str(x.quantize(D('1e-30'))))
        Q.append((rounded(r*c),rounded(r*s)))
        DIRECTIONS.append((rounded(r*(c/5-s)),rounded(r*(s/5+c))))
        THETA.append(str(t))
Q=tuple(Q);DIRECTIONS=tuple(DIRECTIONS)
TRUE_POINT_L1_ERROR_BOUND=F(1,10**28)
assert len(set(Q))==51
