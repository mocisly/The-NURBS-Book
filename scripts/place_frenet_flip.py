"""10.16beside Frenet flip discussion;restore the frame-comparison paragraph."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_23.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.16。[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='前两个问题可以相对容易地解决';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.16. Frenet标架在曲率零点两侧翻转所产生的扫掠退化。'+'\\\\\n'+
       r'选取正则空间五次轨迹，$v=1/2$处曲率为零，$B$的左右极限方向相反。'+'\\\\\n'+
       r'在该点两侧对称放置八个相同截面，并按A10.2进行三次蒙皮。'+'\\\\\n'+
       r'本对称重绘例精确满足$\widehat S(u,1/2)=0$，中间整条截面收缩为原点。'+'\\\\\n'+
       r'粗线为给定截面，细线为真实曲面网格，虚线为参考轨迹；控制数据与标架核验记录于源码。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
needle='显示了如何';pos=s.index(needle)+len(needle);tail=s[pos:]
assert tail.lstrip().startswith(r'\(\mathbf{B}')
s=s[:pos]+' '+tail.lstrip()
f.write_text(s,encoding='utf-8');print('10.16actualdegenerateskin placedbesideFrenetdrawbacks;frame-comparisonparagraphrejoinedafterold15/16scans.')
