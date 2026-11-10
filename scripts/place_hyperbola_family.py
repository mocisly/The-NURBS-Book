"""Place7.3 beside its full hyperbola explanation, before the parabola."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_03.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*(图\s*7\.3\.[^\n]*)'
m=re.search(pattern,s);assert m
caption=m[1];s=s[:m.start()]+s[m.end():]
anchor='类似地， \\(e = 1\\) 和变换';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.3 after hyperbola explanation and before parabola definition.')
