# Prime Alchemy — Status Effects & Elemental Synergies

**Design specification — initial implementation**

## 1. Scope and principles

- Implement status mechanics only for **Fire, Water, and Frost** for now. Earth and Lightning deal damage as usual but have no dedicated status effects yet.
- Use **one shared status/buildup system** for Nova (Q), enchanted ranged attacks (E + RMB), and Signature spells (R). No signature-specific status bonuses or exceptions.
- A Signature's **dominant element** (the element appearing twice) determines its status buildup. For signatures containing three different elements, a primary status element must be assigned individually later; do not automatically apply all three statuses.
- Ordinary elemental interactions depend on the incoming attack's effective element. Reactions are universal, not unique to individual spells.
- Status resistance and elemental damage resistance are separate enemy attributes.
- **No derived elements** and no new status-specific spell unlocks.

## 2. Elemental statuses

| Element | Status | Buildup | Effect at threshold | Suggested duration |
|---|---|---|---|---|
| Fire | Burning | Fire damage builds Burn | Damage over time; subsequent Fire refreshes duration | 4 seconds, ticks every 0.5 sec |
| Water | Wet | Water damage builds Wet | Incoming Fire damage -25%; incoming Frost buildup +50% | 5 seconds |
| Frost | Chill → Frozen | Frost hits accumulate Chill | Chill slows movement up to 35%; at full buildup, Frozen prevents movement and attacks | Frozen 2 seconds |

**Suggested default threshold:** 100 buildup points for ordinary enemies, subject to enemy modifiers. Numbers above are **initial balancing proposals**, not final calibrated values.

**Details:**

- **Burning:** repeated Burn applications refresh the duration, rather than creating limitless independent damage-over-time stacks. Burn tick damage still needs balancing.
- **Wet:** Water refreshes Wet once active. Fire dries the target progressively; while Wet remains, Fire damage is reduced by 25%. The proposed drying rule is **-1.5 seconds of remaining Wet duration per Fire hit**, in addition to ordinary time passage.
- **Chill/Frozen:** Chill scales the movement slow up to 35% at maximum buildup. Reaching the threshold freezes the target. After thawing, retain some Chill buildup, to be tuned. Freeze cannot be extended indefinitely with repeated hits.

## 3. Universal elemental reactions

| Existing target condition | Incoming element | Reaction | Behavior |
|---|---|---|---|
| Wet | Frost | Flash Freeze | Frost applies **+50% Chill buildup** (not a guaranteed instant Freeze) |
| Wet | Fire | Evaporation | Fire deals **25% less damage** while Wet remains and accelerates drying |
| Burning | Water | Extinguish | Burning immediately ends; the Water hit applies Water/Wet buildup normally |
| Frozen | Fire | Thermal Shock | The triggering Fire hit gains **+30% damage**, then Frozen is removed |

**Examples:** A Frost hit supplying 40 buildup supplies 60 to a Wet enemy. A Fire hit that would deal 100 damage to a Frozen enemy deals 130 and thaws it, before any other applicable damage modifiers.

**Status coexistence and transition rules (proposed):**

- Burning and partial Chill can coexist.
- Wet and Burning should not coexist: Water extinguishes Burning; Fire progressively removes Wet before normal burning behavior dominates.
- Fully Frozen removes Burning to avoid contradictory long-lived states.
- Water on a Frozen target may apply/refresh Wet, but should not extend Freeze indefinitely.
- Reactions should never recursively trigger themselves.

## 4. Application by player action

| Action | Status application |
|---|---|
| **Q — Nova** | Uses the selected element or elements according to the normal Nova attack data; applies corresponding Fire/Water/Frost buildup and universal reactions |
| **E — Enhancement** | Enhances subsequent RMB projectiles; their elemental hits apply corresponding status buildup and universal reactions |
| **R — Duo Signature** | Applies buildup for the **dominant element** (two matching slots); no custom status rules per spell |
| **R — Trio Signature** | Uses **one designated primary status element**, to be defined for each three-different-element recipe |
| **Unenchanted RMB** | No elemental buildup by default |

### Duo Signature examples

| Recipe | Signature | Buildup applied |
|---|---|---|
| Fire + Fire + Water | Boiling Geysers | Burn |
| Water + Water + Fire | Scalding Whirlpool | Wet |
| Fire + Fire + Lightning | Firestorm | Burn |
| Lightning + Lightning + Fire | Thunderbolt | No status at present |
| Water + Water + Frost | Flash Freeze (spell) | Wet |
| Frost + Frost + Water | Blizzard | Chill |
| Earth + Earth + Frost | Glacial Bastion | No status at present |
| Frost + Frost + Earth | Crystal Cataclysm | Chill |

This rule similarly covers the remaining dual-element signatures: Earth- or Lightning-dominant ones do not apply a status until their respective statuses are designed. **The spell named Flash Freeze is distinct from the universal Wet → Frost reaction of the same name**; renaming one in the future may improve clarity.

## 5. Multi-hit attacks and element weighting

- Every eligible hit can contribute buildup. Tune **buildup per hit independently of damage** so persistent effects like Firestorm or Blizzard do not apply full statuses instantly.
- Incoming damage calculations may contain multiple elemental components. Maintain the existing elemental-damage composition rules separately from the **dominant-status** rule for R signatures.
- Q and E can use the actual elements present in their attack data to resolve universal reactions. R's status application follows its primary/dominant status element, even if its damage comprises multiple elemental components.
- Resolve an individual hit's damage and status events in a **defined, deterministic order** to avoid a mixed-element attack unintentionally weakening itself. Exact hit-resolution ordering remains to be determined in implementation.

## 6. Enemy-specific resistance

Store damage resistance and status resistance separately. Suggested examples:

| Enemy tier | Illustrative buildup threshold | Crowd-control behavior |
|---|---:|---|
| Standard | 100 | Normal Freeze duration |
| Elementally resistant | 160 for relevant status | Normal or shorter duration |
| Elite | Higher than standard | Reduced Freeze duration |
| Boss | Around 250 for relevant status | Very short interruption instead of full two-second disable, if needed |

These numbers are initial test settings only. An enemy may resist Fire damage while having normal Burn buildup resistance, or vice versa. Add a short post-freeze crowd-control resistance window to avoid repeated lockouts, particularly in multiplayer.

## 7. Implementation notes and open values

**Core systems:** per-target status/buildup state, timers, resistance multipliers, damage-over-time tick scheduler, Chill slow, Freeze immobilization/interrupt, and universal reaction resolution.

**Suggested development sequence:** (1) Burning; (2) Wet and drying; (3) Chill/Freeze and Flash Freeze reaction; (4) Extinguish; (5) Thermal Shock; (6) enemy resistance profiles; (7) tuning persistent and multi-hit spell buildup.

**Balance values still to finalize:** base buildup per attack type, Burn tick damage, Wet buildup per hit, post-thaw Chill retained, crowd-control immunity period, boss interrupt duration, and primary-status assignments for the four trio signatures.

## 8. Related combat rules (reference)

- Five base elements: Fire, Water, Earth, Lightning, Frost.
- Incompatible within a formula: Fire + Frost; Water + Lightning.
- Three element slots. All signatures are usable immediately when required elements are available; no signature unlock mechanic.
- Q casts ordinary Nova (**0.5 s cooldown**); E enchants RMB attacks (**0.5 s cooldown**); R casts Signature (shared **10 s duo** / separate shared **30 s trio** cooldowns).
- Existing boon/rune modifications are governed by the separate boon specification.
