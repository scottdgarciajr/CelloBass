# CelloBass r0.3 — connected study, seated bass priority

This revision responds to the disconnected first view and the concern that it did not look comfortable as a bass. The user identified seated bass as the expected use. This is a design revision, not an ergonomic or structural validation result.

## What was wrong in r0.2

The wings were floating motion envelopes with no integrated hinge/core connection. The ten small STL coupons were independent fit tests, not a set that assembled into the instrument. The first view did not make either distinction clear enough. Two narrow rectangular wings and the retained projecting chest rest were not an adequately developed bass support arrangement.

## What changed

- Preserved the original musical core: Parts 1-6, fixed asymmetric bridge, central bar and nameplate. Removed the original non-string-bearing chest rest from this revision; its reference mesh remains preserved in the source outputs.
- Replaced the rectangular envelopes with two original curved contact frames. A 35 mm-deep upper cushion envelope marks the forearm support. A 50 mm-deep lower cushion envelope follows the concave contact area intended to rest on a seated player's thigh. These are geometry proposals, not chosen foam specifications.
- Bass pose raises the neck 20 degrees from horizontal. This is an initial fitting angle, not an established optimum.
- Added a proposed rear metal rail, lower adapter, secondary upper brace, crossmember, standoffs, actual hinge bases, extended hinge tongues, pivot and locking pins, and two attachment bolts per contact frame. The frame bolt pattern is local radial 48 and 68 mm, 5.5 mm clearance.
- The two hinge centers are staggered fore/aft at (65,-60,150) and (-65,-110,150) mm so the larger frames can occupy different depth layers when folded. This increases packed depth; packing dimensions must not be carried over from r0.2.
- The stowed endpin passes through a 10.6 mm clearance bore in the crossmember and through matching retention brackets. Retention force and actual hardware are not validated.
- Added four thin string paths as illustrations only. Their bearing points and diameters are NOT calibrated; they are not replacement musical CAD.
- Added an animated review with separate live-rotation and travel-fold operations, a close-up hinge view, direct part labels and a thigh-position sketch. The thigh sketch is not in the instrument CAD and is not used for fit or collision calculations.

## How to read the movement

**Cello to bass:** the entire assembly rotates; both contact frames remain open and locked. Bass tone requires a configured external effect chain and one mapped footswitch action. No audio processing is implemented by the viewer. A safe seated support/harness arrangement and bow handoff remain open.

**Travel:** support the instrument offstage, withdraw the two orange wing lock pins, rotate the frames 90 degrees toward the neck, then place the pins into their alternate stow holes. The steel pivots stay in place. The model illustrates the lock sequence; retainers and tether routing have not been finalized. Neither the neck nor the tensioned string path folds.

## What the visible connections do and do not establish

The new hinge-to-frame assembly now has explicit geometry instead of an air gap. The long tongue is bolted to the frame. Its pivot and lock fit through the base. The base mounts on a standoff tied to the proposed metal crossmember.

**The rail's positive attachment to the original steel spine remains unresolved.** The lower adapter is a nominal bore/space proposal, and the upper brace is an interface envelope. Their shapes are not a source-fitted, load-rated joint. Visible contact or overlap is not proof of a mechanical force path. No cross-drilling or tension-ready alteration of the original rod is authorized by these drawings. Strap eyes are shown on the fixed metal rail, not on the folding frames; no wearable harness is included or validated.

## Checks completed

- 18 new solid STEP exports independently re-import as valid solids.
- 50 baseline scene parts have closed, positive-volume mesh geometry. This includes illustrative hardware; it is not a 50-part print kit.
- Original musical reference meshes agree with their prior exact source exports to less than 0.0001 mm.
- The complete live bass assembly recovers into the cello frame through a single inverse rigid transform within 0.001 mm. Zero wing-fold angle in both live poses.
- 546 exact local moving-solid comparisons test the two tongues, two frames and two cushions against their hinge bases at 91 one-degree positions. No positive-volume interference. Hard-stop overtravel is blocked at -1 and 91 degrees for the revised tongue.
- Live orientation, lock withdrawal, folding, lock relocation/insertion and close-up controls function in the local review. No script errors or mobile horizontal overflow detected.

These checks are recorded in `revision_checks.json`, `hinge_sweep.json`, and `ui_checks.json`. They do not replace a complete swept collision check against the other hardware, source, human, clothing, strings, bow or cable. The r0.2 global wing-envelope separation result does not certify this changed r0.3 geometry.

## Final print review

The forearm pad touched the rear rail near the end of the travel fold. Its position moved 3 mm rearward. The updated travel animation passed a surface intersection screen at 201 sampled positions, including pulling and reinserting the lock pins. See `travel_sweep_screen.json` for the scope of the check. The endpin guides still need a positive keeper to hold the tube along its length. The harness and lower knee supports remain open design work.

The four PLA files in `../../print-test-kit/` are ready for a tabletop test print. Their checks cover bed fit, flat orientation, hinge motion, both stops, lock engagement and lock withdrawal. Printed dimensions, ease of assembly and wear need a physical check. The [print guide](../../print-test-kit/START_HERE.html) walks through each test and a separate lightweight seated mock-up. Release of the playable instrument still depends on the supports, metal attachment and physical fit.

## Still NOT TESTED

Comfort, stable balance on the lap, thigh pressure, forearm reach, left-hand reach, instrument roll, cable twisting, bow-string access with the new supports, pin access on the lap, full folding sweep, pivot and frame loads, foam compression, fastener retention, metal-to-core stiffness and strength, tensioned playing, sound and switch time.

Do not print the new `study/` STEP shapes as a production instrument. The next useful object is a supported, non-tensioned seated mock-up sized to the player's thigh and reach, followed by the required structural interface work. An ordinary planted endpin still cannot be rotated sideways without manually stowing it.

## Editable sources

- `source/build_connected_study.py`: new parametric shapes and state geometry.
- `CelloBass_r03_connected_study.blend`: five linked scenes, including rear hinge close-up. Original musical mesh datablocks are shared across states.
- `study/*.step`: new local-coordinate study parts. These are not a complete solid STEP of the original cello.
- `study/*.glb`: connected reference assemblies.
- `reports/bounds.json`: current partial-model bounds. Folded XYZ is approximately 291 x 181 x 1070 mm, with complete harness, cable, tuner hardware and protective padding still absent.

O'Cello source credit and CC BY-NC 4.0 terms remain. No OpenBass geometry was incorporated and no public release or sale was performed.
