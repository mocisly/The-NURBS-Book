"""Collect chapter5's final drawing/table work for fresh final-book review."""
import json
import image_tex as p
root=p.ROOT;build=root/'image_tex/build';d=p.load()
previous=json.loads((build/'chapter5-degree-elevation-batch.json').read_text(encoding='utf-8'))
figures={'5.10':['ch05/fig_5_11.tex'],**previous['figures'],
         '5.39':[f'ch05/fig_5_{n}.tex' for n in range(57,61)],
         '5.40':['ch05/fig_5_61.tex'],'5.41':['ch05/fig_5_62.tex'],'5.42':['ch05/fig_5_63.tex']}
regions={'由式(5.15)生成的控制点三角表':['ch05/table_5_01.tex']}
for paths in list(figures.values())+list(regions.values()):
    for path in paths:
        e=next(e for e in d['images'] if e['tex']=='image_tex/'+path)
        assert e['applied'] and e['compiled']==e['reviewed']==p.signature(e) and e.get('layout_review')
unused=next(e for e in d['images'] if e['tex']=='image_tex/ch05/fig_5_10c_reference.tex')
assert unused['compiled']==unused['reviewed']==p.signature(unused) and unused.get('coverage_review')
geometry=json.loads((build/'chapter5-degree-elevation-geometry.json').read_text(encoding='utf-8'))
for label,name in [('5.39','degree-reduction-stages'),('5.40','bezier-degree-reduction'),
                   ('5.41','spline-degree-reduction'),('5.42','refined-degree-reduction'),
                   ('table5.1','knot-insertion-table'),('5.10c-reference','surface-insertion-reference')]:
    geometry[label]=json.loads((build/(name+'-check.json')).read_text(encoding='utf-8'))
(build/'chapter5-complete-geometry.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
batch={'id':'chapter5-complete','figures':figures,'text_regions':regions,'next_figure':'6.1',
       'geometry_report':'image_tex/build/chapter5-complete-geometry.json',
       'geometry_note':'All chapter5 ordinary figures and HTML Table5.1 now semantic. Degree elevation exact; degree reduction real errors certified, including independent odd/even Bezier error laws and a rigorous coarse quadratic impossibility/refined-fit proof. Original5.10c crop has a reviewed standalone reference and is already represented by the grouped book panel. Final book rechecks5.10 and5.35-5.42 plus the restored table after local pagination/text repairs.'}
(build/'chapter5-complete-batch.json').write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared chapter5 complete batch: fresh final-book compilation and visual page inspection still required.')
