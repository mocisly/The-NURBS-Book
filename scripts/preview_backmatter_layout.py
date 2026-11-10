"""Fast layout-only proof; synthetic index pages are never used for publication."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'tmp/backmatter/layout';BUILD.mkdir(parents=True,exist_ok=True)
terms={e['id']:e for e in json.loads((ROOT/'backmatter/index-entries.json').read_text(encoding='utf-8'))}
points=json.loads((ROOT/'backmatter/index-locations.json').read_text(encoding='utf-8'))
idx=[]
for point in points:
    for key in point['entries']:
        e=terms[key]
        for path in e['paths']:
            label='!'.join(f'{p[0]}@{p[1]}'for p in path)
            encap='see{'+e['see']+'}'if e.get('see')else'hyperpage'
            idx.append(r'\indexentry{'+label+'|'+encap+'}{'+str(point['chapter']*10+int(point['id'][1:])%8)+'}')
(BUILD/'layout-index.idx').write_text('\n'.join(idx)+'\n',encoding='utf-8')
subprocess.run(['makeindex','-s','backmatter/book.ist','-o',(BUILD/'layout-index.ind').relative_to(ROOT).as_posix(),(BUILD/'layout-index.idx').relative_to(ROOT).as_posix()],cwd=ROOT,check=True,capture_output=True)
preamble=(ROOT/'main.tex').read_text(encoding='utf-8').split(r'\begin{document}')[0]
tex=r'\PassOptionsToPackage{outputdir=tmp/backmatter/layout}{minted}'+'\n'+preamble+'\n'+r'\begin{document}\setcounter{chapter}{13}\chapter{参考文献}\subfile{chapter/14.tex}\chapter{索引}\input{tmp/backmatter/layout/layout-index.ind}\end{document}'
(BUILD/'preview.tex').write_text(tex,encoding='utf-8')
for i in range(2):
    with (BUILD/f'console-{i}.txt').open('w',encoding='utf-8')as log:
        result=subprocess.run(['xelatex','-shell-escape','-interaction=nonstopmode','-halt-on-error',f'-output-directory={BUILD}',str(BUILD/'preview.tex')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    assert result.returncode==0,BUILD/f'console-{i}.txt'
subprocess.run(['pdftoppm','-scale-to','2000','-png',str(BUILD/'preview.pdf'),str(BUILD/'page')],check=True)
print('Layout-only bibliography/index proof compiled. Synthetic page numbers are not publication evidence.')
