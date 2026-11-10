import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch12/fig_12_08.tex');assert e['applied'];f=p.ROOT/'chapter/12.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 12\.5\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
caption=r'图 12.5. 标准九点二次NURBS圆的解夹；(a) 原夹紧表示；(b) 按算法A12.1得到的解夹表示。'+'\\\\\n'+r'原偶数控制点权重为1，奇数点权重为$w=\sqrt2/2$；解夹后仅首末齐次控制点改变，权重均为$2-w$。'+'\\\\\n'+r'新端点为$P_0=(1,-w/(2-w))$和$P_8=(1,w/(2-w))$，不再重合；实线仍是完全相同的单位圆。'+'\\\\\n'+r'已在精确代数域$w^2=1/2$中核验全部齐次多项式系数及圆方程；虚线为相应控制多边形，所有权重均为正。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';needle='显然，将这些结果扩展到曲面是直接的。';assert s.count(needle)==1;s=s.replace(needle,block+needle,1)
needle=r'U = \left\{  {0,0,0,\frac{1}{4}';assert s.count(needle)==1;loc=s.rfind(r'\[',0,s.index(needle));s=s[:loc]+'图12.5a显示标准九点二次NURBS圆，其夹紧节点向量为：\n\n'+s[loc:]
f.write_text(s,encoding='utf-8');print('Placed circle comparison in knot section before surface extension; restored circle data lead-in.')
