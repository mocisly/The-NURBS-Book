"""Move9.8 to the endpoint-constrained discussion before the spline subsection."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_08.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.8\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1;s=s.replace('372 曲线与曲面拟合','',1)
anchor='图 9.9 说明了对相同数据点的插值，但具有不同的端切线方向和导数幅度。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.8. 对同一组七个代表性数据点进行端导数约束的全局三次插值。'+'\\\\\n'+
       r'固定$\mathbf D_0=(0,\alpha)$、$\mathbf D_6=(-\alpha,0)$；实线、虚线及点线分别取$\alpha=8,16,24$。'+'\\\\\n'+
       r'参数采用弦长法，节点按公式 (9.9) 平均计算；两端箭头统一按导数向量的$1/8$绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.8 beside Eq9.9..12,with common derivative-arrow scale and explicit representative magnitudes.')
