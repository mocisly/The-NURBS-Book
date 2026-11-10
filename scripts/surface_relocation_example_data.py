"""Representative wavy graph surface, exact point-constrained control relocation."""
from fractions import Fraction as F
from point_relocation_example_data import U as U
from surface_geometry import weights,surface,local_patch,extraction
V=(F(0),)*3+tuple(F(i,5) for i in range(1,5))+(F(1),)*3
GU=tuple(sum(U[i+1:i+4])/3 for i in range(9));GV=tuple(sum(V[j+1:j+3])/2 for j in range(7))
ZU=tuple(map(F,('0','.2','1.5','.8','.2','1.6','1.1','.2','0')))
ZV=tuple(map(F,('0','.1','1.1','-.2','.9','.2','0')))
P=tuple(tuple((8*u-4,7*v-F(7,2),ZU[i]+ZV[j]) for j,v in enumerate(GV)) for i,u in enumerate(GU))
BASE=(U,V,3,2,P)
def single():
    u=v=F(11,20);a,b=weights(U,3,u),weights(V,2,v);R=a[4]*b[3];assert R>0;d=F(3,5);alpha=d/R
    Q=tuple(tuple((x,y,z+alpha) if (i,j)==(4,3) else (x,y,z) for j,(x,y,z) in enumerate(row)) for i,row in enumerate(P));new=(U,V,3,2,Q)
    A=surface(*BASE,u,v);B=surface(*new,u,v);assert tuple(y-x for x,y in zip(A,B))==(0,0,d)
    # Every tensor Bezier coefficient on every knot rectangle, not just samples.
    NI=tuple((F(i==4),) for i in range(9));NJ=tuple((F(j==3),) for j in range(7))
    from native_bspline import segments
    su,sv=segments(U,NI,3),segments(V,NJ,2);checks=unchanged=0
    for s in su:
        for t in sv:
            Apatch=local_patch(*BASE,s['span'],t['span'])[0];Bpatch=local_patch(*new,s['span'],t['span'])[0]
            for i in range(4):
                for j in range(3):
                    assert tuple(y-x for x,y in zip(Apatch[i][j],Bpatch[i][j]))==(0,0,alpha*s['bern'][i][0]*t['bern'][j][0]);checks+=1
            if s['b']<=U[4] or s['a']>=U[8] or t['b']<=V[3] or t['a']>=V[6]:assert Apatch==Bpatch;unchanged+=1
    assert all(p[0]==8*GU[i]-4 and p[1]==7*GV[j]-F(7,2) for i,row in enumerate(Q) for j,p in enumerate(row))
    return new,dict(degrees=(3,2),control_shape=(9,7),u_knots=U,v_knots=V,controls=P,modified_controls=Q,moved_index=(4,3),selected_parameters=(u,v),basis_value_at_selected=R,alpha=alpha,delta_control=(0,0,alpha),selected_point=A,modified_selected_point=B,exact_target_displacement=(0,0,d),whole_tensor_Bezier_vector_coefficient_identities=checks,whole_unchanged_exterior_patches=unchanged,local_support=(U[4],U[8],V[3],V[6]),all_displacements_parallel_to_Z=True,whole_XY_Jacobian=56)
def view(p):
    x,y,z=p
    return F(3,2)*(-F(4,5)*x+F(3,5)*y),F(3,2)*(-F(9,25)*x-F(12,25)*y+F(4,5)*z)

def four():
    u=v=F(3,5);delta=(u-GU[4])/(GU[5]-GU[4]);gamma=(v-GV[3])/(GV[4]-GV[3]);assert delta==F(24,55) and gamma==F(1,2)
    indices=((4,3),(5,3),(4,4),(5,4));beta=((1-delta)*(1-gamma),delta*(1-gamma),(1-delta)*gamma,delta*gamma);assert sum(beta)==1
    a,b=weights(U,3,u),weights(V,2,v);value=sum(c*a[i]*b[j] for c,(i,j) in zip(beta,indices));d=F(3,5);alpha=d/value
    H={index:c*alpha for c,index in zip(beta,indices)}
    Q=tuple(tuple((x,y,z+H.get((i,j),0)) for j,(x,y,z) in enumerate(row)) for i,row in enumerate(P));new=(U,V,3,2,Q)
    A=surface(*BASE,u,v);B=surface(*new,u,v);assert tuple(y-x for x,y in zip(A,B))==(0,0,d)
    checks=unchanged=0
    for ui in range(3,9):
        if U[ui]==U[ui+1]:continue
        for vi in range(2,7):
            if V[vi]==V[vi+1]:continue
            E,FV=extraction(U,3,ui),extraction(V,2,vi)
            oldpatch=local_patch(*BASE,ui,vi)[0];newpatch=local_patch(*new,ui,vi)[0]
            for r in range(4):
                for s in range(3):
                    amount=alpha*sum(c*E[r][i]*FV[s][j] for c,(i,j) in zip(beta,indices))
                    assert tuple(y-x for x,y in zip(oldpatch[r][s],newpatch[r][s]))==(0,0,amount);checks+=1
            if U[ui+1]<=U[4] or V[vi+1]<=V[3]:assert oldpatch==newpatch;unchanged+=1
    assert Q[0]==P[0] and Q[-1]==P[-1] and all(a[0]==b[0] and a[-1]==b[-1] for a,b in zip(Q,P))
    return new,dict(degrees=(3,2),control_shape=(9,7),u_knots=U,v_knots=V,controls=P,modified_controls=Q,moved_indices=indices,delta=delta,gamma=gamma,beta=beta,alpha=alpha,selected_parameters=(u,v),basis_blend_at_selected=value,selected_point=A,modified_selected_point=B,exact_target_displacement=(0,0,d),whole_tensor_Bezier_vector_coefficient_identities=checks,whole_unchanged_exterior_patches=unchanged,all_four_entire_boundary_curves_unchanged=True,local_support=(U[4],U[9],V[3],V[7]),all_displacements_parallel_to_Z=True,whole_XY_Jacobian=56)
