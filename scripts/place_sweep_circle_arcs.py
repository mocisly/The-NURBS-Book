"""Group the four 7.22 panels immediately after the MakeNurbsCircle algorithm."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{n}.tex') for n in (25,26,27)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.22\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='我们以一些关于 NURBS 圆的杂项备注结束这一部分。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+
       '\\begin{minipage}[c]{14.5cm}\\centering\n'+entries[0]['replacement']+'\n\\end{minipage}\\hfill\n'+
       '\\begin{minipage}[c]{14.5cm}\\centering\n'+entries[1]['replacement']+'\n\\end{minipage}\n\\par\\vspace{.8cm}\n'+
       entries[2]['replacement']+'\n\\par\\smallskip\n'+
       r'图 7.22. 算法 A7.1 构造的不同扫掠角圆弧；四图的坐标比例相同，空心圆为控制点。'+'\\\\\n'+
       r'(a) $\theta_s=10^\circ,\ \theta_e=100^\circ$，一段；(b) $\theta_s=30^\circ,\ \theta_e=170^\circ$，两段；'+'\\\\\n'+
       r'(c) $\theta_s=20^\circ,\ \theta_e=250^\circ$，三段；(d) $\theta_s=40^\circ,\ \theta_e=330^\circ$，四段。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert all(s.count(e['replacement'])==1 for e in entries)
f.write_text(s,encoding='utf-8');print('Placed all four7.22 panels together,2by2,after algorithm A7.1 before final circle remarks.')
