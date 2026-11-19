# CelloBass V2 — Codex starter package

## What changed since V1
The user selected **FOLDING BODY ONLY** and explicitly wants **fast mid-song cello↔bass playing switches**. These are different operations:

- **Performance switch**: body wings stay DEPLOYED and LOCKED. The same rigid cello is rotated from upright to horizontal (or temporarily plucked upright), and a footswitch changes the offboard bass DSP preset. No hinge unlocking, retuning, endpin adjustments, cable swaps or reattachment during a song.
- **Transport folding**: after playing, wings fold inward and endpin retracts. Fixed musical core remains full-length. This makes a *slim long* instrument, not a conventional-backpack-sized cello.

**Important feasibility warning:** An ordinary cello with its floor endpin extended cannot be turned horizontal instantly and safely. The intended live-ready setup therefore requires an endpin-stowed, load-rated dual-orientation support/harness that MUST be tested first. Ordinary seated endpin playing stays an alternate slower-switch mode. Do not treat photos, CAD or this document as proof the harness is safe.

## File use
1. Unzip the package and open the directory in Codex.
2. Start with `00_START_HERE/CODEX_PROMPT.md` (or paste `COPY_PASTE_SHORT_PROMPT.txt`).
3. Read `01_DESIGN_BRIEF/ENGINEERING_SPEC.md` and `LIVE_TRANSITION_TEST_PLAN.md` before modeling.
4. Unpack the unmodified project archives with `python 04_TOOLS/unpack_sources.py`.
5. Measure actual O'Cello source dimensions and validate Blender units before claiming compatibility. Use OpenBass for reference of printable structures, not cello geometry.
6. First deliverable is source audit + 4-state kinematic concept + strap/harness and wing hinge test STL coupons, not an entire unverified instrument.

## Contents
- Master prompt, README and copy-paste prompt in `00_START_HERE/`.
- Engineering spec, live-transition test plan, hardware checklist, source/license notes, printer config in `01_DESIGN_BRIEF/`.
- Original O'Cello and OpenBass source archives in `02_ORIGINAL_PROJECTS/`.
- Two visual inspiration files in `03_VISUAL_REFERENCES/` (not dimensionally accurate or mechanically proven).
- Source unpack helper in `04_TOOLS/`.

## Preserved musical requirements
- Four strings C2–G2–D3–A3 and original cello scale/geometry.
- Fixed curved cello bridge with ordinary bow clearance.
- Reinforced fixed spine; no folding neck or load-bearing folding string path.
- Fingerstyle fretless bass technique and optional external -8-semitone pitch shift/EQ/compression for bass-like sound. Pitch shifting C2→E1 does not change standard fifth tuning to bass fourth tuning.
- Traditional bow works as in the cello source; rosin-free electronic sustain remains optional research, not implied in V2.

No completed CelloBass CAD or STL is contained in this ZIP; it is a revised engineering work package for Codex to create, audit and test those artifacts. Review source licenses before redistribution/commercial use.
