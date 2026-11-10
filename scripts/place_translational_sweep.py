"""10.11both panels together immediately after the sum/product formulas."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex') for n in (14,15)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.11\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
s=s.replace('474 高级表面构造技术','',1).replace('过程。我们将在本节末尾','我们将在本节末尾',1)
anchor='现在考虑情况 2。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{35cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+r'\hspace{1cm}'+entries[1]['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.11. 按式(10.17)—(10.19)构造的平移扫掠曲面。'+'\\\\\n'+
       r'(a) 代表性闭合B形截面$C(u)$、空间轨迹$T(v)$及其实际控制多边形；本例均采用三次、单位权值。'+'\\\\\n'+
       r'(b) 同一数据生成的精确张量积曲面，控制点为$P_{i,j}=Q_i+T_j$，细线为真实等参数曲线。'+'\\\\\n'+
       r'各截面只作平移，形状、尺寸与方向保持不变；因$C(1/3)=0$，粗线轨迹满足$S(1/3,v)=T(v)$。'+'\\\\\n'+
       r'两个子图使用相同投影、坐标尺度、字号与线宽；控制点和节点记录于源码。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.11ABsame-scale row afterEq10.19,beforemovingframes;restored B(v) discussion interrupted by old scans/OCR474.')
