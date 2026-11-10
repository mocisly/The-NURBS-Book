"""Keep9.34 with the two-direction closed surface explanation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_41.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.34\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='当数据不均匀分布时，获得令人满意的表面';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{35cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.34. 两个参数方向均闭合的局部双三次插值；(a) 十六个不同的环形数据点，(b) 实际插值曲面。'+'\\\\\n'+
       r'取大、小半径$2,3/5$的环形采样数据，两方向公共参数均为$0,1/4,1/2,3/4,1$；按算法 A9.5 计算周期切向及非零混合导数，构造十六个双三次片。'+'\\\\\n'+
       r'所得多项式曲面精确插值数据，片间及两个闭合接缝的位置、一阶导数一致；两图视角、尺度相同，空心方框为数据点。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.34 from interrupted approximation algorithm list to closed-surface examples after9.33.')
