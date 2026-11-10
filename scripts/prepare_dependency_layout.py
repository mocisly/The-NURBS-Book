"""Use natural drawing width for the two unnumbered chapter2 dependency diagrams."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('number',type=int,choices=[7,8,15,16])
p.add_argument('--place',action='store_true')
a=p.parse_args();root=Path(__file__).resolve().parents[1]
manifest=root/'image_tex/manifest.json'
data=json.loads(manifest.read_text(encoding='utf-8'))
tex=f'image_tex/ch02/fig_2_{a.number:02d}.tex'
entry=next(e for e in data['images'] if e['tex']==tex)
if not a.place:
    assert not entry.get('applied')
    entry['options']=r'max width=\linewidth'
    manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
else:
    path=root/'chapter/2.tex';text=path.read_text(encoding='utf-8')
    block='\\begin{center}\n'+entry['replacement']+'\n\\end{center}\n\\hspace*{3em}'
    assert text.count(block)==1
    caption={7:'局部支持的递推依赖；箭头指向低一次的基函数。',
             8:'单个节点跨度上的非零基函数；箭头指向受影响的高一次基函数。',
             15:'例2.3的非零基函数递推表。',
             16:'单个基函数的三角递推表。'}[a.number]
    width='12cm' if a.number==16 else '10cm'
    new='\\begin{center}\n\\begin{minipage}{'+width+'}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entry['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}'
    text=text.replace(block,new)
    text=text.replace(r'P2. \(1\;',r'P2.1 \(')
    path.write_text(text,encoding='utf-8')
