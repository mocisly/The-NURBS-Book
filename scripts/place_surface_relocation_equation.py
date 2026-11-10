import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_08.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pattern=r'\(11\.14\)\s*\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}'
block='\\[\n'+e['replacement']+'\n\\tag{11.14}\n\\]\n\n';s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1;assert s.count(r'\tag{11.14}')==1
f.write_text(s,encoding='utf-8');print('Restored11.14asnativedisplayequationafter11.13;removedbareOCRnumber/centeredscan.')
