"""Group a reviewed native figure with its caption, optionally by its explanation."""
from pathlib import Path
import argparse,json,re

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--tex',required=True,help='Source path relative to image_tex')
p.add_argument('--figure',required=True,help='Printed figure number')
p.add_argument('--before',help='Unique literal anchor before which to place the group')
p.add_argument('--width',default='14cm')
a=p.parse_args();root=Path(__file__).resolve().parents[1]
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entry=next(e for e in data['images'] if e['tex']=='image_tex/'+a.tex)
assert entry.get('applied')
path=root/entry['chapter_file'];text=path.read_text(encoding='utf-8');ref=entry['replacement']
assert text.count(ref)==1
start=text.index('\\begin{center}\n'+ref)
caption=re.search(r'(?m)^图\s*'+re.escape(a.figure)+r'[.。].*$',text[start:])
assert caption
caption_start=start+caption.start();end=start+caption.end()
assert r'\BookFigure' not in text[start+len('\\begin{center}\n'+ref):caption_start]
caption_text=re.sub(r'^图\s*'+re.escape(a.figure)+r'[.。]\s*','图 '+a.figure+'. ',caption.group())
text=text[:start]+text[end:]
block=('\\begin{center}\n\\begin{minipage}{'+a.width+'}\n'+
       '\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n'+caption_text+'\n\\end{minipage}\n\\end{center}\n\n')
if a.before:
    assert text.count(a.before)==1
    pos=text.index(a.before)
else: pos=start
text=text[:pos]+block+text[pos:]
assert text.count(ref)==1
path.write_text(text,encoding='utf-8')
print(f'Placed Fig{a.figure} in {entry["chapter_file"]}, width{a.width}, caption normalized.')
