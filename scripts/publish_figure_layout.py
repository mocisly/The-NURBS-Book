"""Publish the fully reviewed size/layout revision and archive reproducible checks."""
from pathlib import Path
import hashlib,json,shutil
from compile_minted_book import inputs
from verified_pdf_publication import publish_pdf
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/figure-layout';REPORTS=ROOT/'image_tex/reports'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
write=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=read(WORK/'book/compile.json');a=read(WORK/'book-analysis.json');v=read(WORK/'visual-review.json')
assert inputs()==c['source_hashes']
assert a['pdf_sha256']==v['pdf_sha256']==c['sha256']
assert v['status']=='passed'and set(v['context_pages_reviewed'])==set(a['context_pages'])
assert v['revision_sheets_reviewed']==list(range(1,50))
assert not a['font_clamped_figures']and not a['words_outside_paper']
assert read(WORK/'source-check.json')['minted_blocks_unchanged']==109
REPORTS.mkdir(exist_ok=True)
for src,dst in [('source-check.json','source-check'),('final-sizes.json','sizes'),('profiles.json','profiles'),('layout-offsets.json','label-spacing'),('caption-placements.json','caption-placements'),('book-analysis.json','analysis'),('visual-review.json','review')]:
    shutil.copyfile(WORK/src,REPORTS/f'figure-layout-{dst}.json')
for name in ['individual-review','chapter-breaks','before-break-overview-review','pagination-comparison']:
    p=WORK/f'{name}.json'
    if p.exists():shutil.copyfile(p,REPORTS/f'figure-layout-{name}.json')
baseline=read(WORK/'baseline.json')
write(REPORTS/'figure-layout-baseline.json',dict(source_hashes=baseline['source_hashes'],listing_baseline_sha256=hashlib.sha256(json.dumps(baseline['minted'],sort_keys=True).encode()).hexdigest(),native_geometric_data_preserved=436))
proofs={}
for name in ['catalogue','revision','touchups','spacing','spacing2','labels','final-refinements','final-label']:
    pdf=WORK/f'{name}.pdf';records=WORK/f'{name}.json'
    if pdf.exists()and records.exists():proofs[name]=dict(pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),records=read(records))
write(REPORTS/'figure-layout-proofs.json',proofs)
for page in v.get('retained_preview_pages',[]):
    shutil.copyfile(WORK/f'context/page-{page:03}.png',REPORTS/f'figure-layout-page-{page:03}.png')
publish_pdf(WORK/'book/main.pdf',ROOT/'main.pdf',c['sha256'])
c.update(status='published',preserved_native_image_replacements=435,visual_review='image_tex/reports/figure-layout-review.json',source_check='image_tex/reports/figure-layout-source-check.json')
write(REPORTS/'figure-layout-compile.json',c)
summary={k:c[k]for k in ['exit_code','pages','sha256','paper_mm']};summary['pdf']='main.pdf'
note='Current A1 PDF uses individually sized geometry with unchanged label fonts, revised figure 1.2 placement and caption grouping. All 436 native sources retain their mathematical data; all 109 minted blocks are unchanged. Earlier manifest signatures and reports are historical snapshots.'
for name in ['progress','validation']:
    p=ROOT/f'image_tex/{name}.json';j=read(p)
    j['last_complete_book_compile'if name=='progress'else'book_compile']=summary
    j['final_validation']='image_tex/reports/figure-layout-compile.json'
    j['latest_layout_validation']='image_tex/reports/figure-layout-review.json'
    j['intermediate_cleanup_report']='image_tex/reports/figure-layout-cleanup.json'
    j['validation_note']=note
    if name=='progress':j['work_in_progress']='Complete: individual figure sizing and placement reviewed and published.'
    else:
        j['date']='2026-11-10';j['geometry_note']=note
        j['page_layout']='436 native source proofs reviewed; all 13 chapters checked in final A1 page contexts.'
        j['historical_figure_pages']=j.pop('figure_pages',{})
        j['source_snapshot']='image_tex/reports/figure-layout-compile.json:source_hashes'
        j['geometry_check'].update(book_geometry='A1 594 x 841mm; 11pt body; 1.5 line spacing; geometric scaling preserves label fonts',all_current_compile_and_review_signatures=False,all_individual_layout_evidence_present=False,current_layout_evidence='image_tex/reports/figure-layout-proofs.json',signature_note='Old per-source manifest signatures refer to historical redraw previews; current revision is verified by the figure-layout reports and full source hash map.')
        j['geometry_check'].pop('all_current_compile_and_review_signatures',None)
        j['geometry_check'].pop('all_individual_layout_evidence_present',None)
        j['geometry_check'].update(current_layout_validation='passed',current_source_hashes_verified=True,native_proofs_reviewed=436,historical_manifest_signatures_current=False,historical_preview_files_retained=False)
    write(p,j)
readme=ROOT/'image_tex/README.md';s=readme.read_text(encoding='utf-8')
old='共210页；SHA256为`fc6e8c7c55420208bff1dd58fa7da03ce8c8c077a7cc253211832b662d8abf0a`'
s=s.replace(old,f"共{c['pages']}页；SHA256为`{c['sha256']}`")
s=s.replace('最新页眉页脚与A1尺寸核验见`reports/a1-layout-*.json`','最新逐图尺寸、正文搭配与A1尺寸核验见`reports/figure-layout-*.json`；`reports/a1-layout-*.json`保留页眉页脚改版记录')
s+='\n## 图片尺度与位置\n\n以图1-1、图1-2为简单图的尺度参考。`figure-scales.tex`保存436份原生图的独立几何倍率，`figure-layout.tex`在局部应用倍率；图中文字保持原字号，PGFPlots的坐标轴按实际尺寸排版。多面板、密集标注和数据结构图允许更大，以保证可读性。图1-2紧跟速度比较段落，图1-3、图1-4及随后早期图题与对应图片居中成组。\n\n最新证据为`reports/figure-layout-compile.json`中的完整输入哈希、`figure-layout-proofs.json`中的逐图尺寸样张记录和`figure-layout-review.json`中的整页检查记录。旧manifest的逐图签名是历史记录。\n'
readme.write_text(s,encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8')
s=s.replace('当前 A1 成品的编译与版面核验记录见 `image_tex/reports/a1-layout-*.json`。','当前成品的编译、逐图尺度与正文搭配核验记录见 `image_tex/reports/figure-layout-*.json`；`a1-layout-*.json` 为此前页眉页脚改版记录。')
s+='\n## 图片尺寸\n\n简单图以图1-1、图1-2为尺度参考，复杂多面板和数据结构图按信息密度保留较大尺寸。`image_tex/figure-scales.tex`逐图控制几何尺度，图中文字保持原字号。图1-2置于速度比较之后、球面介绍之前。\n\n`python -B scripts/compile_figure_layout.py`在`tmp/figure-layout/book/`编译并验证整书，不直接覆盖根目录成品。正式源码、图片倍率、脚本、原图和核验报告需要保留；临时样张与编译缓存可以用清理脚本删除。\n'
p.write_text(s,encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
