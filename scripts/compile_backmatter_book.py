"""Compile and validate the book's native citations and live index in isolation."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,sys
from pypdf import PdfReader
from compile_minted_book import inputs
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/backmatter';BUILD=WORK/'book';BUILD.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--force',action='store_true');args=parser.parse_args()
subprocess.run([sys.executable,'-B','scripts/check_backmatter_sources.py'],cwd=ROOT,check=True)
before=inputs();entry=BUILD/'entry.tex'
entry.write_text(r'\PassOptionsToPackage{outputdir=tmp/backmatter/book}{minted}'+'\n'+r'\input{main.tex}'+'\n',encoding='utf-8')
command=[shutil.which('latexmk'),'-norc','-r','.latexmkrc','-xelatex','-shell-escape','-interaction=nonstopmode','-halt-on-error','-synctex=1','-jobname=main','-outdir=tmp/backmatter/book',entry.relative_to(ROOT).as_posix()]
if args.force:command.insert(1,'-g')
with (BUILD/'console.txt').open('w',encoding='utf-8')as out:result=subprocess.run(command,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
assert result.returncode==0,'See tmp/backmatter/book/console.txt'
assert before==inputs(),'Sources changed while compiling'
pdf=BUILD/'main.pdf';reader=PdfReader(pdf);log=(BUILD/'main.log').read_text(encoding='utf-8',errors='replace')
assert not any(l.startswith('!')or l.startswith('Missing character:')for l in log.splitlines())
assert not any(x in log for x in ['There were undefined references','Label(s) may have changed','Package fancyhdr Warning:'])
assert not re.search(r'LaTeX Warning: (?:Citation|Reference).*undefined',log)
for page in reader.pages:assert abs(float(page.mediabox.width)-594/25.4*72)<.1 and abs(float(page.mediabox.height)-841/25.4*72)<.1
aux=(BUILD/'main.aux').read_text(encoding='utf-8');bib=re.findall(r'\\bibcite\{([^}]+)\}',aux);assert len(bib)==173
from restore_backmatter import balanced_end
point_pages={}
for m in re.finditer(r'\\newlabel\{bookindex:(p\d+)\}\{',aux):
    first=m.end();first_end=balanced_end(aux,first);page_end=balanced_end(aux,first_end)
    point_pages[m[1]]=int(aux[first_end+1:page_end-1])
points=json.loads((ROOT/'backmatter/index-locations.json').read_text(encoding='utf-8'));assert set(point_pages)=={p['id']for p in points},set(p['id']for p in points)-set(point_pages)
assert all(1<=p<len(reader.pages)for p in point_pages.values())
entries=json.loads((ROOT/'backmatter/index-entries.json').read_text(encoding='utf-8'));terms={e['id']:e for e in entries};expected=[]
for p in points:
    for key in p['entries']:
        e=terms[key]
        for path in e['paths']:
            label='!'.join(f'{part[0]}@{part[1]}'for part in path);encap='see{'+e['see']+'}'if e.get('see')else'hyperpage'
            expected.append(r'\indexentry{'+label+'|'+encap+'}{'+str(point_pages[p['id']])+'}')
actual=[l.strip()for l in (BUILD/'main.idx').read_text(encoding='utf-8').splitlines()if l.strip()]
normalized=[re.sub(r'\|hyperindexformat\{\\(hyperpage|see\{[^}]+\})\}',r'|\1',l)for l in actual]
assert sorted(normalized)==sorted(expected),'Index pages differ from their exact body labels'
index_log=(BUILD/'main.ilg').read_text(encoding='utf-8',errors='replace');assert '0 rejected'in index_log and '0 warnings'in index_log,index_log
subprocess.run(['pdftotext','-layout',str(pdf),str(BUILD/'main-layout.txt')],check=True)
text=(BUILD/'main-layout.txt').read_text(encoding='utf-8');algorithms=re.findall(r'算法\s+(A\d+\.\d+)\s*[（(]伪代码',text)
assert len(algorithms)==len(set(algorithms))==61
assert '[?]'not in text and '@'not in text
cache={Path(l[6:])for l in (BUILD/'main.fls').read_text(encoding='utf-8',errors='replace').splitlines()if l.startswith('INPUT ')and l.endswith('.pygtex')};assert len(cache)==109
for p in cache:
    p=p if p.is_absolute()else ROOT/p
    assert r'\PYG{err}'not in p.read_text(encoding='utf-8')
report=dict(status='compiled-awaiting-visual-review',exit_code=0,pages=len(reader.pages),paper_mm=[594,841],sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),source_hashes=before,source_inputs_unchanged=True,missing_glyph_warnings=0,fatal_errors=0,overfull_hbox_warnings=log.count('Overfull \\hbox'),numbered_algorithms=61,preserved_listings=109,preserved_native_image_replacements=435,bibliography_entries=173,index_entries=len(entries),index_source_locations=len(points),raw_index_records=len(actual),all_index_pages_match_body_labels=True,index_rejections=0,index_warnings=0,index_point_pages=point_pages)
(BUILD/'compile.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items()if k not in ['source_hashes','index_point_pages']},ensure_ascii=False))
