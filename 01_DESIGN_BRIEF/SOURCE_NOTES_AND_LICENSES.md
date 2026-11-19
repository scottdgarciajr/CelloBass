# Original source file map, documentation and licenses

## 1. O'Cello by Conor O'Kane
Included archive: `02_ORIGINAL_PROJECTS/O-Cello_Source.zip`
- Contents inspected: one Blender source file `O-Cello_Source.blend` (~3.5 MB uncompressed).
- The original O'Cello is a 3D-printable cello. A Blender file is NOT the same as an editable parametric STEP source; Codex needs Blender to import/export and measure it reliably.
- Official original home page: https://o-cello.com/
- Official assembly PDF: https://o-cello.com/files/ocello_assembly_instructions.pdf
- The official build guide specifies: 12 mm diameter, 1 m long steel rod; 10 mm aluminum tube (~45 cm); 20x20x2 mm aluminum L-bar; 4 cello strings; 4 bass tuners; M5 hardware. Verify exact applicability after auditing the provided `.blend` source.
- Official bridge guidance notes an **asymmetrical printed curved bridge**, raised on the C/G side; preserve it. Its mount is designed as a slide-in part, not a moving bridge in use.
- **License listed by official O'Cello site: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. Non-commercial reuse with attribution; commercialization requires permission from the rights holder.

## 2. OpenBass by tbenen
Included archive: `02_ORIGINAL_PROJECTS/OpenBass_Original.zip`
- Contains OpenBass V2.1/V2.0 (`.f3d`, `.step`, `.stl`, `.3mf`), 3D printed maker tools, and exported Printables model PDF page.
- Preferred reference: `OpenBass V2.1/openbass-v21-v27.step` or `.f3d`; use it to study body segmentation and attachment methods. No direct replacement of the O'Cello's neck, bridge or string lengths.
- Original project: https://www.printables.com/model/1378247-openbass-customizable-3d-printed-multiscale-headle
- In the uploaded project PDF, OpenBass V2.1 specs list long/short scales 34.25/33.75 in and 19 mm spacing between strings at bridge. Those dimensions are **not cello requirements**.
- The original model page warns its historic Ploutone headless bridge manufacturer no longer supplies the specified bridges (as of 2026-09-10); avoid designing around that particular part.
- **License shown in uploaded OpenBass model PDF: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)**. Attribute the author and comply with the ShareAlike condition if making a derivative available.

## 3. Combined design license caution
The two originals use **different licensing requirements** (one NonCommercial, one ShareAlike). A combined derivative that actually incorporates copyrightable geometry from both could present compatibility issues for redistribution. For the personal noncommercial prototype, keep provenance and author credits. **Do not assume the combined design can be released under a single license, shared publicly, sold, or described as freely commercializable without verifying the specific permissions and seeking rights-holder permission where required.** Consider using OpenBass for inspiration only, with newly created original wing geometry, to reduce derivative complexity.

## 4. Concept reference images
The generated visuals in `03_VISUAL_REFERENCES/` show **different aesthetic directions**, not photographs of a functioning device or a matched pair of mechanically identical models. Their support legs, switches, bridge and body geometry may be inconsistent. Never reverse-engineer dimensions from them.

## Credits note to retain in future CAD repository
> CelloBass is an experimental independent prototype built using O'Cello (Conor O'Kane; CC BY-NC 4.0) as an initial design reference, and OpenBass (tbenen; CC BY-SA 4.0) as a construction/ergonomics reference where applicable. Original licenses and authorship are retained; new work is not endorsed by the original authors.
