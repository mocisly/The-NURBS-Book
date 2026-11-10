import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_31.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.25\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='最后，我们提醒注意，只有当投影结果至少为';assert s.count(anchor)==1
caption=r'图 11.25. 对同一条细化抛物线投影到相交直线$L:y=3/4$，比较两种选点规则。'+'\\\\\n'+r'(a) 原曲线、控制网和沿$W=(0,-1)$的实际投影；(b) 投影所有位于$L$上方的控制点。'+'\\\\\n'+r'(c) 仅投影支撑完全位于$[u_s,u_e]=[1/4,3/4]$内的控制点：外部曲线严格不变，但端部出现凸起。'+'\\\\\n'+r'点线为原曲线；两种结果均含精确直线段，已逐区间核验其纵坐标多项式恒为$3/4$。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.25 comparison after complete selection-rule explanation, before straight-span condition.')
