# Hades RE helper scripts

Stdlib-only Python scripts used for the Hades teardown. Run with `python -I` and pass paths as arguments. Paths below are for a default Steam install.

| Script | Usage | What it does |
|---|---|---|
| `pdbsyms.py` | `python -I pdbsyms.py <EngineWin64s.pdb> <pubs.tsv>` | Minimal MSF 7.0 reader. Dumps PDB public symbols (S_PUB32) as `address<TAB>flags<TAB>mangled name`, with addresses at image base `0x180000000`. REA's Ghidra import doesn't load companion PDBs, so use this to map names to `FUN_…` addresses. |
| `resolve.py` | `python -I resolve.py <pubs.tsv> 0x1802f7020 …` | Resolves addresses to the nearest public symbol + offset (helpers, `ConfigOptions` globals). |
| `cfgdefaults.py` | `python -I cfgdefaults.py <EngineWin64s.dll> <pubs.tsv> [name-regex]` | Recovers `sgg::ConfigOptions` float/int defaults by scanning `.text` for `mov dword [rip+opt], imm32` stores. |
| `slides.py` | `python -I slides.py <CharacterAnimationsHero.sjson> '<name-regex>'` | Summarizes Slide animations: frames actually shown, skipped (0-duration) frames, holds, chains. |
| `seq.py` | `python -I seq.py <CharacterAnimationsHero.sjson> ZagreusSwordAttack1 …` | Prints the exact shown-frame sequence (`f16x1 … f23x8`) with the animator's marker comments. |

Inputs live under `C:\Program Files (x86)\Steam\steamapps\common\Hades\` (`x64\EngineWin64s.dll`, `x64\EngineWin64s.pdb`, `Content\Game\Animations\*.sjson`). Generated outputs like `pubs.tsv` are derived from the game's files and are intentionally not committed.
