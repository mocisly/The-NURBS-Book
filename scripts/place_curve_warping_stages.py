import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images']if e['tex']==f'image_tex/ch11/fig_11_{n}.tex')for n in(21,22)];assert all(e['applied']for e in entries);f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.19\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='改变定义参数的效果在图 11.20a-11.20c 中得以展示。';assert s.count(anchor)==1
caption=r'图 11.19. 曲线变形的实际计算步骤（同一代表性抛物线，$u_s=1/4,u_e=3/4$）。'+'\\\\\n'+r'(a) 原三次曲线和指定方向$W=(0,-1)$、上限$d=3/5$；(b) 区间内三轮中点细化，曲线完全不变。'+'\\\\\n'+r'(c) 按控制多边形累积弦长确定$t_i$，以$w_3=1$应用式(11.48)；点线为原曲线。'+'\\\\\n'+r'(d) 在全曲线误差预算$\varepsilon=1/200$内实际移除节点；误差以公共基函数系数给出严格上界。'+'\\\\\n'+r'两端区间外的曲线始终完全保持不变；全部控制点、细化和移除记录见源码。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+'\n\\par\\medskip\n'.join(e['replacement']for e in entries)+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.19 AB/CD one aligned group after four-stage explanation, before parameter variants.')
