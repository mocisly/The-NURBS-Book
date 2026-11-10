"""10.5actual rigid placement next to normal-plane explanation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_08.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.5\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{22cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.5. 将图 10.4 的同一组截面刚体定位到脊曲线的五个指定参数处。'+'\\\\\n'+
       r'每条截面均满足$C_k(1/2)=C_s(\widehat v_k)$，实心点标出这五个交点。'+'\\\\\n'+
       r'各截面平面与相应脊切向量严格垂直；定位保持截面原有形状和尺寸。'+'\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('10.5rigid placement caption beside normal-plane paragraph,all shared data preserved.')
