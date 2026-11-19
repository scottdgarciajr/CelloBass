# CelloBass V2 — Mechanical & Music Engineering Specification

## Product mission
A mostly FDM-printable electric cello that can be played **upright as a cello**, switched mid-song to **horizontal fingerstyle bass with external effects**, and after the performance **folded narrower for travel**. The original cello string-playing geometry must remain uncompromised.

## One rigid musical core — ALWAYS
- O'Cello-derived instrument with exactly 4 strings, C2–G2–D3–A3, cello scale, fretless fingerboard, real individual-string bow clearance, constant fixed arched/curved bridge, nut, tailpiece, string anchors and tuners.
- Maintain one full-length rigid backbone and proven metallic reinforcement (O'Cello documentation mentions a 12 mm steel rod; verify in the source/build documents). NO folding of neck/string path, adjusting bridge arc or shortening strings.
- OpenBass reference geometry only for printable segmentation, strap/forearm ergonomics, structural mounting, industrial design or electronics packaging. Not its fretted fingerboard, 34-inch scales, bass string spacing or bass tuning.

## Configuration 1 — Live cello mode
- Upright cello play with unimpeded bow stroke, left-hand access, body stability and ergonomically acceptable knees/torso interface.
- For **mid-song switching**, the body supports and wings are ALREADY deployed and LOCKED. The live-ready support method should allow the instrument to be held upright with **endpin completely stowed**; this likely needs a purpose-designed, physically tested two-pose strap/harness or body/lap support. Do not invent an endpin that retracts by itself during play.
- Traditional extended endpin may be available for stationary seated practice; but switching to bass from that configuration requires stowing endpin and therefore is NOT seamless. Document this exact trade-off prominently.
- Can use ordinary bow (rosin normally required) and finger plucking. E-Bow-like rosin-free system outside scope.

## Configuration 2 — Live bass mode
- Without touching wing locks or music geometry, the performer rotates the whole cello into an approximately horizontal fretless-bass orientation, supported by the same continuously attached harness/strap; right hand plucks and left hand fingers cello strings.
- Add forearm contact/thump rest (if safe) and 2 reinforced strap/harness attachment points, positioned so movement is stable, controllable and does not pull from a plastic-only mount. Bow clearance is still protected in cello pose.
- Audio remains connected. Cello/bass preset switch is ONE foot-operated control action (for actual external processor compatible with chosen controller). Manual preset switch on instrument may be a fallback if it remains reachable in both poses. No external effect assumed to have a remote-control input without checking.
- Target a low register using effects such as a global pitch shift, EQ and compression. An optional -8 semitones shifts C2 to E1, but other open strings DO NOT map to E/A/D/G bass tuning; articulate bass lines may sound good; it is not a replacement for every technique or range of a normal bass.

## Configuration 3 — Packed travel mode
- ONLY non-string-bearing wings/side ergonomic arms fold toward the fixed central core. Endpin stows; cable disconnects if desired. Include folded locks/padding to prevent rattling and hits on strings, bridge and tuners.
- No folding neck. Therefore total instrument length remains approximately its original full length. **Do not advertise ordinary backpack fit**; instead measure packed L×W×D and recommend a long padded backpack-style instrument bag if appropriate.
- Metal pivots and real mechanical positive lock + hard stops. Printed hinges cannot be sole load paths for user weight or strap tension. Design hinges only for non-string-bearing wing loads.

## Architecture: performance and travel transformations MUST be decoupled
1. The body shape must be unchanged in both live playing configurations. No unfolding/folding for switching sounds.
2. Performance switch is **rotation/repositioning + footswitch effect preset**, optionally a short gap in playing; not continuous bowing while rotating.
3. Travel switch is a separate offstage action after music ends: unlock wing latches, fold wings, stow endpin, secure panels.
4. Preserve bridge/nut/fingerboard alignment in all poses and against travel folding forces.

## Physics and safety challenges to solve BEFORE full assembly
- Long cello mass and high neck length produce overturning torque as body turns sideways; compute approximate center of mass from actual geometry and component masses, select 2+ load-rated reinforced anchor locations. A simple strap may not keep upright cello stable for bowing; show feasible upright knee/torso support or state failure.
- Strap must remain attached through orientation changes, not intersect string/bow sweep, snag tuners or cables or lead to inadvertent rolling. If a swivel is proposed, define stops and anti-roll features; do not rely on friction alone. Hold the neck safely through transition.
- Potential forearm support must not block bowing or plucking. The right-hand bass plucking region is near fingerboard/bridge, adjusted for cello string spacing/arc.
- Endpin can remain extended only in practice configuration; for stage rotation it is pre-stowed. It must not point dangerously sideways during transitions.
- Piezo pickup with impedance appropriate to output, cable strain relief or reliable wireless. Keep connector clear when rotating and folding.
- 3D prints are not structural proof: evaluate fastener pullout, creep, layer orientation, fatigue, force application and thermal exposure. No full-string-tension testing until secured by metal reinforcement and physical inspection.

## Suggested verified-by-test targets — not promises
- **Live mode switch:** no tools, no refastening or unplugging, no change to wings, no retuning; one footswitch action plus controlled orientation move. Record elapsed time in user test; optimize to within a musical phrase. Do not claim 1-second transformation until tested.
- **Fold for storage:** all wing locks and pins captive and tool-free, wings compact; record packed volume and steps.
- **Repeatability:** wing locks engage with a visual/tactile confirmation; assembly returns to same stable deployed pose, without bridge/string changes.
- **Audio:** recording examples from same played cello strings in both processing presets; compare latency, attacks, pluck definition and bowing, indicate pedal/computer hardware and settings used.

## CAD deliverables, in order
1. Imported measured original core + source geometries and CAD screenshots.
2. Live cello, live bass, rotation sweep, folded travel state **same assembly**, with unchanged deployed wing geometry in both live modes.
3. Parametric test STLs for the wing hinge, body mount, lock and strap/harness anchor, including real bolt/pin sizes.
4. Editable source CAD, STL exports, STEP when possible, print-volume segmentation, exploded assembly, routing drawings, and part BOM.
5. Verification report with measured packed dimensions, collision checks, bowing clearance, supporting forces, and `NOT TESTED` labeling for all physical claims.

## Licensing and source material
Follow `SOURCE_NOTES_AND_LICENSES.md` and preserve source attribution. Do not infer that the two projects can be freely relicensed together, commercially sold or redistributed without compatible permissions. Preserve original source archives unchanged.
