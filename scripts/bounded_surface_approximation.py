"""Exact tensor type2 bounded removal/refit,starting at degree(2,2).

Documented conservative variant of the surface extension of A9.10: same fixed
certified common mesh chord parameters; datum error accumulated with exact L1
triangle bounds,then reset to exact measured L1after accepted least-squares fit.
"""
from fractions import Fraction as F
from functools import lru_cache
from bounded_curve_approximation import chord_parameters,fit
from global_interpolation_data import interpolate
from surface_geometry import weights,verify_tensor
from surface_knot_projection import remove_surface_to,common_basis_error
from degree_elevation_geometry import elevate_spline
from bounded_surface_example_data import Q

def mesh_parameters():
    params=[];bounds=[]
    for lines in (tuple(zip(*Q)),Q):
        results=[chord_parameters(row) for row in lines];m=len(lines[0]);values=tuple(sum(r[0][i] for r in results)/len(lines) for i in range(m))
        assert values[0]==0 and values[-1]==1 and all(a<b for a,b in zip(values,values[1:]))
        params.append(values);bounds.append(max(r[1] for r in results))
    return tuple(params),bounds
(UP,VP),PARAM_ERROR=mesh_parameters()

@lru_cache(None)
def W(K,p,params):return tuple(tuple(weights(K,p,t)) for t in params)

def grid(net):
    U,V,p,q,P=net;A=W(U,p,UP);B=W(V,q,VP);nu=len(P);nv=len(P[0]);dim=len(P[0][0])
    # Sparse tensor contractions,including exact zeros in local error nets.
    first=tuple(tuple(tuple(sum(a[i]*P[i][j][d] for i in range(nu) if a[i] and P[i][j][d]) for d in range(dim)) for j in range(nv)) for a in A)
    return tuple(tuple(tuple(sum(b[j]*row[j][d] for j in range(nv) if b[j] and row[j][d]) for d in range(dim)) for b in B) for row in first)

def actual_errors(net):
    return tuple(tuple(sum(abs(x-y) for x,y in zip(a,b)) for a,b in zip(row,data)) for row,data in zip(grid(net),Q))

def maximum(errors):return max(map(max,errors))

def initial_interpolant():
    cols=[]
    for j in range(len(Q[0])):
        U,C=interpolate(tuple(row[j] for row in Q),UP,2);cols.append(C)
    temp=tuple(tuple(cols[j][i] for j in range(len(cols))) for i in range(len(cols[0])));P=[]
    for row in temp:
        V,C=interpolate(row,VP,2);P.append(C)
    net=(U,V,2,2,tuple(P));assert maximum(actual_errors(net))==0
    return net

def reduce(net,E,errors):
    history=[]
    while True:
        U,V,p,q,P=net;choices=[]
        for axis,K,deg in [('u',U,p),('v',V,q)]:
            for t in sorted(set(K[deg+1:-deg-1])):
                candidate,_=remove_surface_to(net,axis,(t,))
                difference,_=common_basis_error(net,candidate,(t,) if axis=='u' else (), (t,) if axis=='v' else ())
                changes=tuple(tuple(sum(map(abs,a)) for a in row) for row in grid(difference))
                budget=tuple(tuple(a+b for a,b in zip(row,delta)) for row,delta in zip(errors,changes))
                if maximum(budget)<=E:choices.append((maximum(changes),axis,t,candidate,budget))
        if not choices:break
        _,axis,t,net,errors=min(choices,key=lambda x:(x[0],x[1],x[2]))
        measured=actual_errors(net);assert all(a<=b<=E for row,bound in zip(measured,errors) for a,b in zip(row,bound))
        history.append(dict(axis=axis,knot=str(t),control_shape=[len(net[-1]),len(net[-1][0])],maximum_accumulated_L1_bound=float(maximum(errors))))
    return net,errors,history

def refit(net):
    U,V,p,q,P=net;nu=len(P);nv=len(P[0]);dim=len(P[0][0]);B=W(V,q,VP)
    baseline=tuple(tuple(tuple(sum(b[j]*P[i][j][d] for j in range(nv)) for d in range(dim)) for b in B) for i in range(nu))
    cols=[]
    for j in range(len(VP)):
        cols.append(fit(tuple(row[j] for row in Q),UP,U,p,tuple(row[j] for row in baseline)))
    temp=tuple(tuple(cols[j][i] for j in range(len(VP))) for i in range(nu))
    result=tuple(fit(row,VP,V,q,P[i]) for i,row in enumerate(temp))
    return (U,V,p,q,result)

def elevate(net):
    U,V,p,q,P=net;cols=[];proof=[]
    for j in range(len(P[0])):
        K,C,r=elevate_spline(U,tuple(row[j] for row in P),p,1);cols.append(C);proof.append(r)
    temp=tuple(tuple(cols[j][i] for j in range(len(cols))) for i in range(len(cols[0])));result=[]
    for row in temp:
        L,C,r=elevate_spline(V,row,q,1);result.append(C);proof.append(r)
    out=(K,L,p+1,q+1,tuple(result));assert grid(net)==grid(out)
    return out,dict(all_curve_power_coefficient_identities=True,directional_curves=len(proof))

def final_refit_removals(net,E):
    """After conservative budget exhaustion,try refit and verify actual errors."""
    history=[]
    while True:
        U,V,p,q,P=net;choices=[]
        for axis,K,deg in [('u',U,p),('v',V,q)]:
            for t in sorted(set(K[deg+1:-deg-1])):
                candidate,_=remove_surface_to(net,axis,(t,));candidate=refit(candidate);errors=actual_errors(candidate)
                if maximum(errors)<=E:choices.append((maximum(errors),axis,t,candidate))
        if not choices:break
        err,axis,t,net=min(choices,key=lambda x:(x[0],x[1],x[2]))
        history.append(dict(axis=axis,knot=str(t),exact_normal_equations=True,maximum_actual_L1_error=float(err),control_shape=[len(net[-1]),len(net[-1][0])]))
    return net,history

def approximate(base,E,degree=2):
    net=base;errors=actual_errors(net);stages=[]
    for deg in range(2,degree+1):
        net,errors,history=reduce(net,E,errors)
        print('degree',deg,'E',E,'shape',len(net[-1]),len(net[-1][0]),'removals',len(history),'bound',float(maximum(errors)),flush=True)
        candidate=refit(net);candidate_errors=actual_errors(candidate);accepted=maximum(candidate_errors)<=E
        if accepted:net,errors=candidate,candidate_errors
        net,errors,extra=reduce(net,E,errors)
        stages.append(dict(degree=deg,removals=history,refit_exact_normal_equations=True,refit_accepted=accepted,extra_removals=extra,maximum_L1_bound=float(maximum(errors))))
        if deg<degree:net,proof=elevate(net);stages[-1]['exact_elevation']=proof
    net,final=final_refit_removals(net,E)
    measured=actual_errors(net)
    if final:errors=measured
    assert maximum(measured)<=maximum(errors)<=E
    return net,dict(tolerance=str(E),degrees=list(net[2:4]),control_shape=[len(net[-1]),len(net[-1][0])],stages=stages,final_refit_removals=final,maximum_actual_L1_error=float(maximum(measured)),certified_accumulated_L1_bound=float(maximum(errors)),tensor_checks=verify_tensor(*net,steps=2))
