"""10.2ABCinonealignedcommon-scale row before open/closed and skinning prose."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex') for n in (2,3)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.2\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
anchor=r'注意， \(\mathbf{P}\left( u\right)\) 和';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{35cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+r'\hspace{.7cm}'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 10.2. 由图 10.1 的同一组曲线按公式 (10.3)—(10.6) 生成的$(3,3)$次摆动曲面，取$\alpha=0.12$。'+'\\\\\n'+
       r'(a) $6\times11$控制网；(b) 全部权值为$1$的非有理曲面；(c) 指定权值后的有理曲面。'+'\\\\\n'+
       r'取$w_1^P=w_4^P=5$、$w_1^T=w_4^T=w_6^T=w_9^T=5$，其余为$1$，曲面权值为$w_{ij}=w_i^P w_j^T$。'+'\\\\\n'+
       r'加权前后共用同一欧氏控制网；三个子图统一视角、坐标尺度、字号与线宽，曲面网格为真实等参数曲线。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);s=s.replace('图 10.2b 中的表面是非理性的','图 10.2b 中的表面是非有理的',1)
s=s.replace('曲线。Filip 和 T. Ball','Filip 和 T. Ball',1)
f.write_text(s,encoding='utf-8');print('Grouped10.2ABCsingleunscaledrow33.125cm in35cmblock,allgaps.7cm;exactweight/datacaption;removedcontinuationfromskinninghistory andduplicateword.')
