"""Record actual reviewed coverage of the5.10c standalone reference asset."""
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch05/fig_5_10c_reference.tex')
covered=next(e for e in d['images'] if e['tex']=='image_tex/ch05/fig_5_11.tex')
assert e['kind']=='unused' and not e['applied'] and e['compiled']==e['reviewed']==p.signature(e)
assert covered['applied'] and covered['compiled']==covered['reviewed']==p.signature(covered)
assert covered['layout_review']['evidence']=='image_tex/build/chapter-review/fig510-coverage-context.png'
e['coverage_review']={'source_signature':p.signature(e),'covered_source_signature':p.signature(covered),
                      'chapter_pdf':'image_tex/build/chapter-review/chapter-5.pdf','chapter_page':5,
                      'evidence':'image_tex/build/chapter-review/fig510-coverage-context.png',
                      'note':'Viewed native reference and actual chapter5.10c; same5x5 knot59_data net and six labelledQ indices. Standalone crop covered by existing grouped panel; no duplicate book reference.'}
for key in ('book_pdf','book_page','book_sha256','final_page_evidence'):
    if key in covered['layout_review']:e['coverage_review'][key]=covered['layout_review'][key]
p.save(d);print('Recorded verified5.10c coverage; pending unused sources now only the two chapter9/12 HTML crops.')
