"""Keep8.8 beside the two defining isoparametric properties; fix nine-point knot OCR."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_12.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.8\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
start=s.index('让我们使用九点圆表示法');end=s.index('和权重',start)
s=s[:start]+r'让我们使用九点圆表示法，取节点向量\(U=\{0,0,0,1/4,1/4,1/2,1/2,3/4,3/4,1,1,1\}\)'+s[end:]
anchor='让我们使用九点圆表示法';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.8. 旋转曲面的定义。实线分别为生成曲线$\mathbf C(v)$、纬圆$\mathbf S(u,\bar v)$和旋转后的子午线$\mathbf S(\bar u,v)$。'+'\\\\\n'+
       r'示例生成曲线为六点二次B样条，$V=\{0,0,0,1/3,1/3,2/3,1,1,1\}$，生成线权重均为1；取$\bar v=1/3$和$\bar u=1/4$。'+'\\\\\n'+
       r'此时$\mathbf C(\bar v)=\mathbf P_2$，纬圆的细虚线控制正方形为第2层控制点；$\bar u=1/4$对应绕$z$轴旋转90度。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);s=s.replace(':342 常见曲面的构造',':')
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.8 after defining properties;restored all12 circle knots including repeated quarter knot.')
