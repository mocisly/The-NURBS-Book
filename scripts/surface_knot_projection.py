"""Directional exact-rational inverse-insertion approximations for tensor nets."""
from inverse_knot_projection import remove_to
from knot59_data import insert_surface

def remove_surface_to(net,axis,removed):
    U,V,p,q,P=net;reports=[]
    if axis=='u':
        columns=[]
        for j in range(len(P[0])):
            K,R,proof=remove_to(U,tuple(row[j] for row in P),p,removed);columns.append(R);reports.append(proof)
        Q=tuple(tuple(col[i] for col in columns) for i in range(len(columns[0])))
        return (K,V,p,q,Q),reports
    rows=[]
    for row in P:
        K,R,proof=remove_to(V,row,q,removed);rows.append(R);reports.append(proof)
    return (U,K,p,q,tuple(rows)),reports

def common_basis_error(original,approximation,u_removed=(),v_removed=()):
    refined=approximation
    for t in sorted(u_removed):refined=insert_surface(*refined,'u',t)
    for t in sorted(v_removed):refined=insert_surface(*refined,'v',t)
    assert refined[:4]==original[:4]
    E=tuple(tuple(tuple(a-b for a,b in zip(x,y)) for x,y in zip(A,B)) for A,B in zip(original[-1],refined[-1]))
    bound=max(sum(map(abs,pt)) for row in E for pt in row)
    return original[:4]+(E,),bound
