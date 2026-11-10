"""Place5.42 after both knot vectors and clarify its derivative break."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch05/fig_5_63.tex');assert e['applied']
f=p.ROOT/'chapter/5.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.42\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
old='不可能用二次 B 样条曲线在合理的容差范围内逼近该曲线。在细化节点向量后'
assert s.count(old)==1
s=s.replace(old,r'本代表性示例采用容差$\mathrm{TOL}=0.13$。在原来的各节点区间上，任意二次近似的最大参数误差均不可能小于$\sqrt{449}/80>0.26$，因而不能满足该容差。细化节点向量为',1)
old=r'可以得到合理的近似，如图 5.42b 所示。注意 \(u = 1/2\) 处的间断。这是由于原始曲线中的三重节点。'
assert s.count(old)==1
s=s.replace(old,r'可以得到满足同一容差的二次近似，如图5.42b所示；其整个参数域上的误差不超过$7619/61440<0.125$。注意$u=1/2$处曲线位置连续，而切线不连续：细化后的三次节点向量在此处有三重节点，降次后保留二重节点，因此二次近似在此仅有$C^0$连续性。',1)
caption=(r'图 5.42. 节点细化使三次曲线可在给定容差内降为二次，采用代表性控制点，两个面板保持相同尺度。'
         '\\\\\n'+r'(a)原三次曲线及十个控制点；(b)原曲线和细化后的十九个控制点（实线、圆点），以及二次近似和十一个控制点（虚线、方点）。'
         '\\\\\n'+r'细化保持原曲线不变；近似误差在全参数域内小于$\mathrm{TOL}=0.13$，$u=1/2$处的切线不连续。')
block='\\begin{center}\n\\begin{minipage}{25.5cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor='最后，我们指出，通过将这些曲线技术应用于控制点的行或列';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
# Join5.41's knot vector after removing the scanned image that interrupted it.
old='\\[\nU = \\{ 0,0,0,0,0,0,{0.15},{0.15},{0.3},{0.3},{0.5},{0.5},\n\\]\n\n\\[\n{0.7},{0.7},{0.85},{0.85},1,1,1,1,1,1\n\\]'
new=r'\[U=\{0,0,0,0,0,0,0.15,0.15,0.3,0.3,0.5,0.5,0.7,0.7,0.85,0.85,1,1,1,1,1,1\}.\]'
assert s.count(old)==1;s=s.replace(old,new,1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8');print('Placed5.42 after refinement/error explanation; clarified C0 vs tangent break, and closed5.41 knot vector.')
