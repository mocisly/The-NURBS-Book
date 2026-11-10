import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch12/fig_12_01.tex');assert e['applied'];f=p.ROOT/'chapter/12.tex';s=f.read_text(encoding='utf-8')
caption=r'图 12.1. 未夹紧的均匀 B 样条，$U_1=\{-3,-2,-1,0,1,2,3,4,5\}$。'+'\\\\\n'+r'(a) 六个控制点的二次曲线，有效参数区间$[-1,3]$；(b) 五个控制点的三次曲线，有效参数区间$[0,2]$。'+'\\\\\n'+r'上方为代表性控制多边形及实际曲线，方框标出整数节点处的曲线点；下方显示各基函数的完整支撑及曲线的有效区间。'+'\\\\\n'+r'两条曲线的首尾均不插值首末控制点；所有曲线和基函数均由正文节点向量精确生成。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}'
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 12\.1\.[^\n]*';s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('Placed12.1 exact unclamped basis/curve domains.')
