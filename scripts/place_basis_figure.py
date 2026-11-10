"""Move a reviewed basis diagram next to the relevant formula block."""
from pathlib import Path
import argparse
import json

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('number',type=int)
p.add_argument('anchor',help='Unique literal anchor before which to place the diagram')
p.add_argument('--width',default='16cm')
p.add_argument('--caption-number',type=int)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
path=root/'chapter/2.tex'
text=path.read_text(encoding='utf-8')
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entry=next(e for e in manifest['images'] if e['tex']==f'image_tex/ch02/fig_2_{a.number:02d}.tex')
assert entry.get('applied')
ref=entry['replacement']
start=text.index('\\begin{center}\n'+ref)
caption_number=a.caption_number or a.number
caption=text.index(f'图 2.{caption_number}',start)
end=text.index('\n',caption)
caption_text=text[caption:end].replace(f'图 2.{a.number}。',f'图 2.{a.number}.')
if a.number==4:
    caption_text+=' 实心端点取值为 1，空心端点不包含；图中省略取值为零的部分。'
text=text[:start]+text[end:]
text=text.replace('54 B 样条基函数\n','')
text=text.replace('60 B样条基函数\n','')
block=('\\begin{center}\n\\begin{minipage}{'+a.width+'}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n'+caption_text+'\n\\end{minipage}\n\\end{center}\n\n')
section=text.index('Ex2.2')
assert text[section:].count(a.anchor)==1
pos=text.index(a.anchor,section)
text=text[:pos]+block+text[pos:]
path.write_text(text,encoding='utf-8')
