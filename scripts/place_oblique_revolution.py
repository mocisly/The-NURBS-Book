"""Place8.12 beforeA8.1 and reconnect the split knot-initialization loop."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_16.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.12\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
# These two rules bracketed only a scanned image in the middle of a for-loop.
split=s.index('for (i=0; i<3; j++, i++)');body=s.index(r'\hspace*{1em}',split)
between=s[split:body];assert between.count(r'\HRule')==2
s=s[:split]+between.replace(r'\HRule','')+s[body:]
anchor='PointToLine(   ) :';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.12. 绕任意轴的部分旋转曲面。代表性轴为$\mathbf S+t\mathbf T$，其中$\mathbf S=(4/5,-1,-6/5)$、$\mathbf T=(0,3/5,4/5)$且$\|\mathbf T\|=1$。'+'\\\\\n'+
       r'图示旋转角为150度，由两个75度有理二次圆弧段构造；沿轴方向沿用图8.8生成线经缩放得到的半径与高度。'+'\\\\\n'+
       r'曲面为二次乘二次，实线为边界，细线为等参数线，虚线为旋转轴；末端方向箭头的实际长度为1。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
s=s.replace('注意这个算法与算法 A7.1 之间的相似性。346 常见表面的构造 算法 A8.1','注意这个算法与算法 A7.1 之间的相似性。\n\n算法 A8.1')
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed8.12 before utility list andA8.1;rejoined split end-knot initialization loop.')
