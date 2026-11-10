import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_04.tex');assert e['applied']
f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图11\.4。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='我们提醒读者，';index=s.index(anchor)
captions=[r'图 11.4. 对图11.3的同一曲线插入节点后，重新定位新控制点$Q_4$。',r'按式(11.6)插入$\widehat u=0.44$，使新节点平均值$t_4=0.43=\bar u$；插入本身精确保持原曲线。',r'移动$Q_4$使同一选定点沿相同方向移动$6/5$；实际位移线较集中，变化支撑域由$[0,.71)$缩为$[.2,.71)$。',r'$P_3,P_4$为原控制点，$Q_3,Q_5$为插入生成的相邻控制点；原曲线、目标点、方向和绘图尺度与前两图一致。']
block='\n\n\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
s=s[:index]+block+s[index:];f.write_text(s,encoding='utf-8');print('11.4placedafteritsknot-insertionexplanationandbeforequadraticexception.')
