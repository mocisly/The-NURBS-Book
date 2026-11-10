"""Place9.35 with local plane-preservation examples and remove OCR408header."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_42.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.35\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
assert s.count('408 曲线和表面拟合')==1;s=s.replace('408 曲线和表面拟合','',1)
anchor='当数据不均匀分布时，获得令人满意的表面';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{33cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.35. 具有平面子区域的局部双三次插值；(a) 二十五个代表性数据点，(b) 实际插值曲面。'+'\\\\\n'+
       r'取$\mathbf Q_{i,j}=(i-2,j-2,z_{i,j})$，仅末列的三个高度为$1/2,3/4,1/2$，其余二十二点位于$z=0$。'+'\\\\\n'+
       r'左侧两列共八个完整曲面片精确位于$z=0$；边界抬高处由局部$C^1$曲面平滑连接。两图视角、尺度相同，空心方框为数据点，曲面由四十一条等参数曲线表示。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.35 to local planar-region discussion after9.34;removed OCR408header from approximation list.')
