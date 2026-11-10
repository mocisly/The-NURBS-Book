import re
import image_tex as p
d=p.load();f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');es=[]
for n in (43,44):
    e=next(e for e in d['images']if e['tex']==f'image_tex/ch11/fig_11_{n}.tex');assert e['applied'];es.append(e)
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*'
    s,count=re.subn(pat,'',s,count=1);assert count==1
s,count=re.subn(r'图11\.36\. 基于约束的曲线修改，[^\n]*\n','',s,count=1);assert count==1
s=s.replace('562 形状修改工具','').replace('图11.36. (续)','')
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+es[0]['replacement']+'\n\\par\\medskip\n'+es[1]['replacement']+'\n\\par\\smallskip\n'+r'图 11.36. 同一三次曲线在$u=0.556$处的导数约束，$D=C^{\prime}(u)$。'+'\\\\\n'+r'(a) 允许$P_3,P_4,P_5$移动，使$\widehat D=1.6D$；(b) 仅允许$P_4$移动，仍满足$\widehat D=1.6D$，但所选点发生位移。'+'\\\\\n'+r'(c) 允许$P_3,P_4$移动，同时保持$C(u)$不变并使$\widehat D=0.6D$。'+'\\\\\n'+r'沿用图11.35的代表性控制多边形；按式(11.76)精确求解，箭头以相同的$1/4$比例表示实际导数。'+'\\\\\n'+r'实线为原曲线，虚线为修改结果；三图采用相同坐标尺度，方框标出施加约束的曲线点。'+'\n\\end{minipage}\n\\end{center}\n'
needle='最后，我们提到Fowler和Bartels';start=s.index(needle);end=s.index('\n',start);s=s[:end]+'\n\n'+block+s[end:]
f.write_text(s,encoding='utf-8');print('Placed full ABC group before surface section, same curve and derivative arrow scale.')
