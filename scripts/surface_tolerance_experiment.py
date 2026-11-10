"""Whole-surface tolerance budgets for the common translation surface in5.30."""
from fractions import Fraction as F
from inverse_knot_projection import remove_to
from knot530_data import U,V,R,S,tensor,projection_slopes

def experiments(tolerances):
    cache={};results=[]
    def curve(axis,removed):
        key=(axis,tuple(sorted(removed)))
        if key not in cache:
            K,P,p=(U,R,3) if axis=='u' else (V,S,2)
            cache[key]=remove_to(K,P,p,key[1]) if removed else (K,P,{'certified_whole_domain_L1_error_bound_cm':'0'})
        return cache[key]
    for eps in tolerances:
        removed={'u':[],'v':[]};remaining={'u':list(sorted(set(U[4:len(R)]))),'v':list(sorted(set(V[3:len(S)])))};history=[]
        while remaining['u'] or remaining['v']:
            candidates=[]
            for axis in ('u','v'):
                for knot in remaining[axis]:
                    trial={a:removed[a]+([knot] if a==axis else []) for a in ('u','v')}
                    u=curve('u',trial['u']);v=curve('v',trial['v'])
                    bound=sum(F(c[2]['certified_whole_domain_L1_error_bound_cm']) for c in (u,v))
                    candidates.append((bound,axis,knot,u,v))
            best=min(candidates,key=lambda t:(t[0],t[1],t[2]))
            if best[0]>eps:break
            bound,axis,knot,u,v=best;removed[axis].append(knot);remaining[axis].remove(knot)
            history.append({'direction':axis,'knot':str(knot),'whole_original_surface_error_bound':str(bound)})
        A,Q,uq=curve('u',removed['u']);B,T,vq=curve('v',removed['v']);projection=projection_slopes(Q,T)
        bound=F(uq['certified_whole_domain_L1_error_bound_cm'])+F(vq['certified_whole_domain_L1_error_bound_cm']);assert bound<=eps
        net=(A,B,3,2,tensor(Q,T))
        results.append((net,{'tolerance':str(eps),'u_removed':list(map(str,removed['u'])),'v_removed':list(map(str,removed['v'])),
                            'removal_history':history,'u_projection_proof':uq,'v_projection_proof':vq,
                            'certified_whole_original_surface_L1_bound_cm':str(bound),
                            'projection_orientation':projection,
                            'greedy_termination_no_further_single_removal_within_budget':True}))
    return results

def prepared_examples():
    """Cache mathematically verified nets, invalidating on every input-source change."""
    from pathlib import Path
    import json,hashlib
    from knot530_data import BASE
    from surface_knot_projection import common_basis_error
    from surface_geometry import surface,verify_tensor
    root=Path(__file__).resolve().parents[1]
    files=('knot530_data.py','inverse_knot_projection.py','surface_knot_projection.py','surface_tolerance_experiment.py')
    signatures={f:hashlib.sha256((root/'scripts'/f).read_bytes()).hexdigest() for f in files}
    target=root/'image_tex/build/surface-tolerance-experiments-check.json'
    if target.exists():
        data=json.loads(target.read_text())
        if data.get('source_files_sha256')==signatures:
            return [((tuple(map(F,r['U'])),tuple(map(F,r['V'])),3,2,
                      tuple(tuple(tuple(map(F,pt)) for pt in row) for row in r['controls'])),r['proof']) for r in data['experiments']]
    results=experiments(tuple(F(t) for t in ('.05','.1','.3','.5')));records=[]
    for net,proof in results:
        A,B,p,q,Q=net
        count=verify_tensor(*net,steps=10)
        E,bound=common_basis_error(BASE,net,tuple(map(F,proof['u_removed'])),tuple(map(F,proof['v_removed'])))
        budget=F(proof['certified_whole_original_surface_L1_bound_cm']);assert bound<=budget<=F(proof['tolerance'])
        maximum=F(0)
        for i in range(11):
            for j in range(11):
                u,v=F(i,10),F(j,10);old=surface(*BASE,u,v);new=surface(*net,u,v)
                delta=tuple(a-b for a,b in zip(old,new));assert delta==surface(*E,u,v)
                error=sum(map(abs,delta));assert error<=bound;maximum=max(maximum,error)
        proof.update(exact_tensor_vs_nested_deboor_points=count,exact_common_basis_surface_error_identities=121,
                     certified_common_tensor_basis_L1_bound_cm=str(bound),sampled_max_L1_error_cm=str(maximum))
        records.append({'U':list(map(str,A)),'V':list(map(str,B)),
                        'controls':[[list(map(str,pt)) for pt in row] for row in Q],'proof':proof})
    target.write_text(json.dumps({'source_files_sha256':signatures,'same_base_as530':True,
                                 'experiments':records},indent=2)+'\n')
    return results

if __name__=='__main__':
    for net,proof in prepared_examples():
        print('PASS epsilon='+proof['tolerance']+',net='+str((len(net[-1]),len(net[-1][0])))+
              ',whole original surface bound='+str(float(F(proof['certified_common_tensor_basis_L1_bound_cm']))))
