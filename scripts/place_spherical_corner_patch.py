"""Keep8.19 after the full power-to-Bernstein construction and beforeA8.2."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_24.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.19[.。][^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='现在我们总结完整的算法。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.19. 图8.18的平面片经立体投影复合得到的$4\times2$次有理Bézier球面角片，再以刚体变换调整空间位置。'+'\\\\\n'+
       r'显示球心为$(0,2/5,1)$、半径为1；控制网为$5\times3$，其中$\mathbf P_{0,0}=\cdots=\mathbf P_{4,0}=(0,2/5,2)$，故$t=0$边界退化为一点，共有11个不同控制点。'+'\\\\\n'+
       r'三条非退化边界均为过球心的大圆弧；细虚线为实际控制网，实线为边界，细实线为等参数线。所有15个齐次控制向量均由复合映射的幂系数转换得到。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
formula=r'\left\lbrack  {\mathbf{P}}_{i,j}^{w}\right\rbrack   = {M}_{4}^{-1}\left\lbrack  {\mathbf{b}}_{i,j}^{w}\right\rbrack  {\left( {M}_{2}^{-1}\right) }^{T}'
assert s.count(formula)==1 and r'\tag{8.32}' not in s;s=s.replace(formula,formula+r' \tag{8.32}',1)
s=s.replace('360 公共曲面的构造','')
assert s.count(e['replacement'])==1;assert not re.search(r'\\includegraphics|<img\s',s)
f.write_text(s,encoding='utf-8');print('Placed8.19 beforeA8.2,restored8.32equation tag;chapter8contains no remaining original images.')
