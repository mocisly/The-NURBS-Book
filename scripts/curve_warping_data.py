"""Representative parabolic cubic, true local refinement and Eq11.48 warping."""
from fractions import Fraction as F
from decimal import Decimal,localcontext
from knot51_data import insert
from native_bspline import segments,de_boor
from warping_basis_data import f
from inverse_knot_projection import solve
US,UE=F(1,4),F(3,4)
U=(F(0),)*4+(F(1),)*4;P=((F(0),F(0)),(F(4,3),F(4,3)),(F(8,3),F(4,3)),(F(4),F(0)))
for t in(F(1,4),F(1,2),F(3,4)):U,P,_=insert(U,P,3,t)
K,Q=U,P;ADDED=[]
for _ in range(3):
    midpoints=tuple((a+b)/2 for a,b in zip(K,K[1:])if US<=a<b<=UE)
    for t in midpoints:K,Q,_=insert(K,Q,3,t);ADDED.append(t)
identities=0
for s in segments(K,Q,3):
    original=next(z for z in segments(U,P,3)if z['a']<=s['a']<s['b']<=z['b']);assert s['power']==original['power'];identities+=8
ELIGIBLE=tuple(i for i in range(len(Q))if K[i]>=US and K[i+4]<=UE)
assert ELIGIBLE==tuple(range(K.index(US),K.index(UE)-3))
def length(v):
    with localcontext() as c:
        c.prec=50;return sum(Decimal(x.numerator)/Decimal(x.denominator)*Decimal(x.numerator)/Decimal(x.denominator)for x in v).sqrt()
start,end=min(ELIGIBLE)-1,max(ELIGIBLE)+1;L=[Decimal(0)]
for a,b in zip(Q[start:end],Q[start+1:end+1]):L.append(L[-1]+length(tuple(y-x for x,y in zip(a,b))))
PARAMS={i:F(str(round(L[i-start]/L[-1],12)))for i in ELIGIBLE}
def warp(w=F(1),distance=F(3,5),direction=(F(0),-F(1))):
    R=tuple(tuple(x+distance*f(PARAMS[i],w)*d for x,d in zip(p,direction))if i in PARAMS else p for i,p in enumerate(Q))
    assert all(0<=f(t,w)<=1 for t in PARAMS.values())
    assert all(p==q for i,(p,q)in enumerate(zip(Q,R))if i not in ELIGIBLE)
    return R
def remove_local(R,removed):
    W=list(K)
    for t in removed:W.remove(t)
    W=tuple(W);n=len(W)-4
    A=tuple(tuple(F(i==j)for j in range(n))for i in range(n));V=W
    for t in sorted(removed):V,A,_=insert(V,A,3,t)
    assert V==K
    originalU,originalP=U,P
    for t in sorted(ADDED):
        if t not in removed:originalU,originalP,_=insert(originalU,originalP,3,t)
    assert originalU==W
    fixed={i:originalP[i] for i in range(n)if W[i]<US or W[i+4]>UE}
    for row,pt in zip(A,R):
        if row.count(F(1))==1:
            j=row.index(F(1));assert j not in fixed or fixed[j]==pt;fixed[j]=pt
    free=[i for i in range(n)if i not in fixed]
    residual=tuple(tuple(pt[d]-sum(row[j]*q[d]for j,q in fixed.items())for d in range(2))for row,pt in zip(A,R))
    if free:
        gram=tuple(tuple(sum(row[i]*row[j]for row in A)for j in free)for i in free)
        rhs=tuple(tuple(sum(row[i]*r[d]for row,r in zip(A,residual))for d in range(2))for i in free)
        fixed.update(zip(free,solve(gram,rhs)))
    S=tuple(fixed[i]for i in range(n));reconstructed=tuple(tuple(sum(row[j]*S[j][d]for j in range(n))for d in range(2))for row in A)
    errors=tuple(tuple(x-y for x,y in zip(p,q))for p,q in zip(R,reconstructed));bound=max(sum(map(abs,e))for e in errors)
    assert all(sum(row[j]*e[d]for row,e in zip(A,errors))==0 for j in free for d in range(2))
    return W,S,dict(certified_whole_domain_L1_error_bound_cm=str(bound),common_basis_residuals=errors,protected_exterior_controls=True,method='constrained local least squares inverse insertion; fixed every coarse control whose support extends outside selected interval')
def simplify(R,epsilon=F(1,200)):
    removed=[];remaining=sorted(ADDED);history=[];cache={}
    while remaining:
        choices=[]
        for t in remaining:
            key=tuple(sorted(removed+[t]))
            if key not in cache:cache[key]=remove_local(R,key)
            W,S,report=cache[key];bound=F(report['certified_whole_domain_L1_error_bound_cm']);choices.append((bound,t,W,S,report))
        bound,t,W,S,report=min(choices,key=lambda c:(c[0],c[1]))
        if bound>epsilon:break
        removed.append(t);remaining.remove(t);history.append(dict(removed=t,whole_curve_bound=bound))
    if removed:W,S,report=cache[tuple(sorted(removed))]
    else:W,S,report=K,R,dict(certified_whole_domain_L1_error_bound_cm='0')
    for s in segments(W,S,3):
        if s['b']<=US or s['a']>=UE:
            z=next(z for z in segments(U,P,3)if z['a']<=s['a']<s['b']<=z['b']);assert s['power']==z['power']
    report.update(history=history,tolerance=epsilon,control_counts=(len(Q),len(S)),entire_exterior_spans_unchanged=True)
    return W,S,report
