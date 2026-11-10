"""Collect all5.39 stages and actual-error axes next to the algorithm outline."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in range(57,61)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/5.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.39\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
for header in ('216 基本几何算法','218 基本几何算法'):
    assert s.count(header)==1;s=s.replace(header,'')
caption=(r'图 5.39. 四次曲线逐段降为三次，控制点采用代表性示例；八个面板保持相同尺度。'
         '\\\\\n'+r'$U=\{0,0,0,0,0,u_1,u_1,u_2,u_2,1,1,1,1,1\}$，$u_1=3/10$、$u_2=7/10$。'
         '\\\\\n'+r'(a)原曲线；(b)提取第一段；(c)第一段降次；(d)提取第二段；(e)第二段降次；(f)移除两个$u_1$。'
         '\\\\\n'+r'(g)第三段降次；(h)移除两个$u_2$，得到六个控制点的三次曲线。实线表示原曲线，虚线表示已处理段。'
         '\\\\\n'+r'下方各图采用同一误差刻度，绘制真实参数误差$E(u)=\|C(u)-\widehat C(u)\|_2$；降次按式(5.41)，节点移除采用局部逆插入拟合。')
block=('\\begin{center}\n\\begin{minipage}{27.2cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+
       '\n\\par\\medskip\n'.join(e['replacement'] for e in entries)+'\n\\par\\smallskip\n'+caption+
       '\n\\end{minipage}\n\\end{center}\n\n')
anchor='曲线分解、节点移除以及节点移除误差的界定在第 5.3 和 5.4 节中进行了讨论。'
assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Grouped5.39 eight processing/error views after a-h explanation, preserving reduction formulas.')
