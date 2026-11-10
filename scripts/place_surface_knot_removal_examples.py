"""Move all four5.28 views back to the surface removal explanation."""
import re
import image_tex as pipeline
data=pipeline.load();entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (37,38)]
assert all(e['applied'] for e in entries)
path=pipeline.ROOT/'chapter/5.tex';s=path.read_text(encoding='utf-8')
for e in entries:
    ref=e['replacement'];assert s.count(ref)==1
    pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.28\.[^\n]*'
    s,count=re.subn(pattern,'',s,count=1);assert count==1
assert s.count('190 基本几何算法')==1;s=s.replace('190 基本几何算法','')
old=r'在图 5.27b-5.27d 以及图 \({5.28}\mathrm{\;b} - {5.28}\mathrm{\;d}\) 中，原始曲线/曲面以虚线表示，而移除结点的曲线/曲面以实线表示。'
assert s.count(old)==1;s=s.replace(old,'在图5.27b～5.27e与图5.28b～5.28d中，虚线分别表示原曲线、原控制网，实线表示移除节点后的近似结果。')
old=r'中，分别移除了一个、两个和三个三重结点 \(u = 1/2\) 。'
assert s.count(old)==1;s=s.replace(old,r'中，分别将三重节点\(u=1/2\)移除一、二、三次。')
caption=(r'图 5.28. 三次$\times$二次曲面的近似节点移除，各图使用相同视角与尺度。'
         '\\\\\n'+r'(a)代表性$8\times6$控制网；(b)在$u=3/10$移除三次，得到$5\times6$控制网。'
         '\\\\\n'+r'(c)在$v=1/4$移除一次，得到$8\times5$控制网；(d)两个方向均移除，得到$5\times5$控制网。'
         '\\\\\n'+r'原始$U=\{0,0,0,0,3/10,3/10,3/10,7/10,1,1,1,1\}$、$V=\{0,0,0,1/4,1/2,3/4,1,1,1\}$。'
         '\\\\\n'+r'虚线为原控制网，实线为移除后的控制网；局部逆插入拟合的近似误差已在原张量积基函数上核算。')
block=('\\begin{center}\n\\begin{minipage}{25cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\medskip\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+caption+
       '\n\\end{minipage}\n\\end{center}\n\n')
anchor='图 5.29a 中的曲线移除了所有可移除的结点。';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
path.write_text(s,encoding='utf-8');print('Grouped5.28 all four control nets before5.29, restored degree-elevation text and clarified virtual/solid legend.')
