"""Place5.41 after its full knot vector and before5.42."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch05/fig_5_62.tex');assert e['applied']
f=p.ROOT/'chapter/5.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.41\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
old='\\hspace*{1em} Figure 5.41 shows an example of reducing the degree from five to four. The\n\noriginal knot vector is'
assert s.count(old)==1;s=s.replace(old,'图5.41展示五次B样条曲线降为四次的代表性示例。原始节点向量为',1)
old='实线曲线为原始曲线，而虚线曲线为降低阶数后的曲线。图 5.42a 显示了在节点向量上定义的三次曲线。'
assert s.count(old)==1
caption=(r'图 5.41. 五次B样条曲线降为四次，采用代表性控制点。'
         '\\\\\n'+r'实线、圆点为原曲线及十六个控制点；虚线、方点为四次近似及十个控制点。'
         '\\\\\n'+r'各内部节点的重数由二降为一；逐段降次及局部逆插入拟合的全参数误差已在原分段Bernstein基上核算。')
block='\\begin{center}\n\\begin{minipage}{23cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(old,block+'图 5.42a 显示了在节点向量上定义的三次曲线。',1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8');print('Restored5.41 knot-vector introduction and placed the complete figure before5.42.')
