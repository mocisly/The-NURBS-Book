import re
import image_tex as p
d=p.load();f=p.ROOT/'chapter/12.tex';s=f.read_text(encoding='utf-8');es=[]
for name in('fig_12_03','fig_12_04','fig_12_03c'):
    e=next(e for e in d['images']if e['tex']==f'image_tex/ch12/{name}.tex');assert e['applied'];es.append(e)
for e in es[:2]:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
s,n=re.subn(r'图 12\.3\. 使用不同节点向量[^\n]*\n','',s,count=1);assert n==1
s=s.replace('图 12.3.(续)','');assert s.count(es[2]['replacement'])==1;s=s.replace(es[2]['replacement'],'',1)
s=s.replace(r'\hspace*{44em} (c)','').replace(r'\hspace*{10em} Figure 12.3. (Continued.)','')
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'
for j,e in enumerate(es):
    block+='\\begin{minipage}{17cm}\\centering\n'+e['replacement']+'\n\\end{minipage}'
    block+='\\hspace{1cm}\n'if j==0 else '\n\\par\\medskip\n'if j==1 else'\n'
caption=r'图 12.3. 同一条$C^2$闭合三次曲线的夹紧与解夹表示，有效参数区间均为$[3,8]$。'+'\\\\\n'+r'(a) 正文的夹紧节点向量；(b) 采用正文的非均匀外部节点，控制点不精确环绕；(c) 均匀外部节点产生三点环绕。'+'\\\\\n'+r'沿用图12.2的代表性曲线，分别精确求出三组控制点；五个节点区间的全部多项式系数逐项相同，曲线无近似误差。'+'\\\\\n'+r'实线为实际曲线，虚线为对应控制多边形；三图采用相同坐标尺度和字号。'
block+='\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';needle='在 CAD/CAM 的早期阶段';assert s.count(needle)==1;s=s.replace(needle,block+needle,1);assert '<img'not in s;f.write_text(s,encoding='utf-8');print('Placed complete ABCcomparison, recovered HTML C and removed OCR continuation labels.')
