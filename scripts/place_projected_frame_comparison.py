"""10.17after projected-normal formula/comparison,before Gordon curve networks."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_24.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.17\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1;s=s.replace('486 高级表面构造技术','',1)
anchor='最后，Klok [Klok86] 和 Guggenheimer';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.17. 沿代表性轨迹的投影法线方向与Frenet标架比较。'+'\\\\\n'+
       r'(a) 平面五次轨迹；(b) 三维三次轨迹，两例均在七个给定参数处计算方向。'+'\\\\\n'+
       r'实线箭头为按式(10.27)逐点投影得到的$B_i$，虚线箭头为真实Frenet标架的三个单位轴。'+'\\\\\n'+
       r'两种方法采用相同初始副法线；(a)曲率零点处Frenet标架未定义，投影法线仍有效且保持方向。'+'\\\\\n'+
       r'所有方向箭头使用同一三维单位长度和投影尺度，曲线、参数和归一化核验数据记录于源码。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.17trueprojected/Frenetcomparisonplacedafter10.27andbeforeGordon;compatibilityproserestoredafteroldscan.')
