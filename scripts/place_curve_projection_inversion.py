"""Place6.1 with Newton's equation and clarify stationary vs closest points."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_01.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.1\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
old=r'当 \(f\left( u\right)  = 0\) 时，从 \(\mathbf{P}\) 到 \(\mathbf{C}\left( u\right)\) 的距离最小，无论 \(\mathbf{P}\) 是否在曲线上(图 6.1a 和 6.1b)。'
new=r'距离平方在光滑曲线段内的驻点满足\(f(u)=0\)，无论\(\mathbf P\)是否在曲线上（图6.1a、6.1b）。确定最近投影点时，还须比较其他候选驻点、非光滑节点及端点的距离。'
assert s.count(old)==1;s=s.replace(old,new,1)
caption=(r'图 6.1. 同一条代表性三次曲线上的点投影与点反演。'
         '\\\\\n'+r'(a)投影连线在最近点处与切向量$\mathbf C^{\prime}(u_i)$垂直；(b)目标点$\mathbf P=\mathbf C(\bar u)$在曲线上，箭头连接目标点与当前迭代点。')
block='\\begin{center}\n\\begin{minipage}{25.2cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor='可以使用两个零容差来指示收敛:';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8');print('Placed6.1 after Newton equation6.3; clarified stationary-point condition and endpoint comparison.')
