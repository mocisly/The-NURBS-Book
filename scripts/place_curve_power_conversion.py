"""Place6.18 by the conversion example and repair verified matrix-sum OCR."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_23.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.18\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='我们以两个最后的备注完成 B-spline 到幂基转换的讨论:';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{21cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.18. 代表性三次 B 样条的中间段 $[3/10,7/10]$ 与全局参数的幂基系数。\\\\\n'
       r'方框标出该段上的等参数步长点；从该段提取的 Bézier 控制点经基变换得到 $\mathbf C(u)=\sum_{i=0}^3\mathbf b_i u^i$，箭头显示 $\mathbf b_i/10$。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
wrong='每行和每列的元素之和为一。';assert s.count(wrong)==1
s=s.replace(wrong,'各行元素之和除首行为一外均为零；各列元素之和除末列为一外均为零。',1)
wrong=r'0 & j = 0,\ldots ,k - \\'
right=r'0 & j = 0,\ldots ,k - 1 \\'
assert s.count(wrong)==1;s=s.replace(wrong,right,1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8')
print('Placed6.18 after conversion example; corrected matrix row/column sums and missing upper-triangle index endpoint.')
