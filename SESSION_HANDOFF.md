# Session Handoff — 2026-10-26

Compacted summary of the first design/research session on **Prime Alchemy**: a Roblox action roguelite, Hades-like, 1–4 player co-op, low-poly hand-painted art via Tripo AI. Read this first when resuming on another machine.

## 1. What exists in the repo

| Path | What it is |
|---|---|
| `GameSpec/prime_alchemy_*.md` | The five original design specs: areas/enemies, combat/elements/spells, boons/economy, status effects, co-op. **Corrected this session** (see §3). |
| `GameSpec/hades_feel_reference.md` | **Designer-facing Hades feel reference**: movement, dash, attack frame data and cancels, hit-stop, shake, camera formula and defaults, readability. Includes Roblox implementation notes, stud conversions, and proposed starting values for our LMB/Q/R/E/dash. |
| `Research/hades_feel_teardown.md` | Evidence-level teardown of Hades: data-file values, decompiled engine logic (Ghidra via REA), evidence IDs, open unknowns. |
| `Research/spec_review.md` | **Critical review of our specs (rev 2)**: decisions log, critical gaps, 16 deeper problems, Roblox technical reality, Tripo pipeline, phased build plan, priority checklist. |
| `Research/tools/` | Stdlib Python scripts used for the Hades RE (PDB symbols, config defaults, animation frame tables). See its README. |

## 2. Key Hades findings (the short version)

1. **Movement:** velocity is **assigned**, not accelerated (540 u/s ≈ 13.5 studs/s). Dead stop on stick release. Turning is instant; only the visual turns over ~0.13 s. Overspeed from dash or knockback is steered by force and bled off by linear friction.
2. **Dash:** 0.21 s, ease-in 0 / ease-out 0.8, 0.24 s i-frames, ~10 studs. It cancels attack recovery and ignores slow-mo.
3. **Attacks:** anticipation is collapsed to **one held pose** (sword hit 1 shows 8 of 102 drawn frames), the swing smears at ~7 frames, and the contact pose is held 8–15 frames. Recovery is canceled by any movement. Gameplay locks are tiny: 5 frames hard, then dash-cancelable.
4. **Hit-stop:** 10–50 ms at ~10% speed, 30–70 ms ramp, +40 ms on crit or kill, no stacking, per-weapon cooldown. Most per-swing shake was removed in favour of hit-stop.
5. **Camera:** **rigidly locked** to a weighted tether point, with no follow lag. The only smoothing is the aim lean: zone 800 u, Y × 0.65, camera moves half of it (≤ ~10 studs). Smoothing time constant τ ≈ 0.8 s on mouse and 1.6–2.7 s on controller.
6. **Everything is data-driven** (per-frame hold tables, hit-stop tables, cancel windows). Copy this approach.

## 3. Decisions made by the owner and fixes applied

- Ranged primary attack is **LMB** (all spec references fixed). **RMB is now unassigned.**
- Solo trader stock = **3 items** (1 Big / 1 Normal / 1 Minor). Party scaling lives in the co-op spec §4.
- **Shared single-claim loot is kept.**
- The Wet + Frost reaction is renamed **Deep Chill**; the spell keeps the name **Flash Freeze**.
- The status spec now explicitly flags that stagger/interrupt-based enemy counters depend on an **unspecified Poise/Stagger/CC system**.
- Owner feels 43–62 min runs are long. Analysis: that's comparable to a typical Hades run, but there are 23 stages / ~50 encounters / 6 boss fights and no save. See `spec_review.md` §2.6 for levers.

## 4. Open decisions (next steps, in priority order)

1. **Element-selection input model:** live queue vs **prepared formula slots** (recommended) vs hybrid. Also decide **what E does** (auto-inherit the formula vs a resource cost) and **what RMB becomes** (Q nova, formula radial, or charged shot). Decide **PC-first vs mobile-inclusive**.
2. **Combat commitment:** give Q a cost (meter or charges), lock/cancel windows for LMB, Q and R, an R cast commitment with dash-cancel and partial refund.
3. **Poise/Stagger/CC spec**, plus Lightning **Shock** and Earth **Stagger** statuses in the first implementation.
4. **Feel Spec** with numbers (start from `hades_feel_reference.md` §7).
5. **Third-element balance:** each hero has one "correct" third element (Apprentice and Frog → Earth). **Starting-pair synergy:** Frog's Fire + Water currently self-weakens.
6. Arena-only rooms for v1, room-type variety (elite/challenge/curse/rest/NPC), shorten Area IV.
7. Behaviour-based boons, wider rarity spread, Dash boons.
8. Meta-progression, Heat-like difficulty, hub, retention, cosmetics-only monetization.
9. Save/resume between stages, respawn after the wave instead of spectating, faster revive.

## 5. Recommended build approach (Roblox Studio)

1. **Paper:** settle the decisions in §4 items 1–4.
2. **Graybox combat prototype:**
   - One arena, the Apprentice, three enemies (lunger, kiter, swarmer), all feel features.
   - Test with **100–150 ms simulated latency** (Studio network settings) and 4 clients.
   - Don't build content until it feels responsive and dodges feel honest.
3. **Netcode rules:**
   - Client-predict all player actions and VFX; the server validates and applies damage.
   - Honour dash i-frames using client timestamps within a tolerance.
   - Hit-stop is **local only**.
   - Projectiles: server raycasts with client-only visuals.
4. **Character:** Humanoid WalkSpeed (assigned velocity), `AutoRotate = false`, custom dash/overspeed state, `AnimationTrack:AdjustSpeed(speed/nativeSpeed)`. Camera is Scriptable, updated in `BindToRenderStep` after the character moves.
5. **Tooling:** Rojo + Git, Luau modules, **all tuning in data tables**.
6. **Tripo pilot in parallel:** one enemy end to end (concept → Tripo → cleanup → rig → animate → in-game readability). Time it before committing to the ~33-enemy roster. Rigging and animation are the real cost.
7. **Vertical slice:** Area I + Fallen Captain, three heroes, ~15 boons, hub/lobby, playtests.

## 6. Machine-specific notes (not needed on the main machine)

- On the analysis PC, REA's Ghidra provider uses portable installs: `C:\Tools\ghidra_12.1.4_PUBLIC` and `C:\Tools\jdk-21`, wired through the `rea` server's env in `~/.claude.json`. REA requires Ghidra **12.1.x**. Its Ghidra import doesn't load companion PDBs; use `Research/tools/pdbsyms.py` to map names to addresses.
- Hades build analysed: `EngineWin64s.dll` sha256 `4165a69c…befd`.
