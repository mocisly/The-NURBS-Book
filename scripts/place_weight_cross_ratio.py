import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_12.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.10\.[^\n]*'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+r'图 11.10. 权重的几何意义：同一控制多边形，仅改变$w_4$。'+'\\\\\n'+r'点线、实线、虚线分别取$w_4=0,1,4$；在同一$\bar u=1/2$处得到$R,M,P$。'+'\\\\\n'+r'三点与$P_4$严格共线，式(11.24)的交比恰为4；其余权重均为1。'+'\\\\\n'+r'控制多边形与节点采用明确记录于源码的代表性数据。'+'\n\\end{minipage}\n\\end{center}'
s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('11.10 placed with Eq11.22, natural scale/font.')
