"""Keep both semantic surface conversion panels beside their explanatory example."""
import re
import image_tex as p

d=p.load()
entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch06/fig_6_{i}.tex') for i in (24,25)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.19\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='现在我们讨论将分段幂基曲线或曲面转换为B样条形式的过程。步骤如下:'
assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'
       '\\begin{minipage}{13.6cm}\\centering\n'+entries[0]['replacement']+
       '\n\\end{minipage}\\hfill\n\\begin{minipage}{13.6cm}\\centering\n'+entries[1]['replacement']+
       '\n\\end{minipage}\n\\par\\smallskip\n'
       r'图 6.19. 代表性三次 $\times$ 二次 B 样条曲面到幂基的转换。'+'\\\\\n'
       r'(a) 三个指定面片 $(0,2)$、$(1,1)$、$(2,0)$ 以交叉等参数线标出；(b) 中间面片的部分全局幂基系数向量，箭头为 $\mathbf b_{i,j}/2$。'+'\\\\\n'
       r'系数图采用独立的统一坐标比例；右上框将主图框内两支短向量的投影放大四倍。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
wrong='测试曲面是一个定义在 的度';assert wrong in s
s=s.replace(wrong,'这里采用代表性控制网格重建曲面，其次数为',1)
for e in entries:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8')
print('Placed both6.19 panels after surface conversion example, before reverse-conversion steps.')
