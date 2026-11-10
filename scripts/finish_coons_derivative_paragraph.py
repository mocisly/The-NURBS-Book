from pathlib import Path
import re
f=Path(__file__).resolve().parents[1]/'chapter/10.tex';s=f.read_text(encoding='utf-8')
pattern=r'(必须成立。)(\s*\\begin\{center\}\s*\\begin\{minipage\}\{27cm\}.*?\\end\{minipage\}\s*\\end\{center\})(\s*\\\(\{\\mathbf\{T\}\}.*?四个扭转向量。)'
match=re.search(pattern,s,re.S);assert match
s=s[:match.start()]+match[1]+' '+match[3].strip()+match[2]+'\n\n'+s[match.end():];f.write_text(s,encoding='utf-8');print('Joinedtwistdefinitionbefore26figure.')
