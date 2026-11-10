"""10.3actual five prescribed degrees/knots,exact compatibility andskinning."""
from fractions import Fraction as F
from collections import Counter
from degree_elevation_geometry import elevate_spline
from knot51_data import insert
from native_bspline import segments,de_boor
from bounded_curve_approximation import chord_parameters
from global_interpolation_data import interpolate
from surface_geometry import weights,verify_tensor
X=tuple(map(F,[4,2,0,-2,-4]))
DEGREES=(1,2,1,2,3)
KNOTS=tuple(tuple(map(F,row)) for row in [
 [0,0,1,1],
 [0,0,0,'3/10','1/2','7/10',1,1,1],
 [0,0,'1/5','2/5','3/5','4/5',1,1],
 [0,0,0,'3/10','1/2','7/10',1,1,1],
 [0,0,0,0,'3/10','7/10',1,1,1,1]])
Z=tuple(tuple(map(F,row)) for row in [
 [0,0],
 [0,'.3','.8','.8','.3',0],
 [0,'.4',1,1,'.4',0],
 [0,'.2','.7','.9','.4',0],
 [0,0,'-.2','.2',0,0]])
ORIGINAL=[]
for k,(K,p,z) in enumerate(zip(KNOTS,DEGREES,Z)):
    greville=tuple(sum(K[i+1:i+p+1])/p for i in range(len(K)-p-1));assert len(z)==len(greville)
    P=tuple((X[k],-3+6*t,h) for t,h in zip(greville,z));ORIGINAL.append((K,p,P))
ORIGINAL=tuple(ORIGINAL)

def construct():
    elevated=[];proof=[]
    for K,p,P in ORIGINAL:
        if p<3:L,C,r=elevate_spline(K,P,p,3-p)
        else:L,C,r=K,P,dict(all_global_power_coefficients_identical=True,increment=0)
        elevated.append((L,C));proof.append(r)
    multiplicities={t:max(K.count(t) for K,C in elevated) for t in set(t for K,C in elevated for t in K)}
    U=tuple(t for t,m in sorted(multiplicities.items()) for _ in range(m));assert len(U)-4==22
    expected=(F(0),)*4+tuple(t for t,m in [(F(1,5),3),(F(3,10),2),(F(2,5),3),(F(1,2),2),(F(3,5),3),(F(7,10),2),(F(4,5),3)] for _ in range(m))+(F(1),)*4;assert U==expected
    compatible=[];identities=0;insertions=[]
    for (oldK,p,oldP),(K,P) in zip(ORIGINAL,elevated):
        count=0
        for t,m in sorted(multiplicities.items()):
            for _ in range(m-K.count(t)):K,P,_=insert(K,P,3,t);count+=1
        assert K==U and len(P)==22
        coarse=segments(oldK,oldP,p);fine=segments(U,P,3)
        for segment in fine:
            old=next(s for s in coarse if s['a']<=segment['a'] and segment['b']<=s['b'])
            for a,b in zip(old['power'],segment['power']):
                assert tuple(a)+(F(0),)*(4-len(a))==b;identities+=4
        assert all(s['power'][0]==(oldP[0][0],F(0),F(0),F(0)) and s['power'][1]==(-F(3),F(6),F(0),F(0)) for s in fine)
        compatible.append(P);insertions.append(count)
    # Eq10.8:average normalized control-column chord parameters.
    results=[chord_parameters(tuple(compatible[k][i] for k in range(5))) for i in range(22)]
    VP=tuple(sum(r[0][k] for r in results)/22 for k in range(5));assert VP[0]==0 and VP[-1]==1 and all(a<b for a,b in zip(VP,VP[1:]))
    net=[]
    for i in range(22):
        V,C=interpolate(tuple(compatible[k][i] for k in range(5)),VP,3);net.append(C)
    net=tuple(net);base=(U,V,3,3,net)
    for k,v in enumerate(VP):
        W=weights(V,3,v)
        assert all(tuple(sum(W[j]*net[i][j][d] for j in range(5)) for d in range(3))==compatible[k][i] for i in range(22))
    # The chosen GrevilleYcoordinates makeY=-3+6u for ALL sections/surface.
    assert all(net[i][j][0]==net[0][j][0] and net[i][j][1]==compatible[0][i][1] for i in range(22) for j in range(5))
    dx=tuple(3*(net[0][j+1][0]-net[0][j][0])/(V[j+4]-V[j+1]) for j in range(4));assert max(dx)<0
    report=dict(figure='10.3',representative_control_heights=True,original_degrees=list(DEGREES),original_knots=[list(map(str,K)) for K in KNOTS],original_controls=[[[str(x) for x in q] for q in P] for K,p,P in ORIGINAL],degree_elevation_proofs=proof,elevated_control_counts=[len(C) for K,C in elevated],inserted_knots_per_curve=insertions,common_cubic_knots=list(map(str,U)),all_compatible_control_counts=[22]*5,whole_curve_power_coefficient_identity_count=identities,compatible_controls=[[[str(x) for x in q] for q in P] for P in compatible],v_parameters=list(map(str,VP)),Eq10_8_parameter_error_bound=max(r[1] for r in results),v_degree=3,v_knots=list(map(str,V)),surface_control_shape=[22,5],surface_controls=[[[str(x) for x in q] for q in row] for row in net],all110section_control_interpolation_identities_exact=True,all_five_complete_section_curves_interpolated=True,tensor_checks=verify_tensor(*base,steps=3),all_sections_Y_exactly_minus3plus6u=True,X_v_derivative_controls=list(map(str,dx)),whole_surface_XY_Jacobian_positive_lower_bound=str(-6*max(dx)),no_XY_folding=True)
    return ORIGINAL,tuple(compatible),VP,base,report
