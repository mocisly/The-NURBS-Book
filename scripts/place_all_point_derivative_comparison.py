"""Keep9.11 immediately after degree comparison,then discuss varying magnitudes9.12."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_11.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.11\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='图 9.12 说明了通过在数据点使用不同导数幅度获得的不同曲线插值之间的比较。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.11. 在五个代表性数据点指定一阶导数的全局插值：二次曲线（实线）与三次曲线（虚线）。'+'\\\\\n'+
       r'参数采用弦长法，节点分别按公式 (9.22)、(9.23) 构造；每条曲线同时满足五个位置和五个导数约束。'+'\\\\\n'+
       r'取$\mathbf D_k=d\mathbf T_k$，$d$为总弦长，所有箭头统一按实际导数的$1/5$绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.11 before derivative-magnitude comparison,with allpoint constraints and common arrow scale explicit.')
