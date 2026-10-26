"""Minimal MSF 7.0 PDB reader: dumps S_PUB32 public symbols as RVAs.

Usage: python -I pdbsyms.py <pdb> <out.tsv>
"""
import struct
import sys

MAGIC = b"Microsoft C/C++ MSF 7.00\r\n\x1aDS\0\0\0"


def read_pdb(path):
    data = open(path, "rb").read()
    assert data.startswith(MAGIC), "not an MSF 7.0 PDB"
    block_size, _fpm, num_blocks, dir_bytes, _unk, block_map_addr = struct.unpack_from("<6I", data, 32)

    def block(i):
        return data[i * block_size:(i + 1) * block_size]

    dir_block_count = -(-dir_bytes // block_size)
    dir_block_ids = struct.unpack_from(f"<{dir_block_count}I", block(block_map_addr))
    directory = b"".join(block(i) for i in dir_block_ids)[:dir_bytes]

    num_streams = struct.unpack_from("<I", directory)[0]
    sizes = struct.unpack_from(f"<{num_streams}I", directory, 4)
    pos = 4 + 4 * num_streams
    streams = []
    for size in sizes:
        if size == 0xFFFFFFFF:
            streams.append(b"")
            continue
        n = -(-size // block_size)
        ids = struct.unpack_from(f"<{n}I", directory, pos)
        pos += 4 * n
        streams.append(b"".join(block(i) for i in ids)[:size])
    return streams


def main(pdb_path, out_path):
    streams = read_pdb(pdb_path)
    dbi = streams[3]
    # DBI header: sig, ver, age, gsi stream, build, psi stream, pdbdll, symrec stream, ...
    _sig, _ver, _age, _gsi, _build, _psi, _pdbdll, symrec = struct.unpack_from("<iIIHHHHH", dbi, 0)
    (mod_info_size, sec_contrib_size, sec_map_size, src_info_size,
     type_server_size, _mfc, opt_dbg_size, ec_size) = struct.unpack_from("<iiiiiIii", dbi, 24)
    # Optional debug header follows all substreams; index 5 = section headers stream.
    opt_off = 64 + mod_info_size + sec_contrib_size + sec_map_size + src_info_size + type_server_size + ec_size
    opt = struct.unpack_from(f"<{opt_dbg_size // 2}H", dbi, opt_off)
    sec_stream = streams[opt[5]]
    section_rvas = [struct.unpack_from("<I", sec_stream, i * 40 + 12)[0] for i in range(len(sec_stream) // 40)]

    rec = streams[symrec]
    out = []
    off = 0
    while off + 4 <= len(rec):
        reclen, kind = struct.unpack_from("<HH", rec, off)
        if kind == 0x110E:  # S_PUB32: flags, offset, segment, name
            flags, sym_off, seg = struct.unpack_from("<IIH", rec, off + 4)
            name = rec[off + 14:rec.index(b"\0", off + 14)].decode("utf-8", "replace")
            if 1 <= seg <= len(section_rvas):
                out.append((section_rvas[seg - 1] + sym_off, flags, name))
        off += reclen + 2
    with open(out_path, "w", encoding="utf-8") as f:
        for rva, flags, name in sorted(out):
            f.write(f"0x{0x180000000 + rva:x}\t{flags}\t{name}\n")
    print(len(out), "public symbols; sections:", [hex(r) for r in section_rvas])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
