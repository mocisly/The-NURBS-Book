"""Collect the eight stages of5.35 beside the algorithm explanation."""
import re
import image_tex as pipeline

data=pipeline.load()
entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in range(47,51)]
assert all(e['applied'] for e in entries)
path=pipeline.ROOT/'chapter/5.tex';s=path.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.35\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
assert s.count('202 基本几何算法')==1;s=s.replace('202 基本几何算法','')
caption=(r'图 5.35. 三次曲线逐段升为四次；各面板保持相同的曲线、参数与尺度。'
         '\\\\\n'+r'$U=\{0,0,0,0,3/10,7/10,1,1,1,1\}$，$u_a=3/10$、$u_b=7/10$；控制点坐标为代表性示例。'
         '\\\\\n'+r'(a)原曲线；(b)提取第一段；(c)第一段升次；(d)提取第二段；(e)第二段升次。'
         '\\\\\n'+r'(f)移除两个$u_a$；(g)第三段升次；(h)移除两个$u_b$，得到九个控制点、内部节点重数为二的$C^2$四次曲线。'
         '\\\\\n'+r'空心圆为当前控制点，十字标出原曲线的两个内部节点；$N$为当前控制点总数，中间阶段包含不同次数的处理段。')
block=('\\begin{center}\n\\begin{minipage}{30.2cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+
       '\n\\par\\medskip\n'.join(e['replacement'] for e in entries)+'\n\\par\\smallskip\n'+caption+
       '\n\\end{minipage}\n\\end{center}\n\n')
anchor='第一步是算法 A5.6 的直接应用。';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
path.write_text(s,encoding='utf-8');print('Grouped all eight5.35 stages after their a-h explanation, preserving all algorithm text.')
