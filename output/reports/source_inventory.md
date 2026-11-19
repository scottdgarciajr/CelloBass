# Source audit — CelloBass r0.2

Audit date: 2026-11-10. Originals remain unchanged. SHA256 and file sizes for both archives and every extracted source file are in `source_files.csv` (37 records).

## Actual contents

- O-Cello: one `O-Cello_Source.blend`, Blender 2.81 file header. Successfully opened with portable Blender 4.5.15 LTS, automatic script execution disabled.
- Blender contains 17 evaluated mesh objects. All 17 exported source meshes are watertight as supplied. No missing imports or geometry repairs were concealed.
- The scene uses METRIC, scale_length 1.0, display METERS. World-space evaluated vertices were multiplied by 1000 to export millimetres. All source transforms and modifiers were evaluated first.
- Six body/fingerboard sections, original bridge, central bar, nameplate, chest/knee rests and knee bar are modeled. The left-handed alternate chest rest and loose stand fittings sit off to one side; they must not inflate the assembled instrument bounding box.
- There are NO actual strings, tuner assemblies, bow, performer, pickup, harness or aluminum endpin tube in the Blender file. String contact points, actual tuner envelopes and comfortable hand positions cannot be certified from this archive.
- OpenBass: two versions, each with STEP, Fusion, 3MF and STL assets; nine maker-tool STL files; a seven-page exported project-page PDF. The PDF lists an additional design-guide PDF which is **not actually included** in the archive.
- OpenBass V2.1 STEP imports as a valid seven-solid model. Measured XYZ envelope: 335.430 x 1003.572 x 50.284 mm. The page's nominal assembled width/length differs because hardware/configuration can differ. Do not replace measured geometry with page marketing dimensions.

## Source fidelity

`blender_audit.json` contains object matrices, bounds, modifier types and triangle counts. `object_dimensions.csv` gives all 17 measured object envelopes; `source_dimensions.csv` distinguishes measured envelopes, documented nominal hardware and unresolved functional dimensions.

The assembly study retains exactly the evaluated original Parts 1-6, Bridge, Center bar, Nameplate and right-handed Chest rest. Only the non-string-bearing knee bar and knee rests are omitted from the study and replaced by original wing envelopes. All omitted source meshes remain available separately, including the alternate chest rest and stand fittings.

The original neck and fingerboard surfaces, asymmetric bridge, string-anchor region and tuner-bores are not remodeled. An editable mesh is not a native parametric B-rep. No complete original-core STEP or inferred parametric fingerboard is represented as finished.

## External build reference

Downloaded the [official 15-page O-Cello assembly guide](https://o-cello.com/files/ocello_assembly_instructions.pdf) into `work/reference_docs/`. Text extraction is preserved in `ocello_build_text.txt`. Rendered and inspected assembly reference pages. The guide identifies a nominal 12 mm x 1 m steel rod, 10 mm x 450 mm aluminum endpin tube, M5 joints and an asymmetric slide-in bridge. The supplied central bar mesh has a 12.2 mm maximum X span; these are different kinds of measurement, not grounds to modify the musical core.

## Attribution and licenses

- O'Cello by Conor O'Kane: [official site and license statement](https://o-cello.com/), CC BY-NC 4.0. Source geometry is included in the study, so retain attribution and the noncommercial restriction. Changes: replacement knee-support envelopes and provisional support/stow geometry; original musical meshes preserved.
- OpenBass by tbenen: supplied project PDF states CC BY-SA 4.0. Used for construction reference only; no OpenBass faces, meshes or solids are incorporated in the new geometry.
- New coupon and envelope CAD was authored in this project. No public release, sale or combined relicensing has been performed. Original source files and their existing terms are retained.

## Still unresolved

Exact effective speaking length for each installed string; nut and bridge string-center contact locations; actual tuner and string envelopes; precise mating joint planes/bolt center interfaces for new hardware; metal-to-rod anchoring; physical printer clearances; bridge pickup coupling; performer/harness fit. Preserve the source rather than inventing replacement musical dimensions.
