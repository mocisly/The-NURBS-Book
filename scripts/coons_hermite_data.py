"""Compatible boundary derivatives, corner twists and exact bicubic Coons nets.

Same boundaries as10.24/25. A known graph supplies compatible fields, with an
additional spline f(u)*h10(v) giving a genuinely cubic v dependence. Full common-
basis coefficients, entire boundary curves and derivative fields are checked.
"""
from fractions import Fraction as F
from itertools import combinations
from coons_patch_data import U,V,GU,GV,C0U,C1U,C0V,C1V,CORNERS,view,construct as bilinear_nets
from native_bspline import segments,de_boor
from surface_geometry import weights,isocurve,surface
from inverse_knot_projection import solve
from rational_surface_partials import derived_net
BEZ=(F(0),)*4+(F(1),)*4
VCUB=(F(0),)*4+(F(2,5),F(2,5),F(3,5),F(3,5))+(F(1),)*4
RESID=tuple(map(F,(0,0,1,-1,0,0)))
def add(a,b,s=1):return tuple(x+s*y for x,y in zip(a,b))
def mul(a,s):return tuple(s*x for x in a)
def derivative(K,P,p):return K[1:-1],tuple(mul(add(b,a,-1),F(p,K[i+p+1]-K[i+1])) for i,(a,b) in enumerate(zip(P,P[1:]))),p-1
def convert(K,P,p,L,q):
    t=tuple(sum(L[i+1:i+q+1])/q for i in range(len(L)-q-1));matrix=tuple(tuple(weights(L,q,z)) for z in t)
    Q=solve(matrix,tuple(de_boor(K,P,p,z) for z in t));old,new=segments(K,P,p),segments(L,Q,q)
    for s in new:
        prev=next(a for a in old if a['a']<=s['a'] and s['b']<=a['b'])
        for a,b in zip(prev['power'],s['power']):assert a+(F(0),)*(q-p)==b
    return Q
def convert_net(net,L,M):
    K,J,p,q,P=net
    columns=tuple(convert(K,tuple(row[j] for row in P),p,L,3) for j in range(len(P[0])))
    A=tuple(tuple(col[i] for col in columns) for i in range(len(L)-4))
    return L,M,3,3,tuple(convert(J,row,q,M,3) for row in A)
def make():
    base=bilinear_nets()['S'];fu=tuple(GU[i]-sum(a*b for a,b in combinations(U[i+1:i+4],2))/3 for i in range(6));gv=tuple(GV[j]-V[j+1]*V[j+2] for j in range(5))
    assert all(s['power'][0]==(0,1,-1,0) for s in segments(U,tuple((x,) for x in fu),3))
    assert all(s['power'][0]==(0,1,-1) for s in segments(V,tuple((x,) for x in gv),2))
    seed=tuple(tuple(add(base[4][i][j],(0,0,16*fu[i]*gv[j])) for j in range(5)) for i in range(6))
    D0U=tuple(add(mul(add(row[1],row[0],-1),5),(0,0,4*RESID[i])) for i,row in enumerate(seed))
    D1U=tuple(mul(add(row[-1],row[-2],-1),5) for row in seed)
    D0V=tuple(mul(add(seed[1][j],seed[0][j],-1),10) for j in range(5))
    D1V=tuple(mul(add(seed[-1][j],seed[-2][j],-1),10) for j in range(5))
    DK=(D0U,D1U);DL=(D0V,D1V);twists=[]
    for a in (0,1):
        row=[]
        for b in (0,1):
            K,P,p=derivative(U,DK[b],3);tw=de_boor(K,P,p,F(a));L,Q,q=derivative(V,DL[a],2);assert tw==de_boor(L,Q,q,F(b));row.append(tw)
            K,P,p=derivative(U,(C0U,C1U)[b],3);assert de_boor(K,P,p,F(a))==DL[a][0 if b==0 else -1]
            K,P,p=derivative(V,(C0V,C1V)[a],2);assert de_boor(K,P,p,F(b))==DK[b][0 if a==0 else -1]
        twists.append(tuple(row))
    TW=tuple(twists)
    S1=(U,BEZ,3,3,tuple((C0U[i],add(C0U[i],D0U[i],F(1,3)),add(C1U[i],D1U[i],-F(1,3)),C1U[i]) for i in range(6)))
    cols=tuple((C0V[j],add(C0V[j],D0V[j],F(1,3)),add(C1V[j],D1V[j],-F(1,3)),C1V[j]) for j in range(5))
    S2=(BEZ,V,3,2,tuple(tuple(col[i] for col in cols) for i in range(4)))
    T=[[None]*4 for _ in range(4)]
    for a in (0,1):
        i,h,su=(0,1,1) if a==0 else (3,2,-1)
        for b in (0,1):
            j,k,sv=(0,1,1) if b==0 else (3,2,-1)
            P=CORNERS[a][b];DU=DL[a][0 if b==0 else -1];DV=DK[b][0 if a==0 else -1]
            T[i][j]=P;T[h][j]=add(P,DU,F(su,3));T[i][k]=add(P,DV,F(sv,3));T[h][k]=add(add(add(P,DU,F(su,3)),DV,F(sv,3)),TW[a][b],F(su*sv,9))
    T=(BEZ,BEZ,3,3,tuple(map(tuple,T)))
    TU=derived_net(*T,0);TV=derived_net(*T,1);TUV=derived_net(*TU,1)
    for a in (0,1):
        for b in (0,1):
            assert surface(*T,F(a),F(b))==CORNERS[a][b]
            assert surface(*TU,F(a),F(b))==DL[a][0 if b==0 else -1]
            assert surface(*TV,F(a),F(b))==DK[b][0 if a==0 else -1]
            assert surface(*TUV,F(a),F(b))==TW[a][b]
    refined=tuple(convert_net(net,U,VCUB) for net in (S1,S2,T));A,B,C=(net[4] for net in refined)
    P=tuple(tuple(add(add(A[i][j],B[i][j]),C[i][j],-1) for j in range(8)) for i in range(6));S=(U,VCUB,3,3,P)
    reference=convert_net((U,V,3,2,seed),U,VCUB)[4];h10=convert(BEZ,((F(0),),(F(1,3),),(F(0),),(F(0),)),3,VCUB,3)
    assert all(P[i][j]==add(reference[i][j],(0,0,4*RESID[i]*h10[j][0])) for i in range(6) for j in range(8))
    for b,cur in enumerate((C0U,C1U)):
        assert isocurve(*S,'u',F(b))[2]==cur
        # Endpoint v derivative has the same U coefficients as the supplied field.
        derivative_controls=tuple(mul(add(row[1],row[0],-1),F(15,2)) if b==0 else mul(add(row[-1],row[-2],-1),F(15,2)) for row in P)
        assert derivative_controls==DK[b]
    for a,cur in enumerate((C0V,C1V)):
        assert isocurve(*S,'v',F(a))[2]==convert(V,cur,2,VCUB,3)
        derivative_controls=tuple(mul(add(P[1][j],P[0][j],-1),10) if a==0 else mul(add(P[-1][j],P[-2][j],-1),10) for j in range(8))
        assert derivative_controls==convert(V,DL[a],2,VCUB,3)
    assert any(s['power'][2][3] for s in segments(VCUB,isocurve(*S,'v',F(2,5))[2],3))
    return dict(DK=DK,DL=DL,twists=TW,nets=dict(S1=S1,S2=S2,T=T,refined=refined,S=S),whole_boundary_vector_control_identities=28,whole_derivative_vector_control_identities=28,exact_corner_twist_vector_identities=4,T_corner_jet_vector_identities=16,whole_reference_surface_coefficient_identities=48,actual_cubic_v_dependence=True)
