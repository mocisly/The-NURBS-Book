"""Place9.33 in closed local surface discussion, not global approximation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_40.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.33\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
s,n=re.subn('，并且 406 曲线和表面拟合\\s+因此','。因此',s,count=1);assert n==1
anchor='当数据不均匀分布时，获得令人满意的表面';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{35cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.33. 在一个参数方向闭合的代表性局部双三次曲面；(a) 十六个不同的数据点，(b) 插值曲面。'+'\\\\\n'+
       r'四个轴向位置各给出四个截面数据点，截面按周期 Akima 切向构造；三次边界曲线按公式 (9.57) 确定，混合导数在本平移曲面例中为零。'+'\\\\\n'+
       r'全部数据被精确插值，闭合接缝两侧的位置及一阶导数一致；绘出三十一条闭合截线与十六条较细的纵向等参数线，两图采用同一视角和尺度。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.33 to closed local surface discussion;rejoined approximation introduction and removed OCR406header.')
