"""One compatible representative network for printed10.18--10.23.

Original degrees and input knots retained. Numeric points were not supplied.
L2 and T deliberately share the SAME cardinal interpolation basis, as required
by10.31/10.32. The near-knot reuse suggested by the text is applied at creation.
"""
from fractions import Fraction as F
from surface_geometry import isocurve,weights,surface
from native_bspline import de_boor
from inverse_knot_projection import solve
from global_interpolation_data import interpolate
from knot59_data import insert_surface
UC=(F(0),)*4+(F(3,10),F(7,10))+(F(1),)*4
VC=(F(0),)*3+(F(2,5),F(3,5))+(F(1),)*3
UH=tuple(map(F,('0','.28','.72','1')))
VH=tuple(map(F,('0','.16','.482','.812','1')))
GX=tuple(sum(UC[i+1:i+4])/3 for i in range(6))
GY=tuple(sum(VC[j+1:j+3])/2 for j in range(5))
Z=tuple(tuple(map(F,row)) for row in [('.2','.6','1.4','1.3','.8'),('-.4','.2','1.8','2.3','1.5'),('1.4','2.2','1.1','2','2.7'),('1.2','2.1','.8','1.3','2.2'),('-.5','.7','2.3','2.5','1.2'),('.1','.8','1.6','1.2','.4')])
P=tuple(tuple((8*GX[i]-4,7*GY[j]-F(7,2),Z[i][j]) for j in range(5)) for i in range(6))
INPUT=(UC,VC,3,2,P)
CK=tuple(isocurve(*INPUT,'u',v)[2] for v in VH)
CL=tuple(isocurve(*INPUT,'v',u)[2] for u in UH)
Q=tuple(tuple(de_boor(UC,CK[k],3,u) for k in range(5)) for u in UH)
assert all(Q[l][k]==de_boor(VC,CL[l],2,v) for l in range(4) for k,v in enumerate(VH))
UL1=(F(0),)*4+(F(1),)*4
VL2=(F(0),)*3+(F(321,1000),F(647,1000))+(F(1),)*3

def construct():
    a=tuple(tuple(weights(UL1,3,u)) for u in UH)
    b=tuple(tuple(weights(VL2,2,v)) for v in VH)
    columns=tuple(solve(a,tuple(CL[l][j] for l in range(4))) for j in range(5))
    L1=(UL1,VC,3,2,tuple(tuple(columns[j][i] for j in range(5)) for i in range(4)))
    L2=(UC,VL2,3,2,tuple(solve(b,tuple(CK[k][i] for k in range(5))) for i in range(6)))
    temp=tuple(solve(b,row) for row in Q)
    cols=tuple(solve(a,tuple(temp[l][j] for l in range(4))) for j in range(5))
    T=(UL1,VL2,3,2,tuple(tuple(cols[j][i] for j in range(5)) for i in range(4)))
    commonV=tuple(sorted(VC+tuple(t for t in VL2 if t not in (0,1) and t not in VC)))
    refined=[]
    for net in (L1,L2,T):
        for axis,target in [('u',UC),('v',commonV)]:
            old=net[0 if axis=='u' else 1]
            for t in sorted(set(target)):
                for _ in range(target.count(t)-old.count(t)):net=insert_surface(*net,axis,t)
        assert net[:4]==(UC,commonV,3,2);refined.append(net)
    A,B,C=(net[4] for net in refined)
    S=(UC,commonV,3,2,tuple(tuple(tuple(A[i][j][d]+B[i][j][d]-C[i][j][d] for d in range(3)) for j in range(7)) for i in range(6)))
    # Entire curve coefficient identities, not only sample points.
    for k,v in enumerate(VH):assert isocurve(*S,'u',v)[2]==CK[k]
    for l,u in enumerate(UH):
        # Refine each original v curve to the shared V basis.
        test=(UL1,VC,3,2,tuple(CL[l] for _ in range(4)))
        for t in (F(321,1000),F(647,1000)):test=insert_surface(*test,'v',t)
        assert isocurve(*S,'v',u)[2]==test[4][0]
    return dict(L1=L1,L2=L2,T=T,refined=tuple(refined),S=S)

def view(p):
    x,y,z=p
    return F(3,2)*(-F(4,5)*x+F(3,5)*y),F(3,2)*(-F(9,25)*x-F(12,25)*y+F(4,5)*z)
