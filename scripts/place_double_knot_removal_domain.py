"""Place recovered HTML figure9.48 immediately beside its example."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_48_html.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\hspace\*\{9em\}\s*'+re.escape(e['replacement'])+r'\s*\\hspace\*\{5em\}\s*Figure 9\.48\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
old=re.search(r'Ex9\.3[^\n]*',s).group()
new=r'Ex9.3 见图 9.48。设三次曲线由$\mathbf P_0,\ldots,\mathbf P_{11}$和节点向量$U=\{0,0,0,0,1,2,3,4,4,5,6,7,8,8,8,8\}$定义。移除一次节点$u_8=4$，此时$r=8,s=2$。根据公式 (9.85)，必须为节点$2,3,4,5,6$重新计算$B_r$；根据公式 (9.84)，必须重新计算新基函数$N_{4,3},N_{5,3},N_{6,3}$所对应的参数$\bar u_k$索引范围。'
s=s.replace(old,new,1)
block=('\n\n\\begin{center}\n\\begin{minipage}{23cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.48. 将二重节点$u_8=4$移除一次；上图为按给定节点构造的代表性三次曲线。'+'\\\\\n'+
       r'左右逆递推候选点$\mathbf P^{\prime}_5,\mathbf P^{\prime}_6$精确重合，本例曲线在移除后完全不变。'+'\\\\\n'+
       r'下图为移除前的基函数，虚线$N_{6,3}$的支撑域$[3,6]$给出局部误差可能影响的参数区间。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(new,new+block,1);f.write_text(s,encoding='utf-8')
print('Recovered9.48HTMLreplaced,captionChinese,nativegeometrybesideEx9.3;garbledexample repaired with exact oldknots/r/s/newindexsets.')
