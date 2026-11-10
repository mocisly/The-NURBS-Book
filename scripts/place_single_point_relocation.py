import argparse,re
import image_tex as p
parser=argparse.ArgumentParser();parser.add_argument('number',type=int,choices=(2,3));a=parser.parse_args();n=a.number
d=p.load();e=next(e for e in d['images'] if e['tex']==f'image_tex/ch11/fig_11_{n:02}.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 ?11\.'+str(n)+r'。[^\n]*';s,count=re.subn(pat,'',s,count=1);assert count==1
anchor='对此困境有两种解决方案:'
assert s.count(anchor)==1
# Keep the lead-in to the list intact; put figures after the complete comparison paragraph.
sentence=s.index(anchor)+len(anchor);captions=[r'图 11.'+str(n)+r'. 单控制点$P_3$重新定位，$p=3$、$t_3=0.35$。']
if n==2:captions.append(r'选定$\bar u=0.37$，接近对应节点；实线为原曲线，虚线为修改曲线，细线为实际点位移，彼此平行但长度随参数变化。')
else:captions.append(r'选定$\bar u=0.43$，接近$t_3$与$t_4=0.52$的中点；最大位移发生在选定点左侧，修改表现不对称。')
captions.append(r'两较大圈点为$P=C(\bar u)$与$\widehat P$；其距离精确为$6/5$，方向为单位向量$(7/25,-24/25)$。')
captions.append(r'本组示例采用相同曲线、移动方向和目标距离；控制点与节点数据记录于源码。')
block='\n\n\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
# Insert before the paragraph introducing the comparison, preserving printed order.
if n==2:
    marker='图 11.2 和 11.3 显示了';assert s.count(marker)==1;index=s.index(marker)
else:
    # 11.2 already precedes the discussion. Put11.3 just before that same discussion.
    marker='图 11.2 和 11.3 显示了';assert s.count(marker)==1;index=s.index(marker)
s=s[:index]+block+s[index:]
if n==3:
    old=r'位于 \({t}_{k}\) 和 \({t}_{k + 1}\) 之间的中点';assert s.count(old)==1
    s=s.replace(old,r'接近 \({t}_{k}\) 和 \({t}_{k + 1}\) 之间的中点',1)
f.write_text(s,encoding='utf-8');print('11.'+str(n)+'placedwithpairedcomparison;listandformulaskeptintact.')
