"""Restore5.37's full caption and collect its four panels before surface theory."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (52,53)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/5.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.37\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
s,n=re.subn(r'(?m)^210 基本几何算法[^\n]*\n','',s,count=1);assert n==1
assert s.count('度数提升 211')==1;s=s.replace('度数提升 211','')
caption=(r'图 5.37. 同一条曲线的次数提升，四个面板保持相同尺度与参数化。'
         '\\\\\n'+r'(a)三次；(b)四次；(c)五次；(d)七次；相应控制点数$N$为6、9、12、18。'
         '\\\\\n'+r'原始$U=\{0,0,0,0,4/10,7/10,1,1,1,1\}$；示意采用代表性控制点，各次升次均保持原曲线不变。')
block=('\\begin{center}\n\\begin{minipage}{25.6cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+
       '\n\\par\\medskip\n'.join(e['replacement'] for e in entries)+'\n\\par\\smallskip\n'+caption+
       '\n\\end{minipage}\n\\end{center}\n\n')
anchor=next(line for line in s.splitlines() if '通过将其应用于控制点的行/列来实现曲面的度数提升' in line)
assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Grouped5.37 four views beside the curve elevation explanation; removed only corresponding split caption/header fragments.')
