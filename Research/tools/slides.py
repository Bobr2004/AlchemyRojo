import re,sys
txt=open(sys.argv[1],encoding='utf-8',errors='replace').read()
blocks=re.split(r'\n    \{\s*\n',txt)
rows=[]
for b in blocks:
    m=re.search(r'^\s*Name = "([^"]+)"',b,re.M)
    if not m: continue
    name=m.group(1)
    if not re.match(sys.argv[2],name): continue
    sm=re.search(r'Slides = \[(.*?)\n\s*\]',b,re.S)
    ps=re.search(r'PlaySpeed = ([\d.]+)',b); ch=re.search(r'ChainTo = "([^"]+)"',b)
    tm=re.search(r'TimeModifierFraction = ([\d.]+)',b)
    if not sm:
        nf=re.search(r'NumFrames = (\d+)',b)
        rows.append((name,'Book',nf and nf.group(1),ps and ps.group(1),'',ch and ch.group(1),tm and tm.group(1))); continue
    body=sm.group(1)
    # iterate slides + marker comments
    toks=re.findall(r'/\*([^*]*)\*/|\{([^{}]*)\}',body)
    seq=[];marks=[]
    for c,s in toks:
        if c: marks.append((len(seq),c.strip())); continue
        d=re.search(r'DurationFrames = (\d+)',s); seq.append(int(d.group(1)) if d else 1)
    zeros_lead=0
    for d in seq[1:]:
        if d==0: zeros_lead+=1
        else: break
    total=sum(seq)
    hold=max(seq) if seq else 0
    interesting=[f"{i}:{c}" for i,c in marks if not re.match(r'Frame \d+$',c)]
    rows.append((name,f"slides={len(seq)}",f"played_frames={total} ({total/60:.2f}s@60)",f"zero_frames={seq.count(0)} leading_skip={zeros_lead}",f"maxhold={hold}",ch and ch.group(1),tm and tm.group(1),interesting[:6]))
for r in rows: print(r)
