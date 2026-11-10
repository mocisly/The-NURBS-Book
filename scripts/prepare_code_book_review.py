"""Render representative code/prose/figure pages from the successfully compiled whole book."""
from pathlib import Path
import json,re,hashlib,subprocess
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/minted-review';BUILD=WORK/'full'
report=json.loads((WORK/'full-compile.json').read_text(encoding='utf-8'))
assert report['status']=='compiled-awaiting-visual-review'and report['source_inputs_unchanged']
pdf=BUILD/'main.pdf';assert hashlib.sha256(pdf.read_bytes()).hexdigest()==report['sha256']
pages=(BUILD/'main-layout.txt').read_text(encoding='utf-8').split('\f')
numbers=set();regions={}
for label in [f'A{n}.1'for n in range(1,13)]+['A1.7','A2.5','A3.4','A5.9','A9.12','A10.4']:
    found=[i+1 for i,p in enumerate(pages)if re.search(r'算法\s*'+re.escape(label)+r'\s*[（(]伪代码',p)]
    assert len(found)==1,(label,found);numbers.update(found);regions[label]=found
for label in ['13.4','13.8','13.9']:
    found=[i+1 for i,p in enumerate(pages)if re.search(r'^\s*图\s*'+re.escape(label)+r'\.',p,re.M)]
    assert len(found)==1,(label,found);numbers.update(found);regions['figure'+label]=found
# Include representative long-listing continuations in the actual book.
for label in ['A2.5','A5.9']:numbers.add(regions[label][0]+1)
out=WORK/'final-pages';out.mkdir(exist_ok=True)
images={}
for number in sorted(numbers):
    prefix=out/f'page{number}'
    subprocess.run(['pdftoppm','-f',str(number),'-singlefile','-scale-to','2500','-png',str(pdf),str(prefix)],check=True)
    images[str(number)]=prefix.with_suffix('.png').relative_to(ROOT).as_posix()
reader=PdfReader(pdf);raster=[]
def scan(resources,page,seen):
    if resources is None:return
    resources=resources.get_object();objects=resources.get('/XObject',{})
    if hasattr(objects,'get_object'):objects=objects.get_object()
    for ref in objects.values():
        obj=ref.get_object();key=(getattr(ref,'idnum',id(obj)),getattr(ref,'generation',0))
        if key in seen:continue
        seen.add(key)
        if obj.get('/Subtype')=='/Image':raster.append(page)
        elif obj.get('/Subtype')=='/Form':scan(obj.get('/Resources'),page,seen)
for n,page in enumerate(reader.pages,1):scan(page.get('/Resources'),n,set())
assert not raster,raster
review=dict(status='awaiting-visual-inspection',final_pdf_sha256=report['sha256'],pages=images,regions=regions,raster_image_objects=0)
(WORK/'final-pages.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Final book pages to inspect:',','.join(map(str,sorted(numbers))))
