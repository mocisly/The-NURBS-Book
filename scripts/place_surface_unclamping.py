import re
import image_tex as p
d=p.load();f=p.ROOT/'chapter/12.tex';s=f.read_text(encoding='utf-8');es=[]
for n in(9,10,11):
    e=next(e for e in d['images']if e['tex']==f'image_tex/ch12/fig_12_{n:02d}.tex');assert e['applied'];es.append(e)
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 12\.6\.[^\n]*';s,c=re.subn(pat,'',s,count=1);assert c==1
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'
for j,e in enumerate(es[:2]):
    block+='\\begin{minipage}{16cm}\\centering\n'+e['replacement']+'\n\\end{minipage}%\n'
    if j==0:block+='\\hspace{1cm}%\n'
block+='\\par\\medskip\n'+es[2]['replacement']+'\n\\par\\smallskip\n'
caption=r'图 12.6. 同一张$3\times2$次曲面的解夹，原参数域始终为$[0,1]^2$。'+'\\\\\n'+r'(a) 原曲面及控制网；(b) 只沿$u$方向解夹；(c) 只沿$v$方向解夹；(d) 两个方向均解夹。帽号表示解夹后的节点向量。'+'\\\\\n'+r'采用代表性$6\times5$控制点曲面，逐行或逐列执行算法A12.1；三种结果在九个节点矩形上的全部B\'{e}zier系数均与原曲面相同。'+'\\\\\n'+r'先处理$u$再处理$v$与相反顺序所得控制点完全一致；改变的是外部控制网，实线所示的实际曲面保持不变。'+'\\\\\n'+r'圆点为控制点，虚线为控制网，实线为实际等参线；四图采用相同投影、尺度、字号和线宽。'
block+=caption+'\n\\end{minipage}\n\\end{center}\n\n';needle=r'\section{标准中的 NURBS }';assert s.count(needle)==1;s=s.replace(needle,block+needle,1);f.write_text(s,encoding='utf-8');print('Placed aligned2x2 tensor unclamping before standards section; restored IGES/STEP lists.')
