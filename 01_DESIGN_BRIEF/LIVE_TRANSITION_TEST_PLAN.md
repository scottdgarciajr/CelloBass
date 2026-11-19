# CelloBass V2 — Prototype and Transition Test Plan

**The hardest V2 requirement is NOT the foldable wing. It is stable upright bowing with an endpin-stowed support that can quickly rotate to horizontal bass orientation.** Do not declare it solved before a practical ergonomics test.

## Stage 0 — Bench-only proof of mechanical feasibility
- Measure actual O'Cello overall length, center of mass (model estimate then weigh actual components), head/neck lever arm and wing envelopes.
- Mock up a safe low-cost suspended core (non-tensioned mock instrument or load-equivalent dummy). Place adjustable 2-point harness attachments on rigid/metal-reinforced interfaces.
- Test standing and seated upright posture, horizontal bass posture, and 90° controlled transitions without the user ever detaching the support. Check roll, tipping, strap migration, wrist angles and shoulder load.
- If user cannot bow safely with endpin stowed, offer explicit alternatives: (a) slower planted-endpin change with manual stow; (b) upright 'bass-mode' finger-plucking + instant footswitch, keeping the instrument vertical; (c) separate support/harness redesign. Do not sacrifice genuine cello posture just to claim an instant transition.

## Stage 1 — Performance transition
Script: start upright in live-ready endpin-stowed cello pose, play short cello phrase, stop the bow at a designated musical rest, keep the same harness attached, rotate with controlled grip, operate footswitch to bass effect, play a bass line; reverse into cello mode. Repeat with actual instrument only after low-load tests pass.

**Pass candidates:**
- Continuous physical support through both poses; no slipping, falling or hazardous endpin projection.
- Same wing pose and locked joints throughout; zero adjustment to bridge/neck/string tension.
- No cable unplug, tangled harness, strap rerouting, hardware collisions or bow-arc obstruction.
- Single effect footswitch activation when supported by the chosen processor; no audible pop or unintended preset activation.
- Transition duration measured, not promised. Musical continuity may use a rest or sustained loop; **not literally uninterrupted notes from fingers while rotating**.

## Stage 2 — Travel folding
With instrument supported and NOT in active performance: unlock wing catches, fold against spine, engage travel catches, stow endpin, place in padded sleeve. Check: no contact with strings, bridge, pickup cable, tailpiece or tuning keys; no freely flapping arms; no fastener pieces that can fall out. Measure L/W/D and weight.

## Stage 3 — Strength and repeatability
- Separately test each reinforced strap anchor using actual hardware and a conservative test protocol appropriate to measured instrument weight and player loads; consult a qualified mechanical designer for safety-critical loads. Do not load-test the printed hinge by suspending the instrument from it.
- Repeat deployed↔stowed wing cycles, inspect cracks, pin migration, warping and loss of locking engagement.
- Test printer-specific hinge clearance coupons and thermal/creep resistance before full instrument print.
- No string tension until the core rod, anchors, neck and bridge are mechanically reviewed.

## Stage 4 — Audio validation
- Capture the unchanged string output in Cello and Bass processing states. Verify actual effect latency, C2→E1 optional -8-semitone tracking, bow and pluck articulation, output pops and cable movement.
- If the footswitch needs a MIDI controller or effect software mapping, document specific tested setup and connector path. A passive switch on the instrument doesn't necessarily control external effects.

## Explicit out-of-scope for V2
- Full-size cello fitting in an ordinary backpack (body-fold only cannot shorten the long core).
- Flattening/retuning/changing scale between modes.
- Onboard custom pitch-shift DSP unless separately prototyped.
- Seamless *continuous notes* while rotating; human movement takes a practical pause.
- Rosin-free bowed cello voice from unvalidated electromagnetic hardware.
