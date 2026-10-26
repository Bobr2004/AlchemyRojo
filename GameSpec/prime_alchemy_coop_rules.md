# Prime Alchemy — Co-op Rules

## 1. Overview

- Supports **1–4 players** in the same run.
- All players travel through the **same stage and area**; the party does not split into separate stages.
- Friendly fire is disabled.
- Each player controls their own Alchemist, elements, abilities, boons, runes, HP and personal gold.
- Enemies share their status buildup between attacks from different players. No special co-op-only elemental reactions are required.
- Co-op scales the **total loot available**, enemy pressure, boss durability and trader inventory.

## 2. Loot scaling

The loot budget is shared across the party, not replicated for every participant.

| Players | Total loot budget | Average loot budget per player |
|---|---:|---:|
| 1 | 100% | 100% |
| 2 | 150% | 75% |
| 3 | 200% | 66.7% |
| 4 | 250% | 62.5% |

Formula: `lootMultiplier = 1 + 0.5 * (playerCount - 1)`.

### Reward-budget model

Reward credits are **internal generation values**, not a spendable currency.

| Reward tier | Cost in credits | Examples |
|---|---:|---|
| Big | 4 | Rune or unlock new element |
| Normal | 2 | +25 max HP, +2 stage-entry HP regeneration, elemental affinity, selected elemental empowerment, 100 gold |
| Minor | 1 | Food, 30–50 gold, random elemental empowerment |

Calculate a stage's total credits by multiplying its solo budget by the party loot multiplier. Distribute these credits into discrete reward drops. Do not multiply each individual drop by the number of players. A reward that offers three choices is **one claimable reward**, not three drops.

**Example — Standard stage (2 solo credits):**

| Players | Total credits | Generated rewards |
|---|---:|---|
| 1 | 2 | 1 Normal |
| 2 | 3 | 1 Normal + 1 Minor |
| 3 | 4 | 2 Normal |
| 4 | 5 | 2 Normal + 1 Minor |

**Example — Big-reward stage (4 solo credits):**

| Players | Total credits | Generated rewards |
|---|---:|---|
| 1 | 4 | 1 Big |
| 2 | 6 | 1 Big + 1 Normal |
| 3 | 8 | 2 Big |
| 4 | 10 | 2 Big + 1 Normal |

**Example — Rich exploratory stage (8 solo credits):**

| Players | Total credits | Generated rewards |
|---|---:|---|
| 1 | 8 | 1 Big + 1 Normal + 2 Minor |
| 2 | 12 | 2 Big + 1 Normal + 2 Minor |
| 3 | 16 | 2 Big + 3 Normal + 2 Minor |
| 4 | 20 | 3 Big + 3 Normal + 2 Minor |

The rich-stage example is **not** the standard payout for every exploration map. Maintain a run-wide budget to avoid overproducing Big rewards. Solo progression previously targeted roughly eight Big reward opportunities across the full run; scale the multiplayer *total* budget rather than guaranteeing eight to every player.

When the multiplied credit total is fractional, preserve fractional credits in an accumulator for later stages rather than consistently rounding down.

## 3. Claiming rewards

- Generated world rewards are **shared, single-claim pickups**: one player claims each reward.
- Big reward choices are generated for the **claiming player** based on their unlocked elements and owned Runes.
- A player cannot be offered an element already unlocked. Duplicate Runes should upgrade an existing Rune's rarity if eligible rather than creating duplicate equipped effects; maxed Runes are excluded.
- Personal rewards apply only to the player who claims them.
- Track loot claimed by each player. The game may subtly recommend that the least-rewarded player take the next valuable pickup, but does **not** enforce ownership.
- All players see rewards and can communicate who should take them.

## 4. Traders

Trader stock increases with party size:

| Players | Big offers | Normal offers | Minor offers | Total stock |
|---|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | **3** |
| 2 | 1 | 2 | 1 | **4** |
| 3 | 1 | 2 | 2 | **5** |
| 4 | 2 | 2 | 2 | **6** |

- Trader stock is **shared**; each item is available for purchase once.
- At least one Minor slot offers Food.
- **Shop prices do not scale** with party size; use the same prices as the main boon/economy specification.
- Each player has a **personal gold balance**.
- A purchaser may leave a bought item for a teammate to claim. Unrestricted transfers and item trading are not part of the initial version.
- Rerolls, if available, reroll remaining inventory rather than restoring purchased stock; base reroll proposal: 40 gold for the first reroll, 80 gold for an optional second reroll.

### Gold rewards

- Gold from enemies and encounter completion is automatically divided evenly between party members, regardless of who landed the killing blow.
- Apply the same 100% / 150% / 200% / 250% **total-income scaling** before splitting the generated gold.
- Example: an encounter worth 100 gold solo generates 150 total with two players (75 each), 200 with three players (~66.7 each), and 250 with four players (62.5 each).
- Retain fractional gold in a hidden accumulator so rounding does not consistently penalize parties.
- Separately claimable gold pickups from reward nodes follow the shared single-claim loot rule, unless intentionally marked as an encounter-wide payout.

## 5. Enemy scaling

Initial balancing targets, subject to playtesting:

| Players | Standard enemy HP | Enemy count | Boss HP |
|---|---:|---:|---:|
| 1 | 100% | 100% | 100% |
| 2 | 135% | 140% | 175% |
| 3 | 165% | 175% | 240% |
| 4 | 195% | 210% | 300% |

- Scale regular encounters mainly through **more enemies and moderate HP increases**, not sharply increased enemy damage.
- Keep enemy damage close to solo baseline initially; more simultaneous threats already make combat more difficult.
- Preserve area-specific encounter identity, number of encounters per large stage, and wave structure per small stage.
- Waves may contain additional enemies or additional concurrent enemy types in multiplayer.
- Enforce an active-enemy cap for readability and performance.
- Bosses have more HP and periodically retarget different players, but retain their core movesets; do not simply quadruple their attack frequency.

## 6. Downed state, revive and defeat

### Downed state

- At **0 HP**, a player becomes **Downed** rather than dying immediately.
- Downed players cannot move, attack, or cast.
- A downed player has **25 seconds** to be revived before becoming fully defeated.
- Allies can see and approach the downed player.

### Manual revive

- A living teammate must stand near the downed player and **hold F for 5 uninterrupted seconds**.
- Reviver must remain within interaction range; they cannot attack or cast while channeling.
- Releasing F, leaving interaction range or taking damage interrupts the revive and resets progress (initial rule).
- Successful revive restores **30% of the downed player's maximum HP**.
- Revived player receives **2 seconds of damage protection**.
- Revive needs no currency or consumable.

### Repeat-down penalty within the same stage

| Previous revives received this stage | Timer on next down |
|---|---:|
| 0 | 25 sec |
| 1 | 18 sec |
| 2 | 12 sec |
| 3+ | 8 sec |

- Revive channel time remains 5 seconds.
- The repeat-down counter resets on the next stage.

### Fully defeated players

- Once the downed timer expires, the player spectates until the party clears the stage and transitions onward.
- On entry to the next stage, the defeated player returns with **30% maximum HP**, retaining all their elements, boons, Runes and other run progression.
- Automatic respawn does **not** additionally grant the normal stage-transition HP regeneration.
- During a boss fight, defeated players cannot return until the boss is defeated and the party proceeds to the next stage.
- **If no living players remain** (all teammates are downed or fully defeated), the run ends immediately.

## 7. Stage routes and voting

- Players choose the next stage together after clearing the current one.
- Each available exit shows the destination's **reward tier/type** (Big / Normal / Minor and where appropriate a more specific reward indication).
- Every party member, including downed or spectating members, may cast one vote.
- The route with the **most votes** wins.
- **If votes tie for the highest count, choose randomly among the tied routes**, with equal probability. This explicitly includes a **2–2 split in four-player co-op**; neither the host nor the party leader gets a deciding vote.
- A 1–1 tie in two-player co-op and ties such as 1–1–1 or 2–1–1 where applicable follow the same rule: randomly select among the routes tied for the largest vote count.
- The whole party loads into the selected stage. Players cannot split into separate destination maps.
- The duration of the vote and the behavior when a player does not vote remain implementation settings to finalize; a reasonable default is to abstain after a short timer and resolve using submitted votes, with an equal random choice among available exits if nobody votes.

## 8. Co-op combat interactions

- Friendly fire is off, including area-of-effect Novas and signatures.
- Damage belongs to the caster for damage calculations, elemental boons and kill-related triggers.
- Status buildup (Burning, Wet, Chill/Frozen) is accumulated **on the target**, so different players can cooperate to reach a threshold.
- Use the same status reactions and enemy resistance rules as in solo play.
- Do not introduce additional co-op-only combination spells or dedicated party-buff signatures at this stage.
- Effects that grant a buff to the caster remain personal unless an ability expressly says otherwise.

## 9. Open balancing/implementation decisions

- Exact per-stage loot-credit allocations and generator constraints, especially Big-reward caps and guaranteed early elemental unlock access.
- Fairness indicator UI and whether fairness weighting ever affects generation beyond advice.
- Precise enemy director weights, simultaneous-enemy caps and boss targeting rules.
- Revive interaction radius and whether partial revive progress should persist briefly after interruption.
- Route-vote timer, no-vote handling and disconnect/reconnect handling.
- Whether changing the number of active players mid-run recalculates future budgets only (recommended) and how already-generated rewards are treated.

**Scope:** This file specifies gameplay systems only. Art direction, presentation aesthetics and production styling are intentionally excluded.
