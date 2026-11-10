"""Move9.9 beside endpoint-direction comparison,keeping spline equations uninterrupted."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_09.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.9\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{三次样条曲线插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.9. 与图 9.8 相同的数据、弦长参数及节点，改变端导数方向。'+'\\\\\n'+
       r'A（实线）：$\mathbf D_0=(-12,12)$、$\mathbf D_6=(-12,-12)$；B（虚线）：$\mathbf D_0=(0,16)$、$\mathbf D_6=(-16,0)$；'+'\\\\\n'+
       r'C（点线）：$\mathbf D_0=(12,12)$、$\mathbf D_6=(-12,12)$。曲线均通过七个代表性数据点。'+'\\\\\n'+
       r'各箭头与对应曲线使用相同线型，并统一按实际导数向量的$1/8$绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.9 after endpoint direction comparison,before traditional spline subsection.')
