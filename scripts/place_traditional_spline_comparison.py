"""Keep9.10 after derivative magnitude discussion,before all-derivative interpolation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_10.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.10[.。][^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{指定一阶导数的全局曲线插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.10. 对同一组七个代表性数据点，比较传统三次样条与常规全局三次插值。'+'\\\\\n'+
       r'实线：数据参数作为内部节点，并满足端导数约束；虚线：由弦长参数平均得到内部节点。'+'\\\\\n'+
       r'两者使用相同的弦长参数；实线取$\mathbf D_0=(0,d)$、$\mathbf D_6=(-d,0)$，$d$为总弦长，箭头统一按$1/5$绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.10 before all-derivative interpolation;clarified two knot choices and endpoint arrows.')
