import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_05.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.5\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='假设我们现在想要沿着';assert s.count(anchor)==1
captions=[r'图 11.5. 在原有二次节点处再次插入后，移动新控制点产生尖角。',r'原节点平均值为$\{0,1/8,3/8,5/8,7/8,1\}$；插入已有节点$1/2$使其重数成为2，且$Q_3=C(1/2)$。',r'插入本身保持原曲线及其一阶连续性；随后将$Q_3$向下移动$9/5$，曲线位置连续，但在$u=1/2$左右的切向不一致。',r'实线、虚线分别为移动前后曲线，细线为同参数点的真实位移；代表性控制点和左右导数记录于源码。']
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.5placedafterquadraticexceptionbeforetwo-controlformulas.')
