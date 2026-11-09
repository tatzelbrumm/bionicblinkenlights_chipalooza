<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Bionic Blinkenlights for the Chipalooza sg13cmos5l harness

Four spiking neurons for one slot of the Chipalooza analog harness
([`tatzelbrumm/sg13cmos5l_ocd_chipalooza`](https://github.com/tatzelbrumm/sg13cmos5l_ocd_chipalooza)), IHP
**sg13cmos5l**, 3.3 V thick-oxide devices. They are a CMOS translation of the 4-transistor integrate-and-fire
neuron of [Bionic Blinkenlights](https://cmucsd.bitbucket.io/bionicblinkenlights/index.html) (neuron:
img7.html, schematic: img8.html, demos: img11.html and img12.html). N0..N2 fire at about 1 to 20 Hz, are
coupled through tunable synapses, gap junctions and the harness analog buses, and show their spikes on the
analog buses, where an off-chip ultra-high-impedance amplifier drives an LED per bus. N3 runs on nA instead of
pA, so that the leakage of a harness bus cannot stop it: on chip it sings (0.5 to 9 kHz on `analog_bus3`), and
about 10 nF on that bus brings it down to blinking.

Status and check results: [`docs/SUMMARY.md`](docs/SUMMARY.md). Step-by-step record: [`docs/RUNLOG.md`](docs/RUNLOG.md).

## The neuron

The discrete original: Q1 (npn) turns on when the membrane C1, charged through R3, reaches its base-emitter
voltage; Q3 (pnp) then feeds current back into the membrane (regenerative upstroke) while the LED in Q1's
collector lights; the collector node also discharges C2 through R5 ("slowout"), which turns on Q4 (pnp), whose
collector (reset) turns on Q2 (npn), which discharges the membrane.

The CMOS version (`bbl_neuron`, sheet [`schematic/png/bbl_neuron.png`](schematic/png/bbl_neuron.png)) keeps the
four transistors in the same roles and replaces every resistor by a MOSFET (R5 by two): 9 transistors and two
MOS capacitors.

| original | here | how |
|---|---|---|
| Q1 npn | XM1 nmos 1/1 | membrane -> out; fires at about 0.65 V |
| Q3 pnp + R4 | XM3 pmos 0.3/4 | out low -> about 8 uA into the membrane; its length is R4 |
| Q4 pnp | XM4 pmos 1/0.45 | slow low -> rst high |
| Q2 npn | XM2 nmos 2/0.45 | rst high -> membrane discharged |
| R1 | XMR1 pmos 0.3/20, gate on vss | self-biased pull-up of out |
| R2 | XMR2 nmos 0.3/20, gate on vdd | self-biased pull-down of rst |
| R5 | XMR5A nmos 0.3/100, gate on vdd; XMR5B pmos 0.3/4, gate on vin | XMR5A discharges the slow node fast when out falls and recharges it only to vdd - Vt; XMR5B finishes the recharge slowly (refractory time 1..25 ms, from the DAC bias): the long R5 C2 recovery of the original, which keeps Q2 on until the membrane, and the bus with it, is empty |
| R3 | XMR3 pmos 0.3/30, gate on vin | the only biased one: 8..139 pA from the tuning DAC (1/52 of its 0.38..7.4 nA) |
| C1 | XC1 pmos gate capacitor, 10 pF | membrane |
| C2 | XC2 nmos gate capacitor, 2.6 pF | slow node |

The spike is a few microseconds long (fast spikes; the LED amplifier stretches them). The membrane, and with
it the bus of a bus-coupled neuron, rises by up to about 2 V during the spike (1.2 V with 30 pF on the bus,
0.9 V with 100 pF). Between spikes the neuron draws no static current until its membrane nears the threshold,
where XM1 starts to pull against the pull-up of out (0.2 uA at 0.6 V, 1.2 uA at 0.7 V; DC sweep).

### N3: the neuron that makes itself heard (`bbl_neuron_hi`)

On a harness bus with its switch closed, the PDK pad model leaks 0.1 to 0.36 nA, more than the 8..139 pA
that charge the membranes of N0..N2; N2 stops there (`testbenches/harness_bus/results.md`). N3 is built to
survive it (sheet [`schematic/png/bbl_neuron_hi.png`](schematic/png/bbl_neuron_hi.png); 12 transistors, two MOS
capacitors):

| device | N0..N2 | N3 | why |
|---|---|---|---|
| XMR3 | 0.3/30 | 48/3 x 8 | 16 x the DAC current: 6.1 nA at code 0, 7.4 nA more per step, 118 nA at code 15; about 800 x the 8..139 pA of N0..N2 (DC, membrane at 0.3 V) |
| XMIP, XMIN, XMQ | — | 3/0.45, 0.3/4, 0.3/3 | Schmitt comparator: inverter out -> outb switching at about 2.3 V, pull-up XMQ on out gated by outb. With nF on the membrane the regenerative loop through it (XM3) is too slow; without hysteresis the reset holds the membrane at the threshold |
| XMR5A | 0.3/100, slow to out, gate vdd | 3/0.45, slow to vss, gate outb | empties slow within ns when out falls and stays off afterwards, so rst stays fully high for the whole refractory time |
| XMR5B | 0.3/4 | 10/0.45 x 2 | refractory (membrane held at 0 V) 11 us at code 15 .. 0.19 ms at code 0: a tenth of the period on the bare bus, negligible with nF on it |
| XM4, XM2 | 1/0.45, 2/0.45 | 10/0.45, 40/0.45 | rst fully high; with the bus pass gate XMP3 (40/0.45) about 100 Ohm, so 10 nF on the bus is reset within the refractory time |

N3 resets its membrane and its bus completely (0 .. 0.92 V sawtooth) from 3 pF to 10 nF on the bus. With
100 nF the refractory time (23 us at code 6) is only two time constants of the bus through the reset path
(about 110 Ohm with the harness switch): the bus resets to 0.11 V, and the rate is 15 % above the 1/C line
(0.64 instead of 0.56 Hz). Its spike shows on the bus as the sharp reset at the end of each ramp, not as a
high pulse.

The price of the hysteresis is supply current: the Schmitt trigger holds out high until 0.92 V, so XM1
pulls against XMQ for the top third of every ramp (1.2 uA at 0.7 V, 7 uA at 0.9 V; DC sweep), whatever the
ramp's speed. In the simulated cases the slot draws 0.85 to 1.65 uA from `vdd_3v3` (0.37 to 0.47 uA with four
pA neurons); 0.37 to 0.5 uA where N2 or a half-open pass gate (`vcplb` 0.8 to 1.2 V) cuts N3's ramp short.

## The slot (`bbl_core`)

| block | what |
|---|---|
| `bbl_bias` | self-biased reference: subthreshold beta multiplier (K = 8, rhigh 1.2 MOhm), about 45 nA per branch; start-up by Vgs = 0 leakage; `enable` gates it; 2.5 nA reference `vbnl` for the DACs; weak pull-ups for the coupling voltages |
| `bbl_unit` x 3, `bbl_unit_hi` | neuron + 4-bit tuning DAC (`bbl_dac`); f rises about linearly with the code: 1.2 Hz at code 0, 1.3 Hz more per step (buffered neuron). N3 is `bbl_unit_hi` (above) |
| N0, N1 | buffered: inverters drive `analog_bus0` / `analog_bus1` high while they fire, so bus load does not affect them. Pulse synapses N0 -> N1 and N1 -> N0 (`bbl_syn`, the photoresistor of the demos), gap junction N0 <-> N1 (`bbl_gap`) |
| N2, N3 | membranes on `analog_bus2` / `analog_bus3` through NMOS pass gates (gate `vcplb`; N3's 40/0.45): the bus line's own capacitance and whatever loads the bus become part of the membrane capacitance. N3 can also be connected to `analog_bus2`, which couples it to N2 through the bus |
| `bbl_tielo` | holds `dig_out[11:0]` low |

### What the bus does to N2 and N3

The bus line and whatever loads it become part of the membrane capacitance of N2 and N3, so the firing rate
follows 1 / (10 pF + C_bus). N2 (pA) at code 6: 7.2 Hz with the 3 pF bus line alone, 4.1 Hz with 10 pF
more, 2.2 Hz with 30 pF, 0.84 Hz with 100 pF (exponent -0.99; post-layout 6.96 / 4.01 / 2.17 / 0.83 Hz,
exponent -0.98). N3 (nA) at code 6: 3.9 kHz on the bare bus, 0.5 kHz with 100 pF, 55 Hz with 1 nF, 5.6 Hz
with 10 nF (exponent -0.99; post-layout 3.79 kHz, 485 Hz, 54.8 Hz, 5.56 Hz), and 0.64 Hz with 100 nF, where
its reset is incomplete (above). On the bare bus the refractory time takes a tenth of the period, so the
rate there is about 10 % below the 1/C line through the nF points.
N0 and N1 stay at 9.3 Hz (post-layout 9.0 Hz).
Figure: [`testbenches/ngspice/results/busload.png`](testbenches/ngspice/results/busload.png); all results in
[`docs/SUMMARY.md`](docs/SUMMARY.md).

N3 on `analog_bus2` (`dig_in` 22 / 23; N2 at code 5 on the bare bus, N3 at code 7 with 10 nF on its own):
uncoupled they fire at 6.18 and 6.37 Hz. The weak leg (W/L 0.3/10, about 0.1 MOhm) lets N3's 80 nA onto
bus2. N2 has the lower threshold (0.66 V against 0.92 V) and fires first, at 33 Hz, and its resets
drain N3, which stops firing and hovers at 0.48 to 0.66 V: N2 speaks for N3. The strong leg locks the two
1:1 at 8.8 Hz (vector strength 1.00, with or without 30 pF on bus2).

In the harness the bus switch itself sets the load: open, a slot bus carries about 0.5 pF; closed, it carries
about 9 pF on chip (its own switch, the 17 other slots' switches and the pad) plus the shared wiring and the
board. The closed bus also carries the leakage of the pad and of the other switches, of the order of the
pA membrane currents; with the PDK pad model as it is (0.1..0.36 nA), N2 stops, while N3 slows by 0.25 %
(10 nF, code 6) to 2.6 % (20 pF, code 0). Details and how the chip measures both:
[`testbenches/harness_bus/results.md`](testbenches/harness_bus/results.md).

### Controls

`dig_in` (1.2 V, from the harness registers):

| bits | function |
|---|---|
| 3:0 | N0 tuning code |
| 7:4 | N1 tuning code |
| 11:8 | N2 tuning code |
| 15:12 | N3 tuning code |
| 16, 17 | synapse N0 -> N1, weak / strong leg |
| 18, 19 | synapse N1 -> N0, weak / strong leg |
| 20, 21 | gap junction N0 <-> N1, weak / strong leg |
| 22, 23 | N3 -> `analog_bus2` (coupling N3 to N2 through the bus), weak / strong leg |

`dig_in` = 0 (the harness default) leaves N0..N2 blinking at about 1 Hz and N3 humming at 470 Hz on its
bare bus (0.67 Hz with 10 nF on it), uncoupled except through the buses' own capacitance.

Analog coupling voltages (pulled up on chip, so an open input means full coupling):

| variant | `vcpla` (gap junction N0 <-> N1) | `vcplb` (bus pass gates, N3 -> bus2) |
|---|---|---|
| `bbl_slot_shared` (shared pins only, any slot) | `vbias` (harness voltage bias) | internal |
| `bbl_slot_pads` (two dedicated analog pads) | `s<N>_an_0_esd` | `s<N>_an[1]` |

`vcplb` also sets how much of its bus N3 sees (code 0, 10 nF on `analog_bus3`): 0 V cuts it off (about
600 Hz on its own membrane), 0.8 / 1.2 V let the bus in partly (1.62 / 0.87 Hz), 3.3 V fully (0.67 Hz).

Supplies: `vdd_3v3` / `vss_3v3` (everything), `vdd_1v2` / `vss_1v2` (enable inverter, tie-lows).
`enable` = 0 turns the reference off (2 pA).

### On the board

Each analog bus goes to an LED through an ultra-high-impedance amplifier (input leakage well below 1 pA,
input capacitance a few pF): N0..N2 charge their membranes with 8..139 pA, so a scope probe or a
10 MOhm load on `analog_bus2` stops N2. A bus is high for about 10 us per spike: 3.3 V for N0/N1;
2.0 V for N2 on an unloaded bus, 1.2 V with 30 pF, 0.9 V with 100 pF. The amplifier has to stretch that
pulse to make it visible. The spikes of N2 reach the bus only with `vcplb` high (the open-input default);
at 0.8 to 1.2 V the pass gate clips them, while the bus still loads the membrane.

`analog_bus3` carries N3's sawtooth, 0 to 0.92 V with a sharp reset at every spike: at audio rates with
nothing on it (a speaker amplifier makes it heard, 0.5 to 9 kHz over the codes), at blinking rates with
an external capacitor (10 nF: 0.67 to 12.8 Hz over the codes; 6 nF for about 1 to 20 Hz), which should be a
low-leakage type (C0G or film): N3 tolerates nA of leakage, but every nA shifts its rate. A 10 MOhm scope
probe sinks 92 nA at N3's threshold (0.92 V), more than N3's charging current up to code 11 (6.1 nA + 7.4 nA
per step): it stops N3 there and slows it severely above. Watch the bus through a buffer with pA input
current, as for N2.

Close the harness's bus switches for the buses in use; the shared variant also needs the harness voltage bias
on `vbias` only if a gap junction strength other than "full" is wanted.

## Repository

| path | content |
|---|---|
| `netlist/source/bbl.spice`, `bbl_slot.spice` | source netlist (source of truth) |
| `netlist/cdl/` | `mkcdl.py` and the LVS netlist `bbl.cdl` |
| `netlist/pex/` | kpex 2.5D extracted netlists of both slot variants |
| `schematic/xschem/` | xschem sheets and symbols, checked by `check_sheets.py` (xschem netlist vs source, device by device). `bbl_neuron`, `bbl_syn`, `bbl_bias`, `bbl_dac`, `bbl_gap` are drawn by hand (laid out like the original spike1.asc for the neuron); the hierarchical sheets, the symbols and the testbench `tb_bbl_slot_shared.sch` come from `gen_sheets.py`, which leaves the hand-drawn sheets alone |
| `schematic/png/` | renders of all sheets |
| `layout/scripts/` | layout generator (KLayout Python, IHP PCells): `build.py` (cells), `build_slot.py` (slots) |
| `layout/gds/` | `bbl_cells.gds`, `bbl_slot_shared.gds`, `bbl_slot_pads.gds` |
| `final/gds/` | `slot_3.gds`, the file the harness takes (pads variant in the slot 3 frame, see below) |
| `verification/` | DRC reports (`drc/`), LVS logs, extracted netlists and lvsdb (`lvs/`), kpex logs (`pex/`) of both variants and of `slot_3` (DRC, LVS) |
| `testbenches/ngspice/` | `bbltb.py` (testbench builder), `campaign.py` (all simulation cases), `plots.py`; `results/` |
| `testbenches/harness_bus/` | capacitance and leakage of the harness bus switch and pad (`buscap.py`, `padiv.py`), N2/N3 with the pad on their buses (`padtest.py`); `results.md` |
| `docs/` | run log, summary, chat log |

### Rebuild and check

```bash
export PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l KLAYOUT_PATH=$PDK_ROOT/$PDK/libs.tech/klayout
```

```bash
python3 layout/scripts/build.py layout/gds && python3 layout/scripts/build_slot.py <harness>/gds layout/gds
```

```bash
python3 netlist/cdl/mkcdl.py netlist/cdl/bbl.cdl netlist/source/bbl.spice netlist/source/bbl_slot.spice
```

```bash
python3 $KLAYOUT_PATH/tech/drc/run_drc.py --path=layout/gds/bbl_slot_shared.gds --topcell=bbl_slot_shared --no_density
```

```bash
python3 $KLAYOUT_PATH/tech/lvs/run_lvs.py --layout=layout/gds/bbl_slot_shared.gds --netlist=netlist/cdl/bbl.cdl --topcell=bbl_slot_shared --run_mode=deep --disable_tap_extraction
```

```bash
kpex extract --pdk ihp-sg13cmos5l --gds layout/gds/bbl_slot_shared.gds --schematic netlist/cdl/bbl.cdl --cell bbl_slot_shared --2.5D --mode CC
```

```bash
cd schematic/xschem && python3 gen_sheets.py && python3 check_sheets.py
```

```bash
cd testbenches/ngspice && python3 campaign.py --tag sch && python3 plots.py sch
```

### Slot 3, and moving to another slot

The chip gets `final/gds/slot_3.gds`: top cell `slot_3`, the pads variant in the frame of
`slot3_wrapper` (`vcpla` on `s3_an_0_esd`, `vcplb` on `s3_an[1]`). The harness (`scripts/get_project_gds.sh`)
looks for `slot_<N>.gds` in `final/gds/`, then `gds/`, then anywhere in the repository, reads it read-only and
renames every cell below the top cell, so only the top cell name has to match the slot. Slot 3's frame has a
second `vss_3v3` pin (a Metal2 strip on the right edge, the same port as the TopMetal1 pin on the left;
slot 12 has one too); `build_slot.py` ties it to the ground straps with a via stack.

To move to slot N:

1. Pads. The pads variant needs `s<N>_an[0]` and `s<N>_an[1]` to be `sg13cmos5l_IOPadAnalog` in the
   harness's `config.txt` (in the 2026-11 config: slots 1, 2, 3, 5, 9, 10, 12, 14, 16, 18). `build_slot.py`
   reads the pad types from `config.txt` and refuses other slots. Every slot can take the shared variant
   (`vcpla` on `vbias`, `vcplb` on chip, pulled up).
2. Build and check (from the repository root; `pads` or `shared`):
   ```bash
   python3 layout/scripts/build_slot.py <harness>/gds final/gds <N> pads
   ```
   ```bash
   python3 netlist/cdl/mkcdl.py netlist/cdl/bbl.cdl netlist/source/bbl.spice netlist/source/bbl_slot.spice --slot <N> pads
   ```
   ```bash
   python3 $KLAYOUT_PATH/tech/drc/run_drc.py --path=final/gds/slot_<N>.gds --topcell=slot_<N> --no_density --run_dir=verification/drc/slot_<N>
   ```
   ```bash
   python3 $KLAYOUT_PATH/tech/lvs/run_lvs.py --layout=final/gds/slot_<N>.gds --netlist=netlist/cdl/bbl.cdl --topcell=slot_<N> --run_mode=deep --disable_tap_extraction --run_dir=verification/lvs/slot_<N>
   ```
3. Delete `final/gds/slot_3.gds` and `verification/*/slot_3/`, so that exactly one `slot_<N>.gds` is left;
   update the slot number in this README and in `docs/SUMMARY.md` (file list with sha256).
4. On the harness side (its maintainer; this repository does not change the harness): `s<N>_source` in
   `config.txt` = this repository, `s<N>_version` = branch `main` and the commit to tape out, `slot_<N>` = the
   designer. With the pad types unchanged, the padframe is not rebuilt.
5. The slot frames differ only in pin names (`s<N>_...`), the positions of the dedicated pad pins on the
   right edge and extra supply pins; `build_slot.py` takes all of them from `slot<N>_wrapper.gds`. Slots that
   the chip places mirrored are mirrored by the harness. `bbltb.slot_dut` maps the pins of any slot for
   post-layout simulation of an extracted `slot_<N>`.

## Simulation notes

- Models: IHP PSP 103 (OSDI) in ngspice-47; typical corner, 27 C unless stated.
- The analog buses: the harness bus switch, closed, in front of the bus line (3 pF in all for trunk, pad and
  bond, plus the external load of each case). On `analog_bus2/3`, where the bus is part of a membrane, the
  switch is 10 Ohm (3.5 to 17 Ohm extracted) and 0.5 pF of the bus sits on its slot side (the switch's own
  diffusion). On `analog_bus0/1`, which only show the spikes of the buffered N0/N1, 10 Ohm stalls the solver
  at the inverter's edges; there the switch is 2 kOhm with all of the capacitance on the bus side, the model
  used before 2026-11-09 for every bus (N0/N1 rates agree with either to 0.02 %). Some cases ran with
  intermediate versions of this model (differences up to 0.02 %, [`docs/RUNLOG.md`](docs/RUNLOG.md) rows 84
  ff.); `vcplb_0.0` (pass gates off, slot side of the buses floating) uses 2 kOhm and 0.5 pF on every bus.
- The transient solver: every regenerative loop has a spurious second solution in an implicit time step
  longer than C dV / I of its feedback transistor. With XM3 at full strength (1/0.45) that is about 20 ns,
  and during another neuron's spike Newton occasionally landed there: neurons "fired" through disabled gap
  junctions that carry femtoamperes. Limiting XM3 to about 8 uA (which is R4 of the original) moves the limit
  to about 1 us; the disabled-coupling rates then agree with the uncoupled ones to 0.3 %.
  Occasional "timestep too small" aborts remain, more often since N3 resets nanofarads within microseconds;
  the testbench retries those runs once with half the maximum step and, if both attempts stop, takes the rates
  from the longer one when it covers at least half of the analysis window (`partial` in the results). A
  spurious early spike also still occurs, about once in 15 runs (N0 and/or N1 fire once too early): the
  rates of free-running neurons in the figures and tables are therefore one over the median spike interval;
  the coupling cases give mean rates.
- Spike detection: in the schematic from the neurons' `out` nodes, N3 from the resets of its membrane
  (falling through 0.45 V; its `out` dips for nanoseconds only); post-layout (no internal node names) from
  the bus voltages: N3 from the resets of `analog_bus3`, the others as the start of a fast upstroke (rise of
  more than 0.15 V within 100 us). A level threshold
  misses the spikes of a bus-coupled neuron on a loaded bus, whose pulse peaks at 0.9 V with 100 pF, barely
  above the 0.7 V the membrane ramps to between spikes. Both detectors agree in every schematic case in which
  the spike reaches the bus (all but `vcplb` 0 / 0.8 / 1.2 V).
  `campaign.py --reanalyze` recomputes the results from the saved waveforms.
