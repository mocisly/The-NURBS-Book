"""Explicit representative data for the tolerance experiment in Fig5.29.

Printed knots are exact. The source supplies no coordinates; a hooked cubic is
refined with small explicit local perturbations to provide multiple error scales.
No image coordinates are sampled or traced.
"""
from fractions import Fraction as F
from knot51_data import insert
from surface_geometry import weights

def example():
    U=(F(0),)*4+(F(31,100),)+(F(1),)*4
    P=tuple(tuple(F(str(t)) for t in pt) for pt in [(0,0),(3.5,0),(4.5,10.5),(13.5,1.1),(5,1.1)])
    changes=[('0.702','1.6','0'),('0.16','-0.2','0'),('0.5501','0.06','-0.04'),
             ('0.45','-0.015','0.01'),('0.901','0.015','0.015'),('0.8','0.001','-0.001')]
    operations=[]
    for knot,dx,dy in changes:
        t=F(knot);U,P,alphas=insert(U,P,3,t)
        if t==F('0.702'):
            # A local residual mode perpendicular to the two free insertion
            # columns makes this knot significant without changing endpoints
            # or the horizontal terminal tangent. Only x is perturbed.
            mode={2:-(1-alphas[3])/alphas[2],3:F(1),4:-alphas[3]/(1-alphas[4])}
            scale=max(map(abs,mode.values()));mode={i:c/scale for i,c in mode.items()}
            assert alphas[2]*mode[2]+(1-alphas[3])*mode[3]==0
            assert alphas[3]*mode[3]+(1-alphas[4])*mode[4]==0
            Q=list(P)
            for i,c in mode.items():Q[i]=(Q[i][0]+F(dx)*c,Q[i][1])
            P=tuple(Q);operations.append({'inserted':str(t),'local_x_residual_mode':{str(i):str(c) for i,c in mode.items()},'amplitude':dx})
            continue
        values=weights(U,3,t);i=max(range(1,len(P)-1),key=lambda j:values[j])
        delta=(F(dx),F(dy));Q=list(P);Q[i]=tuple(a+b for a,b in zip(Q[i],delta));P=tuple(Q)
        operations.append({'inserted':str(t),'perturbed_control_index':i,'displacement':list(map(str,delta))})
    assert U==(F(0),)*4+tuple(F(t) for t in ('0.16','0.31','0.45','0.5501','0.702','0.8','0.901'))+(F(1),)*4
    return U,P,operations

U,P,OPERATIONS=example()
