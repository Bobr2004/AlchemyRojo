# Hades Feel Reference — Movement, Dash, Attacks, Camera, Impact

**Purpose:** Design reference for making Prime Alchemy feel like Hades. Every number here was read from Hades' shipped data files or decompiled from its engine (`EngineWin64s.dll`). Raw evidence, addresses and confidence levels are in [`../Research/hades_feel_teardown.md`](../Research/hades_feel_teardown.md).
**Units:** Hades world units. Zagreus is **200 units tall** (`Tallness = 200`). Roblox conversions below use **1 stud ≈ 40 units**, scaling a 5-stud R15 character to Zagreus' height. That's a proportional scale rule, not an engine fact.

---

## 0. The six rules behind the feel

1. **Velocity is assigned, never accelerated.** Full speed on frame 1, dead stop on release.
2. **Gameplay locks are tiny and separate from the art.** Attacks lock you for ~5 frames, and the animation never decides when you regain control.
3. **Anticipation is collapsed to one pose; contact is held.** The swing is a smear, and the hit pose lingers.
4. **Hit-stop is short micro slow-motion, not a freeze.** 10–50 ms at ~10% speed.
5. **The camera never lags the player.** It's rigidly attached; only a smoothed aim lean moves independently.
6. **Everything is data.** Every frame window, hold, slow and shake is a table value designers tune without code.

---

## 1. Movement

| Parameter | Hades | Roblox starting value |
|---|---|---|
| Run speed | 540 u/s (2.7 body heights/s) | **~13.5 studs/s** |
| Acceleration | none for normal running (velocity set directly) | set velocity directly |
| Stop | velocity × 0 on the first frame without input (when ≤ max speed) | zero velocity on release |
| Turn (gameplay) | 216 000 °/s, effectively instant | instant |
| Turn (visual) | 1340 °/s, ~0.13 s for 180° | lerp the visual model only |
| Overspeed (dash, knockback) | not overwritten. Input steers it via a force, and linear friction (`Grip` 1000 u/s²) bleeds it off | ~25 studs/s² linear decel |
| Analog walk | below an input threshold, speed × a low fraction (data suggests 0.5 / 0.2) | stick < ~0.5 → slow walk |
| Backpedal (moving against facing) | × 0.34 | × ~0.35 while aiming backward |
| Collision | doesn't kill hero momentum | keep momentum on light bumps |

**Engine logic (decompiled):**
```
each frame:
  if speed <= maxSpeed + 1 and no force window:
      velocity = inputDir * inputFraction * maxSpeed      -- assigned
  else:
      applyForce(inputDir, accel)                          -- steer the overspeed
  if no input now and input last frame and speed <= maxSpeed and grounded:
      velocity = 0                                         -- instant stop
  friction: velocity -= normalize(velocity) * grip * dt   (clamp at 0)
  runAnim.playSpeed = |velocity| / nativeMoveSpeed         -- no foot sliding
```

**Animation transitions:** a start animation (32 frames) chains into the run loop. Stop, idle and every return-to-idle animation is **canceled by any movement input**; Hades sets that flag on 171 hero animations. The run loop is drawn at native speed 540 and played at `|v| / 540`.

**Roblox:**
- `Humanoid.WalkSpeed` + `Humanoid:Move()` already behaves like assigned velocity. Set `AutoRotate = false` and drive facing from aim. Rotate only the visual root smoothly.
- Implement dash and knockback as a custom overspeed state (LinearVelocity / AssemblyLinearVelocity) with your own friction step, not the Humanoid.
- Drive run animation speed with `AnimationTrack:AdjustSpeed(speed / nativeSpeed)`.
- Character movement is client-owned on Roblox, so movement can be instant. Keep it that way.

---

## 2. Dash

| Parameter | Hades (`RushWeapon`) | Roblox starting value |
|---|---|---|
| Travel time | **0.21 s** | 0.21 s |
| Distance | max 400 u (~2 body heights) | **~10 studs** |
| Easing | ease-in **0**, ease-out **0.8**: full speed on frame 1, decelerates into the end | same curve |
| Invulnerability | **0.24 s** (slightly longer than travel), also immune to knockback | 0.24 s |
| Collision | no unit collision during the dash | pass through enemies |
| Cooldown | 0.05 s between presses; 1 charge regenerating in 0.74 s | match, per-hero charges |
| After dash | ×0.65 move speed for 15 frames (keeps chained dashes from out-running everything) | same |
| Facing | can't rotate for 1 frame, then free | same |
| Cancels | **cancels attack recovery and cancelable disables** | dash cancels LMB/Q/R recovery |
| Animation | 11 frames of motion, then **one streak pose held** for the rest of the blink; recovery canceled by any movement input | same structure |
| Slow-mo | dash animation is only 10% affected by global slowdowns, so dashing during hit-stop still feels instant | dash ignores local hit-stop |

---

## 3. Attacks: frame data and cancel windows

Hades' sword, first hit:

| Phase | Frames (60 Hz) | What's shown |
|---|---|---|
| Startup ("charge") | **4** | **one** extreme anticipation pose (13 drawn frames reduced to 1) |
| Swing | ~7 | one drawing per frame (a smear) |
| Contact hold | **8** (hit 2: 15, hit 3: 4) | the impact pose, frozen |
| Recovery | separate animation | canceled by any movement input |

Gameplay locks (separate from the art):
- **5 frames:** no attack, no rotate, movement allowed, **not** cancelable.
- **11 frames:** no attack, no rotate, **cancelable by dash**.
- Move at ×0.35 speed for 12 frames while firing. Never rooted.
- Combo via weapon swap (hit 1 → hit 2 → hit 3). The next press is buffered during the lock (trigger-lock requests).

**Art rule:** animators draw full, smooth animations. A **per-frame duration table** then decides what ships:
- `0` = skip the frame.
- `N` = hold for N frames.

In Hades' hero file, 15,973 frame entries are set to 0. Sword hit 1 has 102 drawn frames and shows 8.

**Roblox:**
- Author snappy keys: constant or linear easing into the anticipation pose, a hard hold on contact.
- Implement holds with `AnimationTrack:AdjustSpeed(0)` for N frames at a marker, then resume. Skipping is `TimePosition` jumps or just not keying the in-betweens.
- Use `GetMarkerReachedSignal("Hit")` to spawn hitboxes, never wall-clock timers.
- Keep lock and cancel windows in a data table per attack: `startupFrames`, `lockFrames`, `cancelableFrames`, `moveSpeedMul`, `buffer = true`.

---

## 4. Impact: hit-stop, shake, rumble

**Hit-stop (`AdjustSimulationSpeed` via `HitSimSlowParameters`):**

| Weapon / hit | Delay | Slow to | Hold | Ramp back |
|---|---|---|---|---|
| Sword hit 1 | 40 ms | 10% | 10 ms | 30 ms |
| Sword hit 2 | 20 ms | 10% | 20 ms | 70 ms |
| Sword hit 3 | 60 ms | 10% | 50 ms | 70 ms |
| Ranged weapon | 20 ms | 30% | 20 ms | 70 ms |
| Heavy shield rush | 40 ms | 1% | 80 ms | 0 |

Rules:
- Waits run on **real time**, not slowed time.
- **+40 ms hold on crit or kill.**
- **No stacking.** A new hit-stop is ignored while one is active; priority events (last kill, death) override.
- **Per-weapon cooldown** (0.03–0.25 s) so multi-hits don't stutter.
- Only fires when the **player** is the attacker (or the defender opts in).
- **Last enemy killed:** slow to 35% with radial blur, bloom and a frame zoom.

**Roblox (multiplayer):** never slow the server. Apply hit-stop **locally** on the attacking client:
- Pause or slow your own character's `AnimationTrack`s.
- Freeze the hit target's *visual* (anchor its model's render offset).
- Briefly stall local VFX.

Other players don't see your hit-stop, which is fine.

**Screenshake presets** (`Speed / Distance px / Falloff / Duration`):

| Use | Values |
|---|---|
| Light | 300 / 3 / 2000 / 0.3 s |
| Medium | 500–600 / 4–6 / 1000–2000 / 0.3 s |
| Heavy | 900 / 8 / 2000 / 1.05 s |
| Directional hit | 300 / 6 / 0 / 0.1 s, angle along the attack |

Hades **removed most per-swing shake** (commented out in data) and kept hit-stop as the main impact signal. Shake is reserved for heavy moments.

**Rumble:** a short burst per hit, e.g. right motor 17% for 0.15 s. Roblox: `HapticService`.

---

## 5. Camera

### 5.1 Follow: rigid, no lag (decompiled `Camera::Update`)
- The camera position equals the **tether goal every frame**. No lerp, no spring, no dead-zone.
- Tether goal = a **weighted average** of tethered objects plus a script offset, plus the aim-lean point as one extra target.

### 5.2 Aim lean: the only smoothed part
```
v      = virtual cursor vector in normalized screen space (|v| = 1.414 at a corner)
t      = clamp((|v| - MouseDeadZone) / (1.414 - MouseDeadZone), 0, 1)
target = normalize(v) * (XMul, YMul) * t * TetherZone
lean  += toward(target) * min(dist, propel * dt * clamp(dist / TetherZone, 0, 1))
camera = (player * w_player + (player + clampLen(lean, TetherZone)) * w_lean) / (w_player + w_lean)
```

| Default | Value | Roblox starting value |
|---|---|---|
| TetherZone | 800 u | ~20 studs |
| XMul / YMul | 1.0 / **0.65** (less vertical reach) | same |
| MouseDeadZone | 0 | 0 |
| Lean weight vs player | 1 : 1, so **the camera moves half the lean**: ≤ 400 u (~10 studs) horizontal, ≤ 260 u vertical | same |
| Mouse propel | 1000 → **τ ≈ 0.8 s** | same ratio |
| Controller propel (same direction) | 300 → τ ≈ 2.7 s (deliberately slow) | same |
| Controller propel (reversing) | 500 → τ ≈ 1.6 s | same |
| Lean disabled (cinematics) | decays to 0 at the mouse rate | named "zero lean" flags |

### 5.3 Zoom and scripted moves
- Engine zoom moves **linearly** toward the goal zoom at a fixed rate. Eased zoom comes from scripted moves.
- Scripted moves use spline types `Ease`, `Overshoot`, `Undershoot` and moving-hold, e.g. boss reveal: overshoot to 1.0 over 0.17 s.
- Room base zoom is usually 0.75–0.95. Effect zooms are **relative** to the room's base zoom.
- Charge "breath": overshoot to 0.95–0.96 of base over 0.2–0.6 s while charging a big attack.
- Room-to-room zoom change: lerp over 1.4 s.

### 5.4 Roblox implementation
- `Camera.CameraType = Scriptable`. Update in `RunService:BindToRenderStep` *after* the character moves, so there's no 1-frame lag.
- Fixed pitch ~50–60° looking down. A low `FieldOfView` (~20–30) at a large distance gives a near-orthographic Hades look.
- Implement 5.2 in screen-relative 2D, then project onto the ground plane.
- For co-op, use per-player tether weights. The local player gets weight 1 and teammates 0 by default, or small weights for soft group framing. Disable or shrink the lean when more players are in frame.

---

## 6. Readability rules Hades follows

- One shared danger language for enemy telegraphs; windups are long enough to react to (target ≥ 0.35–0.5 s for heavy hits).
- Player VFX must never obscure telegraphs. In co-op, render **other players' VFX at reduced opacity**.
- Status and resistance tells are physical: shells, crystals, colored cores. They must read from a top-down camera.

---

## 7. Starting values for Prime Alchemy's kit

| Action | Proposed starting frame data | Hades source |
|---|---|---|
| LMB shot | 3–4 startup frames (one pose), fire, 5-frame no-attack lock, 8–10 frames dash-cancelable, ×0.5 move while firing, buffered | Sword / ranged weapon |
| Q nova | 4–6 startup frames, burst, 10–14 frame recovery **cancelable by dash**, hit-stop 20 ms @10% → 50 ms ramp | Special |
| R signature | 8–12 frame cast with a pose hold (commitment), dash cancels and refunds part of the cooldown, big shake + 0.95 overshoot zoom "breath" | Cast / Call |
| E enchant | instant, no lock; brief weapon glow plus a one-shot cue | — |
| Dash | 0.21 s, ease 0/0.8, 0.24 s i-frames, ~10 studs, cancels all recovery above | Rush |

These are proposals for the Feel Spec. Tune them in the Phase-1 graybox with simulated latency.
