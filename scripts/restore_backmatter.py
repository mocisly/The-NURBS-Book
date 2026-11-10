"""Restore native bibliography links and generate curated, page-aware index marks."""
from pathlib import Path
import argparse,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/backmatter';DATA=ROOT/'backmatter'
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def bibliography():
    original=(WORK/'before/chapter/14.tex').read_text(encoding='utf-8')
    matches=list(re.finditer(r'^\[([A-Za-z]+\d{2}[a-z]?)\]\s*',original,re.M))
    entries=[]
    for i,m in enumerate(matches):
        end=matches[i+1].start()if i+1<len(matches)else original.index(r'\clearpage',m.end())
        entries.append(dict(key=m[1],text=original[m.end():end].strip()))
    keys={e['key']for e in entries};assert len(keys)==len(entries)==173
    changes=[]
    def citations(text,path):
        def convert(m):
            body=m[1].strip();note=''
            if body.startswith('见 '):body=body[2:];note='见 '
            if not re.search(r'[A-Za-z]+\d{2}',body):return m[0]
            if '\\'in body:return m[0]
            result=[];prefix=None
            for token in re.split(r'\s*[;,；，]\s*',body):
                full=re.fullmatch(r'([A-Za-z]+)(\d{2}[a-z]?)',token.strip())
                if full:prefix=full[1];key=token.strip()
                elif prefix and re.fullmatch(r'\d{2}[a-z]?',token.strip()):key=prefix+token.strip()
                else:raise ValueError((path,m[0],token))
                assert key in keys,(path,key,m[0]);result.append(key)
            replacement=note+r'\cite{'+','.join(result)+'}'
            changes.append(dict(path=path,before=m[0],after=replacement,keys=result))
            return replacement
        return re.sub(r'\[([^\]\n]+)\]',convert,text)
    for n in range(1,14):
        p=ROOT/f'chapter/{n}.tex';s=p.read_text(encoding='utf-8');p.write_text(citations(s,p.relative_to(ROOT).as_posix()),encoding='utf-8')
    tex='\\documentclass[../main.tex]{subfiles}\n\\begin{document}\n\\begin{BookBibliography}\n'
    for e in entries:tex+=f"\\bibitem[{e['key']}]{{{e['key']}}} "+citations(e['text'],'chapter/14.tex')+'\n\n'
    tex+='\\end{BookBibliography}\n\\end{document}\n'
    (ROOT/'chapter/14.tex').write_text(tex,encoding='utf-8')
    DATA.mkdir(exist_ok=True);save(DATA/'bibliography.json',entries);save(WORK/'citation-migration.json',changes)
    print(f'Preserved {len(entries)} bibliography entries; migrated {len(changes)} citation groups.')

def balanced_end(s,start):
    depth=0
    for i in range(start,len(s)):
        if s[i]=='{'and(i==0 or s[i-1]!='\\'):depth+=1
        elif s[i]=='}'and(i==0 or s[i-1]!='\\'):
            depth-=1
            if depth==0:return i+1
    raise ValueError('Unbalanced argument')

def index():
    entries=json.loads((DATA/'index-entries.json').read_text(encoding='utf-8'))
    sources={n:re.sub(r'\\BookIndexMark\{p\d+\}','',(ROOT/f'chapter/{n}.tex').read_text(encoding='utf-8'))for n in range(1,14)}
    points={};records=[]
    def locate(spec):
        kind,value=spec.split(':',1)
        if kind=='a':
            n=int(value.split('.')[0]);s=sources[n]
            m=re.search(r'\\textbf\{算法\s+A'+re.escape(value)+r'(?=[（(\s])',s);assert m,spec
            start=s.index('{',m.start());return n,balanced_end(s,start),m[0]
        n,needle=value.split(':',1);n=int(n);s=sources[n]
        if kind=='s':
            candidates=[]
            for m in re.finditer(r'\\(?:sub)*section\*?\{',s):
                end=balanced_end(s,m.end()-1);title=s[m.end():end-1].strip()
                if title==needle:candidates.append((end,title))
            assert len(candidates)==1,(spec,len(candidates));return n,*candidates[0]
        if kind=='f':
            m=re.search(r'\\BookFigure(?:\[[^\]]*\])?\{ch'+f'{n:02}'+r'/'+re.escape(needle)+r'\}',s);assert m,spec
            return n,m.end(),m[0]
        assert kind=='t',spec
        # Select a body occurrence, never a code token, math formula, title or diagram label.
        protected=[]
        protected.extend((m.start(),m.end())for m in re.finditer(r'(?<!\\)%[^\n]*',s))
        for pattern in [r'\\begin\{minted\}.*?\\end\{minted\}',r'\\\(.*?\\\)',r'\\\[.*?\\\]',r'\\begin\{center\}.*?\\end\{center\}',r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}']:
            protected.extend((m.start(),m.end())for m in re.finditer(pattern,s,re.S))
        for m in re.finditer(r'\\(?:sub)*section\*?\{',s):protected.append((m.start(),balanced_end(s,m.end()-1)))
        candidates=[m for m in re.finditer(re.escape(needle),s)if not any(a<=m.start()<b for a,b in protected)]
        assert candidates,('No body locator',spec)
        m=candidates[0];return n,m.end(),m[0]
    missing=[]
    for target in dict.fromkeys(t for e in entries for t in e['targets']):
        try:locate(target)
        except (AssertionError,ValueError)as error:missing.append(dict(target=target,error=str(error)))
    if missing:
        save(WORK/'index-missing-locators.json',missing)
        raise ValueError(missing)
    for e in entries:
        assert e['paths']and e['targets'],e
        # A see-reference has no printed page list: emit it once, even when
        # the source entry was associated with several relevant passages.
        for target in e['targets'][:1] if e.get('see') else e['targets']:
            n,pos,matched=locate(target);point=points.setdefault((n,pos),dict(chapter=n,offset=pos,entries=[],selectors=[],matched=matched))
            if e['id']not in point['entries']:point['entries'].append(e['id'])
            if target not in point['selectors']:point['selectors'].append(target)
    terms={e['id']:e for e in entries};definitions='% Generated from backmatter/index-entries.json by scripts/restore_backmatter.py.\n'
    sorted_points=sorted(points.values(),key=lambda p:(p['chapter'],p['offset']))
    for i,p in enumerate(sorted_points,1):
        p['id']=f'p{i:04}';s=sources[p['chapter']];pos=p['offset']
        p['line_without_marks']=s[:pos].count('\n')+1;p['context']=s[max(0,pos-100):pos+160]
        commands=[]
        for entry_id in p['entries']:
            for path in terms[entry_id]['paths']:
                assert 1<=len(path)<=3,path
                label='!'.join(f'{part[0]}@{part[1]}'for part in path)
                encap='see{'+terms[entry_id]['see']+'}'if terms[entry_id].get('see')else'hyperpage'
                commands.append(r'\index{'+label+'|'+encap+'}')
        definitions+=r'\expandafter\def\csname BookIndexPoint@'+p['id']+r'\endcsname{'+''.join(commands)+'}\n'
    for n,s in sources.items():
        for p in reversed([p for p in sorted_points if p['chapter']==n]):s=s[:p['offset']]+r'\BookIndexMark{'+p['id']+'}'+s[p['offset']:]
        (ROOT/f'chapter/{n}.tex').write_text(s,encoding='utf-8')
    (DATA/'index-marks.tex').write_text(definitions,encoding='utf-8')
    save(DATA/'index-locations.json',sorted_points)
    print(f'Generated {len(entries)} curated entries at {len(sorted_points)} source locations.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['bibliography','index']);a=p.parse_args()
    bibliography()if a.action=='bibliography'else index()
