"""9.12:repair OCR magnitude fractions and keep comparison before control-point example."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_12.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.12\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
s=s.replace('376 曲线和曲面拟合，','',1)
assert s.count('3/{2d}')==1 and s.count('1/{2d}')==1
s=s.replace('3/{2d}','3d/2',1).replace('1/{2d}','d/2',1)
anchor='图 9.13 显示了对指定点和一阶导数的二次曲线插值的控制点。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.12. 对图 9.11 的同一组五点、单位切向及三次节点，改变各点的导数幅度。'+'\\\\\n'+
       r'实线、虚线和点线分别取$\alpha_k=d,3d/2,d/2$，其中$d$为总弦长，$\mathbf D_k=\alpha_k\mathbf T_k$。'+'\\\\\n'+
       r'全部位置和导数约束均由方程组求解满足；所有箭头统一按实际导数向量的$1/5$绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.12 before control-point example;repaired OCR reciprocal magnitudes to3d/2,d/2.')
