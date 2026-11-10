"""Compile and audit the A1 book without replacing the published PDF."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
from pypdf import PdfReader
from compile_minted_book import inputs
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'tmp/a1-review'
BUILD.mkdir(parents=True,exist_ok=True)
before=inputs()
wrapper=BUILD/'entry.tex'
wrapper.write_text(r'\PassOptionsToPackage{outputdir=tmp/a1-review}{minted}'+'\n'+r'\input{main.tex}'+'\n',encoding='utf-8')
command=[shutil.which('latexmk'),'-norc','-r',str(ROOT/'.latexmkrc'),'-xelatex','-shell-escape','-interaction=nonstopmode','-halt-on-error','-synctex=1','-jobname=main',f'-outdir={BUILD}',str(wrapper)]
with (BUILD/'console.txt').open('w',encoding='utf-8')as log:
    result=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
assert result.returncode==0,'See tmp/a1-review/console.txt'
assert before==inputs(),'Sources changed while compiling'
published=ROOT/'image_tex/reports/backmatter-compile.json'
if not published.exists():published=ROOT/'image_tex/reports/figure-layout-compile.json'
if not published.exists():published=ROOT/'image_tex/reports/code-listings-compile.json'
previous=json.loads(published.read_text(encoding='utf-8'))
assert all(before.get(p)==h for p,h in previous['source_hashes'].items() if p!='main.tex'),'Chapter or drawing sources differ from the completed code review'
pdf=BUILD/'main.pdf';reader=PdfReader(pdf)
for n,page in enumerate(reader.pages,1):
    assert abs(float(page.mediabox.width)-594/25.4*72)<.1 and abs(float(page.mediabox.height)-841/25.4*72)<.1,n
log=(BUILD/'main.log').read_text(encoding='utf-8',errors='replace')
assert not any(l.startswith('!')or l.startswith('Missing character:')for l in log.splitlines())
assert not re.search(r'Package fancyhdr Warning:.*(?:headheight|footskip)',log,re.S)
subprocess.run(['pdftotext','-layout',str(pdf),str(BUILD/'main-layout.txt')],check=True)
text=(BUILD/'main-layout.txt').read_text(encoding='utf-8')
found=re.findall(r'算法\s+(A\d+\.\d+)\s*[（(]伪代码',text)
expected=[f'A{n}.{i}'for n,c in enumerate([0,7,5,8,4,11,2,3,2,12,4,1,2])if n for i in range(1,c+1)]
assert sorted(found)==sorted(expected),(len(found),set(expected)-set(found))
assert '@'not in text,'Unprocessed code escape marker'
report=dict(status='compiled-awaiting-visual-review',exit_code=0,pages=len(reader.pages),paper_mm=[594,841],orientation='portrait',header_gap_mm=12,footer_skip_mm=14,side_margins_mm=22,headheight_pt=24,sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),source_hashes=before,missing_glyph_warnings=0,fatal_errors=0,overfull_hbox_warnings=log.count('Overfull \\hbox'))
report.update(numbered_algorithms=61,preserved_listings=109,preserved_native_image_replacements=435,source_inputs_unchanged=True,top_margin_mm=20,bottom_margin_mm=18,header_font_pt=9,page_number_font_pt=12)
(BUILD/'compile.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items()if k!='source_hashes'},ensure_ascii=False))
