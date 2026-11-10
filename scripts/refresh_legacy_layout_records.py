"""Record freshly inspected chapter1 pages for the 32 early legacy review records."""
import image_tex as p
d=p.load();groups={1:range(1,5),2:range(5,9),3:range(9,17),4:range(17,25),5:range(25,28),6:(28,),7:range(29,33)}
pdf=p.BASE/'build/chapter-review/chapter-1.pdf';assert pdf.exists()
for page,indices in groups.items():
    evidence=f'image_tex/build/chapter-review/chapter1-final-{page:02d}.png';path=p.ROOT/evidence
    assert path.exists()and path.stat().st_mtime>=pdf.stat().st_mtime
    for i in indices:
        e=next(e for e in d['images']if e['tex']==f'image_tex/ch01/fig_1_{i:02d}.tex');sig=p.signature(e)
        assert e['applied']and e['compiled']==e['reviewed']==sig
        if e.get('layout_review'):e['legacy_layout_review']=e['layout_review']
        e['layout_review']=dict(chapter_pdf='image_tex/build/chapter-review/chapter-1.pdf',pdf_page=page,source_signature=sig,evidence=evidence,note='Fresh final QA: all seven actual chapter pages visually inspected, native labels, captions, surrounding explanations and pagination checked. Legacy schema refreshed without geometry changes.')
p.save(d);print('Recorded fresh visual chapter-layout evidence andcurrent signatures for32legacy sources across7actuallyinspected pages.')
