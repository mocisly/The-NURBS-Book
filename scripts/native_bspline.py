"""Native mathematical B-spline geometry, independent of raster coordinates."""
from fractions import Fraction as F
from math import comb
from bspline_math import piece,evaluate,derivative,compose_affine,basis

def number(x):
    x=F(x)
    return str(x.numerator) if x.denominator==1 else f'{float(x):.10f}'.rstrip('0').rstrip('.')

def point(p): return '('+','.join(map(number,p))+')'

def segments(knots,controls,p):
    knots=tuple(map(F,knots));controls=tuple(tuple(map(F,q)) for q in controls)
    assert len(knots)==len(controls)+p+1
    result=[]
    for s in range(p,len(controls)):
        a,b=knots[s:s+2]
        if a==b: continue
        weights=[piece(knots,i,p,s) for i in range(len(controls))]
        power=tuple(tuple(sum((w[k] if k<len(w) else 0)*controls[i][d] for i,w in enumerate(weights)) for k in range(p+1)) for d in range(len(controls[0])))
        local=[compose_affine(c,a,b-a) for c in power]
        bern=tuple(tuple(sum((local[d][k] if k<len(local[d]) else 0)*F(comb(j,k),comb(p,k)) for k in range(j+1)) for d in range(len(local))) for j in range(p+1))
        result.append(dict(span=s,a=a,b=b,power=power,bern=bern))
    return result

def de_boor(knots,controls,p,u):
    s=next((s for s in range(p,len(controls)) if knots[s]<=u<knots[s+1]),len(controls)-1)
    q=[tuple(map(F,v)) for v in controls[s-p:s+1]]
    for r in range(1,p+1):
        for j in range(p,r-1,-1):
            i=s-p+j;alpha=F(u-knots[i],knots[i+p-r+1]-knots[i])
            q[j]=tuple((1-alpha)*a+alpha*b for a,b in zip(q[j-1],q[j]))
    return q[p]

def check(knots,controls,p,segs,steps=41):
    count=0
    for seg in segs:
        a,b,s=seg['a'],seg['b'],seg['span']
        for k in range(steps):
            t=F(k,steps);u=a+(b-a)*t
            weights=[evaluate(piece(tuple(knots),i,p,s),u) for i in range(len(controls))]
            assert min(weights)>=0 and sum(weights)==1
            assert weights==[basis(tuple(knots),i,p,u) for i in range(len(controls))]
            q=list(seg['bern'])
            for r in range(p): q=[tuple((1-t)*x+t*y for x,y in zip(q[i],q[i+1])) for i in range(len(q)-1)]
            assert q[0]==tuple(evaluate(c,u) for c in seg['power'])==de_boor(knots,controls,p,u)
            count+=1
    for left,right in zip(segs,segs[1:]):
        u=left['b'];multiplicity=knots.count(u)
        for d in range(len(controls[0])):
            a,b=left['power'][d],right['power'][d]
            for order in range(p-multiplicity+1):
                assert evaluate(a,u)==evaluate(b,u)
                a,b=derivative(a),derivative(b)
    assert segs[0]['bern'][0]==controls[0] and segs[-1]['bern'][-1]==controls[-1]
    return count

def cubic_path(seg,style=''):
    b=list(seg['bern']);p=len(b)-1
    assert p in (1,2,3)
    while p<3:
        b=[b[0]]+[tuple(F(i,p+1)*x+(1-F(i,p+1))*y for x,y in zip(b[i-1],b[i])) for i in range(1,p+1)]+[b[-1]]
        p+=1
    return r'\draw'+('['+style+']' if style else '')+' '+point(b[0])+' .. controls '+point(b[1])+' and '+point(b[2])+' .. '+point(b[3])+';'
