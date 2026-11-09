<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Summary

Bionic Blinkenlights for the Chipalooza sg13cmos5l harness: four spiking neurons (9 transistors and 2 MOS
capacitors each, all 3.3 V devices, no static current in the neuron), tuned by 4-bit codes: buffered neurons
1.1 to 18 Hz (codes 0 to 13 simulated), bus-coupled neurons 0.9 to 16 Hz (codes 0 to 15, 3 pF bus); coupled
through pulse synapses, a gap junction and the harness analog buses. Repository `tatzelbrumm/bionicblinkenlights_chipalooza`,
branch `main`; the delivered files are pinned by their sha256 below.

## The point: the bus capacitance sets the firing rate

N2 and N3 have their membranes on `analog_bus2` / `analog_bus3`; the bus line and anything on it add to the
10 pF membrane capacitor. N0 and N1 drive their buses through inverters and do not see the load.

| C_bus (3 pF line + load) | 3 pF | 13 pF | 33 pF | 103 pF | exponent of f vs (10 pF + C_bus) |
|---|---|---|---|---|---|
| N2, schematic (code 6) | 7.19 Hz | 4.09 | 2.19 | 0.84 | -0.99 |
| N3, schematic | 7.20 | 4.09 | 2.20 | 0.84 | -1.00 |
| N2, post-layout | 6.95 | — | 2.18 | TBD | TBD |
| N0, N1 (buffered) | 9.32 / 9.34 | 9.32 / 9.34 | 9.33 / 9.34 | 9.32 / 9.34 | 0 |

The rate is inversely proportional to the membrane capacitance including the bus: about -0.55 Hz per pF at
the unloaded bus. The bus pulse a bus-coupled neuron produces shrinks with the load (2.0 V unloaded,
1.2 V at 30 pF, 0.9 V at 100 pF, post-layout), and the spike reaches the bus only with `vcplb` high (pulled up on chip
to 3.3 V when left open); at 0.8 / 1.2 V the pass gate clips it, while the bus still loads the membrane.

## Checks (both variants: `bbl_slot_shared`, `bbl_slot_pads`)

| check | result |
|---|---|
| DRC (IHP `run_drc.py`, no density) | 0 violations, 0 exceptions, both |
| LVS (IHP `run_lvs.py`, deep, `--disable_tap_extraction`) | netlists match, both |
| PEX (kpex 2.5D, `--mode CC`) | 2244 / 2252 coupling capacitors |
| sheets vs source netlist (`check_sheets.py`, xschem netlist device by device) | 11 sheets, 0 mismatches |

## Simulation (IHP PSP 103, typical, 27 C; buses modelled as 2 kOhm switch + 3 pF + load)

| | schematic | post-layout |
|---|---|---|
| tuning, buffered N0/N1, code 0 .. 13 | 1.19 .. 18.30 Hz (N0: about 1.3 Hz + 1.32 Hz per code step) | 3.5 to 4 % lower; code 0: 1.14 Hz |
| tuning, on 3 pF bus N2/N3, code 0 .. 15 | 0.91 .. 16.04 Hz | 3 to 4 % lower; code 0: 0.88 Hz |
| supply current, slot (average, vdd_3v3) | 0.37 uA (all codes 0) .. 0.47 uA | 0.40 .. 0.48 uA |
| pulse synapse N0 -> N1 (N0 13.2 Hz) | N1 2.60 / 4.11 / 6.85 / 9.91 Hz for off / weak / strong / both; strong locks 2:1 (vector strength 0.89) | both: 9.51 Hz |
| mutual synapses (N0 5.33, N1 2.60 Hz) | strong: 1:1 lock, 5.33 / 5.33 Hz, VS 1.00; weak: drift, 5.59 / 3.23 Hz | — |
| gap junction N0 <-> N1 (8.0 / 10.6 Hz) | vcpla 0.3 V: no effect; 0.4 V: both slow (6.39 / 9.79 Hz); 0.5 V and up, and every digital leg: N0 suppressed (both legs: 1.33 Hz) | both legs: N0 fires once in 1.5 s, N1 9.05 Hz |
| N3 -> bus2 (N2 6.17, N3 8.21 Hz) | weak / strong: N2 2.40 / 1.31 Hz, N3 7.20 Hz; strong + 30 pF: N2 stops | off: 5.96 / 7.95 Hz; strong: N2 fires once in 1.5 s, N3 7.03 Hz |

Electrical coupling acts as inhibition here: the membranes charge with 4 to 150 pA, so a coupling conductance
above about 0.1 nS drains more than that while the other neuron is in reset (milliseconds), and a spike (about
10 us) is too short to pass charge. Synchronization comes from the pulse synapses; the gap junction and the
bus coupling demonstrate suppression and desynchronization. Figures and the full table:
`testbenches/ngspice/results/`.

## Files

| file | sha256 |
|---|---|
| `final/gds/bbl_slot_shared.gds` (= `layout/gds/`) | `b3ea7c8bfaa29aecc88830512442f58a8eaa8b95147ca9320e023468758c8738` |
| `final/gds/bbl_slot_pads.gds` (= `layout/gds/`) | `333b2ae429301398d2ee841d43c490152d8ed917d2e4fc7a9cb7c051c884c7a4` |
| `layout/gds/bbl_cells.gds` | `eadc7b38263c6c06f0ae1d790bfc89a7c9fe6bdb785c1425a3729d181da511ff` |
| `netlist/cdl/bbl.cdl` (LVS) | `14edeff7393ec994b9d44e2c1dcac51401bd3152d3db2fffbeaca65e31272441` |
| `netlist/source/bbl.spice` | `9fa234c9592e96d4d1ac57378383f9c3c4a08e3ca2fc786fcc3cb9f7980201d7` |
| `netlist/source/bbl_slot.spice` | `9353d7e297f5c200e3b6ef6ab3feb34e48d7b1c2c92c255f5ae9332fcc022b35` |
| `netlist/pex/bbl_slot_shared.pex.spice` | `a9de7b9856362602bf2671b3887535ffd9539927c98e901e06e3b565e7c6e453` |
| `netlist/pex/bbl_slot_pads.pex.spice` | `f855451d8a8f757c785883c8742465c17ea46ee06ff72e4fd5c1851edd2d0b90` |

DRC (01:20) and LVS (01:19, repeated on `final/gds/` at 06:08) ran on exactly these GDS files.

## Open points

1. Bus line capacitance: 3 pF assumed for trunk, pad and bond wire; the real value shifts the N2/N3 rates
   (by the 1/C law above).
2. The slot number for `final/gds/slot_<N>.gds` is not assigned yet; `build_slot.py` makes it for any slot
   (the pads variant only for slots with two dedicated analog pads).
3. kpex's built-in LVS reports a mismatch because it counts the well taps as devices (451 vs 68); the PDK LVS
   with tap extraction disabled matches. The extracted netlists keep the taps as `ntap1` / `ptap1`.
4. The LED amplifier (off-chip) has to respond to 10 us pulses of 0.9 to 3.3 V with an input leakage well
   below 1 pA.
5. No 1:1 synchronization through the gap junction at 33 % detuning; a finer `vcpla` sweep around 0.4 V or
   less detuned codes may find a locking window.
6. Corners, temperature and mismatch were not simulated.
