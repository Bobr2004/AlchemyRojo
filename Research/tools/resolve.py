import bisect,sys
rows=[l.rstrip('\n').split('\t') for l in open(sys.argv[1],encoding='utf-8')]
addrs=[int(r[0],16) for r in rows]
for a in sys.argv[2:]:
    x=int(a,16); i=bisect.bisect_right(addrs,x)-1
    print(f"{a}\t+{x-addrs[i]:#x}\t{rows[i][2]}" if i>=0 else a)
