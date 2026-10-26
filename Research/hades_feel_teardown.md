# Hades — Movement, Camera & Animation "Snap" Teardown

**Target:** Steam install, `C:\Program Files (x86)\Steam\steamapps\common\Hades`
**Purpose:** Reference for Prime Alchemy's combat feel.
**Method:** REA with Ghidra 12.1.4 (decompilation of `EngineWin64s.dll`) + the shipped PDB's symbols, Lua scripts (`Content/Scripts`), and SJSON data (`Content/Game`).

> **Evidence levels used below.** **Observed**: a value or line read directly from a shipped file. **Decompiled**: Ghidra 12.1.4 pseudocode via REA. Function and global names come from the shipped PDB's public symbols, mapped onto Ghidra addresses (REA's isolated import doesn't load the PDB itself). **Inferred**: a reading of what a field does, based on its name and how it's used, without the code proving it.

---

## 0. How Hades is built (why the feel is mostly data)

| Layer | File(s) | What it owns |
|---|---|---|
| Native engine "gsge" (The Forge based), namespace `sgg::` | `x64/EngineWin64s.dll` (7.2 MB) + **shipped `EngineWin64s.pdb` (44 MB, full symbols)** | Physics, unit movement, camera, animation playback, time scaling |
| Gameplay scripts | `Content/Scripts/*.lua` (Lua 5.2) | Hit-stop, camera moves, screenshake, rumble, room intros |
| Tuning data | `Content/Game/**/*.sjson` | Unit speeds, weapon timings, per-frame animation timing |

REA export inspection of the engine DLL: 67 exports, amd64 PE (Evidence `ev_857aa121…f0e6`, DLL sha256 `4165a69c…befd`).

Engine systems found in the PDB (observed symbol names):

- **Movement:** `Unit::UpdateMovement`, `Unit::MoveInput`, `Unit::GetSpeedOrVelocity`, `Unit::GetMaxSpeed`, `Unit::UpdateAngle`, `Unit::PlayMoveAnimation`, `PlayerUnitInput::DirectMovement`, `PhysicsSystem::ApplyFriction`, `AccelerationSystem`, `VelocitySystem`
- **Camera:** `Camera::Update`, `Camera::LazyTether`, `Camera::GetTetherLocation`, `Camera::GetWeightedZoom`, `Camera::GetDynamicZoomTarget`, `Camera::MoveToOverDuration`, `Camera::ApplyClamp`, `Camera::Shake`, and `CameraSplineHelper::{GenerateEase, GenerateOvershootSpline, GenerateUndershootSpline, GenerateMovingHold}`
- **Animation:** `AnimationFractionFrom{Duration,Frame,Slide}System`, `Animation::SetFractionalFrame`, `Animation::PlayToFraction`, `Animation::UseAttachedToTimeMultiplier`
- **Time:** `TimeModifierSystem`, plus the script binding `AdjustSimulationSpeed`

The engine supplies generic building blocks. The "Hades feel" comes from **the numbers fed into them**.

---

## 1. Movement (Zagreus, `Game/Units/PlayerUnits.sjson` → `_PlayerUnit`)

Observed values:

| Field | Value | Reading |
|---|---|---|
| `Speed` | **540** u/s | Base run speed |
| `Acceleration` | 2000 | **Not used for normal running.** Decompiled: velocity is set directly (§1.1). An acceleration from unit data is only used via `ApplyForce` while a force window is active or the hero is moving faster than max speed. |
| `Thing.Grip` | 1000 | Friction/deceleration (`PhysicsSystem::ApplyFriction`) |
| `RotationSpeed` | **216 000 °/s** | 600 turns per second. Gameplay facing is effectively instant. |
| `CosmeticRotationSpeed` | 1340 °/s | The *visual* turn is separate and fast: ~0.13 s for 180°. |
| `FullControlVelocityThreshold` | 400 | Not read by the functions decompiled here. Those use **max speed + 1** as the full-control cutoff (§1.1). Its exact role is unverified. |
| `BackpedalSpeedModifier` | 0.34 | Speed penalty when moving against the facing direction (e.g. while aiming) |
| `TouchdownVelocityRetention` | 0.7 | Keeps 70% of momentum on landing |
| `StopShiftOnCollision` / `CanVelocityBeAbsorbed` | false / false | Collisions don't kill the hero's momentum |
| `LowSpeedThreshold` / `HighSpeedThreshold` | 0.5 / 700 | Walk vs. run animation switching |

**Animation matches speed (decompiled).** At the end of every `Unit::MoveInput` the engine sets the animation's `PlaySpeedMultiplier` component to `|velocity| / NativeMoveSpeed`. `ZagreusRun` has `NativeMoveSpeed = 540`, equal to `Speed`, so the run cycle plays at exactly 1× at base speed and scales with speed buffs and slows. Feet never slide. The run cycle uses **64 facing angles**. Idle and stop use 32.

### 1.1 Engine movement model (decompiled)

Call chain: `PlayerUnitInput::DirectMovement` (0x1802e45c0) → `Unit::MoveInput` (0x1802eb7b0) → `Unit::UpdateMovement` (0x1802ebb60), with `PhysicsSystem::ApplyFriction` (0x1802ccf80) running separately.

1. **Input → angle + fraction.** `DirectMovement` reads `InputHandler::GetDirection()` and passes it through `rotateInput`. With the shipped defaults `rotateInput` only flips the Y axis to world space; there's no isometric rotation offset. Below an epsilon (1e-4) there's no move this frame. Speed fraction is **1.0**, or a reduced fraction from player unit data when the input magnitude² is under a threshold. Inferred: the threshold/fraction pair is `LowSpeedThreshold`/`LowSpeedFraction` (0.5 / 0.2), i.e. gentle stick = walk. Movement direction is `atan2` of the input, so it's fully analog. An optional axis-lock field can snap movement to one direction or its opposite.
2. **Velocity is assigned, not accelerated.** In `MoveInput`, `maxSpeed = (Speed + bonus) × multiplier`. When the current speed is **≤ maxSpeed + 1** and no force window is active, the engine *writes* `velocity = (cos θ, −sin θ) × fraction × maxSpeed` that frame. **Full speed on frame 1, instant direction reversal, no turn radius.**
3. **Above max speed (dash, knockback)** the input doesn't overwrite velocity. It calls `PhysicsComponent::ApplyForce(angle, …)` instead, so you steer the excess momentum but can't cancel it. The same `ApplyForce` path, using an acceleration value from unit data, is used while a per-physics force timer (decremented in `ApplyFriction`) is running.
4. **Instant stop.** In `UpdateMovement`, if there's no move input this frame, there *was* input last frame, the hero is at or below max speed and not airborne, the engine calls `MultiplyVelocity(0)`. Releasing the stick stops Zagreus dead the next frame. Excess momentum (above max speed) is not zeroed. Friction removes it.
5. **Friction is linear.** `ApplyFriction` subtracts `grip × dt` along the velocity direction and clamps at 0. That's a constant deceleration, not exponential damping, so a dash's overspeed bleeds off at a fixed rate set by `Grip` (1000 on the hero).
6. **Move start/stop events.** `UpdateMovement` integrates position (with a one-shot `ApplyShift` boost along velocity), resolves collision via `ApplyFullShift`, and flips an "is moving" flag when per-frame displacement crosses ~30 × dt (≈30 u/s). That fires `ScriptManager::OnPlayerMoveStarted` / `OnPlayerMoveStopped`, which drive the start/stop animations and Lua hooks.

Evidence: `ev_6d6e6a8e…` (DirectMovement), `ev_cfc0ae1e…` (MoveInput), `ev_736db913…` (UpdateMovement), `ev_4da4e9f6…` (ApplyFriction), `ev_fb60a6b6…` (rotateInput).

**Start/stop transitions never block input.** `ZagreusStart` (32 frames) chains into `ZagreusRun`. `ZagreusStop`, `ZagreusIdle` and every `*_ReturnToIdle` carry **`CancelOnOwnerMove = true`**. That flag appears 171 times in `CharacterAnimationsHero.sjson`. Any stick input cuts a recovery or settle animation on the frame it arrives.

### Dash (`Game/Weapons/PlayerWeapons.sjson` → `RushWeapon`)

The dash is implemented as a **weapon** of `Type = "BLINK"`, not as a movement state.

| Field | Value |
|---|---|
| `BlinkDuration` | **0.21 s** |
| `BlinkMaxRange` / `WeaponRange` | 400 / 300 |
| `BlinkEaseIn` / `BlinkEaseOut` | **0 / 0.8**: full speed on frame 1, then decelerates into the end |
| Invulnerable + `ImmuneToForce` | 0.24 s (slightly longer than the travel) |
| `Cooldown` | 0.05 s |
| `ClipSize` / `ClipRegenInterval` | 1 / 0.74 s |
| `CanCancelDisables` | **true**: dash cancels attack recovery (see §3) |
| `BlockMoveInput` | true during the blink |
| `RushWeaponSelfSlow` | ×0.65 speed for 15 frames after the dash |
| `RushWeaponDisableRotation` | 1 frame |
| `BlinkCameraLerpTime` | Not set on `RushWeapon`. Set to 0 on `SwordSpecialMiniDash` / `FistSpecialMiniDash`, so the camera snaps with those mini-blinks instead of easing. |

---

## 2. Camera

The camera is **rigidly locked to a weighted tether point**. All of its smoothness comes from a separately smoothed **aim lean**, not from lagging behind the player. Room scripts drive it per room.

### 2.1 Follow model (decompiled `Camera::Update` 0x1802f7020, `GetTetherLocation` 0x1802f6c30, `GetMoveGoalLocation` 0x1802f6960, `LazyTether` 0x1802faa50, `GetLocation` 0x1802fa3a0)

1. **Goal point.** `GetMoveGoalLocation` picks one of three sources:
   - If a bounds rectangle is set: the average of all players' positions, clamped into the rectangle via `PointLineIntersection`.
   - Otherwise, if tether targets exist: `GetTetherLocation`, a **weighted average** of the tethered things' positions (per-id weight from `SetCameraTetherWeight`, default 1.0) plus the script offset (`LockCamera` `OffsetX/Y`).
   - Otherwise: a fixed location.
2. **Aim lean is a virtual tether target.** `GetTetherLocation` adds `player + leanOffset` as one more target with weight `MouseTetherWeight`, after clamping the lean length to `MouseTetherZone`. With one hero at weight 1 and lean weight 1, **the camera sits halfway between Zagreus and his lean point**.
3. **No follow lag.** In normal play (no timed move, no lazy flag, editor edge-pan off) `Update` sets `camera = goal` **every frame**. There's no lerp and no spring. Scripted moves are the exceptions:
   - `MoveToOverDuration` evaluates an eased path over a duration.
   - The `CameraSplineHelper` paths (ease, overshoot, moving-hold) run per axis.
   - A speed + acceleration `stepToward` mode is also available.
4. **Lean target.** The input is the virtual cursor vector `v` (normalized screen space; 1.414 = corner). The lean target is
   `v̂ · (MouseXDistanceMultiplier, MouseYDistanceMultiplier) · clamp((|v| − MouseDeadZone)/(1.414 − MouseDeadZone), 0, 1) · MouseTetherZone`.
   Pushing the cursor to a corner targets the full 800 × 520 px lean. The camera moves half of that: **≤ 400 px horizontally, ≤ 260 px vertically**.
5. **Lean smoothing.** The lean offset moves toward its target at `propel × dt × clamp(dist / MouseTetherZone, 0, 1)`. Speed is proportional to remaining distance, which gives an exponential approach with time constant `MouseTetherZone / propel`:
   - Mouse: `MousePropelSpeed` 1000 → **τ ≈ 0.8 s**.
   - Controller, moving further in the same direction: `ControllerPropelSpeed` 300 → **τ ≈ 2.7 s** (deliberately slow, avoids nausea from stick flicks).
   - Controller, reversing (dot ≤ 0): `ControllerReturnPropelSpeed` 500 → **τ ≈ 1.6 s**.
   - Inferred: which pair is used depends on a per-player "using mouse" flag.
   - When the tether is disabled (`ZeroMouseTether`, cinematics), the lean decays to 0 at the mouse rate.
6. **`LazyTether`** applies only while a lazy flag is set. Per axis, if the goal moved *away* from the camera, the camera moves by exactly the goal's per-frame delta. If the goal moved *toward* it, the camera stays still. The existing gap never shrinks on its own, only when the player walks back into it, and the flag clears once camera == goal. It's a "no-drift" hand-off after scripted moves. What sets the flag was not traced.
7. **Zoom** moves linearly toward `GetGoalZoom()` (weighted zoom / dynamic zoom) at a fixed rate × dt. It's not eased in the engine. Eased zoom comes from scripted `FocusCamera` splines.
8. **Final position.** `GetLocation()` = camera position + shake offset. `ApplyClamp` handles bounds afterward.

**Recovered `ConfigOptions` defaults.** These are static initializers in `EngineWin64s.dll`, found by scanning `mov [rip+opt], imm32` / `imm8` stores and confirmed by decompiling the `MouseTetherZone` initializer at 0x18000f1a0:

| Option | Default |
|---|---|
| `MouseTetherEnabled` | true |
| `ZeroMouseTether` | false |
| `MouseTetherWeight` | 1.0 |
| `MouseTetherZone` | 800.0 |
| `MouseXDistanceMultiplier` / `MouseYDistanceMultiplier` | 1.0 / 0.65 |
| `MouseDeadZone` | 0.0 |
| `MousePropelSpeed` | 1000.0 |
| `ControllerPropelSpeed` / `ControllerReturnPropelSpeed` | 300.0 / 500.0 |
| `DeadZone` (stick) | 0.225 |
| `CameraShake` | true |
| `CameraFollowCursor`, `CameraEdgePanSpeed` | 0 (editor-only paths, off in game) |

These are engine defaults. A player's profile config can override any of them at runtime.

**Script-side controls (observed):**
- Scripts call `ZeroMouseTether(flag)` / `UnzeroMouseTether(flag)` (`UIScripts.lua:2513`) to disable the lean during intros, deaths and doors, using named flags.
- Zoom blends per object id via `SetCameraZoomWeight`. Bosses and specific rooms set `CameraZoomWeights`.
- `SetCameraClamp`, `SoftClamp`, `CreateCameraWalls` and `SetCameraRail` handle bounds.

Evidence: `ev_6a89aa71…` (Update), `ev_571c8a31…` (LazyTether), `ev_0aac6b49…` (GetTetherLocation), `ev_b144c069…` (GetMoveGoalLocation), `ev_2b231be9…` (GetLocation), `ev_bcaac3bd…` (MouseTetherZone initializer).

**Per-room zoom (observed, `RoomData*.lua` `ZoomFraction`):** most rooms are 0.75–0.95. The most common values are 0.85 (25 rooms), 0.95 (19), 0.80 (15) and 0.75 (13). Between rooms, zoom lerps over `ZoomFractionAdjustTime` (default 1.4 s, `RoomPresentation.lua:1167`).

**Moves are splines, not plain lerps.** `FocusCamera` and `PanCamera` take a `ZoomType` of `"Ease"`, `"Overshoot"` or `"Undershoot"`, with optional `EaseIn`/`EaseOut`. Examples:
- Boss reveal: `FocusCamera({ Fraction = 1.0, ZoomType = "Overshoot", Duration = 0.17 })` (`RoomPresentation.lua:634`)
- Weapon charge "breath": `ChargeCameraMotion = { ZoomType = "Overshoot", Fraction = 0.95, Duration = 0.6 }` (Bow). Spear spin uses `0.96 / 0.2 s`.
- `DoCameraMotion` (`CombatPresentation.lua:2011`) multiplies the motion's zoom by the room's `ZoomFraction`, so effects are relative. It can also restore the default zoom after `RestoreDefaultDuration`.

**Screenshake (`ShakeScreen`):** parameters are `Speed`, `Distance` (px), `FalloffSpeed`, `Duration`, and an optional `Angle` / `DynamicAngleOffset` (shake along the attack direction). Common presets:

| Use | Speed | Distance | Falloff | Duration |
|---|---|---|---|---|
| Light | 300 | 3 | 2000 | 0.3 |
| Medium | 500–600 | 4–6 | 1000–2000 | 0.3 |
| Heavy | 900 | 8 | 2000 | 1.05 |
| Sword combo hit 2 | 300 | 6 | 0 | 0.1, `Angle = 90` (vertical) |

Many weapon `FireScreenshake` / `HitScreenshake` entries are **commented out** in `WeaponData.lua`. The designers removed most per-swing shake and kept hit-stop as the main impact signal.

---

## 3. Why animations feel snappy

### 3.1 Anticipation is drawn, then skipped
Slide animations list a `DurationFrames` value for **every** source frame. Hades sets most of them to **0**, which skips the frame. Parsed from `CharacterAnimationsHero.sjson` (frames at 60 Hz, inferred):

| Animation | Source frames | Frames actually shown | Shown time | Breakdown |
|---|---|---|---|---|
| `ZagreusSwordCharge1` | 102 | 1 pose | (held during charge) | Only **frame 12 = "Last frame Anticipation 1"**, held ×9 |
| `ZagreusSwordAttack1` | 102 | 8 | **0.25 s** | Frames 16–22 ×1 (swing), **frame 23 held ×8** (contact pose) |
| `ZagreusSwordAttack2` | 102 | 4 | 0.30 s | Frames 38–40 ×1, **frame 41 held ×15** |
| `ZagreusSwordAttack3` | 102 | 21 | 0.40 s | Frames 55–74 ×1, frame 75 held ×4 |
| `ZagreusSpearAttack1` | 66 | — | 0.35 s | 56 of 66 frames skipped |
| `ZagreusGunFire` | 170 | — | **0.25 s** | 156 of 170 frames skipped |

The pattern:
1. **Anticipation collapses to one key pose.** The sword weapon's `ChargeTimeFrames = 4`. During those 4 frames the game shows only the *extreme* of the windup, and the in-between frames are never displayed.
2. **The swing plays at ~1 frame per drawing**, about 7 frames for a full arc, so it reads as a smear.
3. **The contact pose is held** (8–15 frames). The player gets a clear read at the moment of impact.
4. **Recovery is a separate animation** (`*_ReturnToIdle`) with `CancelOnOwnerMove = true`. It's purely cosmetic and any movement input cancels it.

Across the hero file, **15 973** slide entries are `DurationFrames = 0`. Hades animates full, smooth animations in the source art and then *edits the timing in data*. Animators keep their in-betweens, and designers pick which frames ship.

### 3.2 Gameplay locks are short and separate from the art
`SwordWeapon` effects (observed):

- `SwordDisable`: **5 frames**, no attack/rotate, **movement allowed**, not cancelable
- `SwordDisableCancelableAndLockTrigger`: 11 frames, `Cancelable = true`. The dash's `CanCancelDisables` clears it.
- `SwordSelfSlowFire`: ×0.35 move speed for 12 frames. You keep drifting while swinging instead of rooting in place (`RootOwnerWhileFiring = false`).
- `SwapOnFire = "SwordWeapon2"` → 3-hit combo via weapon swapping. `RequestTriggerLock` / `AcceptTriggerLockRequests` / `AllowMultiFireRequest` are inferred to buffer the next press.

Inferred result: you can dash out of a swing after ~5 frames (~83 ms). The animation's length never decides when you regain control.

### 3.3 The dash animation is a held streak
- `ZagreusDashNoCollide` shows frames 0–7 (11 frames), then **holds frame 8 ×99**. That's one stretched "streak" pose for however long the 0.21 s blink lasts.
- It then chains to `ZagreusDashCollide` (recovery, frames 13–59), which has `CancelOnOwnerMove = true`.
- Dash anims set **`TimeModifierFraction = 0.1`**. Inferred: they're only 10% affected by global slow-mo, so a dash started during hit-stop still feels instant.

### 3.4 Hit-stop is micro slow-motion, not a freeze
`DoWeaponHitSimulationSlow` (`CombatPresentation.lua:2072`) reads each weapon's `HitSimSlowParameters` and calls `AdjustSimulationSpeed`. Observed values:

| Weapon | Delay after hit | Slow to | Hold | Ramp back |
|---|---|---|---|---|
| `SwordWeapon` (hit 1) | 40 ms | **10%** | 10 ms | 30 ms |
| `SwordWeapon2` | 20 ms | 10% | 20 ms | 70 ms |
| `SwordWeapon3` | 60 ms | 10% | 50 ms | 70 ms |
| `RangedWeapon` | 20 ms | 30% | 20 ms | 70 ms |
| `ShieldWeaponRush` | 40 ms | 1% | 80 ms | 0 |

Rules (observed in Lua):
- Waits use `waitScreenTime`, which runs on real time and is unaffected by the slow itself.
- **Crits and kills add +40 ms** to the hold (`ShouldIncreasePlayerHitPause`). Vulnerability/backstab bonus is explicitly disabled.
- **No stacking.** If any sim-speed change is active (`MapState.SimSpeedChanges`), a new hit-stop is skipped. Only `Priority` events (last kill, assist, death) override.
- `HitSimSlowCooldown` (0.03–0.25 s) rate-limits hit-stop on multi-hit weapons.
- Hit-stop only fires when the player is the attacker, or when the defender has `SimulationSlowOnHit`.
- Last enemy killed: `AddSimSpeedChange("LastKill", { Fraction = 0.35, Priority = true })` plus radial blur, bloom and a frame zoom (`AdjustFrame`).

Each hit is also layered with controller rumble (`HitRumbleParameters`, e.g. 17% right motor for 0.15 s), hit flash, and occasionally a camera motion.

---

## 4. Takeaways for Prime Alchemy

0. **Assign velocity, don't accelerate it.** Within max speed, set `velocity = dir × speed` every frame and zero it on release. Let only *overspeed* (dash, knockback) be physical: steer it with a force and bleed it off with linear friction. This is the single biggest contributor to Hades's responsiveness.
1. **Split gameplay timing from art timing.** Drive lockouts with short effect windows (5 frames of no-attack, cancelable after that). Let animations be cosmetic and interruptible.
2. **Per-frame hold tables.** Have animators deliver full animations, then use a per-frame duration table (0 = skip, N = hold) to cut anticipation to one key pose and hold the contact pose. This is cheap to tune without new art.
3. **Instant facing, fast cosmetic turn.** Separate gameplay rotation (instant) from visual rotation (~0.1 s for 180°).
4. **Cancel recovery on any input.** A `CancelOnOwnerMove`-style flag on every settle, stop and return-to-idle animation.
5. **Dash = ease-in 0, ease-out ~0.8**, about 0.2 s of travel. Make the i-frames slightly longer than the travel. The dash should cancel attack recovery and be mostly immune to slow-mo.
6. **Hit-stop budget: 10–50 ms at ~10% speed, then a 30–70 ms ramp.** Use real-time waits, no stacking, +40 ms on crits and kills, and a per-weapon cooldown.
7. **Camera.** Lock the camera rigidly to the tether point (no follow lag). Add the aim lean as an extra weighted tether target, clamped to ~800 px with less vertical reach (×0.65). Smooth *only the lean*, with distance-proportional speed: τ ≈ 0.8 s for mouse, slower for stick. Shape scripted zoom moves as overshoot/ease splines, make effect zooms relative to the room's base zoom, and use named "disable lean" flags for cinematics.
8. **Co-op (up to 4 players).** Hades's tether is already a weighted average of multiple targets, and `GetMoveGoalLocation` already averages *all players* when a bounds rectangle is set. That's the right model for framing 4 players: give each player a tether weight, use dynamic zoom with buffers, and clamp to the room. With 4 players, drop or shrink the per-player aim lean (four leans averaged turn to mush). Hit-stop needs a co-op decision: global slow-mo across 4 players gets noisy, so consider per-attacker local time scaling (Hades's `ElapsedTimeMultiplier` / `TimeModifierFraction` show it supports per-object time).

---

## 5. Key file references (Hades install)

- `Content/Game/Units/PlayerUnits.sjson`: `_PlayerUnit` movement constants
- `Content/Game/Weapons/PlayerWeapons.sjson`: `RushWeapon` (dash), `SwordWeapon` disable windows
- `Content/Game/Animations/CharacterAnimationsHero.sjson`: per-frame slide timing
- `Content/Scripts/WeaponData.lua`: `HitSimSlowParameters`, `HitScreenshake`, `ChargeCameraMotion`, rumble
- `Content/Scripts/CombatPresentation.lua`: `DoWeaponHitSimulationSlow` (~l.2072), `AddSimSpeedChange` (~l.2124), `DoCameraMotion` (~l.2011), `DoWeaponScreenshake`
- `Content/Scripts/RoomPresentation.lua`: room-start camera lock/zoom, mouse-tether zeroing
- `x64/EngineWin64s.pdb`: full `sgg::` symbol names (7 040 unique non-template names extracted)

## 6. Question checklist

| Question | Status |
|---|---|
| Movement constants and transitions | **Answered** (data observed) |
| Movement formula (accel/grip/full-control interplay) | **Answered** (decompiled: direct velocity, instant stop, linear friction, force-based overspeed) |
| Camera behaviour model and script API | **Answered** (decompiled + script usage) |
| Camera default tether/lazy/mouse-lean numbers | **Answered** (engine defaults recovered; profile config can override) |
| Animation snappiness | **Answered** (frame tables observed) |
| Hit-stop / impact layering | **Answered** (Lua + data observed) |

## 7. Unknowns and how to close them

Decompiled so far (REA + Ghidra 12.1.4, DLL sha256 `4165a69c…befd`): `Camera::Update`, `Camera::LazyTether`, `Camera::GetTetherLocation`, `Camera::GetMoveGoalLocation`, `Camera::GetLocation`, `PlayerUnitInput::DirectMovement`, `Unit::MoveInput`, `Unit::UpdateMovement`, `PhysicsSystem::ApplyFriction`, `rotateInput`, `ConfigOptions::Defaults`, and the `MouseTetherZone` initializer. PDB-to-address mapping was done with a stdlib MSF reader over the PDB's public symbols. REA's Ghidra import does not load companion PDBs.

Still open:
- **Struct field names.** Fields are reached by raw offsets. Mappings like unit-data `+0x60/+0x64` → `LowSpeedThreshold/LowSpeedFraction`, the physics force timer `+0x48`, and the "using mouse" flag at player `+0x24` are inferred from behaviour. Confirming them needs `UnitData::Read` / `PlayerUnitData` decompiles, or type info from the PDB's TPI stream.
- **`FullControlVelocityThreshold`** was not seen in the decompiled path. Its consumer is untraced.
- **What sets the camera's lazy-tether flag**, and how `TimeModifierFraction` / `ElapsedTimeMultiplier` scale per-object `dt`. Next targets: `Camera::Focus`, `Camera::MoveToOverDuration`, `TimeModifierSystem::RunJobs`.
- **Player profile overrides.** Hades may ship or write config values that override the `ConfigOptions` defaults above. No such file is in the install. A saved profile under Documents was not present on this machine.
- **Frame rate of `DurationFrames`.** Assumed to be 60 Hz game frames. This is consistent with `PlaySpeed = 60` and the `Duration`/`DurationFrames` pairs, but not proven.
