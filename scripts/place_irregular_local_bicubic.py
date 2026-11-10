"""Keep9.36 with the irregular-data discussion, reconnecting approximation steps."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_43.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.36\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\section{全局逼近}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.36. 分布不均匀的代表性局部双三次插值；(a) 十六个数据点，(b) 实际插值曲面。'+'\\\\\n'+
       r'数据沿用图 9.32 的阶梯高度分布，但改变各行的横向间距，局部相邻弦长的最大、最小值之比约为$11.6$；仍按算法 A9.5 计算参数、切向和混合导数。'+'\\\\\n'+
       r'全部数据被精确插值，片间保持$C^1$连续；四十一条等参数线显示不均匀数据引起的局部弯曲和间距变化。两图及图 9.32 采用相同视角与坐标尺度。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.36 after irregular-data explanation before global approximation;rejoined its steps1b/1c.')
