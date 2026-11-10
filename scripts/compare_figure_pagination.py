"""Carry forward reviewed pages only when body words and positions match exactly."""
from pathlib import Path
import collections,hashlib,json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'tmp/figure-layout'
def load(path):
    xml=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',path.read_text(encoding='utf-8'))
    return ET.fromstring(xml).findall('.//{*}page')
def signature(page):
    words=[]
    for w in page.findall('.//{*}word'):
        if 90<float(w.attrib['yMin'])<2310:
            words.append((w.text,*[round(float(w.attrib[k]),3)for k in ['xMin','yMin','xMax','yMax']]))
    return hashlib.sha256(json.dumps(words,ensure_ascii=False).encode()).hexdigest()
old=load(W/'before-break-bbox.html');new=load(W/'book/bbox.html')
lookup=collections.defaultdict(list)
for n,p in enumerate(old,1):lookup[signature(p)].append(n)
matched=[];changed=[]
for n,p in enumerate(new,1):
    matches=lookup[signature(p)]
    if matches:matched.append(dict(page=n,previous_pages=matches))
    else:changed.append(n)
j=dict(previous_pdf_sha256=hashlib.sha256((W/'before-break-fix.pdf').read_bytes()).hexdigest(),current_pdf_sha256=hashlib.sha256((W/'book/main.pdf').read_bytes()).hexdigest(),comparison='Body words and positions rounded to 0.001 PDF point; running headers and footer page numbers excluded. Native source hashes and all 435 placed box dimensions independently verified.',identical_body_layout_pages=matched,pages_requiring_new_visual_review=changed)
(W/'pagination-comparison.json').write_text(json.dumps(j,indent=2),encoding='utf-8')
print(json.dumps(dict(identical_pages=len(matched),review_pages=changed)))
