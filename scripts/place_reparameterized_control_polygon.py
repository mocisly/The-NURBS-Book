"""Put6.10 after all five new controls have been derived."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_10.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.10\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='因此，重新参数化一个没有内部节点的';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.10. 例 Ex6.6 中二次抛物线重参数化后的四次 B 样条表示。\\\\\n'
       r'虚线多边形连接原控制点 $\mathbf P_i$，实线连接新控制点 $\mathbf Q_i$；$+$ 为 $u=i/20$，$\square$ 为 $s=i/20$ 的曲线点。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(ref)==1;f.write_text(s,encoding='utf-8')
print('Grouped6.10 after the final Q2 derivation, with both parameter marker meanings explicit.')
