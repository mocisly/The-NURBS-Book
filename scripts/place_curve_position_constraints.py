import re
import image_tex as p
d=p.load();f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');es=[]
for n in (41,42):
    e=next(e for e in d['images']if e['tex']==f'image_tex/ch11/fig_11_{n}.tex');assert e['applied'];es.append(e)
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*'
    s,count=re.subn(pat,'',s,count=1);assert count==1
s,count=re.subn(r'图 11\.35\. 基于约束的曲线修改使用位置约束。[^\n]*\n','',s,count=1);assert count==1
s=s.replace('560 形状修改工具','').replace('图 11.35. (续)','')
s=re.sub(r'最大的\s*在', '最大的在',s)
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+es[0]['replacement']+'\n\\par\\medskip\n'+es[1]['replacement']+'\n\\par\\smallskip\n'+r'图 11.35. 同一三次曲线的位置约束，$u=1/2$，$\Delta D=(0.04,-0.08)$。'+'\\\\\n'+r'(a) 原曲线；(b) 移动$P_2,P_3,P_4,P_5$；(c) 只移动$P_3,P_4$；(d) 只移动$P_3$。'+'\\\\\n'+r'采用正文节点向量和代表性控制多边形，逐例精确求解式(11.76)；三种结果在方框点处满足相同位移。'+'\\\\\n'+r'实线与虚线分别为原曲线和修改结果，细线为相应控制多边形；四图采用相同坐标尺度。'+'\n\\end{minipage}\n\\end{center}\n'
needle='图 11.35c 显示了仅允许';start=s.index(needle);end=s.index('\n',start);s=s[:end]+ '\n\n'+block+s[end:]
f.write_text(s,encoding='utf-8');print('Placed complete 2x2 figure35 after full example; restored split prose.')
