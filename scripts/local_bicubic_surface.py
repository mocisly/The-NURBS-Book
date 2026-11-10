"""Local bicubic interpolation Eq9.57..59, with optional periodic data seams."""
from fractions import Fraction as F
from local_quadratic_interpolator import add,mul,dot,length,unit
from inverse_knot_projection import remove_to
from surface_geometry import surface,local_patch

def cross(A,B):return (A[1]*B[2]-A[2]*B[1],A[2]*B[0]-A[0]*B[2],A[0]*B[1]-A[1]*B[0])
def magnitude(A):return length(A) if any(A) else F(0)
def akima(data,closed=False):
    n=len(data)-1;q={i:add(data[i],data[i-1],-1) for i in range(1,n+1)};assert n>=3
    if closed:
        assert data[0]==data[-1];q[0]=q[n];q[-1]=q[n-1];q[n+1]=q[1];q[n+2]=q[2]
    else:
        q[0]=add(mul(q[1],2),q[2],-1);q[-1]=add(mul(q[0],2),q[1],-1)
        q[n+1]=add(mul(q[n],2),q[n-1],-1);q[n+2]=add(mul(q[n+1],2),q[n],-1)
    T=[]
    for k in range(n+1):
        a=magnitude(cross(q[k-1],q[k]));b=magnitude(cross(q[k+1],q[k+2]));alpha=a/(a+b) if a+b else F(1,2)
        v=add(mul(q[k],1-alpha),q[k+1],alpha)
        if not any(v):v=q[k+1] if k<n else q[k]
        T.append(unit(v))
    if closed:assert T[0]==T[-1]
    return tuple(T)
def direction_data(lines,closed):
    n=len(lines[0])-1;ell=tuple(tuple(length(add(b,a,-1)) for a,b in zip(line,line[1:])) for line in lines)
    totals=tuple(sum(row) for row in ell);increments=tuple(sum(row[k] for row in ell) for k in range(n))
    params=tuple(sum(increments[:i])/sum(increments) for i in range(n+1))
    D=tuple(tuple(mul(t,total) for t in akima(line,closed)) for line,total in zip(lines,totals))
    return params,totals,D
def blend_weights(params,closed):
    h=tuple(v-u for u,v in zip(params,params[1:]));inside=tuple(h[k-1]/(h[k-1]+h[k]) for k in range(1,len(h)))
    a=h[-1]/(h[-1]+h[0]) if closed else inside[0];b=a if closed else inside[-1]
    return (a,)+inside+(b,)
def field_derivative(values,params,closed):
    slopes=tuple(mul(add(b,a,-1),1/(v-u)) for a,b,u,v in zip(values,values[1:],params,params[1:]));a=blend_weights(params,closed);n=len(slopes)
    if closed:
        assert values[0]==values[-1]
        D=tuple(add(mul(slopes[(k-1)%n],1-a[k]),slopes[k],a[k]) for k in range(n));return D+(D[0],)
    inside=tuple(add(mul(slopes[k-1],1-a[k]),slopes[k],a[k]) for k in range(1,n))
    return (add(mul(slopes[0],2),inside[0],-1),)+inside+(add(mul(slopes[-1],2),inside[-1],-1),)

def construct(Q,closed_u=False,closed_v=False):
    n,m=len(Q)-1,len(Q[0])-1;assert n>=3 and m>=3 and all(len(row)==m+1 for row in Q)
    if closed_u:assert Q[0]==Q[-1]
    if closed_v:assert all(row[0]==row[-1] for row in Q)
    up,r,ducol=direction_data(tuple(zip(*Q)),closed_u);vp,s,dv=direction_data(Q,closed_v)
    du=tuple(tuple(ducol[j][i] for j in range(m+1)) for i in range(n+1));au,bv=blend_weights(up,closed_u),blend_weights(vp,closed_v)
    vu_col=tuple(field_derivative(tuple(dv[i][j] for i in range(n+1)),up,closed_u) for j in range(m+1))
    vu=tuple(tuple(vu_col[j][i] for j in range(m+1)) for i in range(n+1));uv=tuple(field_derivative(row,vp,closed_v) for row in du)
    mix=tuple(tuple(mul(add(mul(uv[i][j],au[i]),vu[i][j],bv[j]),1/(au[i]+bv[j])) for j in range(m+1)) for i in range(n+1))
    full=[[None]*(3*m+1) for _ in range(3*n+1)];patch=[]
    for k in range(n):
        row=[];hu=up[k+1]-up[k]
        for l in range(m):
            hv=vp[l+1]-vp[l];b=[]
            for i in range(4):
                ki=k+int(i>=2);cu=hu/3 if i==1 else -hu/3 if i==2 else F(0);rr=[]
                for j in range(4):
                    lj=l+int(j>=2);cv=hv/3 if j==1 else -hv/3 if j==2 else F(0)
                    pt=add(add(add(Q[ki][lj],du[ki][lj],cu),dv[ki][lj],cv),mix[ki][lj],cu*cv);rr.append(pt)
                    a,bidx=3*k+i,3*l+j;assert full[a][bidx] is None or full[a][bidx]==pt;full[a][bidx]=pt
                b.append(tuple(rr))
            row.append(tuple(b))
        patch.append(tuple(row))
    full=tuple(tuple(row) for row in full);patch=tuple(patch)
    uf=(F(0),)*4+tuple(t for u in up[1:-1] for t in (u,u,u))+(F(1),)*4
    vf=(F(0),)*4+tuple(t for v in vp[1:-1] for t in (v,v,v))+(F(1),)*4
    flat=tuple(tuple(x for pt in row for x in pt) for row in full);U,tmp,ru=remove_to(uf,flat,3,up[1:-1]);assert ru['curve_exactly_unchanged']
    unet=tuple(tuple(tuple(row[3*j+d] for d in range(3)) for j in range(3*m+1)) for row in tmp)
    nu=len(unet);flatv=tuple(tuple(x for i in range(nu) for x in unet[i][j]) for j in range(3*m+1))
    V,tmpv,rv=remove_to(vf,flatv,3,vp[1:-1]);assert rv['curve_exactly_unchanged']
    nv=len(tmpv);P=tuple(tuple(tuple(tmpv[j][3*i+d] for d in range(3)) for j in range(nv)) for i in range(nu));base=(U,V,3,3,P)
    assert all(surface(*base,u,v)==Q[i][j] for i,u in enumerate(up) for j,v in enumerate(vp))
    us=[i for i in range(3,nu) if U[i]<U[i+1]];vs=[i for i in range(3,nv) if V[i]<V[i+1]]
    for k,a in enumerate(us):
        for l,b in enumerate(vs):assert local_patch(U,V,3,3,P,a,b)[0]==patch[k][l]
    edge=0;seam=0
    for k in range(n if closed_u else n-1):
        right=(k+1)%n
        for l in range(m):
            for j in range(4):
                assert patch[k][l][3][j]==patch[right][l][0][j]
                a=mul(add(patch[k][l][3][j],patch[k][l][2][j],-1),3/(up[k+1]-up[k]))
                b=mul(add(patch[right][l][1][j],patch[right][l][0][j],-1),3/(up[right+1]-up[right]))
                assert a==b;edge+=1;seam+=int(right==0)
    for l in range(m if closed_v else m-1):
        right=(l+1)%m
        for k in range(n):
            for i in range(4):
                assert patch[k][l][i][3]==patch[k][right][i][0]
                a=mul(add(patch[k][l][i][3],patch[k][l][i][2],-1),3/(vp[l+1]-vp[l]))
                b=mul(add(patch[k][right][i][1],patch[k][right][i][0],-1),3/(vp[right+1]-vp[right]))
                assert a==b;edge+=1;seam+=int(right==0)
    report=dict(method='A9.5 chord parameters;3D Akima tangents;9.59 Bessel field mixed derivatives;9.57bicubic Hermite patches',closed_directions=[closed_u,closed_v],parameters=[list(map(str,up)),list(map(str,vp))],unit_vector_squared_residual_bound='1e-21',boundary_rule='cyclic Bessel fields on closed seams;Eq9.32 one-sided on open boundaries,nearest interior blend weights',all_data_interpolated_exact=True,whole_patch_coefficient_identities=n*m,whole_edge_C0_C1_coefficient_equalities=edge,closed_seam_coefficient_equalities=seam,mixed_derivatives_nonzero=any(any(v) for row in mix for v in row),composite_control_shape=[3*n+1,3*m+1],minimal_control_shape=[nu,nv],zero_error_u_knot_removal=ru,zero_error_v_knot_removal=rv)
    return base,(up,vp),full,patch,report
