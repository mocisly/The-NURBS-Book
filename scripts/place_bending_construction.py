import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_34.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.28\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='总结来说，';assert s.count(anchor)==1
caption=r'图 11.28. 式(11.56)—(11.58)的曲线弯曲构造，代表性交比$\lambda=3$。'+'\\\\\n'+r'每条射线$OP_i$与抛物线$B(w)=(2+w,2+w^2/2)$相交于$R_i$，再按同一交比确定$\widehat P_i$。'+'\\\\\n'+r'上下两条实曲线分别由原控制点与映射后的控制点计算；细虚线为各自控制多边形。'+'\\\\\n'+r'图中展示一个完整弯曲区段，九组交点和交比均精确成立；与相邻区段的刚体衔接由下文说明。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);s=s.replace('548 形状修改工具\n','');f.write_text(s,encoding='utf-8');print('11.28 after complete crossratio formulas, before summary and external rigid-motion discussion.')
