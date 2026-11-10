"""Place5.25 in its own section; keep the neighboring A5.6 title with its inputs."""
import re
import image_tex as pipeline
data=pipeline.load();e=next(e for e in data['images'] if e['tex']=='image_tex/ch05/fig_5_32.tex');assert e['applied']
path=pipeline.ROOT/'chapter/5.tex';s=path.read_text(encoding='utf-8');ref=e['replacement'];assert s.count(ref)==1
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.25\.[^\n]*'
s,count=re.subn(pattern,'',s,count=1);assert count==1
assert s.count('An example is shown in Figure 5.25.')==1
s=s.replace('An example is shown in Figure 5.25.','')
anchor=r'\section{节点移除}';assert s.count(anchor)==1
caption=(r'图 5.25. 三次$\times$二次曲面的即时Bézier分解，显示三个相邻面片及其$4\times3$控制网。'
         '\\\\\n'+r'代表性$6\times4$控制网定义于$U=\{0,0,0,0,1/3,2/3,1,1,1,1\}$、$V=\{0,0,0,1/2,1,1,1\}$。'
         '\\\\\n'+r'图中取$v\in[1/2,1]$的三个面片，公共边界保持相接。')
block=('示例见图5.25。\n\n\\begin{center}\n\\begin{minipage}{20cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
# A5.6 title was orphaned at the footer in the full-book page review.
title=s.index('ALGORITHM A5.6');start=s.rfind(r'\HRule',0,title)
end=s.index('m = n+p+1;',title)
header=s[start:end];assert header.count(r'\HRule')==1 and '/* Output: nb, Qw */' in header
s=s[:start]+'\\noindent\\begin{minipage}{\\linewidth}\n\\vspace*{.6\\baselineskip}\n'+header+'\\end{minipage}\n\n'+s[end:]
# This empty old OCR page divider also split A5.6 midway through alpha setup.
start=s.index('\\HRule',s.index('Numerator of alpha',s.index('ALGORITHM A5.6')))
end=s.index(r'\hspace*{5em} /* Compute and store alphas',start)
assert re.sub(r'\s|\\HRule','',s[start:end])=='' and s[start:end].count(r'\HRule')==2
s=s[:start]+s[end:]
assert s.count(ref)==1;path.write_text(s,encoding='utf-8')
print('Placed5.25 before knot removal; kept A5.6 heading/inputs together and removed empty OCR divider.')
