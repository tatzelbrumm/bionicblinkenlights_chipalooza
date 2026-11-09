<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Summary

Bionic Blinkenlights for the Chipalooza sg13cmos5l harness, slot 3: four spiking neurons, all 3.3 V devices,
tuned by 4-bit codes and coupled through pulse synapses, a gap junction and the harness analog buses.
N0..N2 are pA neurons (9 transistors, 2 MOS capacitors, charged with 8..139 pA): the buffered N0 / N1 fire at
1.2 to 18 Hz, N2 on the bare `analog_bus2` at 0.91 to 15 Hz. N3 (`bbl_neuron_hi`, 12 transistors) charges with
6..118 nA, so that the leakage of a harness bus cannot stop it: 0.47 to 8.9 kHz on the bare `analog_bus3`,
0.67 to 12.8 Hz with 10 nF on it. Repository `tatzelbrumm/bionicblinkenlights_chipalooza`, branch `main`; the
delivered files are pinned by their sha256 below.

## The point: the bus capacitance sets the firing rate

N2 and N3 have their membranes on `analog_bus2` / `analog_bus3`; the bus line and anything on it add to the
10 pF membrane capacitor. N0 and N1 drive their buses through inverters and do not see the load. Code 6,
rates = 1 / median spike interval:

| C_bus (3 pF line + load) | 3 pF | 13 pF | 33 pF | 103 pF | 1 nF | 10 nF | 100 nF | exponent of f vs (10 pF + C_bus), to 10 nF |
|---|---|---|---|---|---|---|---|---|
| N2, schematic | 7.19 Hz | 4.09 | 2.20 | 0.837 | | | | -0.99 |
| N2, post-layout | 6.96 | 4.01 (partial run, to 1.22 s) | 2.17 | 0.833 (4 s run) | | | | -0.98 |
| N3, schematic | 3880 Hz | 2286 | 1255 | 487 | 54.9 | 5.56 | 0.642 | -0.99 |
| N3, post-layout | 3789 | | | 485 | 54.8 | 5.56 | | -0.97 |
| N0 / N1 (buffered), schematic | 9.32 / 9.34 | 9.32 / 9.34 | 9.32 / 9.34 | 9.32 / 9.34 | 9.32 / 9.34 | 9.32 / 9.34 | 9.32 / 9.34 | 0 |
| N0 / N1, post-layout | 9.02 / 9.06 | 9.03 / 9.06 | 9.07 / 9.05 | 9.01 / 9.01 | 8.96 / 9.00 | 9.02 / 9.06 | | 0 |

The rate is inversely proportional to the membrane capacitance including the bus: N2 over 3 to 103 pF, N3
over 3 pF to 10 nF (3.5 decades). On the bare bus N3's refractory time (23 us at code 6) takes a tenth of
its period, so that point lies about 10 % below the line through the nF points. With 100 nF the refractory
time is only two time constants of the bus through the reset path (about 110 Ohm), the bus resets to 0.11 V
instead of 0, and the rate is 15 % above the line. The extracted wiring adds about 0.4 pF to every membrane:
the post-layout rates of the pA neurons are 3.0 to 3.9 % lower with 3 pF on the bus, N2's 1 % lower at
33 pF; N3's 2.3 % lower on the bare bus, 0.3 % at 103 pF and the same from 1 nF up. Figure: `testbenches/ngspice/results/busload.png`.

The pulse a bus-coupled pA neuron puts on its bus shrinks with the load (2.0 V unloaded, 1.2 V at 30 pF,
0.9 V at 100 pF), and it reaches the bus only with `vcplb` high (pulled up on chip to 3.3 V when left open).
N3's bus carries a sawtooth, 0 to 0.92 V, with a sharp reset at every spike.

## Checks (`slot_3`, and both generic variants `bbl_slot_pads`, `bbl_slot_shared`)

| check | result |
|---|---|
| DRC (IHP `run_drc.py`, no density), 2026-11-09 12:09 | 0 violations, 0 exceptions, all three |
| LVS (IHP `run_lvs.py`, deep, `--disable_tap_extraction`) against the `bbl.cdl` below, 15:26 | netlists match, all three |
| PEX (kpex 2.5D, `--mode CC`), 12:13 | 2288 / 2288 / 2280 coupling capacitors (`slot_3`, pads, shared) |
| sheets vs source netlist (`check_sheets.py`, xschem netlist device by device) | 13 sheets, 0 mismatches |

XOR of `slot_3` against `bbl_slot_pads` (repeated on the current layouts): the frame shapes of
`slot3_wrapper` (pin labels `s3_*`, its Metal2 `vss_3v3` pin; slot 1's no-fill box on layer 67/23 is gone)
and the via stack (Via2 .. TopVia1) that ties that pin to the ground straps; nothing else differs.

## Simulation (IHP PSP 103, typical, 27 C)

Buses: the harness switch closed, 3 pF of line, plus the load of each case (details: README, "Simulation
notes"). N3 has 10 nF on its bus in the system cases (blinking mode). Rates of free-running neurons:
1 / median interval; coupling cases: mean rate.

| | schematic | post-layout (`slot_3`) |
|---|---|---|
| tuning, buffered N0 / N1, codes 0 .. 13 | 1.19 .. 18.3 Hz: 1.19 Hz + 1.32 Hz per step | 3.5 to 3.9 % lower |
| tuning, N2 on its 3 pF bus, codes 0 .. 14 | 0.91 .. 15.06 Hz | 3.3 to 3.4 % lower |
| tuning, N3 with 10 nF, codes 0 .. 15 | 0.672 .. 12.84 Hz | the same within 0.2 % |
| N3 on the bare bus, codes 0 / 3 / 6 / 9 / 12 / 15 | 469 / 2184 / 3880 / 5569 / 7247 / 8916 Hz | codes 0 / 6 / 15: 459 / 3789 / 8682 Hz (2.1 to 2.6 % lower) |
| N3 with the PDK pad's leakage on its bus | 20 pF: -2.6 % (code 0), -0.76 % (code 15); 10 nF, code 6: -0.25 % | code 0, 20 pF: 207.3 Hz (-0.9 % against the schematic) |
| supply current, slot (average, `vdd_3v3`) | 0.37 .. 1.61 uA | 0.44 .. 1.65 uA |
| pulse synapse N0 -> N1 (N0 13.2 Hz, N1 alone 2.60 Hz) | N1 4.07 / 7.08 / 9.91 Hz for weak / strong / both; strong: vector strength 0.91 | both: N0 12.68, N1 9.47 Hz |
| mutual synapses (N0 5.33, N1 2.60 Hz) | strong: 1:1 lock, 5.33 / 5.33 Hz, vector strength 1.00; weak: drift, 5.59 / 3.25 Hz | — |
| gap junction N0 <-> N1 (8.00 / 10.65 Hz) | `vcpla` 0.3 V: 7.90 / 10.59 Hz; 0.4 V: 6.51 / 9.90 Hz; 0.5 V and up, and every digital leg: N0 suppressed (weak 1.04, both legs 1.44 Hz, strong silent) | off: 7.70 / 10.26 Hz; both legs: N0 fewer than 2 spikes in 1.5 s, N1 9.08 Hz |
| N3 -> bus2 (N2 code 5 on 3 pF, N3 code 7 on 10 nF; alone 6.18 / 6.37 Hz) | weak: N2 33.0 Hz, N3 silent (bus3 held at 0.48 .. 0.66 V); strong: 1:1 lock at 8.81 Hz, vector strength 1.00 (8.78 Hz with 30 pF on bus2) | off: 5.98 / 6.37 Hz; strong: 1:1 at 8.74 Hz |
| `vcplb` (N2 code 6 with 30 pF; N3 code 0 with 10 nF) | 0 V: N2 9.33 Hz and N3 599 Hz on their own membranes (partial run, 0.49 s); 0.8 V: 2.95 / 1.62 Hz; 1.2 V: 2.21 / 0.87 Hz; 3.3 V: 2.19 Hz / N3 fewer than 2 spikes in 2.5 s (0.67 Hz in `tune_low`) | — |

Coupling between two pA neurons acts as inhibition: a conductance above about 0.1 nS drains more than the
8..139 pA charging current while the other neuron is in reset (milliseconds), and a spike (about 10 us) is too
short to pass charge. Synchronization comes from the pulse synapses. Between N3 (nA) and N2 (pA) on bus2 the
charge flows the other way: through the weak leg N3 drives N2, whose lower threshold (0.66 against 0.92 V)
fires first and whose resets keep N3 below its own; the strong leg locks the two 1:1. Figures and the full
table: `testbenches/ngspice/results/`.

## Files

| file | sha256 |
|---|---|
| `final/gds/slot_3.gds` (for the harness: pads variant in the slot 3 frame) | `ef1958be8d28899873a0507ce9fc24dd4757a4142c0aa762f8e2c8cbe2e33a54` |
| `layout/gds/bbl_slot_shared.gds` | `2e66cb40718de0aaaa2ee4cc48e6698043809f7fe09026502370391e760225a6` |
| `layout/gds/bbl_slot_pads.gds` | `3390593ba9cb9b7e03b82f7dc0f8e6e1f50301a1814fb3a41fb2376730c0f6a8` |
| `layout/gds/bbl_cells.gds` | `d6036890559552912fe750e0f0731651c6ce85a4d0a9f96a741f5ffdc44edb2c` |
| `netlist/cdl/bbl.cdl` (LVS, with `slot_3`) | `7b32a005abb2fb725260ebf59b0f88a6cb79903060172a9367c6b03efe5b2b8c` |
| `netlist/source/bbl.spice` | `3f610ea8076d15d56cca416dcfc6d194f9e92e13947e1c2b120ac26204b90715` |
| `netlist/source/bbl_slot.spice` | `9353d7e297f5c200e3b6ef6ab3feb34e48d7b1c2c92c255f5ae9332fcc022b35` |
| `netlist/pex/slot_3.pex.spice` | `85fdad042ca149735a5331edcba661dfe1afa9113505d7af39243b91336f2cd0` |
| `netlist/pex/bbl_slot_shared.pex.spice` | `141af5e71ea884238433d8f2e2094c374d4c2bf94947ddd133a7fe6216620b4e` |
| `netlist/pex/bbl_slot_pads.pex.spice` | `a2d5b50c8329dc590d6bc9c77d8a3642f3b1eb0bfde83f2739a8328f8bbc8528` |

The GDS, the extracted netlists and `bbl_slot.spice` are those of commit `252bc48`; `bbl.spice` and `bbl.cdl`
changed since only in comments (corrected currents and times), and LVS was repeated against this `bbl.cdl`.

## Open points

1. Bus capacitance and leakage in the harness (`testbenches/harness_bus/results.md`): with the bus switch
   closed, a slot bus carries about 9 pF on chip (own switch 2 pF, the 17 other slots' open switches 6.8 pF,
   pad 0.2 pF) plus the shared wiring and the board, so 10..20 pF rather than 3 pF; the 1/C law covers that.
   The PDK pad model leaks 0.1..0.36 nA to ground at 0.3..1.6 V (27 C), from the soft-breakdown term of its
   antenna diode models: with it N2 does not fire at any code (8 pA at code 0, 139 pA at code 15), N3 slows by
   0.25 to 2.6 %. Whether real pads leak that much is open; the clamp transistors alone (PSP) push 6..27 pA into
   the node at 27 C. The chip measures both: the rate of N2 (or N3) against that of N0 over the codes gives
   C_bus (slope) and the net leakage (offset).
2. Slot 3 is assigned; the harness's `config.txt` still lists slot 3 for another project
   (`s3_source` `sg13cmos5l_slot3_backup`), which its maintainer changes. Moving to another slot: README,
   "Slot 3, and moving to another slot".
3. kpex's built-in LVS reports a mismatch because it counts the well taps as devices; the PDK LVS with tap
   extraction disabled matches. The extracted netlists keep the taps as `ntap1` / `ptap1`.
4. Off chip: N0..N2 put 10 us pulses of 0.9 to 3.3 V on their buses and need an LED amplifier with an input
   leakage well below 1 pA. N3's sawtooth wants a speaker amplifier (audio) or 6..10 nF of C0G or film
   capacitor on `analog_bus3` (blinking); a 10 MOhm probe stops N3 up to code 11.
5. N3's supply current: its Schmitt trigger holds out high up to 0.92 V, so XM1 draws up to 7 uA against XMQ
   at the top of every ramp; the slot draws 0.85 to 1.65 uA instead of 0.37 to 0.47 uA. A weaker XMQ would cut
   that (not done).
6. With 100 nF on `analog_bus3` N3's reset is incomplete (0.11 V); the 1/C law holds to 10 nF.
7. The transient solver stops ("timestep too small") much more often since N3 resets nanofarads within
   microseconds (at least six post-layout cases needed the retry at half the step; `vcplb_0.0` stopped in every
   attempt and is a partial run), and puts a spurious early spike into about one run in 15; retries, partial
   runs and median rates: README, "Simulation notes", and `docs/RUNLOG.md` rows 83 to 92.
8. No 1:1 synchronization through the gap junction at 33 % detuning; a finer `vcpla` sweep around 0.4 V or
   less detuned codes may find a locking window.
9. Corners, temperature and mismatch were not simulated.
