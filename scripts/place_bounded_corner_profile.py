"""Move9.51beside boundedcurve examples,before unrelatedsurface bounds."""
import re,json
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_59.tex');assert e['applied']
r=json.loads((p.ROOT/'image_tex/build/bounded-corner-profile-check.json').read_text())
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.51\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='在算法 A9.10 的节点移除步骤中';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{31cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.51. 八十五个代表性轮廓数据点的三次逼近，采用与图 9.50 相同的受控移除和重新拟合流程，容差$E=8/100$。'+'\\\\\n'+
       r'空心圆为数据点；方框顶点$\mathbf Q_{56}$作为插值约束，其参数处保留三重节点，精确保留尖角。'+'\\\\\n'+
       r'本例共'+str(len(r['controls']))+r'个控制点，最大数据点欧氏误差约$'+f"{r['actual_maximum_Euclidean_same_parameter_error']:.5f}"+r'<E$；字号、线宽与图 9.50 一致。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
s=s.replace('434 曲线与曲面拟合','',1)
f.write_text(s,encoding='utf-8');print('Placed9.51nextto9.50;captionexplicit85representativedata/protectedcorner/E.08/actualerror;removedsurface-boundinterruption andOCR434header.')
