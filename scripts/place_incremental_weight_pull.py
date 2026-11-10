import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_15.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.13。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='图 11.13 显示了增量拉动的一个例子。注意权重的指数变化。';assert s.count(anchor)==1
caption=r'图 11.13. 沿用图11.11、11.12的同一曲线，在$t_4=\bar u=0.52$处连续拉动四个相等距离增量$\Delta d=0.022$。'+'\\\\\n'+r'初始$w_4=0.2$，按式(11.25)得到$\widehat w_4\simeq0.406,0.777,1.641,5.947$；各步位移严格等距。'+'\\\\\n'+r'下方线性权重轴显示所需权重增量迅速增大；数值由本组代表性数据重新计算。'
block='\n\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n'
s=s.replace(anchor,anchor+block,1);f.write_text(s,encoding='utf-8');print('11.13 moved after incremental explanation, before two-weight subsection.')
