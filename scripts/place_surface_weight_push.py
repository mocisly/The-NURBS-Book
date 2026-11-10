import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_19.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.17\.[^\n]*'
caption=r'图 11.17. 在$\bar u=\bar v=0.55$处减小单个权重，将曲面点推离固定控制点$P_{4,3}$，距离$d=1$。'+'\\\\\n'+r'实线为原曲面，虚线为修改后的局部等参线；箭头连接同一参数点，圆点标出指定的精确位移。'+'\\\\\n'+r'代表性控制网沿用图11.8的节点与其余控制点，升高$P_{4,3}$并使指定射线竖直；其余权重均为1。'+'\\\\\n'+r'$N=N_{4,3}(0.55)N_{3,2}(0.55)$，$w_{4,3}$由1减为$(1-N)/(2-N)>0$，四条边界保持不变。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}';s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1
s=re.sub(r'；见\s*图 11\.14。这些组件','；见图11.14）。这些组件',s,count=1)
f.write_text(s,encoding='utf-8');print('11.17 at surface-weight subsection end, explicit push AWAY from control, natural scale.')
