"""Final-book evidence targets for the common surface and four tolerance examples."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];build=root/'image_tex/build'
geometry={'5.30':json.loads((build/'tolerance-surface-base-check.json').read_text())}
figures={'5.30':['ch05/fig_5_42.tex']}
for i in range(531,535):
    figure='5.'+str(i-500);geometry[figure]=json.loads((build/f'surface-tolerance-{i}-check.json').read_text())
    figures[figure]=[f'ch05/fig_5_{43+i-531}.tex']
(build/'chapter5-surface-tolerances-geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
batch={'id':'chapter5-surface-tolerances','figures':figures,'next_figure':'5.35',
       'geometry_report':'image_tex/build/chapter5-surface-tolerances-geometry.json',
       'geometry_note':'One explicit9x8 unit-weight p3q2 surface using the printed knots. Independent global tolerance experiments0.05/0.1/0.3/0.5 yield8x7/6x7/6x4/5x4 nets. Rational common-basis partition bounds the whole-surface errors, and tangent slope separation certifies projections without folds. Exact native sparse curves share fixed parameters and camera in every view. All five figures grouped by the node-removal explanation; obsolete196/198OCR headers and split caption fragments removed.'}
(build/'chapter5-surface-tolerances-batch.json').write_text(json.dumps(batch,indent=2)+'\n')
print('Prepared5.30-5.34 final-book batch.')
