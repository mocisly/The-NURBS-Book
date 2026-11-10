"""Group9.58AB/Cafteritsinputsettings;explicitzero-toleranceconstruction."""
import re,json
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n}.tex') for n in (70,71)];assert all(e['applied'] for e in entries)
r=json.loads((p.ROOT/'image_tex/build/local-cubic-spatial-check.json').read_text())
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.58\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
old=re.search(r'零容忍导致了一个插值曲线。[^\n]*',s).group()
new=r'零容差子图采用精确局部插值。本图的代表性数据由两段水平平面曲线和一段空间三次连接段采样得到；每相邻两个采样区间构成一个三次段，共二十五段，五十一个数据点均被精确插值。该构造满足$K_{\max}=20$的跨度限制，不要求其分段数最少。'
s=s.replace(old,new,1)
block=('\\begin{center}\n\\begin{minipage}{35cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\par\\smallskip\n'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.58. 同一组五十一个代表性三维数据点的局部三次逼近；首尾各十七个点分别位于$z=0$、$z=3$平面，中间为非平面连接段。'+'\\\\\n'+
       r'(a)、(b) 按算法 A9.12 分别计算非共面构造或平面点与切向最小二乘拟合，使用四段、五段曲线；最大三维数据距离约$0.09279$、$0.00763$。'+'\\\\\n'+
       r'(c) 为二十五段精确局部插值，全部五十一个点的误差为零；各图通过节点参数调整精确满足$C^1$，统一视角、尺度和字号。'+'\\\\\n'+
       r'实心点为数据，方框为各拟合段端点，虚线为双内部节点 B 样条的实际控制多边形；代表性数据与已知切向均在源码中给出。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(new,block+new,1);s=s.replace('452 曲线和曲面拟合','',1)
f.write_text(s,encoding='utf-8');print('Grouped9.58AB/Caftersettingswithactualdata/errors/C1/globalcontrolpolygoncaption;explicit25pairinterpolation/zeroerror/nonminimality,repairedOCR452.')
