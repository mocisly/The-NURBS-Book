import re
import image_tex as p
d=p.load();f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');entries=[]
for n in (9,10):
    e=next(e for e in d['images'] if e['tex']==f'image_tex/ch11/fig_11_{n:02}.tex');assert e['applied'];entries.append(e)
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.8\.[^\n]*';s,count=re.subn(pat,'',s,count=1);assert count==1
anchor='类似于曲线情况，节点插入可以用来限制';assert s.count(anchor)==1
captions=[r'图 11.8. 按式(11.10)—(11.11)移动曲面控制点$P_{4,3}$，选定$\bar u=\bar v=0.55$。',r'(a) 代表性三次$u$、二次$v$曲面的$9\times7$控制网，圈点与箭头表示原控制点及其实际移动；',r'(b) 原曲面的细网格、修改后局部等参数虚线及同参数点的实际位移箭头，两个圈点的距离精确为$3/5$。',r'只有$P_{4,3}$移动，故$\widehat S-S=N_{4,3}(u)N_{3,2}(v)\alpha(0,0,1)$；位移方向相同，大小随基函数变化。',r'变化范围为$[.2,.9)\times[.2,.8)$，外部整片曲面保持不变；两图同投影、尺度、字号，控制数据记录于源码。']
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\hspace{1cm}'+entries[1]['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.8ABplacedtogetherafter11.14andintro;precisewhole-supportdisplacementcaption.')
