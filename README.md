<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Bionic Blinkenlights for the Chipalooza sg13cmos5l harness

Four spiking neurons for one slot of the Chipalooza analog harness
([`tatzelbrumm/sg13cmos5l_ocd_chipalooza`](https://github.com/tatzelbrumm/sg13cmos5l_ocd_chipalooza)), IHP
**sg13cmos5l**, 3.3 V thick-oxide devices. They are a CMOS translation of the 4-transistor integrate-and-fire
neuron of [Bionic Blinkenlights](https://cmucsd.bitbucket.io/bionicblinkenlights/index.html) (neuron:
img7.html, schematic: img8.html, demos: img11.html and img12.html). The neurons fire at about 1 to 20 Hz, are
coupled through tunable synapses, gap junctions and the harness analog buses, and show their spikes on the
four analog buses, where an off-chip ultra-high-impedance amplifier drives an LED per bus.

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
| R3 | XMR3 pmos 0.3/30, gate on vin | the only biased one: 4..150 pA from the tuning DAC |
| C1 | XC1 pmos gate capacitor, 10 pF | membrane |
| C2 | XC2 nmos gate capacitor, 2.6 pF | slow node |

The spike is a few microseconds long (fast spikes; the LED amplifier stretches them). The membrane, and with
it the bus of a bus-coupled neuron, rises by up to about 2 V during the spike (1.2 V with 30 pF on the bus,
0.9 V with 100 pF). Between spikes the neuron draws no static current; the whole slot draws 0.37 to 0.48 uA
from `vdd_3v3` (simulated average, all codes 0 to codes 12..15).

## The slot (`bbl_core`)

| block | what |
|---|---|
| `bbl_bias` | self-biased reference: subthreshold beta multiplier (K = 8, rhigh 1.2 MOhm), about 45 nA per branch; start-up by Vgs = 0 leakage; `enable` gates it; 2.5 nA reference `vbnl` for the DACs; weak pull-ups for the coupling voltages |
| `bbl_unit` x 4 | neuron + 4-bit tuning DAC (`bbl_dac`); f rises about linearly with the code: 1.2 Hz at code 0, 1.3 Hz more per step (buffered neuron) |
| N0, N1 | buffered: inverters drive `analog_bus0` / `analog_bus1` high while they fire, so bus load does not affect them. Pulse synapses N0 -> N1 and N1 -> N0 (`bbl_syn`, the photoresistor of the demos), gap junction N0 <-> N1 (`bbl_gap`) |
| N2, N3 | membranes on `analog_bus2` / `analog_bus3` through NMOS pass gates (gate `vcplb`): the bus line's own capacitance and whatever loads the bus become part of the membrane capacitance. N3 can also be connected to `analog_bus2`, which couples it to N2 through the bus |
| `bbl_tielo` | holds `dig_out[11:0]` low |

### What the bus does to N2 and N3

The bus line and whatever loads it become part of the membrane capacitance of N2 and N3, so the firing rate
follows 1 / (10 pF + C_bus): at code 6, 7.2 Hz with the 3 pF bus line alone, 4.1 Hz with 10 pF more, 2.2 Hz
with 30 pF, 0.84 Hz with 100 pF (exponent -1.0; post-layout 2.18 Hz at 30 pF). N0 and N1 stay at 9.3 Hz.
Figure: [`testbenches/ngspice/results/busload.png`](testbenches/ngspice/results/busload.png); all results in
[`docs/SUMMARY.md`](docs/SUMMARY.md).

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

`dig_in` = 0 (the harness default) leaves every neuron blinking at about 1 Hz, uncoupled except through
the buses' own capacitance.

Analog coupling voltages (pulled up on chip, so an open input means full coupling):

| variant | `vcpla` (gap junction N0 <-> N1) | `vcplb` (bus pass gates, N3 -> bus2) |
|---|---|---|
| `bbl_slot_shared` (shared pins only, any slot) | `vbias` (harness voltage bias) | internal |
| `bbl_slot_pads` (two dedicated analog pads) | `s<N>_an_0_esd` | `s<N>_an[1]` |

Supplies: `vdd_3v3` / `vss_3v3` (everything), `vdd_1v2` / `vss_1v2` (enable inverter, tie-lows).
`enable` = 0 turns the reference off (2 pA).

### On the board

Each analog bus goes to an LED through an ultra-high-impedance amplifier (input leakage well below 1 pA,
input capacitance a few pF): the neurons charge their membranes with 4..150 pA, so a scope probe or a
10 MOhm load on `analog_bus2/3` stops N2/N3. A bus is high for about 10 us per spike: 3.3 V for N0/N1;
2.0 V for N2/N3 on an unloaded bus, 1.2 V with 30 pF, 0.9 V with 100 pF. The amplifier has to stretch that
pulse to make it visible. The spikes of N2/N3 reach the bus only with `vcplb` high (the open-input default);
at 0.8 to 1.2 V the pass gate clips them, while the bus still loads the membrane. Close the harness's bus
switches for the buses in use; the shared variant also needs the harness voltage bias on `vbias` only if a
gap junction strength other than "full" is wanted.

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
| `final/gds/` | the two slot variants as checked (`bbl_slot_shared.gds`, `bbl_slot_pads.gds`); a `slot_<N>.gds` for the slot assigned in the harness's `config.txt` is generated from them (see below) |
| `verification/` | DRC reports (`drc/`), LVS logs, extracted netlists and lvsdb (`lvs/`), kpex logs (`pex/`) of both variants |
| `testbenches/ngspice/` | `bbltb.py` (testbench builder), `campaign.py` (all simulation cases), `plots.py`; `results/` |
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

### A slot for the harness

The harness reads `slot_<N>.gds` with a top cell `slot_<N>`. `build_slot.py <harness>/gds <outdir> <N>
shared|pads` builds it in the frame of slot N (the pads variant only for the slots with two dedicated
analog pads: 1, 2, 3, 6, 7, 12, 13, 16, 17, 18), and `mkcdl.py ... --slot <N> shared|pads` writes its LVS
netlist.

## Simulation notes

- Models: IHP PSP 103 (OSDI) in ngspice-47; typical corner, 27 C unless stated.
- The analog buses are modelled as the harness bus switch (2 kOhm) in series with the bus line capacitance
  (3 pF assumed for trunk, pad and bond, plus the external load of each case).
- The transient solver: every regenerative loop has a spurious second solution in an implicit time step
  longer than C dV / I of its feedback transistor. With XM3 at full strength (1/0.45) that is about 20 ns,
  and during another neuron's spike Newton occasionally landed there: neurons "fired" through disabled gap
  junctions that carry femtoamperes. Limiting XM3 to about 8 uA (which is R4 of the original) moves the limit
  to about 1 us; the disabled-coupling rates then agree with the uncoupled ones to 0.3 %.
  Occasional "timestep too small" aborts at spike onsets remain; the testbench retries those runs once with
  a 5 us maximum step.
- Spike detection: in the schematic from the neurons' `out` nodes; post-layout (no internal node names) from
  the bus voltages, as the start of a fast upstroke (rise of more than 0.15 V within 100 us). A level threshold
  misses the spikes of a bus-coupled neuron on a loaded bus, whose pulse peaks at 0.9 V with 100 pF, barely
  above the 0.7 V the membrane ramps to between spikes. Both detectors agree in every schematic case in which
  the spike reaches the bus (all but `vcplb` 0 / 0.8 / 1.2 V).
  `campaign.py --reanalyze` recomputes the results from the saved waveforms.
