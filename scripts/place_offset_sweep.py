"""10.15next to offset explanation; clarify actual frame choices in these redraws."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_22.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.15。[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1;s=s.replace('484 高级表面构造技术','',1)
old=r'图 10.12 到 10.15 的扫掠表面使用投影法线方法来计算 \({\mathbf{B}}_{i}\) 向量。';assert s.count(old)==1
s=s.replace(old,'图 10.12、10.13 和 10.15 的平面轨迹使用常量法向，这也是投影法线法的结果；重绘图 10.14 使用源码中给出的连续正交方向函数。',1)
anchor='现在我们回到确定合适的方向函数';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{35cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.15. 截面过大引发的偏移折返和自交，两图使用相同平面轨迹、截面及常量方向$B=(0,0,1)$。'+'\\\\\n'+
       r'(a) A10.2，插值七个放置截面；(b) A10.1，插值十一个截面并保持整条轨迹。'+'\\\\\n'+
       r'粗线为$u=151/192$的偏移等参数线，圆点$I$为轨迹参数$1/4$、$3/4$处两个截面共有的空间点。'+'\\\\\n'+
       r'两组不同曲面参数精确得到同一点$I$，两处切平面不同；控制点、参数和核验数据记录于源码。'+'\\\\\n'+
       r'细线为真实等参数网格，横向较粗曲线为给定截面，两图统一视角、尺度、字号与线宽。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.15actual selfintersection besideoffsetparagraph;clarified14analyticBinputvsplanarPNexamples;OCR484removed.')
