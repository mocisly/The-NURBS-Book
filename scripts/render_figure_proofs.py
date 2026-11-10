"""Render labeled size proofs and pack readable sheets for individual review."""
from pathlib import Path
import argparse,json,re,subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'tmp/figure-layout'
p=argparse.ArgumentParser(description=__doc__);p.add_argument('name',nargs='?',default='catalogue');a=p.parse_args()
pdf=BUILD/f'{a.name}.pdf';records=json.loads((BUILD/f'{a.name}.json').read_text(encoding='utf-8'))
assert len(PdfReader(pdf).pages)==len(records)
out=BUILD/f'{a.name}-visual';out.mkdir(exist_ok=True)
subprocess.run(['pdftotext','-bbox',str(pdf),str(out/'bbox.html')],check=True)
xml=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',(out/'bbox.html').read_text(encoding='utf-8'))
pages=ET.fromstring(xml).findall('.//{*}page')
subprocess.run(['pdftoppm','-r','80','-png',str(pdf),str(out/'page')],check=True)
digits=len(str(len(records)));cards=[]
for n,(page,record)in enumerate(zip(pages,records),1):
    bottom=max(float(w.attrib['yMax'])for w in page.findall('.//{*}word'))
    im=Image.open(out/f'page-{n:0{digits}}.png').convert('RGB')
    im=im.crop((0,0,im.width,min(im.height,round(bottom*80/72)+12)))
    cards.append((record['path'],im))
sheets=[]
for start in range(0,len(cards),9):
    chunk=cards[start:start+9];w=max(im.width for _,im in chunk)
    heights=[max(im.height for _,im in chunk[i:i+3])+24 for i in range(0,len(chunk),3)]
    sheet=Image.new('RGB',(3*w,sum(heights)),'#303030');draw=ImageDraw.Draw(sheet)
    y=0
    for row,h in enumerate(heights):
        for col in range(3):
            i=row*3+col
            if i>=len(chunk):break
            name,im=chunk[i];x=col*w
            draw.text((x+8,y+4),f'{start+i+1}: {name}',fill='white')
            sheet.paste(im,(x,y+24))
        y+=h
    path=out/f'sheet-{len(sheets)+1:02}.png';sheet.save(path)
    sheets.append(dict(file=path.relative_to(ROOT).as_posix(),figures=[name for name,_ in chunk]))
(out/'sheets.json').write_text(json.dumps(sheets,indent=2)+'\n',encoding='utf-8')
print(f'{len(records)} labeled figures in {len(sheets)} sheets.')
