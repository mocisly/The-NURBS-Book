"""Move9.16a/b/c back to global surface interpolation,with one complete caption."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex') for n in (18,19)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.16\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='在图 9.17 中描绘了具有不同度数的表面插值。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\smallskip\n'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.16. 使用图 9.15 的同一组代表性数据，比较次数为$(2,3)$的三种全局曲面插值。'+'\\\\\n'+
       r'(a) 均匀参数与均匀节点；(b) 弦长参数与平均节点；(c) 向心参数与平均节点。'+'\\\\\n'+
       r'弦长及向心参数由各行（列）归一化后取平均，节点按公式 (9.8) 计算；三个曲面均通过全部十六点，并使用相同视角和尺度。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.16a/b top,c bottom before degree comparison;removed figures from local curve section.')
