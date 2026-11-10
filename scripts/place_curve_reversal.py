"""Put6.16 beside curve reversal, before introducing surface reversal."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_20.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.16\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
wrong='这在图 6.16 中显示；注意参数化没有改变。';assert s.count(wrong)==1
s=s.replace(wrong,'这在图 6.16 中显示；曲线的几何形状保持不变，参数方向反转。',1)
anchor=r'设 \({\textbf{S}}^{w}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{17cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.16. 代表性三次曲线的反向：$s=1-u$，控制点次序反转，曲线形状保持不变。\\\\\n'
       '两种参数化的等步长采样点（$+$ 与 $\\square$）完全重合；箭头只表示相反的遍历方向。\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(ref)==1
f.write_text(s,encoding='utf-8');print('Placed6.16 after6.67; corrected the claim that parameterization was unchanged.')
