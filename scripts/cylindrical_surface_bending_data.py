"""Bicubic/quadratic plane, true local cylindrical radial maps and rigid ends."""
from fractions import Fraction as F
from circular_bending_data import U,IDS,sqrtq,dot,sub
from native_bspline import de_boor
from surface_geometry import surface
V=(F(0),)*3+tuple(F(i,4)for i in range(1,4))+(F(1),)*3
GU=tuple(sum(U[i+1:i+4])/3 for i in range(len(U)-4));GV=tuple(sum(V[j+1:j+3])/2 for j in range(len(V)-3))
PROFILE=tuple((8*u-4,F(0))for u in GU)
BASE=tuple(tuple((x,6*v-3,z)for v in GV)for x,z in PROFILE)
def make(lam,H=F(3),radius=F(2)):
    O=(F(0),H);Q=list(PROFILE);records=[]
    for i in IDS:
        d=sub(PROFILE[i],O);length=sqrtq(dot(d,d));s=radius/length;den=1+(lam-1)*s;assert den!=0;t=lam*s/den;R=tuple(o+s*x for o,x in zip(O,d));Q[i]=tuple(o+t*x for o,x in zip(O,d));err=abs(dot(sub(R,O),sub(R,O))-radius**2);assert err<F(1,10**13)
        assert t*(1-s)==lam*s*(1-t)
        if s==1:assert t==1 and Q[i]==PROFILE[i]
        elif lam>0:assert 0<t<1
        else:assert t>1
        records.append(dict(index=i,s=s,t=t,denominator=den,radius_residual=err,contact=s==1))
    rigid=[]
    for end,neighbor,indices in[(IDS[0],IDS[0]+1,range(IDS[0])),(IDS[-1],IDS[-1]-1,range(IDS[-1]+1,len(PROFILE)))]:
        a=sub(PROFILE[neighbor],PROFILE[end]);b=sub(Q[neighbor],Q[end]);den=sqrtq(dot(a,a)*dot(b,b));cs=dot(a,b)/den;sn=(a[0]*b[1]-a[1]*b[0])/den;assert abs(cs*cs+sn*sn-1)<F(1,10**12)
        for i in indices:
            x,z=sub(PROFILE[i],PROFILE[end]);Q[i]=(Q[end][0]+cs*x-sn*z,Q[end][1]+sn*x+cs*z)
            assert abs(dot(sub(Q[i],Q[end]),sub(Q[i],Q[end]))-dot(sub(PROFILE[i],PROFILE[end]),sub(PROFILE[i],PROFILE[end])))<F(1,10**10)
        rigid.append(dict(boundary=end,cos=cs,sin=sn,indices=list(indices)))
    Q=tuple(Q);P=tuple(tuple((x,6*v-3,z)for v in GV)for x,z in Q)
    for a in range(11):
        u=F(a,10);p=de_boor(U,Q,3,u)
        for v in(F(0),F(1,3),F(2,3),F(1)):assert surface(U,V,3,2,P,u,v)==(p[0],6*v-3,p[1])
    return (U,V,3,2,P),dict(lambda_value=lam,axis_height=H,radius=radius,profile=Q,records=records,rigid_transforms=rigid,exact_tensor_extrusion_checks=44,control_shape=(len(Q),len(GV)),original_surface_plane_z=0,original_cylinder_contact=H==radius)
