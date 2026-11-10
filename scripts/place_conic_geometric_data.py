"""Place7.27 beside geometric-feature formulas; restore the missing rho root."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{n}.tex') for n in (34,35)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.27\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
wrong=r'\rho  = \alpha {\bar{x}}^{2} + {2\beta }\bar{x}\bar{y} + \gamma {\bar{y}}^{2}'
right=r'\rho = \sqrt{\alpha {\bar{x}}^{2} + {2\beta }\bar{x}\bar{y} + \gamma {\bar{y}}^{2}}'
assert s.count(wrong)==1;s=s.replace(wrong,right,1)
anchor='最后，图 7.28 显示了如何计算';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+
       '\\begin{minipage}[c]{13cm}\\centering\n'+entries[0]['replacement']+'\n\\end{minipage}\\hfill\n'+
       '\\begin{minipage}[c]{23cm}\\centering\n'+entries[1]['replacement']+'\n\\end{minipage}\n\\par\\smallskip\n'+
       r'图 7.27. 从有理二次 Bézier 表示计算的几何数据；三图采用相同坐标比例，空心圆为给定控制点或求得的几何特征点。'+'\\\\\n'+
       r'(a) 抛物线的顶点 $\mathbf V$、焦点 $\mathbf F$ 与轴方向 $\mathbf A$；(b) 椭圆中心 $\mathbf C$、负长轴方向 $-\mathbf U$ 与短轴方向 $\mathbf V$；'+'\\\\\n'+
       r'(c) 双曲线中心 $\mathbf C$、横轴方向 $\mathbf U$、共轭轴方向 $\mathbf V$ 及渐近线 $\mathcal A_1,\mathcal A_2$；虚线矩形的对角方向给出渐近线。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert all(s.count(e['replacement'])==1 for e in entries);f.write_text(s,encoding='utf-8')
print('Grouped7.27a/b/c after geometric-feature discussion; restored rho=sqrt(quadratic norm), yielding unit principal axes.')
