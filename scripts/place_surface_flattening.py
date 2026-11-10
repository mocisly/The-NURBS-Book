import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_33.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.27\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor=r'\subsection{弯曲}';assert s.count(anchor)==1
caption=r'图 11.27. 对图11.8的同一代表性波状曲面作平面展平。'+'\\\\\n'+r'(a) 经实际节点插入细化后的原曲面和参考平面$\pi:z=4/5$；细化不改变曲面。'+'\\\\\n'+r'(b) 仅将平面上方的控制点沿$z$方向投影到$\pi$，其余控制点保持原位。'+'\\\\\n'+r'已核验内部存在整片严格平坦的参数矩形；每片的全部$4\times3$活跃控制点均位于平面，过渡保留简单节点的光滑性。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.27 moved to end of surface-flattening explanation before bending; restored bending formula continuity.')
