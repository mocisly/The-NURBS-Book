"""Keep9.5 and the three-method explanation in one centered native block."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_05.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.5\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.5. 七个分布不均匀的代表性数据点的三次插值比较。'+'\\\\\n'+
       r'实线：均匀参数与均匀节点；虚线：弦长参数与平均节点；点划线：向心参数与平均节点。'+'\\\\\n'+
       r'三组标尺依次表示各方法的数据参数和节点；全部曲线均由同一组七点插值方程求解。'+
       '\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8')
print('Grouped9.5 native curves,computed rulers and caption.')
