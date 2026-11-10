"""Render affected final book pages for subsequent human/model visual inspection."""
from pathlib import Path
import argparse,json,re,subprocess

p=argparse.ArgumentParser(description=__doc__);p.add_argument('batch',type=Path);a=p.parse_args()
root=Path(__file__).resolve().parents[1];build=root/'image_tex/build/book-check'
result=json.loads((root/'image_tex/build/book-check-result.json').read_text(encoding='utf-8-sig'))
assert result['exitCode']==0 and result['pdfExists']
pdf=build/'main.pdf';text=build/'main-layout.txt'
subprocess.run(['pdftotext','-layout',str(pdf),str(text)],check=True)
pages=text.read_text(encoding='utf-8').split('\f')
batch=json.loads(a.batch.read_text(encoding='utf-8'));numbers=set()
for figure in batch['figures']:
    found=[i+1 for i,page in enumerate(pages) if any(re.match(r'^\s*图\s*'+re.escape(figure)+r'\.',line) for line in page.splitlines())]
    assert len(found)==1,(figure,found)
    numbers.add(found[0])
for phrase in batch.get('text_regions',{}):
    found=[i+1 for i,page in enumerate(pages) if re.sub(r'\s+','',phrase) in re.sub(r'\s+','',page)]
    assert len(found)==1,(phrase,found)
    numbers.add(found[0])
batch['inspected_pages']={}
for number in sorted(numbers):
    prefix=build/f"{batch['id']}-page-{number}"
    subprocess.run(['pdftoppm','-f',str(number),'-singlefile','-scale-to','2500','-png',str(pdf),str(prefix)],check=True)
    batch['inspected_pages'][str(number)]=str(prefix.with_suffix('.png').relative_to(root)).replace('\\','/')
a.batch.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Rendered pages to inspect: '+', '.join(map(str,sorted(numbers))))
