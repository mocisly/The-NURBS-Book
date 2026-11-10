"""Fig5.1/5.2: specified cubic knot vector and representative control polygon."""
from fractions import Fraction as F
K=tuple(map(F,[0,0,0,0,1,2,3,4,5,5,5,5]))
P=tuple(tuple(F(str(v)) for v in p) for p in [(0,1.5),(2,2.6),(4,0),(8,0),(10,3),(8,5.6),(4,5.6),(2.8,3.6)])
def insert(U,P,p,u):
    k=next(i for i in range(p,len(P)) if U[i]<=u<U[i+1])
    Q=[];alphas={}
    for i in range(len(P)+1):
        if i<=k-p:Q.append(P[i])
        elif i>k:Q.append(P[i-1])
        else:
            a=(u-U[i])/(U[i+p]-U[i]);alphas[i]=a
            Q.append(tuple(a*x+(1-a)*y for x,y in zip(P[i],P[i-1])))
    return U[:k+1]+(u,)+U[k+1:],tuple(Q),alphas
