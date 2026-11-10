"""Place9.1 immediately after interpolation definition,before approximation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_01.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.1\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='在近似中，我们构建的曲线和曲面不一定精确满足给定数据';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.1. 插值五个点及两个端点一阶导数的三次B样条，采用一组代表性数据。'+'\\\\\n'+
       r'曲线满足$\mathbf C(i/4)=\mathbf Q_i$、$\mathbf C^{\prime}(0)=\mathbf D_0=(4,9)$、$\mathbf C^{\prime}(1)=\mathbf D_4=(6,-9)$，内部为$C^2$连续。'+'\\\\\n'+
       r'两个箭头统一按导数向量的$1/4$绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);s=s.replace('362 曲线和曲面拟合','')
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed9.1 between interpolation and approximation definitions,removed scanned-page header.')
