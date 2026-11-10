import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_36.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 10\.26\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
# The old scan split a sentence immediately before the corner-control formulas.
s=s.replace('作为一个例子，我们展示如何\n\n\n\n计算与角落','作为一个例子，我们展示如何计算与角落',1)
anchor='四个扭转向量。';start=s.index(r'\tag{10.38}');index=s.index(anchor,start)+len(anchor)
captions=[r'图 10.26. 同一组边界的兼容跨边界导数场与角点扭矢量。',r'实线箭头为式(10.37)的实际$D_k(u)$、$D_\ell(v)$，虚线箭头为式(10.38)的真实混合导数$T_{a,b}$。',r'导数箭头按$3/25$、扭矢量按$3/50$的统一因子绘制，保留各自的方向和相对长度；不作单位化。',r'四个角点的两种混合求导结果完全一致；代表性字段与后续高阶Coons曲面的数据记录于源码。']
block='\n\n\\begin{center}\n\\begin{minipage}{27cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
s=s[:index]+block+s[index:];f.write_text(s,encoding='utf-8');print('10.26placedafterfulltwistcompatibility10.38;cornercontrolsentencerestored.')
