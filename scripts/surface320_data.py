"""Representative semantic 5x4 control net for the two pieces of Fig3.20."""
from fractions import Fraction as F
from bspline_math import basis
from native_bspline import de_boor

# The illustration supplies indices but no coordinates, degrees or knot values.
# A documented bicubic example preserves its rectangular topology and stepped sheet.
U=(F(0),)*4+(F(1,2),)+(F(1),)*4
V=(F(0),)*4+(F(1),)*4
xs=(3,1,0,-2);ys=(-1,0,1,2,3)
zi=(F(3,2),F(3,2),F(0),F(-1,4),F(-1,2));zj=(F(0),F(-1,2),F(1,2),F(0))
P=tuple(tuple((F(xs[j]),F(ys[i]),zi[i]+zj[j]) for j in range(4)) for i in range(5))
def weights(k,p,t):
    n=len(k)-p-1
    return [F(i==n-1) for i in range(n)] if t==k[-1] else [basis(k,i,p,t) for i in range(n)]
def tensor(u,v):
    a,b=weights(U,3,u),weights(V,3,v)
    return tuple(sum(a[i]*b[j]*P[i][j][d] for i in range(5) for j in range(4)) for d in range(3))
def verify():
    for a in range(21):
        u=F(a,20);wu=weights(U,3,u);assert min(wu)>=0 and sum(wu)==1
        for b in range(21):
            v=F(b,20);wv=weights(V,3,v);assert min(wv)>=0 and sum(wv)==1
            # Independent nested de Boor in each order agrees exactly with the tensor sum.
            q=[de_boor(U,[P[i][j] for i in range(5)],3,u) for j in range(4)]
            r=[de_boor(V,P[i],3,v) for i in range(5)]
            assert tensor(u,v)==de_boor(V,q,3,v)==de_boor(U,r,3,u)
    assert tensor(F(0),F(0))==P[0][0] and tensor(F(1),F(0))==P[4][0]
    assert tensor(F(0),F(1))==P[0][3] and tensor(F(1),F(1))==P[4][3]
    return {'figure':'3.20','representative_example':True,'degrees':[3,3],
        'U':list(map(str,U)),'V':list(map(str,V)),
        'control_net':[[[str(v) for v in p] for p in row] for row in P],
        'control_count':[5,4],'exact_tensor_vs_deboor_grid_points':441,
        'nonnegative_partition':True,'four_corner_interpolation':True,
        'camera':{'x':['-.9','-.6'],'y':['1','-.35'],'z':['0','1']}}
