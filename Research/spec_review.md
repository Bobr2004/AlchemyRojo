# Prime Alchemy — Spec Review Against the "Feels Like Hades" Goal

**Reviewed:** the five `GameSpec/*.md` files, 2026-10-26 (revision 2).
**Lens:** fast action with a deep, high-skill-ceiling combat system, on Roblox, with Tripo AI low-poly hand-painted art. Hades numbers come from [`GameSpec/hades_feel_reference.md`](../GameSpec/hades_feel_reference.md) (evidence in [hades_feel_teardown.md](hades_feel_teardown.md)).

## Decisions recorded and fixes applied (rev 2)

| Item | Decision / fix |
|---|---|
| Primary ranged attack | It's **LMB**. All 17 "RMB" references in the specs were changed to LMB. **RMB is now unassigned** (see §3.6). |
| Solo trader | **3 items (1 Big / 1 Normal / 1 Minor)**. The areas and boons specs now match the co-op table and point to it for party scaling. |
| Shared single-claim loot | **Kept** (owner's call). Previous objection withdrawn. |
| Flash Freeze name clash | The reaction is renamed **Deep Chill**; the spell keeps "Flash Freeze". |
| Stagger/interrupt dependency | The status spec now states that the enemy counters depend on an unspecified Poise/Stagger/CC system. The system itself is still to be designed (§2.3). |

---

## 1. Verdict

The specs are a strong **systems** design: clear rules, explicit numbers, deterministic reactions, honest TBD lists, a careful co-op loot model. But they specify **what spells do**, not **how fighting feels**. These are all absent or undecided:
- Action commitment and cancel windows.
- Dash frames and i-frames.
- Hit-stop.
- Hit reactions.
- Telegraph timing.
- The camera.
- Latency handling.

The current input model also points at **Magicka rather than Hades**: live 3-slot combining while dodging, plus spammable novas. Pick one on purpose. The biggest risk outside the specs is **Roblox's network model**, which has to be engineered for honest dodges from day one.

---

## 2. Critical gaps

### 2.1 Element selection input is undefined, and it's the core interaction
Nothing says what keys select elements, whether the formula persists or clears after casting, how to change one slot, or how any of it works on gamepad or touch.

| Model | Feel | Skill expression | Mobile |
|---|---|---|---|
| A. Live queueing (Magicka) | Chaotic, improvisational | Execution + knowledge, very high ceiling | Not feasible |
| B. **Prepared formula slots** (recommended) | Hades-like readability | Strategy between encounters, execution in combat | Feasible |
| C. Hybrid | Two or three quick-swap presets (keys or a radial), plus live editing on PC | Both | Feasible with radial |

### 2.2 The primary is ranged LMB, and nothing has commitment
With LMB as the ranged attack, the remaining issues are:
- **Q is a free point-blank AoE on a 0.5 s cooldown.** If its damage is anywhere near LMB's, the dominant play is to stand in the crowd and spam Q. Give Q a **cost**: a reagent meter built by LMB hits, or 2–3 charges with recharge. That creates Hades' attack → special → cast rhythm and makes LMB matter.
- **No startup, lock or cancel windows** on LMB, Q or R. Hades' skill ceiling lives in a ~5-frame lock followed by a dash-cancelable window. Define them. Starting values are in `hades_feel_reference.md` §7.
- **R needs a cast commitment**: a short pose-hold cast. Dashing cancels it and refunds part of the cooldown.
- **Ranged-only combat feels floatier.** Lean harder on per-hit hit-stop for LMB (the ranged weapon in Hades uses 30% for 20 ms), contact holds on Q, and heavy shake only for R.
- Add positional bonuses (point-blank Q bonus, dash-shot) so movement earns damage, not just survival.

### 2.3 Poise/Stagger/CC system is missing
"Stagger", "interrupt", "armor" and "destabilize" appear about 30 times. Earth's and Lightning's identities depend on them, and so do seven enemy counters. Define:
- A per-enemy poise bar, stagger threshold and duration.
- Elite armor / super-armor.
- What "interrupt" means for enemy casts.
- CC-immunity windows.

Then add **Earth: stagger damage multiplier** and **Lightning: Shock** (interrupt + chain).

### 2.4 No Feel Spec
Write it before content. Starting values are in [`GameSpec/hades_feel_reference.md`](../GameSpec/hades_feel_reference.md):
- Assigned velocity.
- 0.21 s dash with ease 0 / 0.8 and 0.24 s i-frames.
- Collapsed anticipation and held contact.
- 10–50 ms hit-stop at 10%.
- Rigid camera with aim lean.
- Telegraph minimums.

### 2.5 No meta-progression, hub, difficulty ladder or Roblox business model
The only long-term goal is "five essences → Prime Demon". Missing:
- A Heat-like opt-in difficulty system (where Hades' skill ceiling lives for good players).
- Permanent upgrades, hero unlock rules (how do IronClad and Frog Wizard unlock?), a hub.
- Daily rewards, badges, a lobby and matchmaking flow.
- Cosmetics-only monetization (skins, VFX colour themes) that doesn't sell power in a skill game.

### 2.6 Run length: why it's 43–62 minutes, and whether that's a problem
The area count isn't the cause. **Stage count and stage size are.** From your own area table:

| Segment | Content | Time |
|---|---|---|
| Area I | 1 stage + boss | 3–5 min |
| Areas II + III | 8 **large** stages × 2–3 encounters each, + 2 shops + 2 bosses | 20–28 min |
| Area IV | **9** stages × 2–4 waves + shop + boss | 10–14 min |
| Area V | 5 stages + shop + 3-phase boss | 7–10 min |
| Demon Lord | 1 boss | 3–5 min |

That's 23 combat stages, around 50 encounters, and **6 boss fights**. Hades has about 40 chambers across 4 biomes with 4 bosses, but each chamber is a single 45–90 s fight with no traversal. A first successful Hades run commonly takes 40–60 minutes, so **your estimate is about the same as Hades for a typical player.** Hades gets away with it because it **saves at every chamber** and runs get much faster with skill.

On Roblox the length becomes a problem because of:
- No resume.
- Co-op parties breaking up mid-run.
- A younger audience with shorter sessions.

Levers if you want ~30–40 minutes:
1. Count encounters, not stages. Two to three encounters per large stage is what doubles II–III.
2. Cut Area IV from 9 stages to 6–7 and add room-type variety (§3.11) instead.
3. Make the Demon Lord a separate "endgame" session after a win, rather than part of every run's length.
4. Add save/resume between stages: solo always, party when the host returns.

---

## 3. Deeper problems (rev 2)

### 3.1 Each hero has exactly one "correct" third element
Computed from the formula rules (Fire/Frost and Water/Lightning are incompatible):

| Hero (start) | Third element → new duos / trios available |
|---|---|
| Apprentice (Fire + Lightning) | **Earth +4 / 1** · Water +2 / 0 · Frost +2 / 0 |
| IronClad (Earth + Frost) | **Water +4 / 1** · **Lightning +4 / 1** · Fire +2 / 0 |
| Frog Wizard (Fire + Water) | **Earth +4 / 1** · Lightning +2 / 0 · Frost +2 / 0 |

Every unlock that's incompatible with a starting element adds half the duos and **no trio**. For Apprentice and Frog, **Earth is the only way to reach any trio signature**. The first Big element pick is therefore solved, and unlocks that aren't Earth feel like traps.

Options:
- Accept it and compensate: incompatible unlocks also grant a free Rune or affinity.
- Give each hero a trio-capable path through *two* unlocks.
- Revisit the incompatibility pairs.

At minimum, make element offers a choice (not random) and tell the player what each one unlocks.

### 3.2 Starting pairs barely use, or actively fight, the reaction system
- **Apprentice (Fire + Lightning):** zero reactions. Lightning has no status.
- **IronClad (Earth + Frost):** only Chill/Freeze. Earth has no status.
- **Frog Wizard (Fire + Water): anti-synergy.** Water applies Wet, Wet makes Fire deal **−25%**, and Water **extinguishes** Burn. Frog's own two signatures weaken each other.

The "elemental synergy" pillar is mostly unreachable for the first ~25 minutes of every run, and one hero is punished for playing their kit. Fixes:
- Make Evaporation a *payoff*: Fire consumes Wet for a steam-burst bonus. Steam as an effect is allowed by the "no derived elements" rule.
- Ship Shock (Lightning) and Stagger (Earth) in the first implementation, not later.
- Check every starting pair has at least one positive reaction.

### 3.3 One shared formula drives Q, E and R at the same time
To have Firestorm (Fire + Fire + Lightning) ready on R, your Q nova and E enchant must also be Fire + Fire + Lightning. You can't keep a "Q formula" and an "R formula". Every swap for one changes all three. With live input that's a constant re-typing tax. With prepared slots (model B), each slot simply *is* a formula and the coupling becomes a build decision.

### 3.4 E is a chore button, not a decision
Re-enchanting is free with a 0.5 s cooldown, so the optimal play is "press E after every formula change and whenever it expires". Either:
- Make LMB **auto-inherit** the current formula and delete E (one less button, better for mobile), or
- Make enchanted shots **consume a resource**, so E becomes a real spend decision.

### 3.5 Lightning and Earth feel flat at launch
Two of three heroes start with a statusless element, and Apprentice's Thunderbolt applies nothing. In a game built on elements, the first elements players touch should be the most expressive. This is the same fix as 2.3: design Shock and Stagger first.

### 3.6 RMB is now free: use it
With the ranged attack on LMB, RMB is unassigned. Candidates:
- **RMB = Q nova.** Mouse-hand ergonomics like Hades' attack + special, which frees Q for formula slot 1.
- **RMB = hold for a formula radial** (works on gamepad as a trigger).
- **RMB = charged LMB variant** (a perfect-release shot for skill expression).

### 3.7 Aim assist isn't specified
Ranged LMB on gamepad and touch needs magnetism. Hades' player weapons use **auto-lock range 650 u (~16 studs) in a 100° arc**, plus reticle magnetism. Specify aim assist per input device, kept weaker on mouse.

### 3.8 Rarity barely matters
Affinity rarity runs Common +30% → Legendary +50% (1.67×). Quick Distillation runs 8 s → 6 s. A Legendary barely beats a Common, so rarity stops being exciting. Meanwhile +30% at *Common* is a very high floor that will stack badly with five affinities plus Empowerment levels. Lower the floor and widen the spread, or make Legendaries add behaviour, not just bigger numbers.

### 3.9 Boons change strength, not behaviour
Hades boons rewrite *what your attack, special, cast and dash do*, and Duo boons combine gods. Map that onto elements:
- Per element: an LMB boon, a Q boon, an R boon and a **Dash boon** (dash currently has none).
- Cross-element **Duo boons**.

Keep the runes as your Daedalus Hammer.

### 3.10 Telegraphs must work for three dash profiles
IronClad has −20% dash distance, Frog has 2 dashes, and Apprentice is baseline. Enemy attacks tuned around Apprentice will either trivialize Frog or be unfair to IronClad. Define telegraph and hitbox standards against the *worst* dash. Better: give IronClad a defensive verb (block/armor window) instead of raw 2× HP, which also lowers the skill ceiling.

### 3.11 Route choices are only reward categories: no room-type variety
Hades' routing is interesting because the doors also lead to *different kinds of rooms*: elite chambers, Chaos gates (risk/reward curses), Erebus gates (harder for more reward), trials and troves, fountains, NPC encounters, and story. Prime only has combat stages, shops and bosses. Add elite and challenge rooms, a risk/reward "curse" room, a rest/heal room and NPC events. That also fixes Area IV's 9-stage monotony.

### 3.12 Scope is very large for Roblox
The current specs add up to:
- ~33 enemy types, 5 multi-phase area bosses, 5 Demon Lords and the Prime Demon.
- 3 heroes, 20 signatures and **43 nova variants**.

Ways to cut it:
- Build Q **compositionally** (per-element layers).
- Use Hades-style **elite affixes** (armored, shielded, hasted) to multiply enemy variety cheaply.
- Ship 1–2 Demon Lords at launch.
- Treat the enemy roster per area as a cap, not a target.

### 3.13 Prime Demon gating is far away for the audience
Reaching the Prime Demon takes five *distinct* Demon Lord wins at ~45–60 minutes each, plus failed runs. That's a long-term goal measured in many hours. Fine as the summit, but it needs shorter goals on the way: hero unlocks, codex entries, cosmetics, Heat tiers, first-clear rewards per Lord.

### 3.14 Co-op power curve
At 4 players each player gets 62.5% of the loot, while total enemy HP × count scales about 4.1×. Per-player builds are weaker against similar per-capita pressure, so late areas get harder in 4-player. That may be intended; simulate it before locking the numbers.

### 3.15 Spectating and revive pacing
- Defeated players spectate until the **stage** clears, which on large stages or bosses can be 5–10+ minutes. Respawn them after the current wave or encounter instead.
- A 5 s uninterrupted revive that resets on damage is long for fast action. Try 2.5–3 s with partial progress that decays.

### 3.16 No narrative layer
There are no characters, dialogue or story beats. Roblox players care less about story than Hades players, but personality (a hub NPC, boss banter, a trader character) is cheap retention. Decide the minimum.

---

## 4. What's good: keep it

- No derived elements, and order-independent formulas.
- Incompatible element pairs create real formula choices.
- Shared status buildup on the target, so co-op teamwork emerges naturally.
- Deterministic hit resolution, no recursive reactions, CC immunity windows.
- Readability rules (telegraphed wards, VFX not obscuring warnings).
- Enemy implementation order, one representative per system.
- Loot-credit budget with fractional accumulators, and the tie-break voting rule.

---

## 5. Roblox technical reality

1. **Latency is the #1 feel risk.** Client-predict everything the player does (animation, VFX, local hit-stop, hit sparks), with the server validating and applying damage. Honour dash i-frames using client-reported timestamps within a tolerance. Test with Studio's network lag simulation from week one.
2. **Hit-stop is local only.** Never slow the server.
3. **Character controller:** Humanoid WalkSpeed is effectively assigned velocity, which is good. Set `AutoRotate = false`. Implement dash and knockback as a custom overspeed state.
4. **Projectiles:** server raycast simulation, client-only visuals.
5. **Enemy AI:** a hard active-enemy cap per arena, cheap data-driven behaviours.
6. **Data-driven tuning:** all timings and windows live in tables. Use Rojo + Git.
7. **Animation:** snappy keys, holds via `AdjustSpeed(0)`, hitboxes from `GetMarkerReachedSignal`.
8. **Platform:** decide PC-first or mobile-inclusive now. The current controls don't fit touch without model B/C, auto-enchant (§3.4) and aim assist (§3.7).

## 6. Tripo AI pipeline

- **Consistency:** style bible + 2D concepts → image-to-3D, not text-to-3D per model.
- **Top-down readability:** exaggerated silhouettes and glowing "read zones" for resistances and auras.
- **Budgets:**
  - Hero ~3–5k tris, enemies ~1.5–4k, props under 1k.
  - 512–1024 hand-painted atlases. Roblox caps texture size and triangles per mesh.
- **Rigging and animation are the real cost.** Non-humanoids (hounds, stag, slimes, treants, chained bosses) need custom rigs, and snappy animation needs a hand animator.
- **Hand-painted textures under Roblox lighting:** test early, and bake shading into the textures.
- **Pilot one enemy end to end and time it** before committing to the roster.

## 7. Build approach

0. **Pillars on paper:**
   - Input model (B/C), platform, run-length target, solo-first quality.
   - Feel Spec, Poise/CC spec, decisions on E and RMB.
1. **Graybox combat prototype:**
   - One arena, Apprentice, three enemies (lunger, kiter, swarmer), full feel features.
   - 100–150 ms simulated latency, 4 clients.
   - Don't build content until it feels responsive and dodges feel honest.
2. **Core systems, data-driven:**
   - Formula slots, statuses + poise, reward generator, run state machine, arena templates, voting, save between stages.
3. **Tripo pipeline pilot** in parallel; lock the style bible.
4. **Vertical slice:**
   - Area I + Fallen Captain, all three heroes, ~15 behaviour boons, hub/lobby.
   - Playtests with real Roblox players, solo and 4-player.
5. **Scale area by area.** Ship early access with Areas I–II plus a Heat-like system.

## 8. Priority checklist

1. Input model (B/C) and platform target.
2. Q resource; lock/cancel windows for LMB, Q and R; decide E (auto-inherit vs resource) and RMB.
3. Poise/Stagger/CC, plus Shock and Stagger statuses, in the first implementation.
4. Feel Spec with numbers (start from `hades_feel_reference.md` §7).
5. Third-element balance (§3.1) and starting-pair synergy (§3.2).
6. Arenas everywhere for v1; room-type variety (§3.11); Area IV length.
7. Behaviour-based boons, rarity spread, Dash boons.
8. Meta-progression, Heat, hub, retention, cosmetics.
9. Save/resume between stages; respawn after wave; faster revive.
10. Prototype netcode and feel before content production.
