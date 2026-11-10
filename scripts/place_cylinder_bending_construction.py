import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_38.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.32\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='图 11.33 和 11.34 显示了圆柱面弯曲的示例。';assert s.count(anchor)==1
caption=r'图 11.32. 圆柱弯曲的轴线、最近点投影和交比构造（代表性平面及半径1的圆柱）。'+'\\\\\n'+r'$O(w)=(0,w,2)=Q+wV$位于中心等参线$C_{u_c}(v)$上方；$O(w_{i,j})$是$P_{i,j}$到轴线的正交投影。'+'\\\\\n'+r'$R_{i,j}$是射线与圆柱的交点，$\widehat P_{i,j}$按式(11.59)—(11.61)及$\lambda=2$计算。'+'\\\\\n'+r'圆截面用原生仿射椭圆表示；所有点的位置均由同一三维构造计算，标注与正文变量对应。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.32 after complete cylinder projection algorithm, before examples; restored axis-offset equation continuity.')
