"""Group7.25's finite and infinite cases after all subdivision formulas."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{n}.tex') for n in (30,31)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.25\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='利用算法 A7.2 和 SplitArc';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{36cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\vspace{.5cm}\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+
       r'图 7.25. 在 $u=1/2$ 处用有理 de Casteljau 算法分割圆锥弧，得到两个以肩点 $\mathbf S=\mathbf Q_2=\mathbf R_0$ 相接的弧段。'+'\\\\\n'+
       r'(a) 原权重 $w_1>0$，扫掠小于 $180^\circ$；(b) $-1<w_1<0$，扫掠大于 $180^\circ$；(c) 非零无穷控制向量，扫掠 $180^\circ$。'+'\\\\\n'+
       r'虚线为原控制多边形的辅助延长线，细实线为分割后的控制多边形；新段归一化后的中间权重均为 $\sqrt{(1+w_1)/2}$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert all(s.count(e['replacement'])==1 for e in entries);f.write_text(s,encoding='utf-8')
print('Grouped7.25a/b/c after subdivision and normalization formulas7.42-7.50.')
