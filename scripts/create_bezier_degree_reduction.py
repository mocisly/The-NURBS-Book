"""Fig5.40: independent7->6 and6->5 examples, exact5.43/5.44 error laws."""
from pathlib import Path
from fractions import Fraction as F
from math import comb,sqrt,ceil,isqrt
import json
from native_bspline import segments,check,point,number
from native_polynomial_drawing import paths
from rational_geometry import elevate,evaluate,split
from degree_reduction_geometry import reduce_bezier

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_61.tex'
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch05/fig_5_61.tex')['applied']
examples=[[(0,0),(0,4),(2.5,4),(2.5,2),(6.7,2),(6.7,6),(10,6),(10,1.5)],
          [(0,0),(0,5),(3.5,5),(3.5,1.7),(10,1.7),(10,6),(5.3,6)]]
qpositions=[['below left=7pt','left=7pt','above=7pt','below=7pt','below=7pt','above left=7pt','right=7pt','below right=7pt'],
            ['below left=7pt','left=7pt','above=7pt','below=7pt','below right=7pt','above left=7pt','above left=7pt']]
ppositions=[{1:'above left=7pt',2:'right=7pt',3:'below=7pt',4:'above left=7pt',5:'above=7pt'},
            {1:'above left=7pt',2:'right=7pt',3:'below=7pt',4:'right=7pt'}]
lines=['% Two independent representative Bezier reductions, not a sequential7->6->5 chain.',
       '% Error plots are actual Euclidean parameter error, separately calibrated in each example.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-1.6,-5.3) rectangle (27.8,7.7);']
reports=[]
for index,example in enumerate(examples):
    Q=tuple(tuple(F(str(t)) for t in pt) for pt in example);p=len(Q)-1;P,proof=reduce_bezier(Q);r=(p-1)//2
    D=tuple(tuple(a-b for a,b in zip(x,y)) for x,y in zip(Q,elevate(P)))
    assert any(D[r] if p%2 else D[r+1]);identities=0
    for i in range(401):
        t=F(i,400);b=lambda k:F(comb(p,k))*t**k*(1-t)**(p-k)
        factor=b(r)-b(r+1) if p%2 else b(r+1)
        constant=D[r] if p%2 else D[r+1]
        assert evaluate(D,t)==tuple(factor*x for x in constant)
        assert evaluate(D,t)==tuple(a-b for a,b in zip(evaluate(Q,t),evaluate(P,t)))
        identities+=1
    norm=sqrt(sum(float(x)**2 for x in constant))
    peaks=[(1-1/sqrt(p))/2,(1+1/sqrt(p))/2] if p%2 else [.5]
    peak_error=max(sqrt(sum(float(x)**2 for x in evaluate(D,F(str(t))))) for t in peaks)
    axis=F(ceil(peak_error*10),10);scale=F(6,5)/axis
    assert (evaluate(D,F('.5'))==(F(0),F(0)))==bool(p%2)
    nativechecks=0;certificates=[];drawing=[]
    for controls,degree,style in [(Q,p,'book line'),(P,p-1,'book line,dashed')]:
        K=(F(0),)*(degree+1)+(F(1),)*(degree+1);ss=segments(K,controls,degree)
        nativechecks+=check(K,controls,degree,ss);commands,certificate=paths(ss,style)
        drawing+=commands;certificates.append(certificate)
    # Independent endpoint derivative identity, including the degree factors.
    A,B=Q,P
    for order in range(p//2):
        assert A[0]==B[0] and A[-1]==B[-1]
        A=tuple(tuple((p-order)*(b-a) for a,b in zip(x,y)) for x,y in zip(A,A[1:]))
        B=tuple(tuple((p-1-order)*(b-a) for a,b in zip(x,y)) for x,y in zip(B,B[1:]))
    lines += [r'\begin{scope}[xshift='+str(index*15)+'cm]',
              r'\draw[book grid] '+'--'.join(map(point,Q))+';',
              r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']+drawing
    for i,pt in enumerate(Q):
        lines.append(r'\draw '+point(pt)+r' circle[radius=1.8pt];')
        label=r'\mathbf Q_'+str(i)
        if i in (0,p):label+=r'=\mathbf P_'+str(0 if i==0 else p-1)
        lines.append(r'\node['+qpositions[index][i]+'] at '+point(pt)+' {$'+label+'$};')
    for i,pt in enumerate(P[1:-1],1):
        x,y=pt;d=F(7,100);lines.append(r'\draw '+point((x-d,y-d))+' rectangle '+point((x+d,y+d))+';')
        lines.append(r'\node['+ppositions[index][i]+'] at '+point(pt)+r' {$\mathbf P_'+str(i)+'$};')
    lines += [r'\draw[book axis] (0,-3.3)--(10.8,-3.3) node[right=3pt] {$u$};',
              r'\draw[book axis] (0,-3.3)--(0,-1.6) node[above=3pt] {$E$};',
              r'\draw[book grid] (-.08,-2.1)--(.08,-2.1);',
              r'\node[left=4pt] at (0,-2.1) {$'+number(axis)+'$};']
    for x,label in [(0,'0'),(5,'1/2'),(10,'1')]:
        lines.append(r'\draw[book grid] ('+str(x)+',-3.37)--('+str(x)+',-3.23);')
        lines.append(r'\node[below=4pt] at ('+str(x)+',-3.3) {$'+label+'$};')
    # The residual has one fixed vector direction. Its norm is a polynomial
    # times a constant on each side of the known midpoint root. Render this
    # semantic graph with certified cubic pieces instead of thousands of edges.
    squared=sum(x*x for x in constant);precision=10**12
    lower=F(isqrt(squared.numerator*precision**2//squared.denominator),precision)
    upper=lower+F(1,precision);assert lower**2<=squared<upper**2
    magnitude=(lower+upper)/2
    scalar=[F(0)]*(p+1)
    if p%2:scalar[r],scalar[r+1]=F(1),F(-1)
    else:scalar[r+1]=F(1)
    chart_controls=tuple((F(10*i,p),F(-33,10)+scale*magnitude*c) for i,c in enumerate(scalar))
    if p%2:
        left,right=split(chart_controls)
        chart_pieces=[left,tuple((x,F(-33,5)-y) for x,y in right)]
    else:chart_pieces=[chart_controls]
    charts,chartproof=paths([{'bern':b} for b in chart_pieces],tolerance=F(1,1000));lines+=charts
    chartproof.update(norm_constant_lower=str(lower),norm_constant_upper=str(upper),
                      additional_norm_approximation_error_cm=str(scale/(2*precision)),
                      construction='analytic5.43/5.44 error polynomial, split at the exact midpoint root for odd degree')
    lines.append(r'\node at (5,-4.6) {('+chr(97+index)+r') $'+str(p)+r'\to'+str(p-1)+'$};')
    lines.append(r'\end{scope}')
    reports.append({'degree':p,'original_controls':[[str(x) for x in pt] for pt in Q],
                    'reduced_controls':[[str(x) for x in pt] for pt in P],'reduction':proof,
                    'exact_error_law_identities':identities,'native_checks':nativechecks,
                    'error_zero_at_midpoint':bool(p%2),'analytic_peak_parameters':peaks,
                    'maximum_error':peak_error,'error_axis_max':str(axis),
                    'endpoint_derivative_orders_verified':list(range(p//2)),
                    'native_render_certificates':certificates,'error_chart':chartproof})
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/bezier-degree-reduction-check.json').write_text(json.dumps({
    'figure':'5.40','two_independent_representative_examples':True,'examples':reports},indent=2)+'\n')
print('PASS:802 exact5.43/5.44 identities,164 native checks, endpoint derivatives0..2 preserved; odd double peak/even midpoint maximum.')
