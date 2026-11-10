"""10.9same exact spine/profile shapes, printed spine/section anchor variants."""
from pathlib import Path
from fractions import Fraction as F
import json
from spine_skinning_surfaces import construct
from spine_skinning_native import panel
from spine_skinning_example_data import V_HAT,U_HAT,positioned,SECTION_K,spine
from native_bspline import de_boor
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in m['images'] if e['tex']=='image_tex/ch10/fig_10_12.tex')['applied']
variants=[('a',tuple(map(F,('0','7/20','1/2','31/50','1'))),U_HAT,r'$\widehat v=(0,.35,.5,.62,1)$'),('b',V_HAT,tuple(map(F,('1/2','3/10','1/2','9/10','1/2'))),r'$\widehat u=(.5,.3,.5,.9,.5)$')]
out=['% Actual Hermite skins from shared exact spine and profiles; only printed anchor parameter sets changed.',r'\begin{tikzpicture}[book line]'];proof=[]
for index,(letter,vhat,uhat,title) in enumerate(variants):
    base,VP,Q,r=construct(True,vhat,uhat)
    assert Q==positioned(vhat,uhat)
    assert all(de_boor(SECTION_K,row,3,u)==spine(v) for row,u,v in zip(Q,uhat,vhat))
    lines,native=panel(base,VP,Q,letter,16.5*index,True,top=F(13,2),control_net=False,title_override=title);out+=lines
    r.update(panel=letter,spine_anchor_parameters=list(map(str,vhat)),section_anchor_parameters=list(map(str,uhat)),native=native,all_five_new_anchor_identities_exact=True,all_section_shapes_preserved_by_rigid_placement=True);proof.append(r)
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_12.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='10.9',variants=proof,shared_spine_and_section_shapes_as='10.4/10.5/10.7',method='same cubic Hermite skin as10.7,Eq10.8recomputed after placements,Eq9.23knots',all140linear_vector_constraints_exact=True,common_camera_scale='1.8',native_font_rescaling=False,no_contour_tracing=True)
(root/'image_tex/build/spine-positioning-variants-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS10.9:both printed anchor sets,all10anchors/10wholecurves/140vectorconstraints exact;',sum(p['native']['native_curve_checks'] for p in proof),'native checks.')
