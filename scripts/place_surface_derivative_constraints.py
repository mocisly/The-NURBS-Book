import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_47.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
caption=r'图 11.39. 同一曲面的位置与偏导数约束，所选中心点$S(1/2,1/2)$始终固定。'+'\\\\\n'+r'(a) 两个一阶偏导数均增大到原来的2倍；(b) 两个偏导数均按$R_y(-\pi/2)$旋转，保持各自长度。'+'\\\\\n'+r'沿用图11.37的代表性曲面，允许12个局部控制点移动，精确求解位置及两个偏导数共三组约束；四条边界保持不变。'+'\\\\\n'+r'细实线为原曲面，虚线为修改后的实际等参线；实线和虚线箭头分别表示原偏导数与新偏导数，统一缩放为$1/4$。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}'
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.39\.[^\n]*';s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('Placed surface derivative constraint figure39.')
