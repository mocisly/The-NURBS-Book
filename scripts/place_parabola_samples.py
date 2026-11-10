"""Place7.7 by7.10 and reconnect the following spatial transformation prose."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_07.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.7\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='参数化标准位置下的抛物线(见图 7.7)。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{16cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.7. 抛物线弧的参数化（式7.10）。\\\\\n'
       r'示例取 $a=1$；加号对应 $u=i/10$（$i=1,\ldots,19$），圆圈为参数端点 $u=0,2$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,anchor+block,1)
s,n=re.subn(r'旋转矩阵和任意的\s+变换向量','旋转矩阵和任意的变换向量',s,count=1);assert n==1
s=s.replace('288 圆锥曲线与圆\n','',1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.7 by7.10; spatial transformation explanation no longer interrupted by figures.')
