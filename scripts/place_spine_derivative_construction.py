"""10.6 keep derivative diagram and full explanation together."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_09.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.6\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.6. 沿用图 10.4、10.5 的数据计算蒙皮导数。'+'\\\\\n'+
       r'(a) 脊交点$P_k$、脊切向量$D_k$及相邻交点弦长$d_k$；细线为定位后的截面。'+'\\\\\n'+
       r'(b) 截面$k=1$的实际控制多边形与七个导数$D_{i,1}$，选标其中三个。'+'\\\\\n'+
       r'所有导数均按式(10.10)、(10.11)由正距离比缩放对应脊切向量，箭头共用$1/12$显示比例。'+'\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('10.6two explanatory panels grouped after10.11,actual shared data/consistent arrow scale.')
