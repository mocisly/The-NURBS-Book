"""Keep9.28 with its positive-root derivation, before piecewise interpolation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_34.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.28[。\.][^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
s,n=re.subn('我们必须构造一个立方 Bézier 曲线。\\s+曲线段','我们必须构造三次 Bézier 曲线段',s,count=1);assert n==1
s,n=re.subn(r'应用方程 \(1\.10\) 并考虑参数范围的二分法，它\s+得出','应用方程 (1.10)，并考虑二分后的参数范围，得出',s,count=1);assert n==1
anchor='现在我们回到立方插值问题。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.28. 在$u=0,1/2,1$处速度均为$\alpha=6$的代表性三次 Bézier 曲线。'+'\\\\\n'+
       r'取$\mathbf P_0=(0,0)$、$\mathbf P_3=(26/5,0)$，单位端切向为$(3/5,4/5)$、$(3/5,-4/5)$；公式 (9.50) 的正根为$6$。'+'\\\\\n'+
       r'三个导数分别为$(18/5,24/5)$、$(6,0)$、$(18/5,-24/5)$，箭头统一按真实导数的$1/2$绘制，故长度相等。虚线为控制多边形。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.28 after positive alpha root derivation;rejoined piecewise cubic introduction and midpoint derivative text.')
