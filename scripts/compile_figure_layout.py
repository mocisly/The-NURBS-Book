"""Compile the resized A1 book and check complete figure and listing coverage."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
from pypdf import PdfReader
from compile_minted_book import inputs
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'tmp/figure-layout/book'
BUILD.mkdir(parents=True,exist_ok=True)
subprocess.run([__import__('sys').executable,'-B','scripts/check_figure_layout_sources.py'],cwd=ROOT,check=True)
before=inputs()
wrapper=BUILD/'entry.tex'
wrapper.write_text(r'\PassOptionsToPackage{outputdir=tmp/figure-layout/book}{minted}'+'\n'+r'\input{main.tex}'+'\n',encoding='utf-8')
command=[shutil.which('latexmk'),'-norc','-r',str(ROOT/'.latexmkrc'),'-xelatex','-shell-escape','-interaction=nonstopmode','-halt-on-error','-synctex=1','-jobname=main',f'-outdir={BUILD}',str(wrapper)]
with (BUILD/'console.txt').open('w',encoding='utf-8')as out:
    result=subprocess.run(command,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
assert result.returncode==0,'See tmp/figure-layout/book/console.txt'
assert before==inputs(),'Sources changed while compiling'
pdf=BUILD/'main.pdf';reader=PdfReader(pdf)
for n,page in enumerate(reader.pages,1):
    assert abs(float(page.mediabox.width)-594/25.4*72)<.1 and abs(float(page.mediabox.height)-841/25.4*72)<.1,n
log=(BUILD/'main.log').read_text(encoding='utf-8',errors='replace')
assert not any(l.startswith('!')or l.startswith('Missing character:')for l in log.splitlines())
assert 'Package fancyhdr Warning:'not in log
assert 'There were undefined references'not in log
assert 'Label(s) may have changed'not in log
subprocess.run(['pdftotext','-layout',str(pdf),str(BUILD/'main-layout.txt')],check=True)
text=(BUILD/'main-layout.txt').read_text(encoding='utf-8')
found=re.findall(r'算法\s+(A\d+\.\d+)\s*[（(]伪代码',text)
expected=[f'A{n}.{i}'for n,c in enumerate([0,7,5,8,4,11,2,3,2,12,4,1,2])if n for i in range(1,c+1)]
assert sorted(found)==sorted(expected)
assert '@'not in text
cache={Path(line[6:])for line in (BUILD/'main.fls').read_text(encoding='utf-8',errors='replace').splitlines()if line.startswith('INPUT ')and line.endswith('.pygtex')}
cache={p if p.is_absolute()else ROOT/p for p in cache}
assert len(cache)==109,len(cache)
assert all(r'\PYG{err}'not in p.read_text(encoding='utf-8')for p in cache)
report=dict(status='compiled-awaiting-visual-review',exit_code=0,pages=len(reader.pages),paper_mm=[594,841],sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),source_hashes=before,missing_glyph_warnings=0,fatal_errors=0,overfull_hbox_warnings=log.count('Overfull \\hbox'),numbered_algorithms=61,preserved_listings=109,source_inputs_unchanged=True)
(BUILD/'compile.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items()if k!='source_hashes'},ensure_ascii=False))
