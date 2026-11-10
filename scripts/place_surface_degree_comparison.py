"""Keep9.17 next to global-surface degree comparison,not local tangent estimation."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex') for n in (20,21)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.17\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='在图 9.18 中演示了无法处理共面的数据。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\smallskip\n'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.17. 图 9.15 的同一组代表性数据在不同次数下的全局曲面插值。'+'\\\\\n'+
       r'(a) 次数$(2,3)$；(b) 次数$(3,2)$；(c) 次数$(3,3)$。三者采用完全相同的弦长网格参数，节点按各次数平均计算。'+'\\\\\n'+
       r'三个曲面均通过全部十六个数据点，并沿用图 9.16 的相同视角、尺度和字号。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.17a/b/c after degree comparison,before coplanarity example;removed from tangent estimation.')
