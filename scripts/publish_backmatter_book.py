"""Publish the reviewed linked bibliography/index and archive validation evidence."""
from pathlib import Path
import hashlib,json,re,shutil
from compile_minted_book import inputs
from verified_pdf_publication import publish_pdf
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/backmatter';REPORTS=ROOT/'image_tex/reports'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
write=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=read(WORK/'book/compile.json');a=read(WORK/'pdf-analysis.json');v=read(WORK/'visual-review.json');s=read(WORK/'source-check.json')
assert inputs()==c['source_hashes']
assert a['pdf_sha256']==v['pdf_sha256']==c['sha256']
assert v['status']=='passed'and set(v['detail_pages_reviewed'])==set(a['detail_pages'])
assert v['overview_sheets_reviewed']==list(range(1,len(a['overview_sheets'])+1))
assert s['preserved_native_sources']==436 and s['preserved_minted_blocks']==109
assert a['all_internal_destinations_resolve']and a['index_terminal_entries_verified']==359
assert not a['words_outside_paper']and not a['font_clamped_figures']
assert c['overfull_hbox_warnings']==0
for source,suffix in [('source-check.json','source-check'),('pdf-analysis.json','analysis'),('visual-review.json','review'),('citation-migration.json','citation-migration')]:shutil.copyfile(WORK/source,REPORTS/f'backmatter-{suffix}.json')
b=read(WORK/'baseline.json')
write(REPORTS/'backmatter-baseline.json',dict(source_hashes=b['source_hashes'],native_figure_hashes=b['native_figure_hashes'],previous_pdf_sha256=b['published_pdf_sha256'],minted_block_hashes={k:[hashlib.sha256(text.encode()).hexdigest()for text in texts]for k,texts in b['minted'].items()}))
for suffix in ['idx','ind','ilg']:shutil.copyfile(WORK/f'book/main.{suffix}',REPORTS/f'backmatter-final.{suffix}')
for n in v['retained_preview_pages']:shutil.copyfile(WORK/f'review/page-{n:03}.png',REPORTS/f'backmatter-page-{n:03}.png')
publish_pdf(WORK/'book/main.pdf',ROOT/'main.pdf',c['sha256'])
c.update(status='published',visual_review='image_tex/reports/backmatter-review.json',source_check='image_tex/reports/backmatter-source-check.json',pdf_analysis='image_tex/reports/backmatter-analysis.json')
write(REPORTS/'backmatter-compile.json',c)
summary={k:c[k]for k in ['exit_code','pages','sha256','paper_mm']};summary['pdf']='main.pdf'
note='Current A1 PDF has 173 native bibliography items, linked author-year citations, and 359 curated index entries generated from 251 body locations. All bibliography targets and generated index page links were verified. Native figure sources and all 109 minted blocks are unchanged from the prior figure-layout publication.'
for name in ['progress','validation']:
    p=ROOT/f'image_tex/{name}.json';j=read(p)
    j['last_complete_book_compile'if name=='progress'else'book_compile']=summary
    j['final_validation']='image_tex/reports/backmatter-compile.json';j['latest_layout_validation']='image_tex/reports/backmatter-review.json'
    j['latest_backmatter_validation']='image_tex/reports/backmatter-analysis.json';j['intermediate_cleanup_report']='image_tex/reports/backmatter-cleanup.json';j['validation_note']=note
    j['bibliography_entries']=173;j['index_entries']=359;j['index_source_locations']=251
    if name=='progress':j['work_in_progress']='Complete: linked bibliography and regenerated index compiled, reviewed and published.'
    else:
        j['date']='2026-11-10';j['source_snapshot']='image_tex/reports/backmatter-compile.json:source_hashes'
        j['page_layout']='All final pages inspected; bibliography/index detail pages reviewed; all citation targets and index page links verified.'
        j['geometry_check']['current_layout_evidence']='image_tex/reports/backmatter-analysis.json'
    write(p,j)
p=ROOT/'image_tex/README.md';text=p.read_text(encoding='utf-8')
text=re.sub(r'共\d+页；SHA256为`[0-9a-f]+`',f"共{c['pages']}页；SHA256为`{c['sha256']}`",text)
text=text.replace('最新逐图尺寸、正文搭配与A1尺寸核验见`reports/figure-layout-*.json`','最新整书、文献和索引核验见`reports/backmatter-*.json`；逐图尺寸与正文搭配见`reports/figure-layout-*.json`')
text+='\n## 参考文献与索引\n\n当前成品包含173条可链接参考文献和359个整理后的索引条目，索引页码来自正文251处标记。新增正式源码位于根目录`backmatter/`，包括索引条目、位置映射、排版设置和MakeIndex样式，需要保留。原始OCR参考文献和索引保存在`reports/backmatter-*-original.tex`。此前报告中的页码和PDF哈希是历史记录。\n'
p.write_text(text,encoding='utf-8')
p=ROOT/'README.md';text=p.read_text(encoding='utf-8')
text=text.replace('xelatex --shell-escape -interaction=nonstopmode -halt-on-error main.tex\nxelatex --shell-escape -interaction=nonstopmode -halt-on-error main.tex','latexmk -xelatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex')
text=text.replace('当前成品的编译、逐图尺度与正文搭配核验记录见 `image_tex/reports/figure-layout-*.json`；','当前整书、参考文献和索引核验见 `image_tex/reports/backmatter-*.json`；逐图尺度与正文搭配见 `figure-layout-*.json`；')
text+='''
## 参考文献与索引

第14章使用原生 `\\bibitem[作者年份编号]{key}`；正文通过 `\\cite{key}` 引用。合并年份已展开为完整文献键，173条文献的原始内容保留。文献条目中的期刊/论文页码属于文献本身，不随本书分页修改。

第15章使用 MakeIndex 自动排页码，四栏显示，主条目按拼音或英文名称排序。359个条目在 `backmatter/index-entries.json` 中维护；正文的 `\\BookIndexMark{pNNNN}` 对应 `backmatter/index-locations.json` 和生成的 `index-marks.tex`。页码均可点击跳至正文；重新分页后无需手工改索引数字。

`.latexmkrc` 为 MakeIndex 指定 `backmatter/book.ist`，因此应使用 `make.bat`、`make` 或上面的 latexmk 命令，不能只执行两次 XeLaTeX 后就认为索引已更新。需要手工构建时，按 XeLaTeX → `makeindex -s backmatter/book.ist main.idx` → XeLaTeX 的顺序执行，并继续编译至引用和页码稳定。

维护索引时，编辑 `backmatter/index-entries.json` 中的层级、排序键和精确定位条件，再执行 `python -B scripts/restore_backmatter.py index` 更新标记。`scripts/curate_book_index.py` 和 `restore_backmatter.py bibliography` 是本次OCR恢复的一次性迁移工具，日常不应覆盖已编辑的数据。

本次恢复流程的 `compile_backmatter_book.py`、`audit_backmatter_pdf.py` 和 `publish_backmatter_book.py` 保存隔离编译、核验和发布步骤，发布依赖对应的迁移基线及审阅报告。清理后如修改源码，应为新的审阅流程建立基线；日常重新排版直接使用 `make.bat` 或 latexmk。`backmatter/`、`.latexmkrc`、章节源码、脚本和报告是正式文件；`tmp/backmatter/` 与编译缓存可清理。
'''
p.write_text(text,encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
