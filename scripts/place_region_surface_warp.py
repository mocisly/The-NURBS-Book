import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images']if e['tex']==f'image_tex/ch11/fig_11_{n}.tex')for n in(25,26)];assert all(e['applied']for e in entries);f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.22\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='注意在图11.23中，该例程处理自相交的多边形。';assert s.count(anchor)==1
caption=r'图 11.22. 用式(11.49)、(11.51)对非凸多边形区域进行曲面变形。'+'\\\\\n'+r'(a) 参数域、区域边界、虚线包围框及实际选中的控制点（+）；(b) 由同一组修改后控制点计算的真实曲面。'+'\\\\\n'+r'代表性原曲面为平面，均匀三次细化后为$35\times35$控制网；归一化弦长参数恰等于节点平均值。'+'\\\\\n'+r'区域内控制点沿$W=(0,0,1)$移动$d=6/5$，曲面经三次基函数平滑过渡，四条外边界保持不变。'+'\\\\\n'+r'曲面变化范围随基函数支撑延伸至多边形外；精确选点、支撑范围和控制数据记录于源码。'
block='\n\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n\\begin{minipage}[c]{17cm}\\centering\n'+entries[0]['replacement']+'\n\\end{minipage}\\hspace{.5cm}\n\\begin{minipage}[c]{19cm}\\centering\n'+entries[1]['replacement']+'\n\\end{minipage}\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n';s=s.replace(anchor,anchor+block,1);f.write_text(s,encoding='utf-8');print('11.22 after complete membership/function definition, paired domain and real surface; restored11.50 S/T definition continuity.')
