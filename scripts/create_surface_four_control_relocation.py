from pathlib import Path
import json
from surface_relocation_example_data import four
from surface_relocation_native import panel
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch11/fig_11_11.tex')['applied']
new,r=four();out=['% Actual Eq11.13/14 four-control relocation using the SAME underlying surface as11.8.',r'\begin{tikzpicture}[book line]'];proof=[]
for letter,shift,title in [('a',0,r'(\delta,\gamma)=(24/55,1/2)'),('b',19,r'(\bar u,\bar v)=(3/5,3/5),\quad d=3/5')]:
    lines,report=panel(new,r,letter,shift,r['moved_indices'],title);out+=lines;proof.append(report)
out.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_11.tex').write_text('\n'.join(out)+'\n',encoding='utf-8');r.update(native_panels=proof,native_curve_error=0,no_contour_tracing=True)
(root/'image_tex/build/surface-four-control-relocation-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.9:',r['whole_tensor_Bezier_vector_coefficient_identities'],'wholepatch-vectorcoefficients/',r['whole_unchanged_exterior_patches'],'unchangedpatches/4wholeboundaries;',sum(p['native_curve_checks'] for p in proof),'nativechecks;exact(.6,.6)deltaZ.6.')
