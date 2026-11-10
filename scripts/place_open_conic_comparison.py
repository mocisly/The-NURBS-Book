"""Place all7.26 panels beside their parameterization comparison."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{n}.tex') for n in (32,33)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.26\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='仍然存在完整椭圆的问题。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\vspace{.5cm}\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+
       r'图 7.26. 用算法 A7.3 构造开放圆锥弧。(a) 扫掠小于 $180^\circ$ 的两段表示；(b) 扫掠大于 $180^\circ$ 的四段表示。'+'\\\\\n'+
       r'(c) 同一条椭圆弧的两种表示：$\square$ 为分割并归一化后的采样点，$+$ 为原弧在 $u=1/2$ 处插入一次节点后的采样点。'+'\\\\\n'+
       r'两组采样均取 $u=i/20$；形状相同，参数化不同。$\mathbf Q_i$ 为四段表示的控制点，$\mathbf R_i$ 为节点插入表示的控制点。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);s,n=re.subn(r'权重和\s+节点与示例','权重和节点与示例',s,count=1);assert n==1
assert all(s.count(e['replacement'])==1 for e in entries);f.write_text(s,encoding='utf-8')
print('Grouped7.26 immediately after parameterization comparison; restored interrupted full-ellipse sentence.')
