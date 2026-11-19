# Verification — CelloBass r0.2 / 2026-11-10

**Release: source-measured kinematic study and bench coupon package. NOT a finished playable or load-rated CelloBass.**

## Completed by computation

| Check | Result | Evidence / limit |
|---|---|---|
| Archive integrity | PASS | SHA256 inventory of 37 archive/extracted records; originals retained |
| O-Cello Blender import | PASS | 17 evaluated meshes; metric conversion recorded in blender_audit.json |
| Original source mesh watertightness | PASS | 17/17 closed meshes; this is not print/load certification |
| Source musical surfaces retained | PASS for modeled surfaces | Exact evaluated Parts 1-6, bridge, bar, nameplate and right chest rest; no bass geometry substitution |
| Exact speaking scale/string-center assignment | UNRESOLVED | Geometry preserved; no false numeric scale inserted |
| OpenBass STEP import | PASS | Valid 7-solid V2.1 model, reference only |
| STL coupon topology | PASS | 10/10 manifold closed meshes, positive volume, consistent winding, one solid each |
| Coupon printer envelope | PASS for placeholder | 10/10 under 200 mm per axis; user's actual printer unknown |
| STEP coupons | PASS | Each exports; independent re-import validity is recorded in regression_checks.json |
| Local hinge sweep | PASS, ideal CAD | 0..90 degrees at 1-degree intervals; no positive-volume base/tongue intersection. Overtravel stop checks recorded separately |
| Both live poses use identical geometry | PASS | Inverse global transform restores every modeled component within 0.001 mm; no folding or neck/bridge change |
| Wing/core travel sweep | PASS for modeled envelopes | AABB separation at 1-degree samples with continuous angular displacement padding; wing pairs also separated. Does not include final hinges, hardware, wires or people |
| Four assembly states | PASS | Editable linked Blender scenes + GLB studies and rendered views |
| Packed envelope | MEASURED PARTIAL MODEL | L 1070.277 x W 187.272 x D 148.481 mm. Complete instrument/hardware/padding can enlarge it |
| Deployed envelope | MEASURED PARTIAL MODEL | L 1070.277 x W 420.000 x D 148.481 mm |

## Preliminary balance, not structural analysis

`mass_balance.json` records each assumed material fraction, density, location and lumped hardware mass. The estimate is about 2.795 kg with COM (-6.417,-17.581,186.969) mm in the original source coordinate frame. Around the provisional rotation center (0,-40,280), the maximum gravity torque about Y is about 2.556 N m. A 280 mm anchor spacing would require about 9.13 N of force couple for that torque, in addition to supporting weight and any dynamic/roll loads. This is NOT a strap-tension or joint-stress solution.

A wider assumed range of 2.5..5 kg and 100..300 mm horizontal lever arms reaches 14.71 N m. Actual mass, COM and human stabilization must be measured. Printed effective solid fraction 0.35 is an estimate, not a slicer infill percentage or a measured print mass.

## NOT TESTED — mandatory before production release

- Actual supporting harness, metal-to-rod attachment, load rating, rod bending stress, metal fatigue, fastener retention, printed pullout, creep and environmental heat.
- Stable upright bowing with endpin stowed, roll control, neck slippage, torso/knee pressure, wrist reach, strap migration, clothing snagging and safe handholds.
- Bow angular sweep, individual-string attack access with the real string diameters, strap/cable collision and fully dressed tuner envelope. Preserving the original bridge does not prove the new harness clears the bow.
- Continuous full-assembly sweep against a human, harness, wires, footswitch, floor or seat. Only internal rigid source geometry is invariant under the live rotation.
- Wing lug/core integration, captive-lock hardware, pinching and final stops under player contact loads; lock release force, print fit, vibration/rattle and cycle wear.
- Endpin stow retention and floor configuration. The ordinary extended-endpin setup does not pass the live rotation requirement.
- Pickup coupling, input impedance selection, cable strain relief, actual effects host/control mapping, pitch tracking, latency, sound and switching noise.
- Physical switch duration. No achieved timing, gapless playing, acoustic fidelity or structural safety is claimed.
- Final bag fit. Choose a long padded instrument sleeve only after complete hardware bounds and clearance are measured; folding wings do not shorten the instrument.

## Gate status

- **Gate A: substantially delivered, functional dimensions open.** Actual source audit, unit provenance, measured envelopes and original views exist. Exact contact/scale and attachment-interface measurements remain unresolved.
- **Gate B: concept delivered; feasibility NOT PASSED.** Four states and preliminary balance exist. Continuously attached, stable upright-to-horizontal support and positive metal load path are unproven. Indexed swivel coupon cannot satisfy no-refastening live switching.
- **Gate C: digital coupons delivered, physical tests NOT TESTED.** Use the coupon manual before adding loads or instrument tension.
- **Gate D: HOLD.** No final production core/wing STLs, integrated structural assembly, full instrument solid STEP, complete exploded production assembly or tension-ready build release. Envelope and source-reference meshes must not be mistaken for those deliverables.
- **Gate E: documented partial validation.** See `validation_checklist_r02.csv`; physical rows remain NOT TESTED.

## Next test gate

Measure and assign the original nut/bridge bearing geometry, then make a supported, non-tensioned full-length dummy using independently supported ballast. A qualified mechanical designer must finalize the positive metal spine/rail load path before a wearable load test. Test both upright and horizontal poses, then a controlled transition with the same support attached, wings locked and endpin pre-stowed. Have a musician assess bow and hand access. Record actual mass, COM, slip/roll, cable rotation, and transition time. If upright support fails, use upright fingerstyle plus a footswitch as the interim musical configuration and redesign the harness.
