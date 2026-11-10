import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_23.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.20。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='我们通过以下几点总结曲线扭曲:';assert s.count(anchor)==1
caption=r'图 11.20. 相同曲线段、细化和弦长参数下，分别改变式(11.48)的三个参数。'+'\\\\\n'+r'(a) $w_3=1/5,1,30$，固定$d=0.12,W=(0,-1)$；(b) 固定$w_3=20,d=0.12$，改变三个单位方向。'+'\\\\\n'+r'$W_1=(-3/5,-4/5),W_2=(0,-1),W_3=(3/5,-4/5)$；箭头表示各方向的上限位移。'+'\\\\\n'+r'(c) 固定$w_3=20,W=(0,-1)$，取$d=0.05,0.10,0.15$；点线、虚线、实线依图例一一对应。'+'\\\\\n'+r'原曲线为$C(u)=(4u/5,4u(1-u)/5)$，区间仍为$[1/4,3/4]$，区间外所有曲线完全重合。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.20 one alignedABC group after variants paragraph, before summary.')
