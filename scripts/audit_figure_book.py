"""Audit placed figure dimensions and prepare actual A1 page review images."""
from pathlib import Path
import hashlib,json,re,subprocess,xml.etree.ElementTree as ET
from pypdf import PdfReader
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/figure-layout';BUILD=WORK/'book'
pdf=BUILD/'main.pdf';report=json.loads((BUILD/'compile.json').read_text(encoding='utf-8'))
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==report['sha256']
log=(BUILD/'main.log').read_text(encoding='utf-8',errors='replace')
rows=[]
for m in re.finditer(r'BOOKFIG\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([\d.p\s]+t)',log):
    path,*dims=m.groups();w,pw,h,lw=[float(re.sub(r'\s','',d).replace('pt',''))for d in dims]
    rows.append(dict(path=path.strip(),native_width_pt=w,placed_width_pt=pw,height_pt=h,container_width_pt=lw,font_factor=pw/w))
assert len(rows)==435,len(rows)
clamped=[r for r in rows if r['font_factor']<.97]
subprocess.run(['pdftotext','-bbox',str(pdf),str(BUILD/'bbox.html')],check=True)
xml=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',(BUILD/'bbox.html').read_text(encoding='utf-8'))
pages=ET.fromstring(xml).findall('.//{*}page');outside=[]
for n,p in enumerate(pages,1):
    for w in p.findall('.//{*}word'):
        x0,y0,x1,y1=[float(w.attrib[k])for k in ['xMin','yMin','xMax','yMax']]
        if x0<0 or y0<0 or x1>float(p.attrib['width'])+.1 or y1>float(p.attrib['height'])+.1:outside.append(dict(page=n,text=w.text,bounds=[x0,y0,x1,y1]))
reader=PdfReader(pdf)
top=[o for o in reader.outline if not isinstance(o,list)]
start=next(i for i,o in enumerate(top)if o.title=='曲线和曲面基础')
starts=[dict(title=o.title,page=reader.get_destination_page_number(o)+1)for o in top[start:start+13]]
assert len(starts)==13,starts
chosen=set()
for c in starts:chosen.update([c['page'],min(len(pages),c['page']+1)])
chosen.update(range(starts[0]['page'],starts[1]['page']))
out=WORK/'context';out.mkdir(exist_ok=True)
for n in sorted(chosen):subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1800','-png',str(pdf),str(out/f'page-{n:03}')],check=True)
overview=WORK/'page-overview';overview.mkdir(exist_ok=True)
subprocess.run(['pdftoppm','-scale-to','600','-png',str(pdf),str(overview/'page')],check=True)
digits=len(str(len(pages)));sheets=[]
for start in range(0,len(pages),9):
    sheet=Image.new('RGB',(1272,1872),'#303030');draw=ImageDraw.Draw(sheet)
    for i,n in enumerate(range(start+1,min(start+10,len(pages)+1))):
        x=(i%3)*424;y=(i//3)*624
        draw.text((x+5,y+4),f'PDF page {n}',fill='white')
        im=Image.open(overview/f'page-{n:0{digits}}.png').convert('RGB');sheet.paste(im,(x,y+20))
    name=f'sheet-{len(sheets)+1:02}.png';sheet.save(overview/name);sheets.append(dict(file=name,pages=list(range(start+1,min(start+10,len(pages)+1)))))
(overview/'sheets.json').write_text(json.dumps(sheets,indent=2),encoding='utf-8')
result=dict(status='awaiting-visual-review',pdf_sha256=report['sha256'],pages=len(pages),placed_figures=len(rows),font_clamped_figures=clamped,words_outside_paper=outside,chapters=starts,context_pages=sorted(chosen),placements=rows)
(WORK/'book-analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items()if k not in ['placements','chapters']},ensure_ascii=False))
