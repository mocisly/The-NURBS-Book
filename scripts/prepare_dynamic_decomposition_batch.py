"""Final-book targets for5.22-5.24, including corrected explanation and algorithms."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];build=root/'image_tex/build'
names={'5.22':'dynamic-bezier-extraction','5.23':'quartic-alpha-intervals','5.24':'on-the-fly-quartic','5.25':'on-the-fly-surface'}
geometry={k:json.loads((build/(v+'-check.json')).read_text()) for k,v in names.items()}
(build/'chapter5-dynamic-decomposition-geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
batch={'id':'chapter5-dynamic-decomposition','figures':{'5.22':['ch05/fig_5_27.tex','ch05/fig_5_28.tex'],'5.23':['ch05/fig_5_29.tex'],'5.24':['ch05/fig_5_30.tex','ch05/fig_5_31.tex']},
       'text_regions':{'为第j个贝塞尔段的第k个控制点':[],'DecomposeCurve':[],'DecomposeSurface':[]},
       'next_figure':'5.26','geometry_report':'image_tex/build/chapter5-dynamic-decomposition-geometry.json',
       'geometry_note':'Exact cubic dynamic extraction work arrays, quartic alpha denominators and three quartic Bezier polygons verified by independent extraction and knot insertion. Degree4 native paths approximate analytic polynomial coefficients with certifiedL1 error<0.0001cm, never raster contours. Three adjacent4x3 surface nets match independently refined10x5 net exactly; exact projected tangent slope separation prevents folding. Restored A5.6/A5.7 continuity, kept A5.6 heading with inputs and corrected local transposed Q indices.'}
batch['figures']['5.25']=['ch05/fig_5_32.tex']
(build/'chapter5-dynamic-decomposition-batch.json').write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n')
print('Prepared dynamic decomposition final-book batch.')
