"""Keep all four skinning stages together after compatibility and v parameters."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex') for n in (4,5,6)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.3\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
s=s.replace('460 高级表面构造技术','',1)
anchor='另一种常见的方法是使用所谓的脊曲线';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\par\\vspace{.5cm}\n'+entries[1]['replacement']+'\\par\\vspace{.5cm}\n'+entries[2]['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.3. 蒙皮构造的四个步骤，使用正文给出的五组次数与节点。'+'\\\\\n'+
       r'(a) 原始截面；(b) 精确升阶、节点细化后的相同曲线，每条有$22$个控制点；'+'\\\\\n'+
       r'(c) 沿$v$向三次插值得到的$22\times5$控制网；(d) 插值全部五条截面的曲面。'+'\\\\\n'+
       r'重绘选取平行截面$x=4,2,0,-2,-4$，令$y(u)=-3+6u$，代表性控制高度记录于源码；'+'\\\\\n'+
       r'$\bar v_k$按式(10.8)取控制列弦长参数的均值，节点$V$由参数平均法确定。'+'\\\\\n'+
       r'实心点与虚线表示实际控制点及控制多边形；(d)细线为等参数曲线，粗线为给定截面。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped10.3ABCDafterEq10.8,all original knot definitions uninterrupted;common camera/font;explicit representative data.')
