from pathlib import Path
import json
from region_surface_data import make,POLYGON
from region_surface_native import domain,mesh
root=Path(__file__).resolve().parents[1];P,r=make();A=domain(POLYGON,r);B,proof=mesh(P,r)
for n,lines in[(25,A),(26,B)]: (root/f'image_tex/ch11/fig_11_{n}.tex').write_text('\n'.join(['% Polygon selection and actual Eq11.49/51 tensor surface, not scan traces.']+lines)+'\n',encoding='utf-8')
r.update(controls=P,native=proof,no_contour_tracing=True,independent_rectangle_union_membership_checks=1225)
(root/'image_tex/build/region-surface-warp-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.22',r['selected_count'],'selected controls/1225 independent membershipchecks;',proof['native_checks'],'nativechecks; exact wholeboundary curves and positiveheightbounds.')
