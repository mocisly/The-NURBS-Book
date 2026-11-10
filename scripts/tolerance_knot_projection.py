"""Greedy removal with a whole-curve error budget measured against the original."""
from fractions import Fraction as F
from inverse_knot_projection import remove_to

def experiment(U,P,p,tolerances):
    original_internal=tuple(sorted(set(U[p+1:len(P)])))
    cache={};results=[]
    def candidate(removed):
        key=tuple(sorted(removed))
        if key not in cache:cache[key]=remove_to(U,P,p,key)
        return cache[key]
    for tolerance in tolerances:
        removed=[];remaining=list(original_internal);history=[]
        while remaining:
            choices=[]
            for t in remaining:
                K,Q,proof=candidate(removed+[t]);bound=F(proof['certified_whole_domain_L1_error_bound_cm'])
                choices.append((bound,t,K,Q,proof))
            best=min(choices,key=lambda c:(c[0],c[1]))
            if best[0]>tolerance:break
            bound,t,K,Q,proof=best;removed.append(t);remaining.remove(t)
            history.append({'removed':str(t),'whole_original_curve_error_bound':str(bound)})
        if removed:K,Q,proof=candidate(removed)
        else:K,Q,proof=U,P,{'certified_whole_domain_L1_error_bound_cm':'0'}
        assert F(proof['certified_whole_domain_L1_error_bound_cm'])<=tolerance
        results.append((K,Q,dict(proof,tolerance=str(tolerance),removal_history=history,
                                 greedy_termination_no_further_single_removal_within_budget=True)))
    return results
