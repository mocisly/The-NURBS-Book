"""Check every bibliography/index destination and render actual book pages for QA."""
from pathlib import Path
import collections,hashlib,json,re,subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/backmatter';BUILD=WORK/'book';REVIEW=WORK/'review';REVIEW.mkdir(exist_ok=True)
c=json.loads((BUILD/'compile.json').read_text(encoding='utf-8'));pdf=BUILD/'main.pdf';assert hashlib.sha256(pdf.read_bytes()).hexdigest()==c['sha256']
r=PdfReader(pdf);top=[o for o in r.outline if not isinstance(o,list)];chapters=[dict(title=o.title,page=r.get_destination_page_number(o)+1)for o in top]
bib_start=next(o['page']for o in chapters if o['title']=='参考文献');index_start=next(o['page']for o in chapters if o['title']=='索引');dest=r.named_destinations
expected_bib={e['key']for e in json.loads((ROOT/'backmatter/bibliography.json').read_text(encoding='utf-8'))}
assert all('cite.'+k in dest for k in expected_bib)
for k in expected_bib:assert bib_start<=r.get_destination_page_number(dest['cite.'+k])+1<index_start,k
layout=(BUILD/'main-layout.txt').read_text(encoding='utf-8').split('\f');citation_links=[];index_links=[];broken=[]
for n,page in enumerate(r.pages,1):
    for item in page.get('/Annots',[]):
        obj=item.get_object();action=obj.get('/A',{});name=action.get('/D',obj.get('/Dest'))
        if isinstance(name,str):
            if name not in dest:broken.append(dict(page=n,destination=name));continue
            target=r.get_destination_page_number(dest[name])+1
            if name.startswith('cite.'):
                assert bib_start<=target<index_start,(n,name,target)
                citation_links.append(dict(page=n,key=name[5:],target=target))
            if index_start<=n<len(r.pages)and name.startswith('page.'):
                number=int(name[5:]);assert target<bib_start
                lines=[l for l in layout[target-1].splitlines()if l.strip()]
                assert re.search(r'(?<!\d)'+str(number)+r'\s*$',lines[-1]),(n,name,target,lines[-1])
                index_links.append(dict(page=n,printed_page=number,target=target))
assert not broken,broken
assert len(citation_links)>=260,len(citation_links)
assert len(index_links)>=300,len(index_links)
# Every terminal index entry must survive MakeIndex with its complete hierarchy.
entries=json.loads((ROOT/'backmatter/index-entries.json').read_text(encoding='utf-8'));ind=(BUILD/'main.ind').read_text(encoding='utf-8');tree=[];seen=set()
for m in re.finditer(r'\\(item|subitem|subsubitem)\s+(.*?)(?=\\(?:item|subitem|subsubitem|BookIndexLetter)\b|\\end\{theindex\}|\Z)',ind,re.S):
    level={'item':1,'subitem':2,'subsubitem':3}[m[1]];label=re.split(r',\s*\\',m[2],maxsplit=1)[0].strip();tree=tree[:level-1];tree.append(label);seen.add(tuple(tree))
expected={tuple(p[1]for p in path)for e in entries for path in e['paths']};assert expected<=seen,expected-seen
# Multiple distant locator pages must never repeat the same see-reference.
for item in re.split(r'\\(?:item|subitem|subsubitem)\s+',ind):
    assert len(re.findall(r'\\see\{',item))<=1,item
subprocess.run(['pdftotext','-bbox',str(pdf),str(REVIEW/'bbox.html')],check=True)
xml=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',(REVIEW/'bbox.html').read_text(encoding='utf-8'));pages=ET.fromstring(xml).findall('.//{*}page');outside=[];hg=[];fg=[]
for n,page in enumerate(pages,1):
    words=page.findall('.//{*}word')
    for w in words:
        x0,y0,x1,y1=[float(w.attrib[k])for k in ['xMin','yMin','xMax','yMax']]
        if x0<0 or y0<0 or x1>float(page.attrib['width'])+.1 or y1>float(page.attrib['height'])+.1:outside.append(dict(page=n,text=w.text,bounds=[x0,y0,x1,y1]))
    head=[w for w in words if float(w.attrib['yMax'])<90];body=[w for w in words if 90<float(w.attrib['yMin'])<2310];foot=[w for w in words if float(w.attrib['yMin'])>2310]
    if n>6 and head and body:hg.append((min(float(w.attrib['yMin'])for w in body)-max(float(w.attrib['yMax'])for w in head))*25.4/72)
    if n>6 and body and foot:fg.append((min(float(w.attrib['yMin'])for w in foot)-max(float(w.attrib['yMax'])for w in body))*25.4/72)
assert not outside,outside
log=(BUILD/'main.log').read_text(encoding='utf-8',errors='replace');clamps=[];figures=[]
for m in re.finditer(r'BOOKFIG\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([\d.p\s]+t)',log):
    p,*dims=m.groups();native,placed,height,line=[float(re.sub(r'\s','',d).replace('pt',''))for d in dims]
    record=dict(path=p.strip(),width_pt=placed,height_pt=height,font_factor=placed/native);figures.append(record)
    if placed/native<.97:clamps.append(record)
assert len(figures)==435 and not clamps,(len(figures),clamps)
detail=set(range(bib_start,len(r.pages)))
by_page=collections.Counter(link['page']for link in citation_links if link['page']<bib_start)
detail.update(n for n,count in by_page.most_common(3));detail.add(next(o['page']for o in chapters if o['title']=='曲线和曲面基础'))
for n in sorted(detail):subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','2400','-png',str(pdf),str(REVIEW/f'page-{n:03}')],check=True)
overview=REVIEW/'overview';overview.mkdir(exist_ok=True)
subprocess.run(['pdftoppm','-scale-to','600','-png',str(pdf),str(overview/'page')],check=True);digits=len(str(len(r.pages)));sheets=[]
for start in range(0,len(r.pages),9):
    sheet=Image.new('RGB',(1272,1872),'#303030');draw=ImageDraw.Draw(sheet)
    for i,n in enumerate(range(start+1,min(start+10,len(r.pages)+1))):
        x=(i%3)*424;y=(i//3)*624;draw.text((x+5,y+4),f'PDF page {n}',fill='white');sheet.paste(Image.open(overview/f'page-{n:0{digits}}.png').convert('RGB'),(x,y+20))
    name=f'sheet-{len(sheets)+1:02}.png';sheet.save(overview/name);sheets.append(dict(file=name,pages=list(range(start+1,min(start+10,len(r.pages)+1)))))
(overview/'sheets.json').write_text(json.dumps(sheets,indent=2),encoding='utf-8')
report=dict(status='automated-checks-passed-awaiting-visual-review',pdf_sha256=c['sha256'],pages=len(r.pages),chapters=chapters,bibliography_pages=list(range(bib_start,index_start)),index_pages=list(range(index_start,len(r.pages))),bibliography_targets=len(expected_bib),citation_links_verified=len(citation_links),index_page_links_verified=len(index_links),index_terminal_entries_verified=len(expected),all_internal_destinations_resolve=True,words_outside_paper=outside,minimum_header_body_gap_mm=round(min(hg),1),minimum_body_footer_gap_mm=round(min(fg),1),figure_placements_verified=len(figures),font_clamped_figures=clamps,detail_pages=sorted(detail),overview_sheets=sheets,citation_links=citation_links,index_links=index_links)
(WORK/'pdf-analysis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items()if k not in ['chapters','citation_links','index_links','overview_sheets']},ensure_ascii=False))
