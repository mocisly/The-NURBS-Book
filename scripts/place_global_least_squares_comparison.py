"""Group9.37a/b/c before weighted/constrained fitting, preserving its introduction."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex') for n in (44,45)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.37[。\.][^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
s,n=re.subn('并插值有约束数据\\s+414 曲线和曲面拟合数据与一个','并精确插值有约束数据，使用一个',s,count=1);assert n==1
anchor=r'\subsection{加权和约束最小二乘曲线拟合}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\smallskip\n'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.37. 相同十八个代表性数据点的全局三次最小二乘拟合；(a) 七个、(b) 九个、(c) 十一个控制点。'+'\\\\\n'+
       r'两端均精确插值，其余数据按公式 (9.62) 最小化同参数点的平方距离和；采用公共弦长参数，节点分别按公式 (9.68)、(9.69) 计算。'+'\\\\\n'+
       r'三组平方误差和依次约为$0.5388,0.1732,0.0965$。实线为实际求解的曲线，虚线为控制多边形；空心圆为数据点。'+'\\\\\n'+
       r'各参数尺中的小圆和短刻线分别表示实际数据参数与节点位置；两端四重节点稍微错开。三图采用相同坐标尺度和字体。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.37a/b/c after simple LSfit discussion;removed continuation scan from weighted-fit definitions and repaired OCR414splice.')
