<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# What a slot's analog bus sees in the harness (2026-11-09)

Sources: the harness repository (read only) `verilog/rtl/chipalooza_frame.v` (topology) and
`netlist/layout/chipalooza_frame.spice` (extracted `analog_switch_med` with its gate driver); the PDK pad
`sg13cmos5l_IOPadAnalog` (`libs.ref/sg13cmos5l_io/spice`). IHP models, typical, ngspice 47.

Topology: each slot's `analog_bus<k>` pin goes through its own `analog_switch_med` (NMOS and PMOS, 40 x 10 um
each) to `user_analog_shared[k]`, which is the chip's analog pin `analog[k]` (pad). 18 slots share each bus.

## Capacitance and leakage (`buscap.py`)

C from the AC current at 1 kHz; leakage = DC current from the node into the part (+: pulls the node down,
-: pushes current into it).

| part | C (pF) | leakage at 0.3 / 0.8 / 1.5 V, 27 C (pA) | 60 C (pA) |
|---|---|---|---|
| this slot's switch, closed (both sides) | 1.71 / 1.66 / 2.35 | -0.6 / -0.3 / 0.0 | -18 / -15 / -11 |
| a switch, open, slot side (other side at 0.8 V) | 0.45 / 0.44 / 0.43 | -30 / -5 / -0.1 | -93 / -24 / -6 |
| a switch, open, shared side (other side at 0.8 V), x 17 | 0.42 / 0.40 / 0.39 | -30 / -5 / -0.1 | -93 / -24 / -6 |
| analog pad (clamps, diodes, secondary protection) | 0.21 | +106 / +187 / +336 | +178 / +368 / +689 |
| the pad's two clamp transistors alone | 0.11 | -27 / -10 / -6 | -152 / -103 / -86 |

On-chip capacitance on a slot bus:

- switch open: about 0.45 pF (switch) plus the slot's own wiring;
- switch closed: 1.7..2.4 (own switch) + 17 x 0.40 (the other slots' switches) + 0.21 (pad) = about 9 pF, plus
  the shared bus wiring (not extracted here: the harness's own extraction is for LVS, without capacitance,
  and the switch and IO layouts are not in this container; estimate 1..2 pF), plus everything off chip.

The 3 pF of the simulations is therefore low for a closed switch: 10..20 pF is more likely. The firing
rate follows 1 / (10 pF + C_bus) up to 103 pF (schematic and post-layout), so the circuit tolerates it; at
code 6, 15 pF gives about 3.7 Hz instead of 7.2 Hz.

## Leakage: the pad model stops N2 and N3 (`padiv.py`, `padtest.py`)

The pad's leakage in the model comes from the antenna diodes (`dantenna`, `dpantenna`, 2 x 35 um^2 each): their
models carry a soft-breakdown term (`bv` 11.6 V, `nbv` 48.9) fitted down to -15 V and are marked "designed for
reverse direction". At 0.3..1.5 V that term gives 1.5..5 pA per um^2, orders of magnitude above the usual
junction leakage; it may be an artefact of the fit. The clamp transistors alone push current into the node.

Transients (schematic, 2.5 s) with the pad's DC I-V (table) and 0.21 pF on `analog_bus2/3`:

| case | N2, N3 | membrane |
|---|---|---|
| code 15, 10 pF, no pad (reference) | 10.46 / 10.47 Hz (1/C law: 10.43 Hz) | fires |
| code 6, 3 pF + pad, 27 C | no spike | settles at 0.094 V (charging current = leakage, about 62 pA) |
| code 10, 3 pF + pad, 27 C | no spike | settles at 0.25 V (about 97 pA) |
| code 15, 3 pF + pad, 27 C | no spike | settles at 0.51 V (about 139 pA) |
| code 15, 3 pF + pad, 60 C | no spike | settles at 0.22 V |
| code 15, 10 pF + pad, 27 C | no spike | settles at 0.51 V |

N2 and N3 fire only while the net leakage at the threshold (about 1.6 V) is below their charging current:
about 9 pA at code 0, 62 pA at code 6, 139 pA at code 15. The model's pad sinks 364 pA there (27 C). The
open switches of the other slots push or pull 0.1..30 pA each (27 C), depending on the voltage on their slot
side. N0 and N1 drive their buses through inverters and are not affected.

## Reading the bus off the chip

With the bus switch closed, rate against code gives both numbers. N0 (buffered, same circuit) gives
f0(k) = I_k / (C_m dV); N2 on the bus gives f2(k) = (I_k + I_bus) / ((C_m + C_bus) dV). Over the codes,
f2 against f0 is a straight line: slope C_m / (C_m + C_bus) gives the bus capacitance, the offset
I_bus / ((C_m + C_bus) dV) gives the net leakage (C_m = 10.4 pF post-layout). If N2 stops at the low codes,
the code where it starts gives I_bus directly.
