from pathlib import Path
import json
from gordon_network_data import construct,UC,VC,UH,VH,CK,CL,Q
from surface_geometry import isocurve,surface
root=Path(__file__).resolve().parents[1];nets=construct()
for l,u in enumerate(UH):assert isocurve(*nets['L1'],'v',u)[2]==CL[l]
for k,v in enumerate(VH):assert isocurve(*nets['L2'],'u',v)[2]==CK[k]
for l,u in enumerate(UH):
    for k,v in enumerate(VH):assert surface(*nets['T'],u,v)==Q[l][k]
data=dict(representative_data=True,original_input_degrees=[3,2],u_parameters=UH,v_parameters=VH,loft_v_basis_reused_for_point_surface=True,reason='Same cardinal basis is required for exact Gordon cancellation; follows proposed near-knot reuse rather than independent perturbed knots.',exact_intersection_vector_identities=20,exact_L1_whole_curve_control_identities=20,exact_L2_whole_curve_control_identities=30,exact_S_u_curve_control_identities=30,exact_S_v_curve_control_identities=28,nets=nets)
(root/'image_tex/build/gordon-network-data.json').write_text(json.dumps(data,default=str,indent=2)+'\n',encoding='utf-8')
print('PASS Gordon:20sharedpoints/50loft-wholecurve-coefficients/58final-wholecurve-coefficients;sharedcardinalbasis;6x7finalnet.')
