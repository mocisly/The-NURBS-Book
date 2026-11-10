import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_32.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 10\.24\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='双线性混合的 Coons 补丁定义为';assert s.count(anchor)==1
block='\\begin{center}\n\\begin{minipage}{24cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+r'图 10.24. 定义Coons补片的四条兼容边界曲线。'+'\\\\\n'+r'采用代表性的三次$u$曲线与二次$v$曲线，四个端点完全一致；圈点满足$S_{1,0}=C_0(1)=C_1(0)$。'+'\\\\\n'+r'曲线数据记录于源码，后续图使用相同边界；所有权值为1。'+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(anchor,block+anchor,1)
# Obvious OCR loss: bilinear interpolation needs affine blending factors.
s=s.replace('双线性张量积-\n\nuct 表面','双线性张量积表面',1)
old=r'\begin{array}{ll} 1 & u \end{array}';new=r'\begin{array}{ll} 1-u & u \end{array}';assert s.count(old)==1;s=s.replace(old,new,1)
old=r'\begin{array}{l} 1 \\  v \end{array}';new=r'\begin{array}{l} 1-v \\  v \end{array}';assert s.count(old)==1;s=s.replace(old,new,1)
f.write_text(s,encoding='utf-8');print('10.24placedafter10.35;bilinearOCRaffinefactorsrestored.')
