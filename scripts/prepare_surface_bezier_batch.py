"""Collect exact checks and final-book review targets for5.20/5.21."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];build=root/'image_tex/build'
geometry={mode:json.loads((build/f'surface-bezier-{mode}-check.json').read_text()) for mode in ('base','patch-net','patch-surface')}
(build/'chapter5-bezier-surfaces-geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
batch={'id':'chapter5-bezier-surfaces','figures':{'5.20':['ch05/fig_5_24.tex'],'5.21':['ch05/fig_5_25.tex','ch05/fig_5_26.tex']},
       'next_figure':'5.22','geometry_report':'image_tex/build/chapter5-bezier-surfaces-geometry.json',
       'geometry_note':'Same representative5x4 p3q2 tensor surface using the printed knots. Exact directional polynomial restrictions,7x5 refined net and four4x3 extracted Bezier nets agree. Only display translations open the seams; surface parameterization retained. Both figures placed together after surface decomposition explanation.'}
(build/'chapter5-bezier-surfaces-batch.json').write_text(json.dumps(batch,indent=2)+'\n')
print('Prepared5.20/5.21 final-book batch.')
