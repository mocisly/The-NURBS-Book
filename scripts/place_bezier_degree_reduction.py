"""Place5.40 with its error laws and repair the corresponding parity OCR."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch05/fig_5_61.tex');assert e['applied']
f=p.ROOT/'chapter/5.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.40\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
old=r'对于 \(p\) ，即使最大误差发生在';new=r'当\(p\)为偶数时，最大误差发生在'
assert s.count(old)==1;s=s.replace(old,new,1)
old=r'对于 \(p\) 奇数';assert s.count(old)==1;s=s.replace(old,r'当\(p\)为奇数时',1)
old='左右各有两个峰值';assert s.count(old)==1;s=s.replace(old,'左右各有一个峰值',1)
caption=(r'图 5.40. 两个独立的Bézier降次示例，控制点采用代表性坐标。'
         '\\\\\n'+r'(a)七次降至六次；(b)六次降至五次。实线、圆点为原曲线和$\mathbf Q_i$，虚线、方点为近似曲线和$\mathbf P_i$。'
         '\\\\\n'+r'下方绘制真实参数误差$E(u)=\|C(u)-\widehat C(u)\|_2$，各自误差轴按数值标定；(a)中点误差为零，(b)中点误差最大。')
block='\\begin{center}\n\\begin{minipage}{30.5cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor='我们现在提出一种算法，用于在最大误差容忍度 TOL 的限制下降低 B 样条曲线的阶数。'
assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8');print('Placed5.40 beside its parity/error explanation; corrected even-degree wording and one peak on each side.')
