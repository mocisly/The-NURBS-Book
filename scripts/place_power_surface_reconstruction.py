"""Keep all three6.21 surface stages and their caption as one readable group."""
import re
import image_tex as p
d=p.load();ee=[next(e for e in d['images'] if e['tex']==f'image_tex/ch06/fig_6_{i}.tex') for i in (28,29)]
assert all(e['applied'] for e in ee)
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8')
for e in ee:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.21\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\section*{练习}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'
       '\\begin{minipage}{13cm}\\centering\n'+ee[0]['replacement']+
       '\n\\end{minipage}\n\\par\\medskip\n\\begin{minipage}{26.4cm}\\centering\n'+ee[1]['replacement']+
       '\n\\end{minipage}\n\\par\\smallskip\n'
       r'图 6.21. 同一代表性三次 $\times$ 二次曲面的九面片幂基到 B 样条转换。'+'\\\\\n'
       r'(a) 九个多项式面片的边界；(b) 逆变换并拼接得到的 $10\times7$ Bézier 控制网；(c) 精确去除多余节点后的 $6\times5$ 控制网。'+'\\\\\n'
       r'实线为面片边界，虚线与圆点为控制网；三图采用同一视角与比例，曲面几何形状相同。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1).replace('278 高级几何算法\n','',1)
for e in ee:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Placed6.21 grouped native panels before exercises.')
