"""Move all five5.38 control nets into the surface elevation section."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (54,55,56)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/5.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}'
    s,n=re.subn(pat,'',s,count=1);assert n==1
s,n=re.subn(r'(?m)^图\s*5\.38\.[^\n]*\n','',s);assert n==3
old=next(line for line in s.splitlines() if line.startswith('表面度数提升的例子如图 5.38'))
new=r'图5.38a～5.38e展示同一三次$\times$二次曲面的次数提升，依次得到$(4,3)$、$(5,4)$、$(6,6)$和$(9,9)$次表示。原控制网以虚线表示，升次后的控制网以实线表示，曲面的几何形状与参数化保持不变。'
s=s.replace(old,new,1)
caption=(r'图 5.38. 同一曲面的次数提升，各面板保持同一视角与尺度，坐标采用代表性示例。'
         '\\\\\n'+r'(a)$(3,2)$次、$4\times4$控制网；(b)$(4,3)$次、$5\times6$；(c)$(5,4)$次、$6\times8$。'
         '\\\\\n'+r'(d)$(6,6)$次、$7\times12$；(e)$(9,9)$次、$10\times18$。实线和圆点表示当前控制网，虚线表示原控制网。'
         '\\\\\n'+r'原始$U=\{0,0,0,0,1,1,1,1\}$、$V=\{0,0,0,1/2,1,1,1\}$，所有权重为一；两个方向分别精确升次。')
block=('\\begin{center}\n\\begin{minipage}{25.5cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+
       '\n\\par\\medskip\n'.join(e['replacement'] for e in entries)+'\n\\par\\smallskip\n'+caption+
       '\n\\end{minipage}\n\\end{center}\n\n')
anchor=r'\section{次数降低}';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Grouped all five5.38 nets before degree reduction; restored full caption and removed214OCR header with old caption.')
