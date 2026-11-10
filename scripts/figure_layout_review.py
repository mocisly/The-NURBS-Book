"""Build physical-size figure proofs; geometric scaling keeps TeX labels unchanged."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/'tmp/figure-layout'
PYTHON_FILES=sorted((ROOT/'image_tex').glob('ch*/*.tex'))

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare():
    BUILD.mkdir(parents=True,exist_ok=True)
    assert not (BUILD/'baseline.json').exists(),'Keep the original baseline; do not prepare again after editing.'
    sources=[ROOT/'main.tex']+list((ROOT/'chapter').glob('*.tex'))+PYTHON_FILES+[ROOT/'image_tex/common.tex']
    baseline=dict(source_hashes={p.relative_to(ROOT).as_posix():digest(p)for p in sources},
        minted={p.name:re.findall(r'\\begin\{minted\}.*?\\end\{minted\}',p.read_text(encoding='utf-8'),re.S)for p in (ROOT/'chapter').glob('*.tex')})
    (BUILD/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copyfile(ROOT/'chapter/1.tex',BUILD/'chapter-1-before.tex')
    entries=[]
    for p in PYTHON_FILES:
        s=p.read_text(encoding='utf-8');clean=re.sub(r'%[^\n]*','',s)
        panels=len(set(re.findall(r'\{\(([a-h])\)\}',clean)))
        nodes=len(re.findall(r'\\node\b|node\[',clean))
        spatial=bool(re.search(r'\\addplot3|z=|\\mathbf\s*[NS]|\\mathbf\s*\{[NS]\}|surface|曲面',s))
        dense=nodes>25 or '\\begin{tabular}'in s
        if panels>1:kind='multiple panels';w,h=6.0*min(panels,3),6.0
        elif dense:kind='dense labels / diagram';w,h=9.5,7.5
        elif '\\begin{axis}'in s or '\\begin{groupplot}'in s:kind='function plot';w,h=6.5,5.5
        elif spatial:kind='spatial geometry';w,h=7.0,6.0
        else:kind='single geometry';w,h=5.0,4.5
        path=p.relative_to(ROOT/'image_tex').as_posix()
        if path in ['ch01/fig_1_01.tex','ch01/fig_1_02.tex']:kind='reference size';w,h=99,99
        if path.startswith('ch13/'):kind='data structure';w,h=9.5,7.5
        entries.append(dict(path=path,kind=kind,target_width_cm=w,target_height_cm=h,panels=panels,nodes=nodes))
    (BUILD/'profiles.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Prepared {len(entries)} individual profiles and source baseline.')

def catalogue(paths=None,name=None):
    BUILD.mkdir(parents=True,exist_ok=True)
    profiles=BUILD/'profiles.json'
    if not profiles.exists():profiles=ROOT/'image_tex/reports/figure-layout-profiles.json'
    entries=json.loads(profiles.read_text(encoding='utf-8'))
    if paths:entries=[e for e in entries if e['path']in paths]
    preamble=(ROOT/'main.tex').read_text(encoding='utf-8').split(r'\begin{document}')[0]
    # Proof sheets have the same 11pt body and 10pt labels as the book.
    paper=r'\geometry{paperwidth=340mm,paperheight=230mm,margin=8mm,noheadfoot}'if any(e.get('min_scale',0)>=1 and e['path'].startswith('ch13/')for e in entries)else r'\geometry{paperwidth=210mm,paperheight=190mm,margin=8mm,noheadfoot}'
    tex=preamble+'\n'+paper+'\n'
    tex+=r'''
\newsavebox{\NaturalFigure}
\newsavebox{\SizedFigure}
\makeatletter
\newcommand{\ProofFigure}[4]{%
\def\BookGeometryScale{1}\def\BookAxisInverseScale{1}%
\sbox{\NaturalFigure}{\input{image_tex/#1}}%
\pgfmathsetmacro{\FigureScale}{max(#4,min(1,(#2-.4)*28.45274/(\strip@pt\wd\NaturalFigure),(#3-.3)*28.45274/(\strip@pt\dimexpr\ht\NaturalFigure+\dp\NaturalFigure\relax)))}%
\ifnum\pdfstrcmp{#1}{ch01/fig_1_01.tex}=0\def\FigureScale{1}\fi
\ifnum\pdfstrcmp{#1}{ch01/fig_1_02.tex}=0\def\FigureScale{1}\fi
\let\BookGeometryScale\FigureScale
\pgfmathsetmacro{\BookAxisInverseScale}{1/\FigureScale}%
\sbox{\SizedFigure}{\input{image_tex/#1}}%
\typeout{FIGSIZE|#1|\FigureScale|\the\wd\NaturalFigure|\the\dimexpr\ht\NaturalFigure+\dp\NaturalFigure\relax|\the\wd\SizedFigure|\the\dimexpr\ht\SizedFigure+\dp\SizedFigure\relax}%
\noindent\texttt{\detokenize{#1}}\par
正文比例参照：曲线的位置、方向和控制点应当清晰。\par\medskip
\begin{center}\usebox{\SizedFigure}\end{center}
图示标注保持原字号；仅调整几何坐标尺度。\par\clearpage
}
\makeatother
\begin{document}\pagestyle{empty}
'''
    for e in entries:tex+=f"\\ProofFigure{{{e['path']}}}{{{e['target_width_cm']}}}{{{e['target_height_cm']}}}{{{e.get('min_scale',0)}}}\n"
    tex+='\\end{document}\n'
    name=name or ('sample'if paths else'catalogue')
    (BUILD/f'{name}.tex').write_text(tex,encoding='utf-8')
    with (BUILD/f'{name}.console.txt').open('w',encoding='utf-8')as log:
        p=subprocess.run(['xelatex','-shell-escape','-interaction=nonstopmode','-halt-on-error',f'-output-directory={BUILD}',str(BUILD/f'{name}.tex')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    assert p.returncode==0,f'See {BUILD/name}.console.txt'
    log=(BUILD/f'{name}.log').read_text(encoding='utf-8',errors='replace')
    # TeX wraps long typeout lines; normalize just this structured record.
    records=[]
    for m in re.finditer(r'FIGSIZE\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([\d.p\s]+t)',log):
        path,scale,*dims=m.groups()
        values=[float(re.sub(r'\s','',d).replace('pt',''))for d in dims]
        records.append(dict(path=path.strip(),scale=float(scale),natural_width_pt=values[0],natural_height_pt=values[1],width_pt=values[2],height_pt=values[3]))
    assert len(records)==len(entries),(len(records),len(entries))
    (BUILD/f'{name}.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    print(f'{name}: {len(records)} proofs compiled.',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','catalogue']);p.add_argument('paths',nargs='*');p.add_argument('--name');a=p.parse_args()
    if a.action=='prepare':prepare()
    else:catalogue(a.paths,a.name)
