"""Check listing coverage, preserved figures and restored C syntax (not library behavior)."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/minted-review'
if not (WORK/'before').exists():
    published=ROOT/'image_tex/reports/backmatter-compile.json'
    if not published.exists():published=ROOT/'image_tex/reports/figure-layout-compile.json'
    if not published.exists():published=ROOT/'image_tex/reports/a1-layout-compile.json'
    if not published.exists():published=ROOT/'image_tex/reports/code-listings-compile.json'
    assert published.exists(),'No migration baseline or archived publication report; regenerate review evidence first'
    previous=json.loads(published.read_text(encoding='utf-8'))
    assert all((ROOT/p).exists()and hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in previous['source_hashes'].items()),'Sources have changed since publication; regenerate chapter, source and visual checks before publishing'
    print('Current sources match the archived 109-listing / 61-algorithm publication checks.')
    raise SystemExit(0)
inventory=json.loads((WORK/'inventory.json').read_text(encoding='utf-8'))
assert len(inventory)==109
algorithms=[r for r in inventory if r.get('kind')=='pseudocode'];assert len(algorithms)==61
counts={};figures=0
for number in range(1,14):
    source=(ROOT/f'chapter/{number}.tex').read_text(encoding='utf-8')
    before=(WORK/f'before/{number}.tex').read_text(encoding='utf-8')
    old=re.findall(r'\\BookFigure[^\n]+',before);new=re.findall(r'\\BookFigure[^\n]+',source)
    assert old==new,number;figures+=len(new)
    assert re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',before,re.S)==re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',source,re.S),number
    blocks=list(re.finditer(r'\\begin\{minted\}(?:\[[^\]]*\])?\{([^}]+)\}\n(.*?)\\end\{minted\}',source,re.S))
    assert len(blocks)==source.count(r'\begin{minted}')==source.count(r'\end{minted}'),number
    counts[str(number)]=len(blocks)
    for block in blocks:
        assert not any('@'in m[0]for m in re.finditer(r'/\*.*?\*/',block[2],re.S)),(number,'Unprocessed escape in comment')
        comments=list(re.finditer(r'/\*.*?\*/',block[2],re.S))
        assert all(m[0].count('/*')==1 for m in comments),(number,'Nested/missing comment delimiter')
        assert len(comments)==block[2].count('/*')==block[2].count('*/'),(number,'Unbalanced comment delimiters')
        plain=re.sub(r'@[^@]*@|\$[^$]*\$','',block[2])
        assert not re.search(r'\\(?:hspace|HRule|section|mathrm|operatorname|begin)',plain),(number,plain[:100])
        if number!=13:assert plain.count('{')==plain.count('}'),number
    if number==13:
        outside=re.sub(r'\\begin\{minted\}.*?\\end\{minted\}','',source,flags=re.S)
        assert not re.search(r'typedef|\\#(?:define|include)|\\HRule',outside)

checkdir=WORK/'c-syntax';checkdir.mkdir(exist_ok=True)
listings=WORK/'listings'
read=lambda name:(listings/f'13-{name}.c').read_text(encoding='utf-8')
header='#ifndef BOOK_SYNTAX_STUB\n#define BOOK_SYNTAX_STUB\n#include <stdio.h>\n#include <stdlib.h>\n#include <float.h>\n#include <limits.h>\n#define VOID void\n#define LEFT 0\n'
for name in ['scalar-types','numeric-limits','sentinels','point-records','polygon-knot-records','curve-record','net-record','surface-record','allocation-node-records','error-record']:
    header+=read(name)+'\n'
for name in ['I1DNODE','I2DNODE','R1DNODE','R2DNODE','KNTNODE']:
    header+=f'typedef struct {name} {{ void *ptr; struct {name} *next; }} {name};\n'
header+='typedef struct { I1DNODE *i1d; I2DNODE *i2d; R1DNODE *r1d; R2DNODE *r2d; C1DNODE *c1d; C2DNODE *c2d; KNTNODE *knt; } STACKS;\n'
header+='\n'.join(l for l in read('error-defines').splitlines()if l.startswith('#'))+'\nextern volatile ENODE NERR;\n'
header+='REAL *S_getr1d(); CPOINT *S_getc1d(); CPOINT *S_getcpa(); CPOLYGON *S_getpol(); KNOTVECTOR *S_getknt(); CNET *S_getnet();\n#endif\n'
(checkdir/'nurbs.h').write_text(header,encoding='utf-8');(checkdir/'globals.h').write_text('extern volatile ENODE NERR;\n',encoding='utf-8')
compiler=shutil.which('gcc');assert compiler,'GCC is required for the restored C syntax checks'
names=['S_getc2d','E_seterr','E_kntdef','E_curdef','E_curwei','E_curinp','U_makcu1','U_makp12','U_makcu3','U_maksu2','A_initcp','A_updcpt','A_euclid','N_evncur','N_evnsur','curve-driver','surface-driver']
results=[]
for name in names:
    target=checkdir/f'{name}.c';target.write_text(read(name),encoding='utf-8')
    result=subprocess.run([compiler,'-std=gnu89','-fsyntax-only','-Wno-everything','-w','-I',str(checkdir),str(target)],capture_output=True,text=True)
    results.append(dict(name=name,exit_code=result.returncode,diagnostic=result.stderr))
failed=[r for r in results if r['exit_code']]
report=dict(status='failed'if failed else'passed',total_listings=109,numbered_algorithms=61,chapter13_listings=45,supplementary_algorithm_fragments=3,chapter_counts=counts,figure_calls_unchanged=figures,c_syntax_checks=results,c_syntax_scope='17 complete routines/drivers with lightweight type declarations. Partial sketches and numbered pseudocode are not asserted to be standalone C programs; no Nlib linking or runtime tests.',formatting='minted 2.9 / monokai; language c, except text call hierarchy; Consolas and Microsoft YaHei; mathematical pseudocode retained via escapeinside/mathescape',ocr_repairs=['C tokens and escapes, pointer arrows, comments, full-width punctuation','Rejoined whole routines across printed running headers','Restored C declarations mistyped as prose and macro mistyped as a section','Restored missing/misread braces, including two spurious zero-knot cases formulas in A2.5/A3.4','A2.5 zeroth-degree support test restored from its indicator interval','Locally consistent NOZ/NOW sentinel spelling and case of p/s/cur/sur variables'])
(WORK/'source-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=report['status'],listings=109,algorithms=61,unchanged_figure_calls=figures,c_syntax_passed=len(results)-len(failed)),ensure_ascii=False))
for item in failed:print(item['name'],item['diagnostic'])
assert not failed
