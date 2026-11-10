"""Restore Table5.1 at Eq5.15, with correct retained-boundary description."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch05/table_5_01.tex');assert e['applied']
f=p.ROOT/'chapter/5.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\HRule\s*\\hspace\*\{1em\}\s*'+re.escape(ref)+r'\s*\\HRule'
caption=r'表 5.1. 由式(5.15)生成的控制点三角表。'
block='\\begin{center}\n\\begin{minipage}{14cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+caption+'\n\\par\\smallskip\n'+ref+'\n\\end{minipage}\n\\end{center}'
s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1
old='保留内层的控制点，外层的被丢弃。';assert s.count(old)==1
s=s.replace(old,'生成表格外边界上的控制点保留为新控制点，内部辅助点不再保留。',1)
assert s.count(ref)==1 and '<img' not in s
f.write_text(s,encoding='utf-8');print('Restored Table5.1 and corrected reversed interior/boundary OCR; chapter5 HTML placeholder removed.')
