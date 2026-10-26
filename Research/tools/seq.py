import re,sys
txt=open(sys.argv[1],encoding='utf-8',errors='replace').read()
for name in sys.argv[2:]:
    i=txt.index(f'Name = "{name}"\n'); b=txt[i:txt.index('\n    }',i)]
    body=re.search(r'Slides = \[(.*)\]',b,re.S).group(1)
    seq=[];out=[]
    for c,s in re.findall(r'/\*([^*]*)\*/|\{([^{}]*)\}',body):
        if c:
            if not re.match(r'Frame \d+$',c.strip()): out.append(f'<{c.strip()}>')
            continue
        d=re.search(r'DurationFrames = (\d+)',s); d=int(d.group(1)) if d else 1
        if d: out.append(f'f{len(seq)}x{d}')
        seq.append(d)
    print(name,':',' '.join(out))
