# CODEX MASTER PROMPT — CELLOBASS V2: FOLDING BODY + LIVE MODE SWITCHING

You are the lead mechanical CAD engineer, additive-manufacturing designer, and prototype test engineer. Given the two original projects in this workspace, create a **real editable CAD assembly, fit-test STLs, and eventually the individual production STLs** for a single transformable electric **CelloBass V2**. This brief replaces the V1 plan in the prior package. Do not respond with only images or a conceptual proposal: inspect the originals, measure geometry, generate CAD, export usable files, and report what is verified versus assumed.

**Read first**:
1. `00_START_HERE/README_FIRST.md` and `01_DESIGN_BRIEF/ENGINEERING_SPEC.md`
2. `01_DESIGN_BRIEF/LIVE_TRANSITION_TEST_PLAN.md` (especially the endpin/harness feasibility gate)
3. `01_DESIGN_BRIEF/PROJECT_CONFIG.yaml` and `01_DESIGN_BRIEF/HARDWARE_BOM.csv`
4. `01_DESIGN_BRIEF/SOURCE_NOTES_AND_LICENSES.md`
5. Unpack original sources in `02_ORIGINAL_PROJECTS/` with `python 04_TOOLS/unpack_sources.py`.
6. Consider `03_VISUAL_REFERENCES/` as aesthetic references ONLY. The two images are inconsistent early concepts and NOT dimensional ground truth.

## 1. The updated product definition — THREE modes, TWO kinds of transitions

**A. LIVE CELLO MODE**: Full cello-scale, four cello strings tuned C2–G2–D3–A3, fretless fingerboard, original fixed curved bridge, real individual-string bow access, appropriate upright ergonomics. Natural piezo pickup output (or EQ/reverb offboard). For rapid changes, use a load-rated, testable dual-orientation strap/harness or seated support with **endpin already stowed**. A conventional extended endpin is allowed as an optional stationary seated configuration, but NOT as the basis of a claimed instantaneous switch.

**B. LIVE BASS MODE**: Same unmodified and tensioned strings, fixed neck and bridge, held approximately horizontally like a fretless bass and plucked fingerstyle. Bass effects preset offboard (pitch-shift, EQ, compression), preferably switched by **one footswitch action**, with no cable swapping, tuning, fretboard change, bridge modification, folding, or refastening. The continuous, reinforced central core never moves relative to itself. The user changes its ORIENTATION and right-hand technique, not its string geometry.

**C. TRAVEL MODE**: Only the **non-string-bearing body wings/ergonomic frame folds in**, endpin retracts/removes, exposed hardware is protected. The entire tensioned neck, fingerboard, bridge, tailpiece, tuners and string-bearing spine remain rigid, fixed and full length. This makes the instrument **slimmer, not shorter**. DO NOT claim it fits a normal backpack; measure the packed bounding box and recommend an appropriately long padded sleeve/pack. No folding neck or string-management system in V2.

**CRITICAL DISTINCTION:** Cello↔Bass is a performance orientation/preset change, **NOT a body-folding operation**. Wings remain deployed and POSITIVELY LOCKED in the SAME PERFORMANCE CONFIGURATION in BOTH live modes. Only fold them AFTER the song for transport. A quick mode change must not require bolts, wing hinges, detaching strings, detaching a strap, retracting an extended endpin, or manually replugging electronics.

## 2. Mandatory musical geometry — cello first
- Base all musical/string geometry on the supplied O'Cello source; inspect actual `.blend` objects and verify units before modeling. Preserve its effective scale length, neck and fingerboard profile, nut/bridge string positions and spacing, tailpiece/tuners, original bowing clearance, rigid steel-rod reinforcement or a validated equivalent.
- Original cello curved bridge stays **fixed in both live modes**. Do NOT invent an adjustable bridge, sliding frets, detachable neck, standard bass fretboard, extra strings, or a second attached instrument.
- OpenBass Fusion/STEP models are a construction and industrial-design reference for sectional printability, ergonomics, mounting and electronics; its 34-inch multiscale bass-string geometry must not be copied into the cello core.
- A cello C2 open string is about 65.4 Hz, bass E1 is about 41.2 Hz. Optional -8 semitone external pitch shift maps C2 to E1 but the other strings do NOT magically become standard bass E-A-D-G. Treat usable low-register bass tone as an experiment, especially for polyphony.
- Preserve sufficient bow arc and body clearance in live cello mode; assess the dual-orientation strap/harness and cable against bow movement.

## 3. Performance ergonomics (PRIORITY 1)
- Design **one always-attached, quick-reposition dual-orientation supporting system** (for example reinforced two-point strap + tested swivel/rotation geometry, or a wearable support/harness) that permits safe upright bowing and horizontal plucking **without disconnecting support**. Analyze rotation direction, pitch/yaw/roll behavior, center of mass, cable twisting, reachable handholds, string clearance, clothing snag hazards and gravity-induced sliding.
- The chosen system must not require folding/unfolding the wings during a song; body silhouette is fixed in both playable poses. Provide a cello knee/torso contact and a bass waist/forearm contact that coexist without obstructing each other or the bow. Optional fixed/retractable thumb rest may be added ONLY if it cannot interfere with cello bowing, and must require no setup mid-song.
- For the **live-ready setup**, endpin must be fully stowed **before performance** (or design a distinct stable and credible endpin-free upright support). The center structure must safely support an upright cello playing pose while allowing transition to horizontal. The optional conventional floor endpin remains available for seated practice, with the explicit limitation that it cannot switch instantly while extended.
- Define a feasible hand sequence: play cello → stop bow motion at a musical transition → support/rotate instrument to bass orientation using harness → operate mapped footswitch with one action → pluck; reverse similarly. Never promise literal gapless string playing during the rotation. If truly continuous sound is desired, optional looping or a held effect can bridge the few-second mechanical switch, but **looping is out of scope** for V2.
- Model clearly labeled upright, horizontal, in-transition sweep, and folded-for-travel states of THE SAME assembly and THE SAME wing geometry (only travel state wings rotate). Include user-reachable control positions and noncolliding strap routing.

## 4. Folding body ONLY (PRIORITY 2)
- Implement two or more non-string-bearing, lightweight printable wing frames with steel pivot pins/shoulder bolts, mating hard stops, positive captive locks, and no accidental-folding under gravity or normal player loads. Wings must lock solidly in the deployed performance pose, independent of orientation.
- Do not route the main string-tension load, strap load, or endpin floor load through an unsupported printed hinge. Strap anchors must transfer to the reinforced fixed structure and use validated metal hardware. Wing pivots handle only wing/ergonomic loads.
- Add soft or replaceable buffers to stop rattles, secure stowed wings, avoid string/tuner contact, and leave electronics and strings protected. Show separate deployed/packed dimensions, hinge axis locations, lock access, full swept-envelope collisions, and stow protection.
- Reuse original rigid frame/spine as much as possible. For all load-bearing printed components document layer orientation, material, fasteners, creep and reinforcement assumptions.

## 5. Electronics: instantly selectable, not magically automatic
- Plan a real piezo pickup or bridge transducer, high-input-impedance path if needed, shielded wire, stable output jack and cable strain relief with clearance in BOTH live poses and throughout rotation.
- In V2 prototype, leave pitch shifting, EQ, and compression **offboard** in a phone/computer/pedal/modeler. Recommend a practical **footswitch-controlled two-preset signal path** or a single offboard effect chain with preset bypass, and provide a mount/wiring provision if desired. If it needs specific host software, MIDI or an interface, document all required hardware; do not imply a passive toggle on the cello can automatically command arbitrary third-party software.
- The device should maintain the pickup connection and audio output during pose changes. A detachable cable is acceptable for storage, NOT for performance switching. Optional tilt sensor for later versions, but prevent unwanted auto-preset switching during motion; user-controlled footswitch is the primary V2 requirement.
- Cello-mode bowed sound with a normal bow remains supported, which ordinarily uses rosin. A rosin-free electromagnetic sustainer is a **separately scoped experimental future feature**, not a V2 requirement or something claimed to work from the supplied source files.

## 6. Source audit BEFORE any geometry
1. Inventory and verify actual archive contents. O'Cello is expected to include a Blender `.blend`; OpenBass includes Fusion/STEP/STL. Keep originals unmodified.
2. Use Blender headless for O'Cello object inspection/export if possible. If impossible, do NOT fabricate dimensions or claim successful import; report blocker, create only provisional measured-interface fixtures and request a STEP/STL/OBJ neutral export.
3. Make `output/reports/source_dimensions.csv` with measured provenance for cello scale length, bow bridge arch, neck and fingerboard envelope, fixed steel rod, bridge/nut string spacing, tailpiece/tuning geometry, existing body-section interfaces, endpin, high-risk physical attachment zones and total length.
4. Confirm the original hardware/build instructions and license constraints in the supplied notes.

## 7. Required deliverables in order

### Gate A — Measured baseline
Produce: `output/reports/source_inventory.md`, `source_dimensions.csv`, `design_decisions.md`, screenshot/orthographic views of actual original assemblies, list of source licenses and unresolved dimensions.

### Gate B — Live-rotation kinematic assembly FIRST
Produce editable parametric CAD of the reinforced original cello core and an **unchanged deployed body profile** for BOTH cello and bass. Add load-rated reinforced strap/harness mount proposals and optional upright endpin-free support. Export four same-assembly views (cello/upright, bass/horizontal, transition sweep, travel/folded), with clearances and preliminary center-of-mass/torque analysis. Validate no bow collision, strap/wire twist, neck slippage, instability or pinch points. If a fully safe and effortless upright↔horizontal rotation is not credible, SAY SO and propose the best fast practical compromise without lying.

### Gate C — First printable mechanism tests
Generate actual, isolated STL fit coupons + editable source for: reinforced strap-anchor interfaces, mock strap swivel or dual-orientation mount, wing hinge with locking stop, folded latch, endpin stow clip and a clearance test piece. Include real hardware sizes, fastener access, print orientation and what to measure. Run simple CAD unit/regression checks, print-envelope tests and mesh watertight checks.

### Gate D — Full CAD assembly and exports
Deliver editable CadQuery or FreeCAD source, individual correctly scaled STLs, complete STEP if toolchain permits, exploded assembly, BOM, wiring routing and instructions, with prototype revisions clearly labeled. Keep large parts modular and within configured printer envelope (currently placeholder 200×200×200 mm). Provide separate source and STL folders.

### Gate E — Validation report
Produce `output/reports/verification.md` and a versioned checklist assessing measured source-geometry fidelity, all state swept collisions, hinge deployment/stow, strap force path and mass balance, static-endpin tradeoffs, bow sweep, pickup/cable path, musician hand access, storage dimensions and whether real physical tests were done. Label untested force/load/acoustic/performance assumptions as `NOT TESTED`. Do not certify structural safety or timing purely from CAD renders.

## 8. Acceptance tests (and truths you must NOT misrepresent)
- **No tool, fastener, hinge unlock, retune, string changes, bridge movement, endpin adjustment or cable swap between live modes.** Body wings stay locked/deployed during the performance switch.
- Audio preset selection via **one accessible footswitch action** (if the external processing path is actually wired and configured). The mechanical rotation may take seconds and must be tested by a musician; do NOT claim gapless playing or an achieved timing goal before testing.
- With the normal planted endpin extended, a fast live sideways switch is NOT certified; provide the live-ready alternative with endpin stowed and stable upright support, otherwise state why the requirement cannot yet be met.
- Foldable body is only for packed mode. **No full-length cello geometry fits an ordinary backpack merely because its wings fold**; report actual length and packed envelope.
- Four cello strings C2–G2–D3–A3, rigid reinforced core, fixed curved bridge and fingerboard. True cello bow access must remain.
- FDM-only high-stress neck or strap anchors are forbidden without proper structural design and real testing. Keep tensioned parts out of moving joints and prototype fit before tensioning.
- STL exports must be manifold where appropriate, labeled, dimensioned, sized for printer, and backed by editable CAD. If dependencies/toolchain are missing, report what actually succeeded and supply the maximum viable partial output, not fictitious files.

## 9. Style of work
Proceed independently without unnecessary clarifying questions. Use provisional, tagged assumptions for non-musical dimensions, but derive musical geometry from actual source. Do not skip CAD validation. Favor a practical, playable V2 over adding extra abilities. Start by auditing and measuring O'Cello and OpenBass, then create a 4-state motion concept and the small strap-anchor + hinge CAD coupons. **Do not build the full instrument before proof of the live transition and load path.**
