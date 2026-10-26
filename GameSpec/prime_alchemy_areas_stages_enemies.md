# Prime Alchemy — Areas, Enemies & Bosses

**Status:** Working game design summary  
**Scope:** World progression, stage structure, enemy roster, elemental enemy mechanics, area bosses and Demon Lords.  
**Co-op:** Up to 4 players planned; no dedicated co-op mechanics defined yet.

## 1. Run structure

The game progresses from large multi-encounter exploration stages in the first three areas to compact wave-based combat rooms in the final two areas.

**Terminology:** A **stage** is one map/room; an **encounter** is an enemy engagement within a stage. Large outdoor stages have 2–3 encounters. Dungeon/lab stages typically have a single encounter with multiple enemy waves.

| Area | Setting | Stage structure | Combat style | Area boss |
|---|---|---|---|---|
| I — Ashen Outpost | Starting camp and forest gate | **1 large stage** with **2–3 encounters**, then boss; **no shop** | Short onboarding, open map | Fallen Captain |
| II — Withering Wilds | Forest, fields and ruins | **4 large stages**, then shop and boss | 2–3 engagements in each stage, exploration | Hollow Stag |
| III — Drowned Mire | Cursed swamp and drowned villages | **4 large stages**, then shop and boss | 2–3 engagements in each stage, hazardous terrain | Mother of the Mire |
| IV — Obsidian Prison | Ancient underground dungeon | **9 short combat stages**, then shop and boss | One arena encounter per stage, typically 2–4 waves | First Prisoner |
| V — Forgotten Crucible | Lost alchemy laboratory | **5 short combat stages**, then shop and boss | Shorter, intense arcane combat arenas | Grand Alchemist |

**Proposed count:** 23 ordinary combat stages + 4 shops + 5 area boss encounters = **32 total stages/rooms**, followed by **one chosen Demon Lord** encounter. These numbers are provisional balance targets, not finalized production requirements.

### Branching route rule

After clearing a stage, players choose which stage/reward route to take next. The five *areas* remain sequential, but the path **within** each area branches. For example, one exit might promise an elemental boon, another gold, and another a harder elite encounter with a better reward. Only the chosen route counts toward the stage quota. An area ends with its trader (except Area I) and fixed area boss.

### Level-design guidelines

- **Areas I–III:** Larger handcrafted open maps, multiple encounter sites, exploration, cover, side discoveries, patrols and environmental hazards. The stage exit opens after the mandatory encounters; optional activities can be skipped.
- **Areas IV–V:** Compact handcrafted arenas, a single event per room, enemy waves and immediate reward/exit choice after clearing. Later waves can arrive as prior waves thin out, subject to an active-enemy cap.
- **Replayability:** Maintain a larger pool of handcrafted stage layouts than a player sees during one run; vary layout selection, enemy packs, events and exit rewards.
- **Target run duration (tentative):** Area I 3–5 min; II 10–14; III 10–14; IV 10–14; V 7–10; Demon Lord 3–5. Total ~43–62 minutes before balancing and co-op variance.

## 2. Area I — The Ashen Outpost

**Environment:** Abandoned camp, smoke, palisades, ruined watchtowers, path into dark forest.  
**Purpose:** Teach mobility, dash, LMB attack, elemental Q nova, E enchantment, and R signature spell.

| Enemy | Role / behavior |
|---|---|
| Possessed Scout | Straightforward melee attacker; telegraphed lunge |
| Ember Imp / Cinder Imp | Throws fireballs, leaves small burning patches; **elemental enemy** |
| Hollow Archer | Ranged attacker that maintains distance |
| Cinder Hound | Charges in a line, leaves short fire trail |

**Elemental mechanic — Cinder Imp:** 60% Fire resistance; Water attacks extinguish its flames for ~3 seconds, disabling fireball attacks temporarily. This is the first simple lesson in elemental counters. Avoid absolute immunity here, because starting heroes have only two elements.

**Boss — The Fallen Captain:** Corrupted armored commander. Slow sword sweeps, shield charges and occasional scout summons. Designed to teach attack telegraphs, dash timing and recovery windows. Defeat opens the forest route. **No shop before this boss.**

## 3. Area II — The Withering Wilds

**Environment:** Withered fields, forests, abandoned farms, sacred groves, old shrines.  
**Purpose:** Mobility, enemy swarms, support-target prioritization, environmental obstacles and open-area choices.

| Enemy | Role / behavior |
|---|---|
| Thornling | Weak swarmer, occasionally burrows |
| Rootbound Guardian | Slow frontline tank; frontal root barrier |
| Blight Archer | Ranged pressure; arrows leave hazardous patches |
| Briar Witch | Summons vines that briefly root players |
| Raging Treant | Elite; large slams and roots |
| **Runebark Totem** | **Elemental support:** stationary aura protecting nearby enemies |
| **Stormhorn Stag** | **Elemental elite:** mobility and charge-up retaliation |

**Runebark Totem:** Has ~60% Earth resistance. Every ~12 seconds grants nearby enemies ~50% Earth resistance for ~6 seconds. Fire strips its bark shell and interrupts protection. Prioritize it before the group it protects.

**Stormhorn Stag:** ~70% Lightning resistance. Lightning attacks charge its antlers; at full charge it emits an electrical pulse. Earth attacks reduce the charge and increase stagger buildup. Visibly telegraph the charge level.

**Boss — The Hollow Stag:** Corrupted forest guardian. Phase 1: antler charges and thorn walls. Phase 2: spectral deer and expanded attack patterns. Fire can destroy thorn obstacles; positioning and movement are central.

## 4. Area III — The Drowned Mire

**Environment:** Black water, rotting paths, bridges, flooded ruins and villages, corrupted vegetation.  
**Purpose:** Hazard positioning, status effects, elementally protected groups, and changing battlefield safety.

| Enemy | Role / behavior |
|---|---|
| Bog Crawler | Ambushes from shallow water |
| Plague Toad | Leaps and launches toxic projectiles |
| Mire Shaman | Heals allies / maintains hostile totems |
| Drowned Knight | Armored melee fighter; wave-producing attacks |
| Leech Colony | Splits into smaller creatures |
| Swamp Hag | Elite caster using curses and illusions |
| **Tidal Slime** | **Elemental support:** Water-resistant shielding |
| **Mire Channeler** | **Elemental support:** rotating resistance ward |

**Tidal Slime:** ~80% Water resistance. Grants up to three nearby enemies ~50% Water resistance for ~5 seconds. Frost rapidly freezes the slime, collapsing its protection and opening it to follow-up damage.

**Plague Toad elemental interaction:** ~50% Water resistance. Its poison pools can be burned away with Fire, producing a small explosion that harms nearby enemies. This is hazard manipulation, not a separate derived-element system.

**Mire Channeler:** Grants nearby enemies ~70% resistance to a *visibly indicated* element for ~6 seconds. Casting is interruptible via stagger, knockback or Freeze. Avoid an untelegraphed or unreadable random ward.

**Boss — Mother of the Mire:** Ancient witch merged with swamp roots. Phase 1: poison pools, roots, crawler summons. Phase 2: flooded sections of arena, illusions, toxic water waves. Frost can temporarily freeze suitable shallow-water hazards; Fire clears toxic vegetation.

## 5. Area IV — The Obsidian Prison

**Environment:** Stone cells, chains, rune traps, narrow corridors and enclosed ritual chambers.  
**Purpose:** Move to short, harder wave arenas; stagger windows, group coordination, interruptible support units and readable environmental traps.

| Enemy | Role / behavior |
|---|---|
| Chain Wraith | Spectral chain pull |
| Obsidian Sentinel | Armored frontline construct; **elemental enemy** |
| Bone Conjurer | Summons skeletons until interrupted |
| Rune Turret | Rotating projectile patterns |
| Mimic Chest | Ambushes players who open it |
| Prison Executioner | Elite with delayed heavy hammer swings |
| **Runic Custodian** | **Elemental support:** adapts to incoming damage |
| **Frostbound Warden** | **Elemental elite:** suppressive freezing zone |

**Obsidian Sentinel:** ~70% Earth / ~50% Fire resistance. Reinforced Shell temporarily reduces incoming damage until staggered; Lightning attacks accelerate destabilization/stagger.

**Runic Custodian:** Every ~10 seconds grants nearby enemies ~75% resistance to the element that recently dealt it the most damage. Its current protected element is shown by a colored crystal. Using a different element can break that crystal and end the aura.

**Frostbound Warden:** ~80% Frost resistance. Creates a suppression zone that slows movement and spell-cooldown recovery. Lightning destabilizes its crystal, disabling the zone briefly.

**Boss — The First Prisoner:** Colossal chained demon. Phase 1: long chain sweeps, pillar destruction, grabs/pulls. Phase 2: faster unchained leaps and aggressive melee. Earth attacks are effective for stagger; pillars can interfere with attacks.

## 6. Area V — The Forgotten Crucible

**Environment:** Alchemy engines, hazardous reactors, unstable experiments, libraries, brass machinery and ritual platforms.  
**Purpose:** Final skill test: changing resistances, signature-inspired enemy magic and complex combined encounters.

| Enemy | Role / behavior |
|---|---|
| Failed Homunculus | Mutates attack behavior when hurt |
| Alchemical Slime | Splits into smaller forms |
| Living Experiment | Hybrid monster using multiple elemental attacks |
| Arcane Construct | Charges / sweeping beam attacks |
| **Prismatic Slime** | **Elemental enemy:** periodically changes affinity |
| **Corrupted Alchemist** | **Elemental elite:** mimics the player's chosen element |
| **Elemental Conductor** | **Elemental support:** networked resistance and shields |

**Prismatic Slime:** Changes affinity every ~8 seconds. Takes ~85% reduced damage from its currently indicated element; other elements work normally. Enough stagger forces an early shift.

**Corrupted Alchemist:** Copies the dominant element of the last signature spell cast against it, gaining ~60% resistance to that element for ~8 seconds. Casts simplified elemental signature-like attacks. Stagger removes its copied resistance.

**Elemental Conductor:** Connects to nearby enemies via visible beams; protects their most relevant elemental vulnerabilities and periodically shields a weakened linked target. Break line of sight or destroy the conductor to cut its network.

**Boss — The Grand Alchemist:** Final area boss. Phase 1: recognizable primary-element spells. Phase 2: more complex mixed-element spell attacks. Phase 3: activates laboratory reactors and rotating hazards. Defeat activates the **alchemy summoning circle**, where players select the Elemental Demon Lord they will face.

## 7. Five Elemental Demon Lords

Demon Lords are **separate from area bosses**. After defeating the Grand Alchemist, players select **one** of the five Lords through the summoning circle.

| Element | Demon Lord | Encounter identity | Reward |
|---|---|---|---|
| Fire | **Ignivar, Lord of Cinders** | Aggressive melee, wildfires, flaming blades | Fire essence |
| Water | **Thalassar, the Drowned King** | Tidal waves, water prisons, drowned summons | Water essence |
| Earth | **Gorath, the Mountain Eater** | Armor, earthquakes, falling boulders | Earth essence |
| Lightning | **Veyr, the Storm Tyrant** | Teleports, chain lightning, delayed strikes | Lightning essence |
| Frost | **Nyxara, the Winter Queen** | Frozen terrain, ice mirrors and shattering patterns | Frost essence |

**Meta-progression:** Collect the five distinct elemental essences across successful runs to unlock the **Prime Demon**, the final boss. Duplicate Lord victories should provide some other repeatable reward (e.g., a separately defined upgrade currency), rather than another required essence.

## 8. Elemental enemy system — shared design rules

**Goal:** Make element selection and changing formulas strategically meaningful **without** rendering a starting hero useless against certain enemies.

| Mechanic | Description | Example |
|---|---|---|
| Innate resistance | Built-in resistance to one or more elements | Cinder Imp |
| Protection aura | Grants nearby enemies a temporary typed resistance | Runebark Totem, Tidal Slime |
| Absorption / punishment | Attacking with a resisted element can charge a counterattack | Stormhorn Stag |
| Disruption | Creates zones or effects that complicate spells | Frostbound Warden |
| Adaptive resistance | Changes protection in response to player behavior | Runic Custodian, Corrupted Alchemist |
| Elemental transformation | Cycles through resistance modes | Prismatic Slime |
| Hazard interaction | Elements affect enemies' environmental hazards | Plague Toad |

**Suggested balance tiers (provisional):** Minor resistance 25%; strong 60%; extreme 85%; 100% immunity only for rare, heavily telegraphed special cases. A counter-element weakness can start around +25% damage. Most ordinary enemies should remain elementally neutral.

**Clarity and fairness:**

1. Use distinctive colors, runes, shells, crystals and effects to show active resistances and protected enemies.
2. Make aura source enemies clearly identifiable and targetable.
3. Use strong resistances more often than immunities; avoid hard locks for heroes with only their starting pair unlocked.
4. For multi-element signatures, calculate damage by elemental contributions, rather than assigning the entire spell to one element (exact damage weighting TBD).
5. Elite/boss crowd-control resistance should prevent indefinite stunlock.
6. Avoid screen-filling effects that obscure enemy attack warnings, especially with up to four players.
7. **No derived-element system:** Environmental reactions are bespoke spell/enemy interactions, not new selectable elements.

## 9. Enemy implementation order

Start with one representative behavior from each system before scaling up the content roster:

1. **Cinder Imp:** elemental damage resistance + simple Water counter.
2. **Runebark Totem:** protective aura, group targeting, Fire interrupt.
3. **Tidal Slime:** selective ally protection + Frost interruption.
4. **Prismatic Slime:** timed resistance transformation with readable effects.
5. **Runic Custodian:** adaptive protection after the base resistance and aura systems are stable.

Build representative **large open stage** and **small wave arena** templates in parallel; then use shared enemy spawning, telegraph, reward and exit-choice systems across levels.

## 10. Current reward and progression integration

- Stages offer route selection after completion; a route's reward category is visible before choosing it.
- **Big:** new elemental unlock or skill Rune. **Normal:** +25 max HP, +2 stage-entry regeneration, elemental damage boon, chosen elemental empowerment, or 100 gold. **Minor:** food, 30–50 gold, random elemental empowerment.
- Initial balancing target: **8 Big reward opportunities from stages/bosses across a full run**, plus optional shop purchases. Distribution: Outpost 1, Wilds 2, Mire 2, Prison 2, Crucible 1. An element unlock should be available by the end of Wilds. These are tuning targets, not hard-coded drop rates.
- Four traders, one before each area boss except the Outpost boss; solo trader format is **1 Big + 1 Normal + 1 Minor** (3 offers). Party-size stock scaling is defined in `prime_alchemy_coop_rules.md` §4.
- Selected Demon Lord follows the Grand Alchemist, with one of the five different elemental essences awarded for victory.

See `prime_alchemy_boons.md` for store costs and reward balance.
