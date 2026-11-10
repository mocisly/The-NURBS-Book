"""10.8same data/parameters as10.7, position-only cubic interpolation."""
from pathlib import Path
from fractions import Fraction as F
import json
from spine_skinning_surfaces import construct
from spine_skinning_native import panel
from spine_skinning_example_data import tangent,V_HAT
from bspline_math import piece,derivative,evaluate
from surface_geometry import weights
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in m['images'] if e['tex']=='image_tex/ch10/fig_10_11.tex')['applied']
base,VP,Q,r=construct(False);old=json.loads((root/'image_tex/build/spine-hermite-skin-data.json').read_text())
assert r['v_parameters']==old['v_parameters'] and r['u_knots']==old['u_knots']
U,V,p,q,net=base;sines=[];counterexamples=[]
for k,v in enumerate(VP):
    span=next((s for s in range(3,5) if V[s]<=v<V[s+1]),4);wd=tuple(evaluate(derivative(piece(V,j,3,span)),v) for j in range(5));D=tangent(V_HAT[k])
    for u in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
        wu=weights(U,3,u);dv=tuple(sum(wu[i]*wd[j]*net[i][j][d] for i in range(7) for j in range(5)) for d in range(3))
        cross=(dv[1]*D[2]-dv[2]*D[1],dv[2]*D[0]-dv[0]*D[2],dv[0]*D[1]-dv[1]*D[0]);n=sum(x*x for x in cross)
        if n:counterexamples.append(dict(section=k,u=str(u),cross_product_squared=str(n)))
        sines.append(n/(sum(x*x for x in dv)*sum(x*x for x in D)))
assert counterexamples
out=['% Same five whole section curves/parameters as10.7; no derivative constraints. Exact7x5 tensor skin.',r'\begin{tikzpicture}[book line]'];proof=[]
for letter,shift in [('a',0),('b',16.5)]:
    lines,pr=panel(base,VP,Q,letter,shift,False,top=F(13,2));out+=lines;proof.append(pr)
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_11.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(figure='10.8',same_sections_and_v_parameters_as_10_7=True,native_panels=proof,nonparallel_derivative_exact_counterexamples=counterexamples,maximum_sampled_derivative_sine_squared=str(max(sines)),extra_top_margin_only_for_actual_control_overshoot=True,no_contour_tracing=True)
(root/'image_tex/build/spine-interpolated-skin-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.8:35exact vector constraints/same10.7 data+parameters;',len(counterexamples),'exact nonparallel derivative counterexamples;',sum(p['native_curve_checks'] for p in proof),'native checks.')
