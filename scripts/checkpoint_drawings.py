"""Persist honest progress for the continuous, figure-by-figure redraw task."""
import argparse
import json
import re
from pathlib import Path
import image_tex as pipeline


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--layout',nargs='*',default=[],help='Sources whose current chapter layout was visually checked')
    parser.add_argument('--page',type=int)
    parser.add_argument('--evidence',help='Actually inspected PNG, relative to repository')
    parser.add_argument('--working',default='')
    args=parser.parse_args()
    data=pipeline.load()
    if args.layout:
        assert args.page and args.evidence
        assert (pipeline.ROOT/args.evidence).exists()
        for target in args.layout:
            entry=next(e for e in data['images'] if e['tex']=='image_tex/'+target)
            assert entry['applied']
            assert entry['compiled']==entry['reviewed']==pipeline.signature(entry)
            entry['layout_review']={
                'chapter_pdf':f"image_tex/build/chapter-review/chapter-{entry['chapter']}.pdf",
                'pdf_page':args.page,'source_signature':pipeline.signature(entry),
                'evidence':args.evidence,
                'note':'Visually checked in actual chapter geometry: font, label clearance, explanation, caption and pagination.'}
        pipeline.save(data)
    pending=[e for e in data['images'] if e['kind']!='unused' and not e.get('applied')]
    unused=[e for e in data['images'] if e['kind']=='unused' and not (pipeline.ROOT/e['tex']).exists()]
    validation=json.loads((pipeline.BASE/'validation.json').read_text(encoding='utf-8'))
    progress={
        'status':'active','instruction':'Continue until every image is natively redrawn; never use contour tracing.',
        'applied_drawings':sum(bool(e.get('applied')) for e in data['images']),
        'authored_sources':sum((pipeline.ROOT/e['tex']).exists() for e in data['images']),
        'remaining_active_original_images':len(pending),'remaining_unused_sources':len(unused),
        'remaining_inline_ocr_image_placeholders':sum(len(re.findall(r'<img\s',p.read_text(encoding='utf-8'))) for p in (pipeline.ROOT/'chapter').glob('*.tex')),
        'work_in_progress':args.working,
        'next_original':{k:pending[0][k] for k in ['tex','image','chapter_file']} if pending else None,
        'last_complete_book_compile':validation.get('book_compile'),
        'note':'Counts are live. The root PDF is only replaced after a successful full-book compile and visual review.'}
    (pipeline.BASE/'progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(progress,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
