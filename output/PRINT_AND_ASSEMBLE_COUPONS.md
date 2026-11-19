# CelloBass r0.2 — bench coupons only

These are real editable CAD and checked STL files for fit/kinematic tests. They are not structural parts for a tensioned or suspended instrument. Use a table fixture or independently supported dummy. Never hang the instrument or player load from these prints.

## Printer setup

The brief's 200 x 200 x 200 mm printer is a placeholder. Each individual coupon fits that envelope in its exported orientation. STL units are millimetres; confirm dimensions in the slicer against `reports/coupon_checks.csv` before printing. No production settings are asserted for your unknown printer/nozzle.

Start with C09 and C10 gauges. Prototype starting settings: PETG, 0.2 mm layers, 5 perimeters and 5 solid top/bottom layers, 40% infill, calibrated extrusion. C08 is a separate TPU retention test. These settings are untested; shell count, anisotropy, creep, heat and bolt-bearing stresses need actual evaluation. Do not apply the source cello's 15% infill instructions to the new anchor/hinge coupons as a strength claim.

| File | Quantity | Purpose / hardware | Print orientation |
|---|---:|---|---|
| C01_anchor_drill_template | 1 | 64 x 34 x 6 mm layout template: four M5 clearance holes at X +/-24, Y +/-10; central M8 clearance. Candidate metal backplate 64 x 34 x 3 mm must be separately engineered. | Flat 64 x 34 face |
| C02_rod_saddle_half | 2 | 12.4 mm bore-fit cradle for a separate nominal 12 mm dummy rod; four M5 holes. M5 x 40 bolts, washers and nuts for a paired mock clamp. No friction-only live anchor accepted. | Flat base, groove up |
| C03_swivel_mock | 2 | M8 x 30 bolt, broad washers, locknut; optional M4 index pin at radius 22 mm; 26 x 4 mm slot for 25 mm mock webbing. No live rotation or load rating. | Disk flat |
| C04_wing_hinge_base | 1 | 6 mm steel clevis/pivot pin, usable grip >=18 mm; pin length about 25 mm including retention allowance. 4 mm steel lock pin, usable grip >=18 mm. Two M5 fixture bolts. | Lower disk flat; removable support under upper disk |
| C05_wing_hinge_tongue | 1 | M6 pin bore 6.3 mm; M4 index bore 4.3 mm at radius 24 mm. Tongue thickness 9.4 mm in 10 mm gap. | Broad face flat |
| C06_travel_latch | 1 | 4 mm cross pin, usable grip >=44 mm, about 50 mm total with retention; two M5 fixture bolts. | Base flat; clean transverse bores |
| C07_travel_tang | 1 | Mating tang for C06. Place its underside at Z=3 mm in C06 coordinates to align holes at Z=14 mm. | Base flat |
| C08_endpin_stow_clip | 2 | TPU C-clip, bore 10.5 mm; M3 mounting clearance 3.5 mm. Retains stowed tube only. | Flange flat |
| C09_M6_clearance_gauge | 1 | Left to right along X: 6.1, 6.2, 6.3, 6.4, 6.5 mm holes. | Flat |
| C10_rod_clearance_gauge | 1 | Left to right along X: 12.0, 12.2, 12.4, 12.6 mm holes. | Flat |

Pin lengths above are bench selection starting points; actual washers, end retainers and chosen clevis-pin catalog dimensions determine final lengths. Use steel pins with positive end retention and tether both pivot and removable lock pins to the fixture. The CAD does not include captive-pin retainers, lanyards or their clearances; verify those physically. Standard bolt shanks should carry the hinge bearing surface; avoid threads abrading the printed bore.

## Hinge test

1. Support the upper overhang during printing. Remove support without gouging the bearing faces. Measure the base gap at several positions; nominal 10.0 mm.
2. Measure C05 thickness; nominal 9.4 mm. Check the actual axial clearance, nominal total 0.6 mm. Do not add washers inside that gap without updating CAD.
3. Insert C05 between the disks with its lower face at base Z=4.3 mm. Align pivot holes at (0,0). The tongue extends in local +X when deployed.
4. Insert and positively retain the 6 mm pivot. Verify a smooth 0..90 degree sweep. The base's Y=-9 mm face is the deployed hard stop; X=-9 mm is the folded hard stop. No overtravel should be accepted as normal operation.
5. At 0 degrees the tongue's lock hole is at (24,0); at 90 degrees it is at (0,24). Insert a tethered steel 4 mm lock pin through both base plates and the tongue. Verify complete engagement visually and by hand. The lock is independent of gravity.
6. Work only with a light dummy ergonomic arm, not the string core or harness. Record rattle, stop contact, pin insertion, side play and access. Add replaceable pads only after confirming their thickness does not prevent pin alignment.

The CAD checks 91 positions and the hard-stop overtravel. It does not model a load-rated wing joint, captive spring pin or cycle fatigue.

## Latch, stow and anchor tests

The latch's matching tang should align its cross hole without forcing. Trial a removable buffer under the tang; nominal 3 mm elevation is required by this bench fixture. The pin must be tethered and end-retained. Printed tang/cheeks have no fatigue rating.

Test C08 with the actual 10 mm tube and the chosen TPU. Check retention, release force and wire clearance. C08 is not an endpin floor clamp and must not carry floor load.

Use C01 to compare the nominal metal backplate and fastener access in a dummy fixture. The central eye's load must go through engineered metal hardware and a positively retained metal backbone. C02 and C03 establish fit only. Stop the assembly plan at this point if the metal-to-spine force path remains unresolved; it currently is unresolved.

## Record before changing CAD

Record printer/nozzle, material and drying, orientation, layer/infill, slicer compensation, measured bore/gap/tongue sizes, pin hardware, edge distances, rattle and insertion force. Photos should include a ruler and orientation. Update `source/build_coupons.py`, regenerate both STEP and STL, and rerun checks after dimensional changes. Do not file a coupon to fit and report its original CAD clearance as verified.
