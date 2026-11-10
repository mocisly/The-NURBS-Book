"""Place6.3 with surface Newton projection and repair its cosine OCR."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_03.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.3\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
caption=(r'图 6.3. 控制网边上采样点到代表性三次$\times$二次曲面的最近投影。'
         '\\\\\n'+r'虚线为控制网，实线为曲面边界及部分等参线，细线连接184个采样点与迭代求得的最近曲面点。')
block='\\begin{center}\n\\begin{minipage}{20.5cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor=r'\section{曲面切向量反演}';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
# Both OCR copies have a missing residual norm in the first denominator and
# an extraneous surface-position norm in the second. Restore actual cosines.
matches=[m for m in re.finditer(r'\\\[\s*(.*?)\s*\\\]',s,re.S)
         if r'{\epsilon }_{2}' in m[1] and r'{\mathbf{S}}_{u}' in m[1] and r'{\mathbf{S}}_{v}' in m[1]]
assert len(matches)==2
formula=(r'\begin{aligned}'+'\n'+
         r'\frac{|\mathbf S_u(u_i,v_i)\cdot(\mathbf S(u_i,v_i)-\mathbf P)|}{\|\mathbf S_u(u_i,v_i)\|\,\|\mathbf S(u_i,v_i)-\mathbf P\|}&\le\epsilon_2,\\'+'\n'+
         r'\frac{|\mathbf S_v(u_i,v_i)\cdot(\mathbf S(u_i,v_i)-\mathbf P)|}{\|\mathbf S_v(u_i,v_i)\|\,\|\mathbf S(u_i,v_i)-\mathbf P\|}&\le\epsilon_2.'+'\n'+r'\end{aligned}')
for index,m in reversed(list(enumerate(matches))):
    replacement='\\[\n'+formula+(r'\tag{6.8}' if index==0 else '')+'\n\\]'
    s=s[:m.start()]+replacement+s[m.end():]
assert s.count('\n(6.8)\n')==1;s=s.replace('\n(6.8)\n','\n',1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8');print('Grouped6.3 after projection criteria; restored two true zero-cosine tests and6.8 equation tag.')
