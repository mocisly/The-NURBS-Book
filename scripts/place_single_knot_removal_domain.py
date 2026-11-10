"""Place9.49next toEx9.4and repair newbasis index-range sentence."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_57.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.49\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
old=re.search(r'Ex9\.4[^\n]*',s).group()
new=r'Ex9.4 见图 9.49。设三次曲线由$\mathbf P_0,\ldots,\mathbf P_{10}$和节点向量$U=\{0,0,0,0,1,2,3,4,5,6,7,8,8,8,8\}$定义。移除单节点$u_7=4$，此时$r=7,s=1$。根据公式 (9.85)，必须为剩余内部节点$1,2,3,5,6,7$重新计算$B_r$；根据公式 (9.84)，必须重新计算新基函数$N_{3,3},N_{4,3},N_{5,3},N_{6,3}$所对应的参数$\bar u_k$索引范围。'
s=s.replace(old,new,1)
block=('\n\n\\begin{center}\n\\begin{minipage}{23cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.49. 将单节点$u_7=4$移除一次；图形尺度、线宽和字号与图 9.48 一致。'+'\\\\\n'+
       r'代表性曲线的中间控制点$\mathbf P_5$恰为左右逆递推候选点$\mathbf P^{\prime}_4,\mathbf P^{\prime}_6$的中点，故移除误差为零。'+'\\\\\n'+
       r'下图为移除前的基函数；虚线$N_{5,3}$的支撑域为$[2,6]$，较图 9.48 的区间更宽。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(new,new+block,1);f.write_text(s,encoding='utf-8')
print('Moved9.49besideEx9.4,samecamera/fontsas9.48;exactcandidate condition andoldbasis support explained;newN3..6indexsentence repaired.')
