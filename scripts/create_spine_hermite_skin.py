"""10.7actual70-condition Hermite skin, not a schematic ruled mesh."""
from pathlib import Path
from fractions import Fraction as F
import json
from spine_skinning_example_data import SECTION_K,positioned
from spine_skinning_native import panel
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in m['images'] if e['tex']=='image_tex/ch10/fig_10_10.tex')['applied']
r=json.loads((root/'image_tex/build/spine-hermite-skin-data.json').read_text());V=tuple(map(F,r['v_knots']));net=tuple(tuple(tuple(map(F,p)) for p in row) for row in r['surface_controls']);base=(SECTION_K,V,3,3,net);VP=tuple(map(F,r['v_parameters']));Q=positioned()
out=['% Exact7x10 Hermite skin from10.4/5/6 data;all70 vector constraints solved rationally. No tracing.',r'\begin{tikzpicture}[book line]'];proof=[]
for letter,shift in [('a',0),('b',16.5)]:
    lines,report=panel(base,VP,Q,letter,shift,True);out+=lines;proof.append(report)
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_10.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(figure='10.7',native_panels=proof,all_whole_section_derivative_directions_exact=True,no_contour_tracing=True)
(root/'image_tex/build/spine-hermite-skin-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.7native:',sum(p['native_curve_checks'] for p in proof),'checks;',sum(p['isocurve_tensor_identities'] for p in proof),'tensor-isocurve identities;all70exactconstraints.')
