"""Actual local bicubic Hermite construction, Eq9.55..59 and A9.5.

Reuse the16representative step-profile data from9.15..17. Common mesh parameters
sum chord increments across lines, as A9.5; unit tangents use Akima estimates.
At boundaries use Eq9.32 one-sided Bessel field derivatives and the nearest
interior alpha/beta. All shared positions, first derivatives and knot removals
are exact rational equalities for the certified represented length constants.
"""
from fractions import Fraction as F
from mesh_interpolation_example_data import Q
from local_quadratic_interpolator import add,mul,length,tangents,unit
from inverse_knot_projection import remove_to
from surface_geometry import surface,local_patch

def matrix(rows):return tuple(tuple(r) for r in rows)
ULINES=tuple(tuple(Q[i][j] for i in range(4)) for j in range(4));VLINES=Q
def direction_data(lines,axis):
    ell=tuple(tuple(length(add(B,A,-1)) for A,B in zip(line,line[1:])) for line in lines)
    totals=tuple(sum(row) for row in ell);increments=tuple(sum(row[k] for row in ell) for k in range(3))
    params=tuple(sum(increments[:i])/sum(increments) for i in range(4))
    derivatives=[]
    for line,total in zip(lines,totals):
        projected=tuple((q[axis],q[2]) for q in line);D=[]
        for a,b in (unit(t) for t in tangents(projected,'akima')):
            D.append((a*total,F(0),b*total) if axis==0 else (F(0),a*total,b*total))
        derivatives.append(tuple(D))
    return params,totals,tuple(derivatives)
UP,R,DUCOL=direction_data(ULINES,0);VP,S,DV=direction_data(VLINES,1)
DU=tuple(tuple(DUCOL[j][i] for j in range(4)) for i in range(4))

def field_derivative(values,params):
    slopes=tuple(mul(add(B,A,-1),1/(v-u)) for A,B,u,v in zip(values,values[1:],params,params[1:]))
    a=tuple((params[k]-params[k-1])/(params[k+1]-params[k-1]) for k in (1,2))
    inside=tuple(add(mul(slopes[k-1],1-a[k-1]),slopes[k],a[k-1]) for k in (1,2))
    return (add(mul(slopes[0],2),inside[0],-1),)+inside+(add(mul(slopes[-1],2),inside[-1],-1),)
def blend_weights(params):
    a=tuple((params[k]-params[k-1])/(params[k+1]-params[k-1]) for k in (1,2));return (a[0],a[0],a[1],a[1])
AU,BV=blend_weights(UP),blend_weights(VP)
VU_COL=tuple(field_derivative(tuple(DV[i][j] for i in range(4)),UP) for j in range(4))
VU=tuple(tuple(VU_COL[j][i] for j in range(4)) for i in range(4))
UV=tuple(field_derivative(row,VP) for row in DU)
MIX=tuple(tuple(mul(add(mul(UV[i][j],AU[i]),VU[i][j],BV[j]),1/(AU[i]+BV[j])) for j in range(4)) for i in range(4))
assert any(any(x for x in v) for row in MIX for v in row)
PATCH=[];FULL=[[None]*10 for _ in range(10)]
for k in range(3):
    row=[];hu=UP[k+1]-UP[k]
    for l in range(3):
        hv=VP[l+1]-VP[l];b=[]
        for i in range(4):
            ki=k+int(i>=2);cu=hu/3 if i==1 else -hu/3 if i==2 else F(0);rr=[]
            for j in range(4):
                lj=l+int(j>=2);cv=hv/3 if j==1 else -hv/3 if j==2 else F(0)
                pt=add(add(add(Q[ki][lj],DU[ki][lj],cu),DV[ki][lj],cv),MIX[ki][lj],cu*cv)
                rr.append(pt);a,bidx=3*k+i,3*l+j
                assert FULL[a][bidx] is None or FULL[a][bidx]==pt;FULL[a][bidx]=pt
            b.append(tuple(rr))
        row.append(tuple(b))
    PATCH.append(tuple(row))
PATCH=tuple(PATCH);FULL=matrix(FULL)
UC=(F(0),)*4+tuple(t for x in UP[1:-1] for t in (x,x,x))+(F(1),)*4
VC=(F(0),)*4+tuple(t for x in VP[1:-1] for t in (x,x,x))+(F(1),)*4
# Batch all spatial coordinates as multiple exact right-hand sides.
flat=tuple(tuple(x for pt in row for x in pt) for row in FULL)
U,tmp,REMOVE_U=remove_to(UC,flat,3,UP[1:-1]);assert REMOVE_U['curve_exactly_unchanged']
U_NET=tuple(tuple(tuple(row[3*j+d] for d in range(3)) for j in range(10)) for row in tmp)
flatv=tuple(tuple(x for i in range(8) for x in U_NET[i][j]) for j in range(10))
V,tmpv,REMOVE_V=remove_to(VC,flatv,3,VP[1:-1]);assert REMOVE_V['curve_exactly_unchanged']
P=tuple(tuple(tuple(tmpv[j][3*i+d] for d in range(3)) for j in range(8)) for i in range(8))
assert len(P)==len(P[0])==8
assert all(surface(U,V,3,3,P,u,v)==Q[i][j] for i,u in enumerate(UP) for j,v in enumerate(VP))
# Prove that all9whole extracted bicubic patches exactly equal the construction.
USPAN=[i for i in range(3,8) if U[i]<U[i+1]];VSPAN=[i for i in range(3,8) if V[i]<V[i+1]]
for k,us in enumerate(USPAN):
    for l,vs in enumerate(VSPAN):assert local_patch(U,V,3,3,P,us,vs)[0]==PATCH[k][l]
# Full-edge derivative coefficient equalities, stronger than sampled C1 checks.
EDGE_CHECKS=0
for k in range(2):
    for l in range(3):
        for j in range(4):
            a=mul(add(PATCH[k][l][3][j],PATCH[k][l][2][j],-1),3/(UP[k+1]-UP[k]))
            b=mul(add(PATCH[k+1][l][1][j],PATCH[k+1][l][0][j],-1),3/(UP[k+2]-UP[k+1]))
            assert a==b;EDGE_CHECKS+=1
for k in range(3):
    for l in range(2):
        for i in range(4):
            a=mul(add(PATCH[k][l][i][3],PATCH[k][l][i][2],-1),3/(VP[l+1]-VP[l]))
            b=mul(add(PATCH[k][l+1][i][1],PATCH[k][l+1][i][0],-1),3/(VP[l+2]-VP[l+1]))
            assert a==b;EDGE_CHECKS+=1
BASE=(U,V,3,3,P)
