"""10.1natural-size diagram next to its definition,shared data documented."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_01.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.1\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{24cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 10.1. 摆动曲面的代表性轮廓曲线$P(u)$与轨迹曲线$T(v)$，分别位于$xz$、$xy$平面。'+'\\\\\n'+
       r'两条曲线均为三次夹持 B 样条，分别由六个、十一个控制点定义；实心点为控制点，虚线为控制多边形。'+'\\\\\n'+
       r'所选控制点及节点记录于源码，图 10.2 将原样使用它们，以比较等权与指定权值下的曲面。'+
       '\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8')
print('10.1placednatural21cmgeometryin24cmcaptionblockbeside10.3;explicitsharedrepresentativedatafor10.2.')
