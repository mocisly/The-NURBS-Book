"""Restore the book's code boundaries and verbatim listings from reviewed source ranges.

The original chapters are saved once in tmp/minted-review/before. Without
--apply, write proposed chapters and a change inventory for inspection only.
"""
from pathlib import Path
import argparse, hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'tmp/minted-review'


def original(chapter):
    path = WORK / 'before' / f'{chapter}.tex'
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / f'chapter/{chapter}.tex').read_bytes())
    return path.read_text(encoding='utf-8')


def c_math(text):
    """Decode only the elementary typesetting used inside the chapter 13 C code."""
    text = text.replace(r'\{', '\x01').replace(r'\}', '\x02')
    text = re.sub(r'\\(?:left|right)\b', '', text)
    tokens = {'lbrack':'[','rbrack':']','langle':'<','rangle':'>',
              'cdot':'.','leq':'<=','geq':'>=','neq':'!=','times':'*'}
    for key, value in tokens.items():
        text = re.sub(r'\\'+key+r'\b\s*', lambda m:value, text)
    text = re.sub(r'\\(?:mathrm|operatorname|mathtt|texttt|text)\b\s*', '', text)
    text = re.sub(r'\\[;,!: ]', '', text)
    for old,new in [(r'\&','&'),(r'\_','_'),(r'\%','%')]:text=text.replace(old,new)
    text = text.replace('{','').replace('}','')
    text = text.replace('\x01','{').replace('\x02','}')
    text = re.sub(r'-\s+>', '->', text)
    text = re.sub(r'\+\s+\+', '++', text)
    text = re.sub(r'!\s+=', '!=', text)
    text = re.sub(r'<\s+=', '<=', text)
    text = re.sub(r'>\s+=', '>=', text)
    return text


def c_text(text):
    lines=[]
    for line in text.splitlines():
        line=line.strip()
        if not line or line==r'\HRule': continue
        if re.fullmatch(r'(?:内存分配|错误控制|实用例程)\s+\d+|\d+\s+B-spline.*',line):continue
        line=re.sub(r'\\hspace\*?\{[^}]+\}\s*','',line)
        line=re.sub(r'\\section\*\{(.*?)\}',r'\1',line)
        line=re.sub(r'\\\((.*?)\\\)',lambda m:c_math(m[1]),line)
        for old,new in [(r'\#','#'),(r'\_','_'),(r'\&','&'),(r'\%','%'),(r'\{','{'),(r'\}','}')]:
            line=line.replace(old,new)
        line=line.translate(str.maketrans({'；':';','，':','}))
        line=re.sub(r'/\s+\*','/*',line);line=re.sub(r'\*\s+/','*/',line)
        lines.append(line)
    return '\n'.join(lines)


def indent_c(code):
    """Indent scopes and brace-free nested loops without changing their statements."""
    lines=[l.strip() for l in code.splitlines()if l.strip()];result=[]
    def emit(line,level):
        if line.startswith('#'):level=0
        if re.match(r'\w+:$',line):level=max(0,level-1)
        result.append('    '*level+line)
    def statement(i,level):
        line=lines[i];scan=re.sub(r'/\*.*?\*/','',line).strip()
        if scan.startswith('{') and not '}' in scan:
            emit(line,level);i+=1
            while i<len(lines) and not lines[i].startswith('}'):i=statement(i,level+1)
            if i<len(lines):emit(lines[i],level);i+=1
            return i
        control=bool(re.fullmatch(r'(?:for|while|if)\s*\(.*\)|else',scan))
        emit(line,level);i+=1
        if control:
            # Explanatory comment lines do not consume a loop/if body.
            while i<len(lines)and lines[i].startswith('/*'):
                emit(lines[i],level+1);i+=1
            if i<len(lines)and not lines[i].startswith('}'):
                i=statement(i,level if lines[i].startswith('{')else level+1)
            if scan.startswith('if')and i<len(lines)and lines[i].startswith('else'):
                i=statement(i,level)
        elif line.endswith(','):
            while i<len(lines)and lines[i-1].endswith(','):
                emit(lines[i],level+1);i+=1
        if not control and scan.startswith('if')and i<len(lines)and lines[i].startswith('else'):
            i=statement(i,level)
        return i
    i=0
    while i<len(lines):i=statement(i,0)
    return '\n'.join(result)


# Inclusive line ranges in the saved, pre-migration chapter 13. These include
# whole routines across old page headers, and include braces outside HRule pairs.
C_RANGES=[
 (91,107,'scalar-types'),(111,115,'index-type'),(123,135,'numeric-limits'),
 (147,151,'curve-prototype'),(179,207,'point-records'),(240,246,'sentinels'),
 (252,274,'polygon-knot-records'),(300,314,'curve-record'),(330,344,'object-access'),
 (350,364,'net-record'),(381,399,'surface-record'),(425,457,'malloc-example'),
 (479,519,'session-sketch'),(523,543,'stack-record'),(560,680,'S_getc2d'),
 (684,706,'allocation-node-records'),(712,766,'N_enurbs'),(790,804,'call-hierarchy'),
 (823,835,'error-record'),(839,857,'error-defines'),(861,865,'error-global'),
 (869,885,'E_seterr'),(889,935,'E_kntdef'),(941,1033,'E_curdef'),
 (1039,1085,'E_curwei'),(1097,1137,'E_curinp'),(1147,1171,'U_makcu1'),
 (1175,1235,'U_makp12'),(1239,1293,'U_makcu3'),(1299,1359,'U_maksu2'),
 (1368,1386,'A_initcp'),(1392,1422,'A_updcpt'),(1426,1470,'A_euclid'),
 (1481,1559,'N_evncur'),(1587,1653,'curve-driver'),(1657,1773,'N_evnsur'),
 (1785,1853,'surface-driver'),(1863,1887,'scalar-records'),(1893,1921,'polynomial-records'),
 (1925,1951,'domain-records'),(1957,1979,'bezier-records'),(1985,2011,'vector-line-records'),
 (2015,2039,'plane-circle-records'),(2043,2061,'matrix-record'),(2065,2079,'matrix-enum')
]


def restore_c(code,name):
    # Unambiguous OCR repairs, cross-checked against the declarations and uses
    # within each listing. These do not redesign allocation/error algorithms.
    code=code.replace('!==','!=')
    code=re.sub(r'!\s+=', '!=', code)
    code=re.sub(r'(?<!\w)(NOZ|NOW)\b',r'_\1',code)
    code=code.replace('标记错误;', 'FLAG error;')
    if name=='curve-prototype':code=code.rstrip()+';'
    if name=='S_getc2d':
        code=code.replace('1 = 0 ;','l = 0;').replace('S->c2d = c2d','S->c2d = c2d')
        code=re.sub(r'S\s*->\s*c2\s*d\s*=\s*c2\s*d','S->c2d = c2d',code)
    if name=='N_enurbs': code=code.replace('KNTNODE *krp;', 'KNTNODE *knp;')
    if name=='U_makcu3':
        code=re.sub(r'Pw = S - getcpa\(\s*wx,\s*wy,\s*wz,\s*w,\s*n,\s*S\s*\)', 'Pw = S_getcpa(wx, wy, wz, w, n, S)',code)
    if name=='U_maksu2': code=code.replace('DEGREE P,','DEGREE p,').replace('INDEX S,','INDEX s,')
    if name=='N_evncur':code=re.sub(r'N = S_\s*-\s*getr1d\s*\(', 'N = S_getr1d(',code)
    if name=='curve-driver':code=code.replace('CURVE CUR;', 'CURVE cur;')
    if name=='surface-driver':code=code.replace('SURFACE SUR;', 'SURFACE sur;')
    if name=='N_evnsur':
        # The opening preprocessor line was attached to the preceding prose.
        code=code[code.index('#include'):]
        code=code.replace('#include "nurbs.h" static STRING', '#include "nurbs.h"\nstatic STRING')
    return code


def chapter13(source):
    lines=source.splitlines(keepends=True); replacements=[]; records=[]
    for start,end,name in C_RANGES:
        old=''.join(lines[start-1:end]);code=restore_c(c_text(old),name)
        language='text' if name=='call-hierarchy' else 'c'
        code=indent_c(code) if language=='c' else '\n'.join('    '*(1 if i in [1,2,3,4] else 2 if i==5 else 0)+s for i,s in enumerate(code.splitlines()))
        assert '\\' not in code,(name,code)
        prefix=''
        if name=='N_evnsur':prefix=old.split(r'\#include',1)[0].strip()+'\n\n'
        new=prefix+f'% book-code: {name}\n\\begin{{minted}}{{{language}}}\n{code}\n\\end{{minted}}\n'
        replacements.append((start,end,new));records.append(dict(chapter=13,name=name,original_lines=[start,end],language=language,lines=len(code.splitlines())))
        (WORK/'listings').mkdir(parents=True,exist_ok=True)
        (WORK/'listings'/f'13-{name}.{ "c" if language=="c" else "txt"}').write_text(code+'\n',encoding='utf-8')
    for start,end,new in reversed(replacements):lines[start-1:end]=[new]
    result=''.join(lines)
    result=re.sub(r'^\\HRule\s*\n','',result,flags=re.M)
    result=result.replace(r'\section*{612 B-spline Programming Concepts}'+'\n','')
    result=re.sub(r'^\d+\s+B-spline 编程概念\s*\n','',result,flags=re.M)
    # These old page separators interrupted continuous explanatory paragraphs.
    result=re.sub(r'(?m)^\\hspace\*\{1em\} (?=(?:These routines|As mentioned earlier|The next test program|The input checking routine))','',result)
    for start,end in [('As a practical matter,','constructed from curves.'),
                      ('As mentioned earlier,','The rest of the code deals with the'),
                      ('The next test program shows','know that memory allocation is required.'),
                      ('These routines are used','curve and surface evaluations.')]:
        result=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda m:re.sub(r'\s*\n\s*',' ',m[0]),result,flags=re.S)
    return result,records


# Algorithm labels and inclusive boundaries were checked against the surrounding
# prose and figures. Several end braces are outside the old horizontal rules.
ALGORITHMS={
 1:[(227,247,1),(542,572,2),(587,627,3),(645,663,4),(760,788,5),(1259,1279,6),(1392,1432,7)],
 2:[(889,923,1),(1022,1064,2),(1176,1312,3),(1370,1448,4),(1537,1661,5)],
 3:[(48,72,1),(352,386,2),(588,622,3),(664,706,4),(808,848,5),(1028,1100,6),(1230,1284,7),(1288,1356,8)],
 4:[(217,243,1),(357,385,2),(617,659,3),(797,847,4)],
 5:[(398,458,1),(490,542,2),(602,691,3),(866,948,4),(952,1050,5),(1242,1336,6),(1378,1484,7),(1787,1913,8),(2423,2649,9),(2669,2756,10),(3052,3248,11)],
 6:[(1862,1922,1),(2134,2190,2)],
 7:[(1046,1146,1),(1259,1321,2),(1421,1523,3)],
 8:[(358,486,1),(1044,1070,2)],
 9:[(279,325,1),(467,513,2),(701,769,3),(823,863,4),(1527,1649,5),(2030,2178,6),(2272,2328,7),(2457,2523,8),(2571,2639,9),(2645,2699,10),(2927,3015,11),(3278,3424,12)],
 10:[(547,649,1),(651,711,2),(1089,1127,3),(1420,1484,4)],
 11:[(1822,1940,1)],12:[(149,213,1),(523,583,2)]
}


def algorithm_code(text,name):
    # Move comment delimiters that OCR incorrectly included in mathematics
    # back into the C token stream, so comments do not swallow later code.
    inline=r'((?:(?!\\\)).)*?)'
    text=re.sub(r'\\\('+inline+r'\s*\*\\\)\s*/',lambda m:r'\('+m[1]+r'\) */',text,flags=re.S)
    text=re.sub(r'\\\('+inline+r'\s*\*\s*/\\\)',lambda m:r'\('+m[1]+r'\) */',text,flags=re.S)
    text=re.sub(r'\\\('+inline+r'/\s*\*\\\)',lambda m:r'\('+m[1]+r'\) /*',text,flags=re.S)
    text=re.sub(r'^\s*\\HRule\s*$', '',text,flags=re.M)
    text=re.sub(r'^.*(?:ALGORITHM|算法)\s*A\d+\.\d+.*$', '',text,flags=re.M)
    text=re.sub(r'\\hspace\*?\{[^}]+\}\s*','',text)
    text=re.sub(r'\\(?:noindent)?\\?begin\{minipage\}\{[^\n]+\}\s*','',text)
    text=re.sub(r'\\end\{minipage\}|\\vspace\*?\{[^\n]+\}', '',text)
    # Old printed running headers inside algorithm continuations.
    text=re.sub(r'^\s*\d+\s+(?:B.?样条|B-spline|NURBS|曲线|曲面).*$','',text,flags=re.M)
    allowed={'left','right','lbrack','rbrack','mathrm','operatorname','mathtt','texttt','text','leq','geq','neq','cdot','times'}
    def math(m):
        value=m[1].strip(); commands=set(re.findall(r'\\([A-Za-z]+)',value))
        if commands<=allowed and not re.search(r'(?<!\\)[_^]',value):
            simple=c_math(value.replace(r'\cdot',r'\times'))
            if '\\' not in simple:return simple
        # Preserve actual mathematics instead of inventing equivalent C.
        return '@$'+re.sub(r'\s+',' ',value)+'$@'
    text=re.sub(r'\\\[(.*?)\\\]',math,text,flags=re.S)
    text=re.sub(r'\\\((.*?)\\\)',math,text,flags=re.S)
    for old,new in [(r'\#','#'),(r'\_','_'),(r'\&','&'),(r'\%','%'),(r'\{','{'),(r'\}','}')]:
        # Escape spans contain real TeX and must keep their own escapes intact.
        parts=re.split(r'(@[^@]*@)',text)
        text=''.join(p if p.startswith('@') else p.replace(old,new) for p in parts)
    result=[];in_comment=False
    for line in text.splitlines():
        line=line.strip()
        if not line:continue
        parts=re.split(r'(@[^@]*@)',line)
        line=''.join(p if p.startswith('@') else re.sub(r'\*\s+/', '*/',re.sub(r'/\s+\*','/*',p)) for p in parts)
        # mathescape handles formulae inside comments; escapeinside handles code.
        if in_comment or '/*' in line:
            # Only formulae after the comment opener use the comment route.
            split=line.find('/*') if not in_comment else 0
            line=line[:split]+re.sub(r'@\$(.*?)\$@',r'$\1$',line[split:])
        if '/*' in line:in_comment=True
        if '*/' in line:in_comment=False
        if not in_comment and not '/*' in line:
            # The C lexer treats Chinese algorithm instructions as error tokens.
            # Pass their glyphs through TeX while keeping mathematical escapes.
            parts=re.split(r'(@[^@]*@)',line)
            line=''.join(p if p.startswith('@') else re.sub(r'[\u3400-\u9fff]+',lambda m:'@'+m[0]+'@',p) for p in parts)
        result.append(line)
    code='\n'.join(result)
    parts=re.split(r'(@[^@]*@|\$[^$]*\$)',code)
    for i,p in enumerate(parts):
        if p.startswith(('@','$')):continue
        p=re.sub(r'=\s+=','==',p);p=re.sub(r'!\s+=','!=',p)
        p=re.sub(r'\|\s+\|','||',p);p=re.sub(r'&\s+&','&&',p)
        p=re.sub(r'\+\s+\+','++',p);p=re.sub(r'-\s+>','->',p)
        p=p.translate(str.maketrans({'；':';','，':',','。':'.','：':':','、':',','（':'(','）':')','’':"'"}))
        parts[i]=p
    code=''.join(parts)
    # OCR sometimes replaced an opening C brace with a long, unrelated list
    # of zero-valued knots. Restore the scope indicated by its existing close.
    if name in ['A2.5','A3.4']:
        code=re.sub(r'@\$\\begin\{cases\}.*?\\end\{cases\}\$@','{',code,flags=re.S)
    if name=='A2.1':code=code.replace('mid = (low+high)/2;\n{\nreturn(mid);','mid = (low+high)/2;\n}\nreturn(mid);')
    if name=='A1.7':code=code.replace('/* Output: S\n','/* Output: S */\n')
    if name=='A10.4':code=code.replace('/* Create bicubically blended Coons surface. *\n','/* Create bicubically blended Coons surface. */\n')
    if name=='A2.4':
        code=re.sub(r'if @\$.*?\$@\n\(i == m-p-1 && u == U\[m\]\)\) /\* cases \*/',
                    'if ((i == 0 && u == U[0]) ||\n    (i == m-p-1 && u == U[m])) /* Special cases */',code,flags=re.S)
    if name=='A2.5':
        code=re.sub(r'^if \( u\).*$', 'if (u >= U[i+j] && u < U[i+j+1]) N[j][0] = 1.0;',code,flags=re.M)
        code=re.sub(r'if @\$.*?N\\left\\lbrack j\\right\\rbrack \\left\\lbrack 0\\right\\rbrack = \{1\.0\}\$@ ;',
                    'if (u >= U[i+j] && u < U[i+j+1]) N[j][0] = 1.0;',code)
    if name=='A5.2':code=code.replace('C = Rw[0]/w;','}\nC = Rw[0]/w;')
    if name=='A6.1':code=code.replace('M[i][i] = bin[p][i];','{\nM[i][i] = bin[p][i];')
    if name=='A9.5':code=code.replace('{ /* through ( n + 1) ( m + 1) points */','/* through ( n + 1) ( m + 1) points */')
    if name in ['A3.6','A3.8']:
        # l is the v-derivative loop index in SKL[k][l]; OCR read it as 1.
        code=code.replace('SKL[k][1]','SKL[k][l]')
        code=code.replace('for ( 1 = 0;1 <= d - k;1 ++ )','for (l=0; l<=d-k; l++)')
    if name=='A10.1':
        code=re.sub(r'^.*minimum parameter value\.$',r'Set @$\\bar v_0$@ to the minimum parameter value of @$\\mathbf{T}(v)$@.',code,flags=re.M)
        code=re.sub(r'^.*maximum parameter value\.$',r'Set @$\\bar v_{\\mathrm{nsect}-1}$@ to the maximum parameter value of @$\\mathbf{T}(v)$@.',code,flags=re.M)
        code=code.replace(" 's knot vector", " @'s@ knot vector")
        code=re.sub(r'/\*.*?\*/',lambda m:m[0].replace("@'s@","'s"),code,flags=re.S)
    return indent_c(code)


def algorithm_chapter(number,source):
    lines=source.splitlines(keepends=True);changes=[];records=[]
    for start,end,index in ALGORITHMS[number]:
        old=''.join(lines[start-1:end]);name=f'A{number}.{index}'
        assert re.search(r'(?:ALGORITHM|算法)\s*'+re.escape(name),old),name
        code=algorithm_code(old,name)
        new=f'% book-code: algorithm {name}\n\\par\\medskip\\noindent\\textbf{{算法 {name}（伪代码）}}\\par\n\\begin{{minted}}[escapeinside=@@,mathescape]{{c}}\n{code}\n\\end{{minted}}\n'
        changes.append((start,end,new));records.append(dict(chapter=number,name=name,original_lines=[start,end],language='c',kind='pseudocode',lines=len(code.splitlines())))
        (WORK/'listings'/f'{name}.txt').write_text(code+'\n',encoding='utf-8')
    if number==5:
        for start,end,name in [(2403,2421,'degree-elevation-work-arrays'),(2828,2842,'degree-reduction-sketch'),(3034,3048,'degree-reduction-work-arrays')]:
            code=algorithm_code(''.join(lines[start-1:end]),name)
            new=f'% book-code: {name}\n\\begin{{minted}}[escapeinside=@@,mathescape]{{c}}\n{code}\n\\end{{minted}}\n'
            changes.append((start,end,new));records.append(dict(chapter=5,name=name,original_lines=[start,end],language='c',kind='pseudocode-fragment',lines=len(code.splitlines())))
    changes.sort()
    for start,end,new in reversed(changes):lines[start-1:end]=[new]
    result=''.join(lines)
    if number==1:
        # This old wrapper held algorithm A1.3 and its accompanying table.
        result=result.replace('\\noindent\\begin{minipage}{\\linewidth}\n算法 A1.3 计算','算法 A1.3 计算',1)
        result=result.replace('\\end{center}\n\\end{minipage}\n\\par\\medskip\n\n\\hspace*{2em} Algorithm A1.4','\\end{center}\n\\par\\medskip\n\nAlgorithm A1.4',1)
    if number==3:result=result.replace('\\HRule\n\n\\}'+ '\n\n算法 A3.8','\\}\n\n算法 A3.8')
    if number in [2,5,6]:result=re.sub(r'^\\HRule\s*\n','',result,flags=re.M)
    return result,records


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    if not (WORK/'before').exists()and all('% book-code:'in(ROOT/f'chapter/{n}.tex').read_text(encoding='utf-8')for n in range(1,14)):
        print('Already migrated. Edit the minted blocks in chapter/*.tex directly; no files changed.')
        return
    WORK.mkdir(parents=True,exist_ok=True);out=WORK/'proposed';out.mkdir(exist_ok=True)
    records=[]
    state_path=WORK/'applied-hashes.json'
    state=json.loads(state_path.read_text(encoding='utf-8'))if state_path.exists()else {}
    for n in [13]+list(ALGORITHMS):
        source=original(n)
        updated,items=chapter13(source) if n==13 else algorithm_chapter(n,source)
        records+=items
        (out/f'{n}.tex').write_text(updated,encoding='utf-8')
        if args.apply:
            current=ROOT/f'chapter/{n}.tex'
            assert current.read_text(encoding='utf-8') in [source,updated]or hashlib.sha256(current.read_bytes()).hexdigest()==state.get(str(n)),f'Concurrent edits: {n}'
            current.write_text(updated,encoding='utf-8')
            state[str(n)]=hashlib.sha256(current.read_bytes()).hexdigest()
    if args.apply:state_path.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
    (WORK/'inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(records)} reviewed-boundary listings; '+('applied' if args.apply else 'proposals only'))


if __name__=='__main__': main()
