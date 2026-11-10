import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_01.tex');assert e['applied']
f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.1。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='从用户界面的角度来看';assert s.count(anchor)==1
captions=[r'图 11.1. 重新定位$P_4$引起的曲线局部移动（代表性控制数据）。',r'三次曲线采用$\bar u=3/5$、$t_4=(u_5+u_6+u_7)/3=0.52$；实线为原曲线，虚线为移动后的曲线。',r'$P_4$向下移动2个坐标单位，曲线上点的移动为$2N_{4,3}(u)$，$d$和$d_{\max}$取自同一个真实基函数。',r'下方基函数与上方曲线均由原始节点和控制点精确生成；支撑区间$[u_4,u_8)$之外的整段曲线保持不变。']
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.1placedafterrelocationformula11.3;originalu/t4preserved.')
