import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch12/fig_12_02.tex');assert e['applied'];f=p.ROOT/'chapter/12.tex';s=f.read_text(encoding='utf-8')
caption=r'图 12.2. 闭合的$C^2$连续未夹紧三次曲线；$U_2=\{0,1,\ldots,11\}$，有效区间$[3,8]$。'+'\\\\\n'+r'五边形为代表性控制多边形，将前三个控制点依次重复在末尾：$P_5=P_0,P_6=P_1,P_7=P_2$。'+'\\\\\n'+r'方框标出整数节点处的曲线点；在$u=3$与$u=8$处，位置、一阶导数及二阶导数精确相同。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}'
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 12\.2\.[^\n]*';s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('Placed12.2 periodic unclamped cubic.')
