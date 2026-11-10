"""Algorithm A12.1 over exact homogeneous or Euclidean control vectors."""
from fractions import Fraction as F
def left_stages(K,P,p):
    U=list(K);Q=list(P);n=len(Q)-1;states=[]
    for i in range(p-1):
        U[p-i-1]=U[p-i]-(U[n-i+1]-U[n-i]);k=p-1;ops=[]
        for j in range(i,-1,-1):
            alpha=(U[p]-U[k])/(U[p+j+1]-U[k]);assert 0<=alpha<1
            old=Q[j];Q[j]=tuple((a-alpha*b)/(1-alpha)for a,b in zip(Q[j],Q[j+1]));assert old==tuple((1-alpha)*a+alpha*b for a,b in zip(Q[j],Q[j+1]));ops.append(dict(index=j,alpha=alpha,before=old,after=Q[j]));k-=1
        states.append(dict(i=i,knots=tuple(U),controls=tuple(Q),operations=ops))
    U[0]=U[1]-(U[n-p+2]-U[n-p+1]);return tuple(U),tuple(Q),states
def unclamp(K,P,p):
    U,Q,states=left_stages(K,P,p);U=list(U);Q=list(Q);n=len(Q)-1
    for i in range(p-1):
        U[n+i+2]=U[n+i+1]+U[p+i+1]-U[p+i]
        for j in range(i,-1,-1):
            alpha=(U[n+1]-U[n-j])/(U[n-j+i+2]-U[n-j]);assert 0<alpha<=1
            Q[n-j]=tuple((a-(1-alpha)*b)/alpha for a,b in zip(Q[n-j],Q[n-j-1]))
    U[n+p+1]=U[n+p]+U[2*p]-U[2*p-1]
    assert all(a<=b for a,b in zip(U,U[1:]));return tuple(U),tuple(Q)
