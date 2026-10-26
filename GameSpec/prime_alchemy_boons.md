# Prime Alchemy — Boons, Rewards & Economy

**Status:** Working gameplay specification. Listed numbers are agreed where supplied directly; economy distribution and prices are initial balancing proposals.

## 1. Reward tiers versus item rarity

These are distinct concepts. **Reward tier** determines the significance of a stage/shop reward; **rarity** controls the numerical strength and availability of a boon.

| Reward tier | Contents |
|---|---|
| **Big** | New element available for the current run, or one skill-modifying Rune |
| **Normal** | +25 max HP; +2 stage-entry HP recovery; elemental damage boon; chosen Elemental Empowerment; 100 gold |
| **Minor** | Food healing; 30–50 gold; random Elemental Empowerment |

Exactly four rarities: **Common, Rare, Epic, Legendary** (no Uncommon). Where a boon has four numbers they map Common/Rare/Epic/Legendary. Three numbers map Rare/Epic/Legendary; two numbers map Epic/Legendary. One number means a fixed effect unless otherwise specified.

## 2. Elemental Boons (Normal rewards)

One affinity per base element, affecting that element's share of damage through Q, E/LMB and R.

| Affinity | Element | Common | Rare | Epic | Legendary |
|---|---|---:|---:|---:|---:|
| Flame Affinity | Fire | +30% | +38% | +45% | +50% |
| Tidal Affinity | Water | +30% | +38% | +45% | +50% |
| Stone Affinity | Earth | +30% | +38% | +45% | +50% |
| Storm Affinity | Lightning | +30% | +38% | +45% | +50% |
| Winter Affinity | Frost | +30% | +38% | +45% | +50% |

Elemental Empowerment levels up an **owned** affinity without changing its rarity. Repeated levels grant diminishing bonuses. A provisional example of additive *percentage-point* increments: +10, +6, +4, +3, +2, +1 for levels 2–7; not finalized. Choosing Empowerment allows the player to select which owned affinity; random Empowerment chooses an eligible owned affinity automatically. If no eligible boon exists, don't offer that reward.

## 3. Rune Boons (Big rewards)

Nine runes, three each for Q, R and E. Runes affect their named ability only, unless explicitly stated otherwise.

### Q — Nova

| Rune | Common | Rare | Epic | Legendary | Effect |
|---|---|---|---|---|---|
| Echo Nova | — | Second strike 60% damage | 68% | 75% | Repeats Q Nova once; delay TBD |
| Expanding Pulse | +20% radius | +26% | +31% | +35% | Expands Q Nova area |
| Shrapnel Nova | — | 4 shards | 6 shards | 8 shards | Q releases elemental projectiles; projectile damage TBD |

### R — Signature spells

| Rune | Common | Rare | Epic | Legendary | Effect |
|---|---|---|---|---|---|
| Quick Distillation | 8 s | 7 s | 6.5 s | 6 s | Replaces shared 10-second duo-signature cooldown |
| Supreme Distillation | — | 22 s | 18 s | 16 s | Replaces shared 30-second trio-signature cooldown |
| Perfect Resonance | — | — | Duo +35% | Duo +50% | Strengthens duo signatures; interpreted as damage pending confirmation |

### E — Enhancement / enchanted LMB

| Rune | Common | Rare | Epic | Legendary | Effect |
|---|---|---|---|---|---|
| Ricochet | — | — | 70% | 100% | Enchanted shot bounces to another enemy at listed damage fraction |
| Extended Infusion | +30% | +38% | +45% | +50% | Bonus to Enhancement effectiveness; exact affected stat TBD (damage vs duration/charges) |
| Volatile Ammunition | — | Every 4th hit, 60% AoE damage | Every 3rd, 60% | Every 3rd, 90% | Enchanted LMB hits periodically trigger an elemental area attack |

**Implementation policy proposed:** one copy of each named Rune per player; if offered again, it may replace the previous version with a higher rarity. Duplicate triggered effects should never recursively activate themselves. These policies are not finalized.

## 4. Other buffs and consumables

| Item | Tier | Effect |
|---|---|---|
| Vitality | Normal | +25 maximum HP; suggested also +25 current HP |
| Regeneration | Normal | +2 HP restored on entry to each next stage (not passive HP/sec) |
| Chosen Elemental Empowerment | Normal | Level one chosen owned elemental boon |
| Gold | Normal | +100 gold |
| Food small | Minor | Restore 20% of max HP immediately |
| Food medium | Minor | Restore 40% of max HP immediately |
| Food large | Minor | Restore 60% of max HP immediately |
| Gold | Minor | +30–50 gold |
| Random Elemental Empowerment | Minor | Level a randomly selected owned elemental boon |

**Clarification pending:** Stage-entry recovery example in design discussions uses base 3 HP plus a +2 regeneration upgrade = 5 HP per transition. Confirm whether 3 HP base recovery is intended. Food sizes need not correspond to boon rarities.

## 5. Trader prices — proposed initial values (gold)

### Big offers

| Offer | Gold |
|---|---:|
| New element | 250 |
| Common Rune | 180 |
| Rare Rune | 220 |
| Epic Rune | 280 |
| Legendary Rune | 360 |

### Normal offers

| Offer | Gold |
|---|---:|
| +25 max HP | 110 |
| +2 stage-entry recovery | 120 |
| Common elemental boon | 110 |
| Rare elemental boon | 140 |
| Epic elemental boon | 180 |
| Legendary elemental boon | 220 |
| Chosen Elemental Empowerment | 100 |

### Minor offers

| Offer | Gold |
|---|---:|
| Food: heal 20% | 35 |
| Food: heal 40% | 60 |
| Food: heal 60% | 85 |
| Random Elemental Empowerment | 65 |

Gold rewards are received from stages, not sold by traders. No element already owned by the player should appear as an unlock offer.

## 6. Reward frequency and shop inventory — playtest target

- Five areas contain **23 regular combat stages**, four traders, five area bosses, then one chosen Demon Lord.
- Target among the 23 regular stage completion rewards: ~3 Big, ~13 Normal, ~7 Minor; optional rewards from encounters may add supply pickups.
- Each of the five area bosses offers a **Big reward opportunity**, bringing the target to **eight non-shop Big opportunities** per completed run. Area budget: Ashen Outpost 1, Withering Wilds 2, Drowned Mire 2, Obsidian Prison 2, Forgotten Crucible 1.
- Traders can add roughly 1–2 purchased Big rewards in a gold-rich run. A player starting with two elements may spend up to three Big choices unlocking the remaining three elements. Full five-element access is possible, not mandatory.
- Guarantee an opportunity for a third element no later than completion of the Withering Wilds; later unlocks may be optional.
- Four trader stops: before area bosses in Wilds, Mire, Prison and Crucible. Solo inventory: **1 Big, 1 Normal, 1 Minor**; the Minor slot always offers healing food. Party-size stock scaling is defined in `prime_alchemy_coop_rules.md` §4.
- Trader reroll price idea: 40 gold first reroll, 80 gold second if enabled; selection re-rolls, not rarity upgrades.
- Target total gold income ~750 per run before optional special rewards. Fine-tune after playtesting; an example allocation: Outpost 45, Wilds 175, Mire 175, Prison 210, Crucible 145.

### Provisional gold sources

| Source | Gold |
|---|---:|
| Small enemy | 1–2 |
| Standard enemy | 2–4 |
| Elite | 10–15 |
| Encounter completion | 5–8 |
| Hidden cache | 15–30 |
| Minor gold reward | 30–50 |
| Normal gold reward | 100 |

## 7. Controls and interaction with boons

| Input | Base cooldown | Rune family |
|---|---:|---|
| Q Nova | 0.5 s | Echo Nova, Expanding Pulse, Shrapnel Nova |
| E Enhancement | 0.5 s | Ricochet, Extended Infusion, Volatile Ammunition |
| R Duo Signature | Shared 10 s | Quick Distillation, Perfect Resonance |
| R Trio Signature | Separate shared 30 s | Supreme Distillation |

No derived elements and no requirement to unlock individual signature recipes. Acquiring new elements during a run makes their applicable recipes immediately accessible.

## 8. Unresolved rules

- Damage of Shrapnel Nova projectiles and delay of Echo Nova.
- Whether Extended Infusion modifies enchant damage, empowered shot count, duration, or a combination.
- Whether Perfect Resonance is damage-only.
- Affinity level-up increments and maximum boon level.
- Whether max-HP and regeneration boons stack indefinitely and whether there is 3 HP baseline stage-entry regeneration.
- Whether upgrading a Rune rarity replaces, stacks with, or is disallowed alongside an existing copy.
- Shop inventory randomness, rune rarities by area, and gold rewards in co-op.
