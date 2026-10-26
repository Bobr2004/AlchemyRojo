# Prime Alchemy — Combat Design

**Status:** Working combat specification  
**Genre:** Action roguelike; planned cooperative play for up to four players  

## 1. Core combat loop

1. Move and dash to avoid enemy attacks and position around groups.
2. Select up to **three elements** to assemble a formula.
3. Press **Q** to cast an ordinary elemental nova using the selected formula, regardless of whether it also matches a signature recipe.
4. Press **R** to cast the matching signature spell, if one exists and its cooldown is ready.
5. Press **E** to enchant the **LMB ranged attack** using the selected elements. **E never casts signature spells.**
6. Adapt formulas to enemies, terrain, boons, and cooldown availability.

Signature spells are the centerpiece of spellcraft. There are **20 possible mixed-element signatures** using the current rules.

## 2. Elements and formula rules

### Five primary elements

| Element | Intended combat identity |
|---|---|
| Fire | Burn, explosive damage, persistent hazards |
| Water | Push, displacement, movement manipulation |
| Earth | Stagger, obstacles, protection, control |
| Lightning | Burst, chains, interrupts |
| Frost | Chill, Freeze, shatter, slow |

### Formula assembly

- A formula contains **1–3 slots**.
- Elements can repeat.
- **Fire and Frost cannot coexist** in a formula.
- **Water and Lightning cannot coexist** in a formula.
- **Slot order does not matter**: Fire + Lightning + Fire = Fire + Fire + Lightning.
- There are **no derived elements** as a separate game system. Steam, magma, and mud may occur as effects within individual spells but never as selectable ingredients or standalone elemental categories.
- **A signature must contain at least two distinct elements and occupy all three slots.** Three identical elements are **not** signatures; they can produce ordinary/empowered elemental novas.
- Two copies of an element plus one other form a *dominant-element* signature. Reversing the proportion results in a different signature (e.g., Fire + Fire + Lightning vs. Lightning + Lightning + Fire).
- Three distinct compatible elements form a *trio signature*.

### Formula count

| Type | Count | Signature? |
|---|---:|---|
| Three identical | 5 | No |
| Two identical + one different (compatible) | 16 | Yes — duo |
| Three distinct (all compatible) | 4 | Yes — trio |
| **Total three-slot signatures** | **20** | |

## 3. Controls and cooldowns

| Input | Action |
|---|---|
| Movement | Reposition, kite, navigate arenas |
| Dash | Evasive movement; varies by Alchemist |
| LMB | Ranged attack |
| Q | Always cast an ordinary nova using the current formula |
| R | Cast the matched signature spell, if available and off cooldown |
| E | Enchant LMB attacks with current elements |

### Cooldown design

- **Duo signatures (2 different elements in a 3-slot recipe): shared 10-second cooldown.**
- **Trio signatures (3 different elements): shared 30-second cooldown, independent of duo cooldown.**
- Casting a duo signature does **not** trigger the trio cooldown and vice versa.
- **Ordinary nova (Q):** Available for **every valid formula**, including formulas matching a signature. **0.5 s cooldown**, currently a minimum anti-spam interval.
- **Signature (R):** Only casts when the selected three-slot formula matches a signature and its duo/trio cooldown is ready. Otherwise R does not cast; the player can still press Q to use the ordinary nova.
- Changing formulas cannot bypass the shared duo or trio signature cooldowns.
- **E enchantment:** **0.5 s activation cooldown**. Applies normal elemental enhancements to LMB for a limited number of attacks and/or time; exact values to playtest.

**Design intent:** **Q is always the reliable nova**, **R is always the signature spell**, and **E is always the ranged enchantment**. A signature-ready formula never overrides Q.

## 4. Playable Alchemists

Baseline comparisons are relative to **Apprentice**.

| Alchemist | Starting elements | Stats and movement | Starting duo signatures |
|---|---|---|---|
| **Apprentice** | Fire + Lightning | Baseline movement, HP, dash, nova radius and LMB speed | Firestorm; Thunderbolt |
| **IronClad** | Earth + Frost | **-5% movement**, **-20% dash distance**, **2× HP**, **larger nova radius**, **-10% LMB attack speed** | Glacial Bastion; Crystal Cataclysm |
| **Frog Wizard** | Fire + Water | **+5% movement** relative to Apprentice, **two consecutive dashes**, **-20% HP** | Boiling Geysers; Scalding Whirlpool |

A hero's starting two elements are sufficient for their two respective duo signatures. Unlocking more elements within a run expands available formulas.

## 5. Signature spell catalog

**Rules for all entries:** Press **R** with the three listed elements. Duo spells have a **shared 10 s cooldown**. Descriptions below are *design proposals*; timings and damage are playtest targets, not finalized balance.

### Fire + Water

#### 01 — Boiling Geysers
**Recipe:** Fire + Fire + Water  
**Role:** Close-range burst / knock-up  
Several boiling geysers erupt around the caster in sequence, damaging and launching smaller enemies. Repeated hits on the same target deal bonus damage.  
**Use:** Punish clustered enemies after an aggressive dash.

#### 02 — Scalding Whirlpool
**Recipe:** Water + Water + Fire  
**Role:** Mobile AoE / pull / movement  
A scalding whirlpool follows the caster for **4 s**, damaging enemies and pulling smaller targets toward its edge. Grants **+15% movement speed** while active.  
**Use:** Mobile fighting and close-range kiting. **This is not a healing spell.**

### Fire + Earth

#### 03 — Volcanic Eruption
**Recipe:** Fire + Fire + Earth  
**Role:** Delayed explosion / persistent hazard  
A fissure erupts beneath nearby enemies after a brief warning, dealing heavy damage and leaving burning ground for **4 s**.  
**Use:** Area denial and punishment of slow targets.

#### 04 — Meteor Barrage
**Recipe:** Earth + Earth + Fire  
**Role:** Directed bombardment / stagger  
Five burning meteors strike sequentially within an area in the cursor direction. Repeated hits deal substantial stagger damage.  
**Use:** Large targets, elites, and bosses.

### Fire + Lightning

#### 05 — Firestorm
**Recipe:** Fire + Fire + Lightning  
**Role:** Moving AoE / damage over time  
A flaming tornado travels slowly in the cursor direction for **5 s**, continuously damaging targets and occasionally arcing lightning to enemies within it.  
**Use:** Group clearing and mobile area denial.

#### 06 — Thunderbolt
**Recipe:** Lightning + Lightning + Fire  
**Role:** Precision burst / chain lightning  
A powerful lightning strike hits the nearest enemy along the aimed direction. It triggers a fiery explosion and chains lightning to up to **3 nearby enemies**.  
**Use:** Priority-target elimination.

### Water + Earth

#### 07 — Crushing Tide
**Recipe:** Water + Water + Earth  
**Role:** Knockback / environmental collision  
A powerful wave expands outward from the caster, pushing enemies away. Enemies slammed into walls or objects take extra damage and a brief stun.  
**Use:** Creating space and exploiting terrain.

#### 08 — Sinking Ground
**Recipe:** Earth + Earth + Water  
**Role:** Area slow / root  
Creates an unstable patch of ground around the caster. Enemies inside are slowed **50% for 4 s**; those remaining for **2 s** become briefly rooted.  
**Use:** Trapping pursuers and setting up ranged attacks.

### Water + Frost

#### 09 — Flash Freeze
**Recipe:** Water + Water + Frost  
**Role:** Expanding wave / Freeze buildup  
Releases a ring of freezing water outward, damaging and applying heavy Chill. Targets already near their Freeze threshold freeze immediately.  
**Use:** Fast crowd control and interrupting groups.

#### 10 — Blizzard
**Recipe:** Frost + Frost + Water  
**Role:** Stationary area denial / sustained Chill  
Creates a localized blizzard at the caster's position for **5 s**, repeatedly damaging and chilling enemies. Frozen targets receive additional ice-shard damage.  
**Use:** Holding territory and punishing clustered foes.

### Earth + Lightning

#### 11 — Thunder Spires
**Recipe:** Earth + Earth + Lightning  
**Role:** Temporary obstacles / electrical area denial  
Summons **3 stone pillars** around the caster for **6 s**, periodically arcing lightning between them. Enemies crossing the arcs are damaged and briefly slowed.  
**Use:** Zone control and creating safe angles.

#### 12 — Seismic Pulse
**Recipe:** Lightning + Lightning + Earth  
**Role:** Radial interrupt / stun / stagger  
Sends an instantaneous electrical shockwave through the ground around the caster. Briefly stuns enemies and deals extra stagger to armored targets.  
**Use:** Interrupting dangerous melee pressure.

### Earth + Frost

#### 13 — Glacial Bastion
**Recipe:** Earth + Earth + Frost  
**Role:** Defensive barrier / knockback  
A ring of jagged frozen stone spikes erupts around the caster, damaging and pushing enemies back. The formation blocks hostile projectiles for **3 s** and temporarily protects the caster.  
**Use:** Defensive positioning and resets.

#### 14 — Crystal Cataclysm
**Recipe:** Frost + Frost + Earth  
**Role:** Delayed burst / shatter  
Large ice crystals appear in a circle around the caster, then shatter after **1 s**. Frozen enemies take bonus Shatter damage, while survivors accumulate Chill.  
**Use:** Burst after freezing enemies.

### Lightning + Frost

#### 15 — Shatterstorm
**Recipe:** Lightning + Lightning + Frost  
**Role:** Multi-target strikes / Chill synergy  
Creates a storm around the caster that strikes up to **5 nearby enemies over 3 s**. Chilled or frozen targets suffer extra damage and release ice fragments.  
**Use:** Clearing mobile groups and exploiting control effects.

#### 16 — Frost Lances
**Recipe:** Frost + Frost + Lightning  
**Role:** Homing / piercing projectiles  
Summons **6 large ice lances** that briefly orbit the caster, then launch at enemies. Lances pierce targets and discharge small electrical bursts on impact.  
**Use:** Ranged clearing and targeted pressure.

## 6. Trio signatures — 30-second shared cooldown

These are major battlefield-changing abilities, not ordinary damage novas. They have their own **shared 30 s cooldown**, independent of the duo-signature timer.

#### 17 — Cataclysm
**Recipe:** Fire + Water + Earth  
**Role:** Three-stage AoE / crowd control  
1. A water shockwave pushes nearby enemies outward.
2. The earth fractures and jagged rocks erupt underneath them.
3. Flames burst through the cracks, leaving a wide hazard.

Enemies caught by all three stages suffer bonus finishing damage.  
**Use:** High-payoff multi-stage control in crowds.

#### 18 — Armageddon
**Recipe:** Fire + Earth + Lightning  
**Role:** Massive directed burst / stagger  
Conjures an enormous electrified meteor that crashes down in the aimed direction. The impact stuns survivors, produces lightning strikes, and scatters smaller burning fragments over the area.  
**Use:** Boss damage and spectacle.

#### 19 — Frozen Kingdom
**Recipe:** Water + Earth + Frost  
**Role:** Temporary territory / slow / protection  
Transforms a large region surrounding the player into a frozen battlefield for **8 s**. Enemies are heavily slowed, and periodic ice pillars launch targets upward. The caster gains faster movement and reduced incoming damage while inside.  
**Use:** Defensive battlefield control.

#### 20 — Eye of the Tempest
**Recipe:** Earth + Lightning + Frost  
**Role:** Mobile storm / sustained pressure  
Creates a large storm following the player for **7 s**. Orbiting stones and ice shards hit nearby enemies while lightning strikes targets inside. Periodic pulses push enemies outward. LMB remains usable during the storm.  
**Use:** Aggressive mobile pressure.

## 7. Ordinary Q novas, R signatures and E enchantments

### Ordinary nova (Q)

- Cast with **any valid formula**, including a full three-slot formula that also has a signature spell.
- Produces an outward elemental effect around the player using the chosen ingredients.
- Baseline elemental themes: Fire applies Burn; Water displaces; Earth staggers/protects; Lightning shocks; Frost chills/freezes.
- Exact multi-element blending and damage coefficients are to be specified; **Q has a 0.5 s cooldown**.
- **Signature spells never replace the ordinary nova.** The player chooses independently between Q (nova) and R (signature).

### Signature casting (R)

- Requires a matching three-slot, mixed-element signature recipe.
- If its signature category is on cooldown, R cannot cast; Q remains available independently.
- All duo signatures share one 10-second cooldown, while all trio signatures share a separate 30-second cooldown.

### Ranged enchantment (E)

- Applies the selected elements' normal effects to LMB ranged attacks.
- Has a **0.5 s activation cooldown**. Attack-count and duration limits remain open for playtesting.
- **Does not trigger a signature spell**, even if the active three-slot recipe is a signature.
- Enchantment effects should remain mechanically simpler than signature spells.

## 8. Signature availability and progression

- **No spell unlocking and no Grimoire progression.** All 20 signature recipes are known and castable from the outset if their required elements are available.
- Each Alchemist begins a run with two specified elements. New elements can be acquired as **Big rewards** during the run.
- The spellbook, if implemented, is a reference menu only, listing recipes and which are currently castable.
- Q and E are independent of the duo and trio R cooldown timers.
- A temporary or permanent change in elemental availability immediately changes which recipes can be assembled.

## 9. Outstanding combat tuning

- LMB baseline rate/damage, normal Nova base damage and area, E enchant duration/shot count, status strength and stacking.
- Detailed dash timing, invulnerability behavior and hero-specific numerical baselines.
- Damage allocation by element for mixed formulas and resistance calculations.
- Exact cooldown-start rules for E replacement/reapplication and Q interaction with rune follow-up hits.

See `prime_alchemy_boons.md` for rewards and tuning rules.
