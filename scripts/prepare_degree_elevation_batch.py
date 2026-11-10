"""Collect completed, independently checked5.35-5.38 for final book review."""
from pathlib import Path
import json
import image_tex as p
root=p.ROOT;build=root/'image_tex/build';d=p.load()
figures={'5.35':[f'ch05/fig_5_{n}.tex' for n in range(47,51)],'5.36':['ch05/fig_5_51.tex'],
         '5.37':['ch05/fig_5_52.tex','ch05/fig_5_53.tex'],
         '5.38':[f'ch05/fig_5_{n}.tex' for n in range(54,57)]}
for paths in figures.values():
    for path in paths:
        e=next(e for e in d['images'] if e['tex']=='image_tex/'+path)
        assert e['applied'] and e['compiled']==e['reviewed']==p.signature(e) and e.get('layout_review')
reports={'5.35':'degree-elevation-stages-check.json','5.36':'elevated-knot-removal-check.json',
         '5.37':'curve-degree-comparisons-check.json','5.38':'surface-degree-comparisons-check.json'}
geometry={key:json.loads((build/path).read_text(encoding='utf-8')) for key,path in reports.items()}
(build/'chapter5-degree-elevation-geometry.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
batch={'id':'chapter5-degree-elevation','figures':figures,'next_figure':'5.39',
       'geometry_report':'image_tex/build/chapter5-degree-elevation-geometry.json',
       'geometry_note':'Native sequential degree elevation, exact Bezier extraction/elevation/inverse insertion and whole polynomial identities. Four cubic degree representations and five tensor surface degree representations verified with unchanged parameterization. Actual chapter layouts individually inspected; split captions reunited and figures removed from unrelated algorithm/reduction sections.'}
(build/'chapter5-degree-elevation-batch.json').write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared5.35-5.38 batch; final book compilation and fresh page inspection still required.')
