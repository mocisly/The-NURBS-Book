import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images']if e['tex']==f'image_tex/ch11/fig_11_{n}.tex')for n in(27,28)];assert all(e['applied']for e in entries);f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.23\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='现在我们描述表面曲线变形。';assert s.count(anchor)==1
caption=r'图 11.23. 对具有五个自交点的星形多边形应用相同的区域变形。'+'\\\\\n'+r'(a) 精确奇偶规则选出的控制点（+）和包围框；(b) 由这组控制点实际计算的双三次曲面。'+'\\\\\n'+r'中心五边形按奇偶规则不选控制点；水平与竖直射线分别检验，1225个候选点的归属一致。'+'\\\\\n'+r'沿用图11.22的平面、$35\times35$控制网、$d=6/5$、投影和字号；平滑过渡由基函数支撑决定。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n\\begin{minipage}[c]{17cm}\\centering\n'+entries[0]['replacement']+'\n\\end{minipage}\\hspace{.5cm}\n\\begin{minipage}[c]{19cm}\\centering\n'+entries[1]['replacement']+'\n\\end{minipage}\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.23 one aligned domain/surface group before curve-on-surface subsection; removed intervening scan from11.54.')
