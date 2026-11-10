"""Align OCR-fragmented recurrence tables and group the existing Fig2.3 caption."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1];path=root/'chapter/2.tex'
text=path.read_text(encoding='utf-8')

def replace_table(anchor,end_anchor,body,backup):
    global text
    pos=text.index(anchor);start=text.index(r'\[',pos);end=text.index(end_anchor,start)
    old=text[start:end]
    assert r'\BookFigure' not in old and r'\includegraphics' not in old
    out=root/'image_tex/build'/backup
    if not out.exists(): out.write_text(old,encoding='utf-8')
    text=text[:start]+body+'\n\n'+text[end:]

first=r'''\begin{center}
\small
\(\begin{array}{cccc}
N_{0,0} & & & \\
 & N_{0,1} & & \\
N_{1,0} & & N_{0,2} & \\
 & N_{1,1} & & N_{0,3} \\
N_{2,0} & & N_{1,2} & \\
 & N_{2,1} & & N_{1,3} \\
N_{3,0} & & N_{2,2} & \\
 & N_{3,1} & & \\
N_{4,0} & & & \\
\vdots & \vdots & \vdots & \vdots
\end{array}\)
\par\smallskip
不同次数基函数的递推排列。
\end{center}'''
replace_table('计算 \\(p\\) 度的函数会生成一个截断的三角形表', '为了简洁',first,'definition-table-before-layout.tex')
second=r'''\begin{center}
\small
\(\begin{array}{cccc}
 & & & N_{i-p,p} \\
 & N_{i-1,1} & \cdots & \vdots \\
N_{i,0} & & \cdots & \vdots \\
 & N_{i,1} & \ddots & \vdots \\
 & & & N_{i,p}
\end{array}\)
\par\smallskip
非零基函数的反三角递推排列。
\end{center}'''
replace_table('现在我们来解决第二个算法',r'\section*{示例}',second,'nonzero-table-before-layout.tex')
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entry=next(e for e in data['images'] if e['tex']=='image_tex/ch02/fig_2_03.tex')
ref=entry['replacement'];start=text.index('\\begin{center}\n'+ref)
caption=text.index('图 2.3.',start);end=text.index('\n',caption)
caption_text=text[caption:end]
block='\\begin{center}\n\\begin{minipage}{18cm}\n\\centering\n'+ref+'\n\\par\\smallskip\n'+caption_text+'\n\\end{minipage}\n\\end{center}'
text=text[:start]+block+text[end:]
assert text.count(ref)==1
path.write_text(text,encoding='utf-8')
print('Compacted two recurrence arrays; centered existing Fig2.3 caption.')
