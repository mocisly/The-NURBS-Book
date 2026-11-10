"""Author Fig.1.26 from Fig.1.24 by changing only w01 from 1 to 5."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    a=ROOT/'image_tex/ch01/fig_1_37.tex'; b=ROOT/'image_tex/ch01/fig_1_38.tex'
    if a.exists() or b.exists(): raise FileExistsError('Rational surface sources already exist')
    source=(ROOT/'image_tex/ch01/fig_1_34.tex').read_text(encoding='utf-8')
    for expr in [r'(1-\k/10)^2*3*\s*(1-\s)^2',r'(1-\s)^2*3*(\k/10)*(1-\k/10)^2']:
        assert source.count('{'+expr+'}')==1
        source=source.replace('{'+expr+'}','{5*('+expr+')/(1+4*('+expr+'))}')
    source=source.replace(r'$B_{0,2}(u)B_{1,3}(v)$',r'$R_{0,1}(u,v),\quad w_{0,1}=5$')
    source='% Fig.1.26(a): R01=5f/(1+4f), f=B02(u)B13(v). All other weights are ONE.\n% This is not the constant function that zero other weights would produce.\n'+source[source.index(r'\begin{tikzpicture}'):]
    a.write_text(source,encoding='utf-8')
    source=(ROOT/'image_tex/ch01/fig_1_35.tex').read_text(encoding='utf-8')
    definitions=r'''
  \pgfmathdeclarefunction{rprod}{2}{\pgfmathparse{(1-#1)^2*3*#2*(1-#2)^2}}
  \pgfmathdeclarefunction{ratX}{2}{\pgfmathparse{(2-4*#2+(8/3)*rprod(#1,#2))/(1+4*rprod(#1,#2))}}
  \pgfmathdeclarefunction{ratY}{2}{\pgfmathparse{(4*#1-2-8*rprod(#1,#2))/(1+4*rprod(#1,#2))}}
  \pgfmathdeclarefunction{ratZ}{2}{\pgfmathparse{(bezsurfz(#1,#2)+8.8*rprod(#1,#2))/(1+4*rprod(#1,#2))}}
'''
    needle='+2*#2^3)}}'
    assert source.count(needle)==1
    source=source.replace(needle,needle+definitions)
    source=source.replace(r'({2-4*\s},{4*(\k/4)-2},{bezsurfz(\k/4,\s)})',
                          r'({ratX(\k/4,\s)},{ratY(\k/4,\s)},{ratZ(\k/4,\s)})')
    source=source.replace(r'({2-4*(\k/6)},{4*\s-2},{bezsurfz(\s,\k/6)})',
                          r'({ratX(\s,\k/6)},{ratY(\s,\k/6)},{ratZ(\s,\k/6)})')
    source=source.replace(r'\node[above left] at (P01) {$\mathbf P_{0,1}$};',
                          r'\node[above left] at (P01) {$\mathbf P_{0,1}$};'+'\n'+
                          r'  \node[below left,xshift=-5pt] at (P01) {$w_{0,1}=5$};')
    source='% Fig.1.26(b): same Pij as Fig.1.24(b), only w01=5, all other weights=1.\n% Srat=(S+4*f*P01)/(1+4*f). P01=(2/3,-2,2.2), f=B02*B13.\n'+source[source.index(r'\begin{tikzpicture}'):]
    b.write_text(source,encoding='utf-8')


if __name__=='__main__': main()
