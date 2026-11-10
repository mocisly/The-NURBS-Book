"""Semantic local quadratic interpolation, Eq9.28..44; exact rational Bezier pieces.

Directions and intersections are exact. Irrational lengths use certified rational
enclosures of width <=1e-24, with unit-vector residuals explicitly checked.
"""
from fractions import Fraction as F
from math import isqrt
from native_bspline import segments,check

SCALE=10**24
def add(A,B,t=F(1)):return tuple(a+t*b for a,b in zip(A,B))
def mul(A,t):return tuple(t*a for a in A)
def cross(A,B):return A[0]*B[1]-A[1]*B[0]
def dot(A,B):return sum(a*b for a,b in zip(A,B))
def length(A):
    s=dot(A,A);assert s>0
    n,d=isqrt(s.numerator),isqrt(s.denominator)
    if n*n==s.numerator and d*d==s.denominator:return F(n,d)
    lo=F(isqrt(s.numerator*SCALE*SCALE//s.denominator),SCALE);hi=lo+F(1,SCALE)
    assert lo*lo<s<hi*hi
    return (lo+hi)/2
def unit(A):
    t=mul(A,1/length(A));assert abs(dot(t,t)-1)<F(1,10**21)
    return t
def tangents(Q,method='akima',corners=False,closed=False):
    n=len(Q)-1;q={i:add(Q[i],Q[i-1],-1) for i in range(1,n+1)}
    if method=='bessel':
        ell={i:length(q[i]) for i in range(1,n+1)}
        ds={i:mul(q[i],1/ell[i]) for i in q};D={}
        for k in range(1,n):
            alpha=ell[k]/(ell[k]+ell[k+1]);D[k]=add(mul(ds[k],1-alpha),ds[k+1],alpha)
        D[0]=add(mul(ds[1],2),D[1],-1);D[n]=add(mul(ds[n],2),D[n-1],-1)
    else:
        assert method=='akima'
        if closed:
            assert Q[0]==Q[-1]
            q[0]=q[n];q[-1]=q[n-1];q[n+1]=q[1];q[n+2]=q[2]
        else:
            q[0]=add(mul(q[1],2),q[2],-1);q[-1]=add(mul(q[0],2),q[1],-1)
            q[n+1]=add(mul(q[n],2),q[n-1],-1);q[n+2]=add(mul(q[n+1],2),q[n],-1)
        D={}
        for k in range(n+1):
            a=abs(cross(q[k-1],q[k]));b=abs(cross(q[k+1],q[k+2]))
            alpha=a/(a+b) if a+b else F(1) if corners else F(1,2)
            D[k]=add(mul(q[k],1-alpha),q[k+1],alpha)
            if dot(D[k],D[k])==0:D[k]=q[k+1] if k<n else q[k]
    return tuple(D[i] for i in range(n+1))

def interpolate(Q,method='akima',corners=False,closed=False):
    D=tangents(Q,method,corners,closed);T=tuple(unit(d) for d in D)
    if closed:assert D[0]==D[-1]
    flagged=set()
    if corners:
        assert method=='akima'
        n=len(Q)-1
        for k in (range(n) if closed else range(2,n-1)):
            def chord(i):
                return add(Q[(i-1)%n+1],Q[(i-1)%n],-1) if closed else add(Q[i],Q[i-1],-1)
            a,b,c,d=(chord(i) for i in (k-1,k,k+1,k+2))
            if cross(a,b)==cross(c,d)==0 and cross(b,c)!=0:flagged.add(k)
    result=[];proof=[]
    for k,(A,B) in enumerate(zip(Q,Q[1:])):
        da,db=D[k:k+2];delta=add(B,A,-1)
        # At a flagged corner the preceding collinear run ends with its own
        # incoming chord; the next run starts with the alpha=1 outgoing chord.
        if k in flagged:da=delta
        if k+1 in flagged or closed and k+1==len(Q)-1 and 0 in flagged:db=delta
        ta,tb=unit(da),unit(db);den=cross(da,db)
        if den:
            a=cross(delta,db)/den;b=cross(delta,da)/den
        else:a=b=F(0)
        if den and a>0 and b<0:
            R=add(A,da,a);assert R==add(B,db,b)
            triples=[(A,R,B)];kind='proper intersection'
        elif cross(da,delta)==cross(db,delta)==0:
            triples=[(A,mul(add(A,B),F(1,2)),B)];kind='collinear midpoint'
        else:
            chord=length(delta)
            if cross(da,db)==0:gs=ge=chord/2;kind='parallel two-piece'
            else:
                cs=abs(dot(ta,delta))/chord;ce=abs(dot(tb,delta))/chord
                alpha=F(2,3);gs=chord/(4*(alpha*ce+(1-alpha)*cs));ge=chord/(4*(alpha*cs+(1-alpha)*ce));kind='inflection two-piece'
            Rs=add(A,ta,gs);Re=add(B,tb,-ge);J=mul(add(mul(Re,gs),Rs,ge),1/(gs+ge))
            triples=[(A,Rs,J),(J,Re,B)]
            assert cross(add(J,Rs,-1),add(Re,J,-1))==0 and dot(add(J,Rs,-1),add(Re,J,-1))>0
        for tri in triples:
            K=(F(0),)*3+(F(1),)*3;ss=segments(K,tri,2);nc=check(K,tri,2,ss,steps=13)
            assert ss[0]['bern']==tri;result.append(ss[0])
        assert triples[0][0]==A and triples[-1][-1]==B
        proof.append(dict(interval=k,kind=kind,pieces=len(triples),native_checks=13*len(triples)))
    # Check every geometric join, including those at original data points.
    joins=[]
    pairs=list(zip(result,result[1:]))
    if closed:pairs.append((result[-1],result[0]))
    for a,b in pairs:
        assert a['bern'][-1]==b['bern'][0]
        va=add(a['bern'][-1],a['bern'][-2],-1);vb=add(b['bern'][1],b['bern'][0],-1)
        cr=cross(va,vb);dt=dot(va,vb)
        if not corners:assert cr==0 and dt>0
        joins.append(dict(G1=cr==0 and dt>0,cross=str(cr)))
    return result,dict(method=method,closed=closed,corner_flag=corners,flagged_corner_indices=sorted(flagged),data=[list(map(str,q)) for q in Q],directions=[list(map(str,d)) for d in D],unit_vector_residual_bound='1e-21',intervals=proof,joins=joins)
