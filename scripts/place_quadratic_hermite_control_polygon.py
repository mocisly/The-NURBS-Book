"""Move9.13 out of surface parameterization prose to the quadratic Hermite example."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_13.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.13\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
s,n=re.subn(r'存储弦长\s+距离','存储弦长距离',s,count=1);assert n==1
anchor=r'\subsection{全局曲面插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.13. 图 9.11 的二次插值曲线及其十个求解所得的控制点。'+'\\\\\n'+
       r'实心圆为五个代表性数据点，空心圆为其余控制点，虚线为控制多边形；两端数据点与端控制点重合。'+'\\\\\n'+
       r'曲线满足全部五个位置和五个导数约束，箭头与图 9.11 一样按实际导数的$1/5$绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.13 before surface interpolation;rejoined interrupted chord-distance sentence.')
