"""Place complete9.45AB; separate combined original scan without tracing."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_53.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.45\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='当然，可以先拟合';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.45. 同一组八十一个数据点的$(2,3)$次最小二乘拟合，使用$5\times6$控制网。'+'\\\\\n'+
       r'(a) 按算法 A9.7 计算的拟合面，实心点为原始数据；(b) 数据参数处三维误差$e_{ij}=\|S(\bar u_i,\bar v_j)-Q_{ij}\|$的折线网格。'+'\\\\\n'+
       r'两图视角与平面尺度相同，误差高度统一放大四倍；均方根误差约$0.1415$，最大误差约$0.3494$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
old='当然，可以先拟合 \\(r + 1\\) 列，然后再拟合结果 \\(m + 1\\) 控制点的行。一般来说，结果并不相同。我们不知道有什么标准可以提前决定哪种方法会为特定数据集提供“最佳”拟合。'
new=r'也可以交换两个方向的拟合顺序。当两方向的公共参数、节点向量及线性端点约束预先固定时，算法 A9.7 的两次线性拟合可写为$P=F_uQF_v^{\mathsf T}$，因此交换顺序所得控制网相同。若在第一轮拟合之后重新计算参数、节点或约束，则一般不能保证结果相同。'
assert s.count(old)==1;s=s.replace(old,new,1)
old=r'该点在 \(u\) 方向上受到约束。';assert s.count(old)==1
s=s.replace(old,r'该点先在\(u\)方向上按算法 A9.6 进行受约束曲线拟合。',1)
s,n=re.subn(r'\s*曲线拟合，如算法 A9\.6 所示。然后，','然后，',s,count=1);assert n==1
# Upper half is9.45b, now genuinely redrawn above. Retain ONLY9.46a until its turn.
next_e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_54.tex');assert not next_e['applied']
old=next_e['original'];assert s.count(old)==1
cropped=r'\includegraphics[max width=0.9\textwidth,trim=0 0 0 900bp,clip]{'+next_e['image']+'}'
s=s.replace(old,cropped,1)
next_e['full_scan_original']=old;next_e['original']=cropped
next_e['options']=r'max width=0.9\textwidth,trim=0 0 0 900bp,clip'
next_e['note']='Combined scan upper9.45b redrawn in source53;900bp top TeX crop leaves only9.46a. Source54 awaits its own native redraw.'
f.write_text(s,encoding='utf-8');p.save(d)
print('Placed complete9.45AB beside comparison;fixed parameter order statement;cropped only completed upper9.45b from pending9.46a scan,manifest exact original updated.')
