import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_20.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.18\.[^\n]*'
caption=r'图 11.18. 式(11.43)—(11.45)的归一化有理变形函数，$w_3=1/5,1,30$。'+'\\\\\n'+r'点线、虚线、实线依次对应三个权重；各曲线关于$t=1/2$对称，峰值严格为1。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}';s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('11.18 natural19x8.2cm graph with actual normalized functions.')
