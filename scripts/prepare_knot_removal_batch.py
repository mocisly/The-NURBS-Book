"""Collect checked5.26-5.28 sources for final book publication."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];build=root/'image_tex/build'
names={'5.26':'triple-knot-removal','5.27':'curve-knot-removal-examples','5.28':'surface-knot-removal-examples'}
geometry={k:json.loads((build/(v+'-check.json')).read_text()) for k,v in names.items()}
(build/'chapter5-knot-removal-geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
batch={'id':'chapter5-knot-removal','figures':{'5.26':['ch05/fig_5_33.tex'],'5.27':['ch05/fig_5_34.tex','ch05/fig_5_35.tex','ch05/fig_5_36.tex'],'5.28':['ch05/fig_5_37.tex','ch05/fig_5_38.tex']},
       'next_figure':'5.29','geometry_report':'image_tex/build/chapter5-knot-removal-geometry.json',
       'geometry_note':'Exact three-stage cubic knot removal independently verified by equations5.25-5.27 and inverse insertion. Representative approximate curve/surface removals solve rational local inverse-insertion equations with unaffected controls fixed; whole-domain errors certified by common-basis partition. Ten controls and original ticks confirm triple1/2 in5.27; corrected caption OCR and table5.2 reference. All views use common camera/scale and remain beside knot-removal explanations.'}
(build/'chapter5-knot-removal-batch.json').write_text(json.dumps(batch,indent=2)+'\n')
print('Prepared5.26-5.28 final-book batch.')
