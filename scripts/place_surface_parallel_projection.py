"""Keep6.7 and its explanation together, before homogeneous matrix operations."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_07.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'图 6\.7 显示了 NURBS 曲面的平行投影。\s*\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.7\.[^\n]*'
block=('图 6.7 显示了 NURBS 曲面的平行投影。\n\n\\begin{center}\n\\begin{minipage}{20cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.7. 代表性双二次 NURBS 曲面的平行投影。\\\\\n'
       '实线为原曲面的控制网及等参线，虚线为同一控制网和曲面的投影；各控制点均沿 $\\mathbf W$ 投影，权重保持不变。\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1 and s.count(ref)==1
f.write_text(s,encoding='utf-8');print('Grouped6.7 with the surface parallel-projection explanation.')
