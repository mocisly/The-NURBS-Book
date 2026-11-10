"""Group7.17 after all prescribed control data and restore the verified C1 sentence."""
import re
import image_tex as p
d=p.load();ee=[next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{i}.tex') for i in (18,19)]
assert all(e['applied'] for e in ee)
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
for e in ee:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.17\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'在 \(a = \cos {30}^{ \circ  }\) 处。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{36cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'
       '\\begin{minipage}{19.5cm}\\centering\n'+ee[0]['replacement']+
       '\n\\end{minipage}\\hfill\n\\begin{minipage}{14cm}\\centering\n'+ee[1]['replacement']+
       '\n\\end{minipage}\n\\par\\smallskip\n'
       r'图 7.17. 基于七点三角形的 NURBS 圆，两图使用 Ex7.3 给出的同一组节点、控制点和权重。'+'\\\\\n'
       r'(a) 控制多边形与等参数步长采样点 $u=i/60$，节点采样点与控制点圆圈重合，坐标比例与图7.16一致；(b) 对应的七个有理基函数 $R_{i,2}$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,r'其中 \(a = \cos {30}^{ \circ  }\)。'+block,1)
wrong=r'读者可以验证 \(\mathbf{C}\left( u\right)\) 在 \({C}^{1}\) 和 \(u = 1/3\) 处是 \(u = 2/3\) 连续的，尽管基函数在那里是 \({C}^{0}\) 连续的(见图 7.17b)。'
right=r'曲线 \(\mathbf C(u)\) 在 \(u=1/3\) 和 \(u=2/3\) 处均为 \(C^1\) 连续，尽管相应基函数在那里仅为 \(C^0\) 连续（见图7.17b）。'
assert s.count(wrong)==1;s=s.replace(wrong,right,1)
for e in ee:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Placed7.17 after complete data; corrected garbledC1join prose using verified derivatives.')
