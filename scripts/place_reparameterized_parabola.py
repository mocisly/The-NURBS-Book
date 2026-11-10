"""Group6.9 with exact derivatives and correct the endpoint OCR in Ex6.4."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_09.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.9\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{17cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.9. 例 Ex6.4 的同一条抛物线及重参数化后的端点一阶导数。\\\\\n'
       r'$u=1/2$ 对应 $s=3/5$；两支切向量按同一坐标尺度绘制，长度比为 $7/12$。'+'\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1
wrong=r'\mathbf{C}\left( {s = 1}\right)  = \mathbf{C}\left( {u = 1}\right)  = \left( {0,0}\right)'
right=wrong.replace('{0,0}','{1,0}');assert s.count(wrong)==1;s=s.replace(wrong,right,1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8')
print('Grouped6.9 after exact derivatives; corrected endpoint1 to(1,0).')
