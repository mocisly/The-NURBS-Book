"""Compile the minted book in isolation; publish only after explicit visual review records."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/minted-review';BUILD=WORK/'full'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def inputs():
    paths=[ROOT/'main.tex']
    for folder in ['chapter','cover','colophon','introduction','preface','image_tex','backmatter']:
        paths.extend(p for p in (ROOT/folder).rglob('*')if p.is_file()and (p.suffix in ['.tex','.eps']or(folder=='backmatter'and p.suffix in ['.json','.ist']))and not any(t in p.relative_to(ROOT).parts for t in ['build','reports','backups']))
    paths.extend(p for p in [ROOT/'.latexmkrc',ROOT/'make.bat',ROOT/'Makefile']if p.exists())
    return {p.relative_to(ROOT).as_posix():digest(p)for p in sorted(set(paths))}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--publish',action='store_true');args=parser.parse_args()
    result_path=WORK/'full-compile.json'
    if not args.publish:
        BUILD.mkdir(parents=True,exist_ok=True)
        before=inputs();wrapper=BUILD/'entry.tex'
        wrapper.write_text(r'\PassOptionsToPackage{outputdir=tmp/minted-review/full}{minted}'+'\n'+r'\input{main.tex}'+'\n',encoding='utf-8')
        compiler=shutil.which('latexmk');assert compiler
        command=[compiler,'-norc','-r',str(ROOT/'.latexmkrc'),'-xelatex','-shell-escape','-interaction=nonstopmode','-halt-on-error','-synctex=1','-jobname=main',f'-outdir={BUILD}',str(wrapper)]
        with (BUILD/'console.txt').open('w',encoding='utf-8')as log:
            process=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
        report=dict(exit_code=process.returncode,command=command,source_hashes=before,source_inputs_unchanged=(before==inputs()))
        result_path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        assert process.returncode==0,'See tmp/minted-review/full/console.txt'
        assert report['source_inputs_unchanged'],'Sources changed while compilation was running; compile again'
        pdf=BUILD/'main.pdf';reader=PdfReader(pdf);log=(BUILD/'main.log').read_text(encoding='utf-8',errors='replace')
        missing=[l for l in log.splitlines()if l.startswith('Missing character:')]
        fatal=[l for l in log.splitlines()if l.startswith('!')or'Undefined control sequence'in l or'LaTeX Error:'in l or'Package minted Error:'in l]
        assert not missing and not fatal,(missing,fatal)
        used_cache=set()
        for line in (BUILD/'main.fls').read_text(encoding='utf-8',errors='replace').splitlines():
            if line.startswith('INPUT ')and line.endswith('.pygtex'):
                path=Path(line[6:]);path=path if path.is_absolute()else ROOT/path
                used_cache.add(path.resolve())
        assert used_cache,'No minted listings were included'
        lexer_errors=[str(p)for p in used_cache if r'\PYG{err}'in p.read_text(encoding='utf-8')]
        assert not lexer_errors,('Pygments error tokens in final PDF',lexer_errors)
        for page in reader.pages:assert abs(float(page.mediabox.width)-594/25.4*72)<.1 and abs(float(page.mediabox.height)-841/25.4*72)<.1
        subprocess.run(['pdftotext','-layout',str(pdf),str(BUILD/'main-layout.txt')],check=True)
        text=(BUILD/'main-layout.txt').read_text(encoding='utf-8')
        found=re.findall(r'算法\s+(A\d+\.\d+)\s*[（(]伪代码',text)
        expected=[f'A{n}.{i}'for n,c in enumerate([0,7,5,8,4,11,2,3,2,12,4,1,2])if n for i in range(1,c+1)]
        assert sorted(found)==sorted(expected),(len(found),set(expected)-set(found))
        assert '@'not in text,'Unprocessed escape marker visible in PDF'
        report.update(status='compiled-awaiting-visual-review',pages=len(reader.pages),sha256=digest(pdf),numbered_algorithms=61,missing_glyph_warnings=0,fatal_errors=0,lexer_error_spans=0,used_highlight_cache_files=len(used_cache),overfull_hbox_warnings=log.count('Overfull \\hbox'),geometry_cm=[59.4,84.1])
        result_path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in report.items()if k not in ['source_hashes','command']},ensure_ascii=False))
    else:
        report=json.loads(result_path.read_text(encoding='utf-8'));assert report['exit_code']==0 and report['source_inputs_unchanged']
        assert report['source_hashes']==inputs()and report['sha256']==digest(BUILD/'main.pdf')
        review=json.loads((WORK/'visual-review.json').read_text(encoding='utf-8'))
        assert review['status']=='passed'and review['final_pdf_sha256']==report['sha256']
        assert set(review['chapters_reviewed'])==set(range(1,14))
        source=json.loads((WORK/'source-check.json').read_text(encoding='utf-8'));assert source['status']=='passed'
        staged=ROOT/'main.pdf.new';shutil.copyfile(BUILD/'main.pdf',staged);os.replace(staged,ROOT/'main.pdf')
        assert digest(ROOT/'main.pdf')==report['sha256']
        report['status']='published-and-verified'
        archive=ROOT/'image_tex/reports';archive.mkdir(exist_ok=True)
        for name in ['source-check.json','inventory.json','visual-review.json','lexer-check.json','chapters-compiled.json']:
            shutil.copyfile(WORK/name,archive/f'code-listings-{name}')
        (archive/'code-listings-compile.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        # Update live summaries; earlier image-only reports remain historical.
        for filename in ['progress.json','validation.json']:
            path=ROOT/'image_tex'/filename;data=json.loads(path.read_text(encoding='utf-8'))
            key='last_complete_book_compile'if filename=='progress.json'else'book_compile'
            if 'image_redraw_book_compile'not in data:data['image_redraw_book_compile']=data.get(key)
            data[key]=dict(exit_code=0,pages=report['pages'],pdf='main.pdf',sha256=report['sha256'])
            data['latest_code_listing_validation']='image_tex/reports/code-listings-compile.json'
            data['final_validation']='image_tex/reports/code-listings-compile.json'
            data['validation_note']='Image redraw snapshot and layout records are historical. Latest code, chapter and whole-book checks are in reports/code-listings-*.json.'
            if filename=='progress.json':data['work_in_progress']='Complete: 435 native image replacements and 109 minted listings; final book compiled, visually reviewed and published.'
            path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        path=ROOT/'image_tex/README.md';text=path.read_text(encoding='utf-8')
        text=re.sub(r'共\d+页；SHA256为`[0-9a-f]{64}`',f"共{report['pages']}页；SHA256为`{report['sha256']}`",text)
        if '## 代码排版更新'not in text:text+='\n## 代码排版更新\n\n全书109段代码和算法草图已改用minted/monokai，其中61段为编号算法，第13章45段为C代码及调用层次示例。最新整书编译、源码和版面检查见`reports/code-listings-*.json`；此前final开头的图片报告记录的是代码排版修改前的历史版本。\n'
        path.write_text(text,encoding='utf-8')
        print(f"Published {report['pages']} pages; SHA256 {report['sha256']}")

if __name__=='__main__':main()
