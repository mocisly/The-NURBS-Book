"""Final-book review targets for5.29 and the restored elevation lead-in."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];build=root/'image_tex/build'
batch={'id':'chapter5-tolerance-curve','figures':{'5.29':['ch05/fig_5_39.tex','ch05/fig_5_40.tex','ch05/fig_5_41.tex']},
       'text_regions':{'重数必须增加为':[]},'next_figure':'5.30',
       'geometry_report':'image_tex/build/tolerance-knot-removal-check.json',
       'geometry_note':'One explicit representative cubic using the printed knots; all tolerance experiments start from this original. Exact inverse-insertion projection and common-basis partition certify whole-curve errors within0.007/0.025/0.07/0.6/1.2. Native exact cubic paths, actual removed nodes circled, counts11/10/8/7/6/5. Restored the elevation continuity explanation split by old figure fragments, with internal multiplicity increasing by1.'}
(build/'chapter5-tolerance-curve-batch.json').write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n')
print('Prepared5.29 final-book batch.')
