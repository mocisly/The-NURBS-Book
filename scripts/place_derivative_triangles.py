"""Restore the four derivative tables around the misplaced k=1 image."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1];path=root/'chapter/2.tex'
text=path.read_text(encoding='utf-8')
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entry=next(e for e in data['images'] if e['tex']=='image_tex/ch02/fig_2_17.tex')
assert entry.get('applied')
anchor=(r'\section*{76 B-样条基函数}' if r'\section*{76 B-样条基函数}' in text
        else '使用三角表，我们必须计算以下四种情形。')
assert text.count(anchor)==1
start=text.index(anchor)
end=text.index('用语言描述，该算法为:',start)
old=text[start:end]
assert old.count(entry['replacement'])==1
backup=root/'image_tex/build/derivative-triangles-before-layout.tex'
if not backup.exists(): backup.write_text(old,encoding='utf-8')

def array(k):
    steps=3 if k==0 else k
    base=0 if k==0 else 3-k
    cells=[['']*(steps+1) for _ in range(2*steps+1)]
    for col in range(steps+1):
        for row in range(steps-col+1):
            index='i' if not row else f'i+{row}'
            label=f'N_{{{index},{base+col}}}'
            if k and col: label+=f'^{{({col})}}'
            cells[2*row+col][col]=label
    return (r'\('+'\n'+r'\begin{array}{'+'c'*(steps+1)+'}\n'+
            '\\\\\n'.join(' & '.join(row) for row in cells)+
            '\n'+r'\end{array}'+'\n'+r'\)')

def panel(k):
    body=entry['replacement'] if k==1 else array(k)
    return (r'\begin{minipage}[t]{10cm}'+'\n'+r'\vspace{0pt}\centering\small'+'\n'+
            f'\\(k={k}\\)\\par\\smallskip\n'+body+'\n'+r'\end{minipage}')

block=('使用三角表，我们必须计算以下四种情形。每一列由前一列通过相应递推式得到。\n\n'+
       r'\begin{center}'+'\n'+r'\begin{minipage}{24cm}'+'\n'+r'\vspace*{.6\baselineskip}\centering'+'\n'+
       panel(0)+'\n'+r'\hspace{1cm}'+'\n'+panel(1)+'\n'+
       r'\par\medskip'+'\n'+panel(2)+'\n'+r'\hspace{1cm}'+'\n'+panel(3)+'\n'+
       r'\par\smallskip'+'\n'+'三次基函数的各阶导数递推表。\n'+
       r'\end{minipage}'+'\n'+r'\end{center}'+'\n\n')
assert block.count(entry['replacement'])==1
path.write_text(text[:start]+block+text[end:],encoding='utf-8')
print('Restored k=0,1,2,3 table order and aligned indices.')
