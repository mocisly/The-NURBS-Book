import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_25.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图10\.18\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='我们希望构造一个NURBS曲面';assert s.count(anchor)==1
block='\\begin{center}\n\\begin{minipage}{24cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+r'图 10.18. 兼容的双向B样条曲线网络。'+'\\\\\n'+r'五条三次$C_k(u)$与四条二次$C_\ell(v)$在二十个实心点处满足式(10.29)，其中圈点$Q_{3,1}=C_1(u_3)=C_3(v_1)$。'+'\\\\\n'+r'采用示例10.1的次数与输入节点；代表性控制点、交点参数记录于源码，后续图沿用同一数据。'+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.18placedaftercompatibilityequation10.29.')
