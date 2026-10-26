"""Recover ConfigOptions defaults: find `mov dword [rip+rel32], imm32` (C7 05) storing into each option static."""
import re, struct, sys
dll = open(sys.argv[1], 'rb').read()
pe = struct.unpack_from('<I', dll, 0x3c)[0]
nsec = struct.unpack_from('<H', dll, pe + 6)[0]
opt_size = struct.unpack_from('<H', dll, pe + 20)[0]
sec_off = pe + 24 + opt_size
text = None
for i in range(nsec):
    name, vsize, va, rsize, rptr = struct.unpack_from('<8sIIII', dll, sec_off + i * 40)
    if name.rstrip(b'\0') == b'.text':
        text = (va, rptr, rsize)
va, rptr, rsize = text
BASE = 0x180000000
opts = {}
for line in open(sys.argv[2], encoding='utf-8'):
    a, _f, n = line.rstrip('\n').split('\t')
    m = re.match(r'\?(\w+)@ConfigOptions@sgg@@2([MH_N])', n)
    if m:
        opts[int(a, 16)] = (m.group(1), {'M': 'float', 'H': 'int'}.get(m.group(2), 'bool'))
hits = {}
for m in re.finditer(b'\xC7\x05', dll[rptr:rptr + rsize]):
    off = m.start()
    instr = BASE + va + off
    rel, imm = struct.unpack_from('<iI', dll, rptr + off + 2)
    tgt = instr + 10 + rel
    if tgt in opts:
        hits.setdefault(tgt, []).append(imm)
want = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
for tgt, (name, kind) in sorted(opts.items(), key=lambda kv: kv[1][0]):
    if want and not want.search(name):
        continue
    vals = hits.get(tgt)
    if not vals:
        print(f'{name:36s} {kind:5s} (no imm32 store found)')
        continue
    shown = sorted({(round(struct.unpack('<f', struct.pack('<I', v))[0], 4) if kind == 'float' else v) for v in vals}, key=str)
    print(f'{name:36s} {kind:5s} {shown}')
