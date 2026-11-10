"""Publish a successful book build only after the affected final pages are reviewed."""
import argparse,hashlib,json,re,shutil,subprocess
from datetime import date
from pathlib import Path
from pypdf import PdfReader
import image_tex as pipeline
from verified_pdf_publication import publish_pdf


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch',type=Path,help='JSON with figures->source paths and inspected_pages->PNG evidence')
    args=parser.parse_args(); root=pipeline.ROOT; build=root/'image_tex/build/book-check'
    batch=json.loads(args.batch.read_text(encoding='utf-8'))
    result=json.loads((root/'image_tex/build/book-check-result.json').read_text(encoding='utf-8-sig'))
    assert result['exitCode']==0 and result['pdfExists']
    pdf=build/'main.pdf'; digest=hashlib.sha256(pdf.read_bytes()).hexdigest()
    subprocess.run(['pdftotext','-layout',str(pdf),str(build/'main-layout.txt')],check=True)
    pages=(build/'main-layout.txt').read_text(encoding='utf-8').split('\f')
    data=pipeline.load(); figure_pages={};book_data=data;book_root=root
    if batch.get('source_snapshot'):
        book_root=(root/batch['source_snapshot']).resolve();assert root.resolve() in book_root.parents
        metadata=json.loads((book_root/'snapshot.json').read_text(encoding='utf-8'))
        assert metadata['batch_id']==batch['id']
        manifest=book_root/'image_tex/manifest.json'
        assert hashlib.sha256(manifest.read_bytes()).hexdigest()==metadata['manifest_sha256']
        for relative,expected in metadata['input_sha256'].items():
            assert hashlib.sha256((book_root/relative).read_bytes()).hexdigest()==expected,relative
        commands=[token for attempt in result['attempts'] for token in attempt.get('command',[])]
        assert any(token.lower().endswith('main.tex') and Path(token).resolve()==book_root/'main.tex' for token in commands)
        assert pdf.stat().st_mtime>=(book_root/'snapshot.json').stat().st_mtime
        book_data=json.loads(manifest.read_text(encoding='utf-8'))
    regions=[(key,value,False) for key,value in batch['figures'].items()]
    regions += [(key,value,True) for key,value in batch.get('text_regions',{}).items()]
    for figure,sources,is_text in regions:
        if is_text:
            matches=[i+1 for i,page in enumerate(pages) if re.sub(r'\s+','',figure) in re.sub(r'\s+','',page)]
        else:
            matches=[i+1 for i,page in enumerate(pages) if any(re.match(r'^\s*图\s*'+re.escape(figure)+r'\.',line) for line in page.splitlines())]
        assert len(matches)==1,(figure,matches)
        number=matches[0]; figure_pages[figure]=number
        evidence=root/batch['inspected_pages'][str(number)]
        assert evidence.exists() and evidence.stat().st_mtime>=pdf.stat().st_mtime, evidence
        for path in sources:
            entry=next(e for e in data['images'] if e['tex']=='image_tex/'+path)
            assert entry['applied'] and entry['compiled']==entry['reviewed']==pipeline.signature(entry)
            if book_data is not data:
                frozen=next(e for e in book_data['images'] if e['tex']==entry['tex'])
                assert frozen['applied'] and frozen['reviewed']==entry['reviewed'],path
            assert entry.get('layout_review'),path
            assert entry['layout_review']['source_signature']==pipeline.signature(entry),path
            entry['layout_review'].update(book_pdf='main.pdf',book_page=number,book_sha256=digest,
                                          final_page_evidence=str(evidence.relative_to(root)).replace('\\','/'))
    previous=pipeline.BASE/'validation.json'
    archive=root/'image_tex/build'/('validation-before-'+batch['id']+'.json')
    if not archive.exists(): shutil.copy2(previous,archive)
    old=json.loads(previous.read_text(encoding='utf-8'))
    summary={
        'date':date.today().isoformat(),'policy':'semantic TikZ/PGFPlots only; no contour tracing',
        'withdrawn_contour_sources':425,
        'authored_sources':sum((book_root/e['tex']).exists() for e in book_data['images']),
        'applied_drawings':sum(bool(e.get('applied')) for e in book_data['images']),
        'remaining_active_original_images':sum(e['kind']!='unused' and not e.get('applied') for e in book_data['images']),
        'unused_original_images':sum(e['kind']=='unused' for e in book_data['images']),
        'new_figures':list(batch['figures']),
        'reviewed_text_regions':list(batch.get('text_regions',{})),
        'new_sources':sum(bool(e.get('applied')) for e in book_data['images'])-old.get('applied_drawings',0),
        'reviewed_sources':sum(len(value) for _,value,_ in regions),
        'figure_pages':figure_pages,'next_figure':batch['next_figure'],
        'book_compile':{'exit_code':0,'pages':len(PdfReader(pdf).pages),'pdf':'main.pdf','sha256':digest},
        'previous_validation':str(archive.relative_to(root)).replace('\\','/'),
        'previous_contour_report':old.get('previous_contour_report'),
        'geometry_note':batch.get('geometry_note',''),
        'page_layout':'All listed figures independently previewed and checked in chapters and final book pages.',
    }
    if batch.get('source_snapshot'):
        summary.update(source_snapshot=batch['source_snapshot'],snapshot_inputs_verified=True,
                       live_applied_drawings_at_publication=sum(bool(e.get('applied')) for e in data['images']))
    if batch.get('geometry_report'):
        summary['geometry_check']=json.loads((root/batch['geometry_report']).read_text(encoding='utf-8'))
    # Editor builds may be writing main.pdf and its auxiliary files concurrently.
    # Keep isolated compiler logs in build; replace only the reviewed PDF atomically.
    publish_pdf(pdf,root/'main.pdf',digest)
    assert hashlib.sha256((root/'main.pdf').read_bytes()).hexdigest()==digest
    pipeline.save(data)
    previous.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
