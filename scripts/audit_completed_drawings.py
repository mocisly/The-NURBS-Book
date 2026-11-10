"""Audit all live native replacements before freezing the final full-book build."""
from pathlib import Path
import json,re
import image_tex as p
d=p.load();active=[e for e in d['images']if e['kind']!='unused'];unused=[e for e in d['images']if e['kind']=='unused']
assert len(active)==435 and all(e.get('applied')for e in active)
for e in active:
    p.tex_source_ok(e);sig=p.signature(e)
    assert e['compiled']==e['reviewed']==sig,e['tex']
    assert e.get('layout_review')and e['layout_review']['source_signature']==sig,e['tex']
    assert(p.ROOT/e['layout_review']['evidence']).exists(),e['tex']
    assert p.uncomment((p.ROOT/e['chapter_file']).read_text(encoding='utf-8')).count(e['replacement'])==1,e['tex']
chapters=[p.ROOT/f'chapter/{i}.tex'for i in range(1,16)];assert all(f.exists()for f in chapters)
for f in chapters:
    s=p.uncomment(f.read_text(encoding='utf-8'));assert not re.search(r'\\includegraphics\b|<img\s',s),f
s=(p.ROOT/'chapter/13.tex').read_text(encoding='utf-8');point=s[s.index(r'\node[left=7pt]'):s.index('这些定义的一个吸引人的特点')]
assert r'$wx$'in point and r'$wy$'in point and r'$wz$'in point and r'\phantom'not in point
enode=s[s.index('typedef struct enode'):s.index(r'\} ENODE;')];assert r'\begin{cases}'not in enode and r'\{'in enode and 'INTEGER eno;'in enode and 'STRING fna;'in enode
assert '*knv;'in s and '*krv;'not in s
main=(p.ROOT/'main.tex').read_text(encoding='utf-8');assert 'headfoot'not in main
assert 'paperwidth=40cm'in main and 'paperheight=80cm'in main and 'fontsize=11pt'in main
report=dict(status='all_native_sources_and_chapter_references_verified',active_original_references=435,applied_native_drawings=len(active),authored_manifest_sources=sum((p.ROOT/e['tex']).exists()for e in d['images']),remaining_original_images=0,remaining_HTML_images=0,chapter_files_checked=15,content_chapters=13,bibliography_and_index_also_checked=True,all_current_compile_and_review_signatures=True,all_individual_layout_evidence_present=True,no_contour_or_raster_wrappers=True,covered_unused_references=[e['tex']for e in unused],inline_native_repairs=['13.1 POINT/CPOINT cells restored from adjacent typedefs'],adjacent_OCR_repairs=['SURFACE knv spelling','ENODE opening brace; removed spurious zero formula'],book_geometry='40cm x80cm,11ptbody,1.5lines; originalgeometry retained; headfoot option replaced by valid dimensions')
(p.BASE/'build/final-native-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
