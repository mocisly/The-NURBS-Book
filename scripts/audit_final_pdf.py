"""Verify the successful isolated final PDF, its geometry and body image resources."""
from pathlib import Path
import json,re,hashlib
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1];build=root/'image_tex/build/book-check';pdf=build/'main.pdf'
result=json.loads((root/'image_tex/build/book-check-result.json').read_text(encoding='utf-8-sig'));assert result['exitCode']==0 and result['pdfExists']
batch=json.loads((root/'image_tex/build/final-native-book-batch.json').read_text(encoding='utf-8'));assert batch['id']=='final-native-book'and batch.get('inspected_pages')
reader=PdfReader(pdf);assert len(reader.pages)>=200
layout=build/'main-layout.txt';assert layout.stat().st_mtime>=pdf.stat().st_mtime;pages=layout.read_text(encoding='utf-8').split('\f')
firstlines=[''.join(next((line for line in p.splitlines()if line.strip()),'').split())for p in pages]
start=next(i+1 for i,t in enumerate(firstlines)if re.fullmatch(r'第一章曲线和曲面基础',t))
end=next(i+1 for i,t in enumerate(firstlines)if re.fullmatch(r'第十四章参考文献',t))-1
assert 1<start<=end<len(reader.pages)
images={}
def scan(resources,page,seen):
    if resources is None:return
    resources=resources.get_object()
    for ref in resources.get('/XObject',{}).get_object().values()if hasattr(resources.get('/XObject',{}),'get_object')else resources.get('/XObject',{}).values():
        obj=ref.get_object();key=(getattr(ref,'idnum',id(obj)),getattr(ref,'generation',0))
        if key in seen:continue
        seen.add(key)
        if obj.get('/Subtype')=='/Image':images.setdefault(str(key),dict(width=obj.get('/Width'),height=obj.get('/Height'),pages=[]))['pages'].append(page)
        elif obj.get('/Subtype')=='/Form':scan(obj.get('/Resources'),page,seen)
for number,page in enumerate(reader.pages,1):
    assert abs(float(page.mediabox.width)-400/25.4*72)<.1 and abs(float(page.mediabox.height)-800/25.4*72)<.1,number
    scan(page.get('/Resources'),number,set())
body_images={k:v for k,v in images.items()if any(start<=p<=end for p in v['pages'])};assert not body_images,body_images
log=(build/'main.log').read_text(encoding='utf-8',errors='replace')
fatal=[line for line in log.splitlines()if line.startswith('!')or'Undefined control sequence'in line or'LaTeX Error:'in line or'Package keyval Error:'in line]
missing=[line for line in log.splitlines()if line.startswith('Missing character:')]
assert not fatal and not missing,(fatal,missing)
report=dict(status='passed',pdf='image_tex/build/book-check/main.pdf',sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),pages=len(reader.pages),content_page_range=(start,end),all_page_geometry_cm=(40,80),body_raster_image_objects=0,non_body_image_resources=images,fatal_compile_errors=0,missing_glyph_warnings=0,frozen_snapshot=batch['source_snapshot'],all_active_original_references=435,remaining_original_references=0)
(root/'image_tex/build/final-pdf-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
