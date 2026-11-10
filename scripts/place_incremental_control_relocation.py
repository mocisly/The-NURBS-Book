import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_07.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.7。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='最后，设计师可以通过选择两个额外的曲线点';assert s.count(anchor)==1
captions=[r'图 11.7. 在$\bar u=3/5$处，以四个相等的距离增量拉动同一条三次曲线。',r'每次选定点精确移动$\Delta d=2/5$，控制点$P_4$按固定$\Delta\alpha=\Delta d/N_{4,3}(3/5)$沿同一单位方向移动。',r'四条虚线为各步实际曲线；选定参数处的五个圈点共线且相邻距离相等，终点为$\widehat P$。',r'细线显示最终实际位移；支撑域外的整段曲线不变。节点、控制点与增量核验记录于源码。']
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.7placedafterincrementalexplanationbeforelimited-domainandsurfaceformulas.')
