import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_16.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.14。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='方程 (11.27)-(11.31) 导致了';assert s.count(anchor)==1
caption=r'图 11.14. 同时改变相邻权重$w_4,w_5$，以重心坐标构造实际拉动及辅助线。'+'\\\\\n'+r'在$\bar u=3/5$处，两权重从$1/5$同时增至1，其余权重保持1；实线与虚线为前后曲线。'+'\\\\\n'+r'$R$取两权重均为零的曲线点，$Q=RP\cap P_4P_5$；$A,B,C,D$由式(11.32)的平行投影精确计算。'+'\\\\\n'+r'控制多边形采用与图11.10相同的代表性数据；辅助线、交比与重心坐标均已核验。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);s=s.replace('权重修改 527\n','');f.write_text(s,encoding='utf-8');print('11.14 placed after complete11.31, before construction explanation.')
