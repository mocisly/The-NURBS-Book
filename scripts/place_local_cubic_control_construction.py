"""Group9.29 with its complete double-knot vector and control explanation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_35.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.29\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.29. 四个代表性数据点的$C^1$局部三次插值；三段分别满足公式 (9.46)，取$\alpha_0,\alpha_1,\alpha_2=3,4,3$。'+'\\\\\n'+
       r'原始参数区间长度为$3,4,3$；归一化后数据参数为$(0,3/10,7/10,1)$。去掉两个内部数据控制点及各一个节点后，留下图示八个控制点，曲线完全不变。'+'\\\\\n'+
       r'带中心点的圆圈为数据点，空心圆为内部 Bézier 控制点；下方参数尺按实际节点位置绘制，两端四重、内部双重。'+
       '\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1
for old,new in [(r'{\mathbf{P}}_{n - 2,2,,}',r'{\mathbf{P}}_{n - 2,2},'),(r'{\mathbf{P}}_{n - 1,2,,}',r'{\mathbf{P}}_{n - 1,2},')]:
    assert s.count(old)==1;s=s.replace(old,new,1)
f.write_text(s,encoding='utf-8');print('Grouped9.29 immediately after9.54;repaired duplicate OCR commas in9.53 control indices.')
