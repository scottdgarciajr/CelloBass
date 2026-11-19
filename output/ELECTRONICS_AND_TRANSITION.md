# Audio and live transition — proposed, NOT TESTED

The pickup, impedance interface, processor and controller have not been selected or installed. Nothing in this package creates functioning electronics or changes the bass tuning to E-A-D-G.

## Candidate one-action processing path

For a prototype using a computer already available to the player:

`bridge-compatible piezo -> suitable high-input-impedance piezo preamp/buffer -> audio interface -> REAPER input-monitoring track -> output interface -> amplifier/PA`

Use the preamp/input impedance recommended by the chosen pickup maker. A conventional line input is not automatically appropriate for a passive piezo. The preamp should feed the interface at its specified level; phantom power must follow the actual hardware instructions. A pickup model and power supply remain to be chosen.

In REAPER, make a dedicated monitored track for the instrument. Proposed bass FX: ReaPitch (-8 semitones, wet-only), ReaEQ and ReaComp. Set the desired cello sound with that bass chain bypassed. Keep any always-required input gain/high-pass processing outside the toggled track-FX group, for example in the input FX chain after checking monitoring behavior. Do not create a second dry monitoring path that doubles the input unintentionally.

Connect a USB MIDI footswitch that can send one MIDI event per press. Enable it for control messages and assign a REAPER action that toggles the instrument track FX bypass; verify that the action targets this track rather than whichever track is selected. Configure the chain so a single press toggles the entire bass chain and the next press restores cello. Match the bypass-state gain before live use. Do not map both press and release to a toggle or one press can toggle twice. Actual action mapping, event handling, sound and latency are NOT TESTED.

Required additional items are the piezo, compatible impedance buffer/preamp and its power source, shielded instrument lead, suitable audio interface/driver, computer with a REAPER license as applicable, USB MIDI foot controller, monitoring/output cables, and amplifier or PA. None is supplied here. This is a candidate setup, not a purchase instruction; first check equipment already owned by the player.

Manufacturer documentation supports the availability of ReaPitch/ReaEQ/ReaComp and host FX-bypass/control functions, but does not establish the specific CelloBass mapping or audible result: [REAPER user guides](https://www.reaper.fm/userguide.php), [ReaEffects guide](https://www.reaper.fm/guides/ReaEffectsGuide.pdf). No DAW or effect software was downloaded as part of this project.

At -8 semitones, C2-G2-D3-A3 becomes approximately E1-B1-F#2-C#3. Fifth tuning remains fifth tuning. Assess bowed and plucked notes separately, especially latency, low-note tracking, polyphony and attack definition. There is no automatic tilt-controlled effect selection.

## Wiring provisions to develop

The Blender purple curve is a routing sketch from the bridge underside to the rear/left side of the fixed structure. It is not a bored conduit, physical mounting interface or collision-verified cable. Do not drill the original bridge or neck from that curve.

Mount a shielded output jack on a fixed reinforced structure, with a separate strain-relief clamp taking cable tug load before the solder terminals. Keep a service loop behind the instrument, clear of wing stops, pin heads, endpin and tuners. The same lead remains attached during the orientation change. Route pickup wire and harness independently. Final jack footprint, pickup coupling, shielding/ground scheme and bend radius depend on actual hardware and remain open.

## Candidate hand sequence after support validation

1. Before the song: wings deployed and positively locked; endpin fully stowed; harness continuously attached; cable supported; footswitch mode and gain checked.
2. At a musical rest: stop bow motion. Support the neck with the left hand and take a tested fixed-core handhold with the right. The bow must be safely held clear or parked in a verified holder; no holder is modeled or validated yet.
3. Rotate the complete instrument through the tested direction while the harness carries it. Do not release wing locks, move the bridge, adjust the endpin, retune or rehook support.
4. Press the mapped footswitch once, confirm the preset state, then pluck. The reverse sequence restores upright bowing.

There may be seconds of silence during repositioning. Bow handoff/parking is an unresolved ergonomic issue, not a solved detail. No looping or rosin-free sustain is implemented.

Until the harness and bow-hand sequence pass, the practical fallback is to remain upright, stop bowing and pluck while selecting the bass chain. An extended planted endpin can remain for that stationary fallback, but cannot accompany a claimed rapid sideways transition.
