"""Group9.4 and its legend/caption after the parameterization comparison."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_04.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.4\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.4. 使用图 9.3 的同一组代表性数据比较三种三次插值。'+'\\\\\n'+
       r'实线：均匀参数与均匀节点；虚线：弦长参数与平均节点；点划线：向心参数与平均节点。'+'\\\\\n'+
       r'三组标尺依次对应上述方法，圆圈表示数据参数，短刻线表示节点；所有曲线均通过七个数据点。'+
       '\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8')
print('Grouped9.4 with three-method legend and computed parameter/knot rulers.')
