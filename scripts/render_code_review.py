"""Render actual code pages with Poppler, plus legible crops for visual review."""
from pathlib import Path
import argparse,json,subprocess,hashlib
import pdfplumber
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/minted-review'
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('chapters',type=int,nargs='+');args=parser.parse_args()
out=WORK/'visual';out.mkdir(parents=True,exist_ok=True)
for chapter in args.chapters:
    pdf=ROOT/f'image_tex/build/chapter-review/chapter-{chapter}.pdf'
    crops=[];pages=[];segments=[];sheets=[]
    with pdfplumber.open(pdf)as doc:
        for number,page in enumerate(doc.pages,1):
            rects=[r for r in page.rects if r.get('fill')and r['width']>100 and isinstance(r.get('non_stroking_color'),(list,tuple))and len(r['non_stroking_color'])==3 and max(abs(a-b)for a,b in zip(r['non_stroking_color'],(39/255,40/255,34/255)))<.002]
            if not rects:continue
            pages.append(number);prefix=out/f'ch{chapter}-page{number}'
            subprocess.run(['pdftoppm','-f',str(number),'-singlefile','-r','105','-png',str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            full=Image.open(prefix.with_suffix('.png')).convert('RGB');scale=full.width/float(page.width)
            for index,r in enumerate(rects,1):
                chars=[c for c in page.chars if r['top']-1<=c['top']<=r['bottom']+1 and r['x0']-1<=c['x0']<=r['x1']+1]
                right=min(r['x1'],max((c['x1']for c in chars),default=r['x1'])+12)
                bbox=(int(r['x0']*scale),max(0,int((r['top']-13)*scale)),int(right*scale),min(full.height,int((r['bottom']+5)*scale)))
                crop=full.crop(bbox);segments.append(dict(page=number,segment=index,rectangle_points=[r['x0'],r['top'],r['x1'],r['bottom']],crop_pixels=list(crop.size)))
                if crop.width>1250:crop=crop.resize((1250,round(crop.height*1250/crop.width)))
                # Split tall code continuations into readable sheets without
                # shrinking text; each part remains an actual rendered crop.
                for top in range(0,crop.height,2150):
                    crops.append((number,index,crop.crop((0,top,crop.width,min(top+2150,crop.height)))))
    pending=[];height=0
    def save():
        global pending,height
        if not pending:return
        width=max(c.width for _,_,c in pending)+24;sheet=Image.new('RGB',(width,height+12),'#181818');draw=ImageDraw.Draw(sheet);y=8
        for page,segment,crop in pending:
            draw.text((10,y),f'Chapter {chapter} / page {page} / code segment {segment}',fill='#e0e0e0');y+=23
            sheet.paste(crop,(12,y));y+=crop.height+16
        path=out/f'ch{chapter}-sheet{len(sheets)+1}.png';sheet.save(path);sheets.append(str(path.relative_to(ROOT)).replace('\\','/'));pending=[];height=0
    for page,index,crop in crops:
        if height+crop.height+39>2400:save()
        pending.append((page,index,crop));height+=crop.height+39
    save()
    report=dict(chapter=chapter,pdf=str(pdf.relative_to(ROOT)).replace('\\','/'),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),code_pages=pages,segments=segments,sheets=sheets)
    (out/f'ch{chapter}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'Chapter {chapter}: {len(pages)} code pages, {len(segments)} segments, {len(sheets)} visual sheets',flush=True)
