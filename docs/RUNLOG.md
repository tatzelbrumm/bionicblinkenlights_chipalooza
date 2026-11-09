<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Run log: Bionic Blinkenlights slot for the Chipalooza sg13cmos5l harness

Cloud session, 2026-11-08 / 09 (times UTC, taken from the session transcript). Repositories: this one
(`/home/user/bionicblinkenlights_chipalooza`, branch `main`), the harness `tatzelbrumm/sg13cmos5l_ocd_chipalooza`
(read only, `/home/user/sg13cmos5l_ocd_chipalooza`), `tatzelbrumm/claude-cloud-config` (environment, read only).
Scratch work in the session scratchpad (not committed); `S` below is that scratchpad.

## Tool versions (once)

| tool | version |
|---|---|
| ngspice | ngspice-47 (`/foss/tools`, claude-cloud-config archive) |
| xschem | 3.4.8RC |
| KLayout | 0.30.12 (Debian package and Python module) |
| klayout-pex | 0.6.8 (2.5D engine) |
| magic / netgen | 8.3.685 / 1.5.324 (not used for the checks) |
| PDK | `/foss/pdks/ihp-sg13cmos5l` (IHP-Open-PDK iic-jku fork `df4c5054`), OSDI models of the archive |
| Python | 3.13 (`psutil` installed for the PDK PCell library) |

## Steps

| # | time | cwd | command / action | exit | log / output | result |
|---|---|---|---|---|---|---|
| 1 | 21:56 | `/foss` | read `/foss/setup.log` | 0 | — | setup script stopped after `APT_OK`: no `PIP_OK`, `OSDI_OK`, `CACE_OK`, `SETUP_DONE` |
| 2 | 21:57 | `/` | the missing steps of `setup-cloud.sh` by hand: OSDI copy, tool symlinks, `pip install klayout==0.30.12 klayout-pex==0.6.8`, kpex wrapper | 0 | — | tools on `PATH`; CACE not installed (not used) |
| 3 | 21:57 | harness | read `README`, `config.txt`, `gds/slot*_wrapper.gds` | 0 | — | slot 537.15 x 273 um; shared pins identical in all 18 wrappers; 2-pad slots 1, 2, 3, 6, 7, 12, 13, 16, 17, 18 |
| 4 | 21:58 | — | fetch `cmucsd.bitbucket.io` (agent, then `curl`) | fail | proxy 403 | host not in the environment's allowlist |
| 5 | 21:58 | — | environment `sg13cmos5l`: host `cmucsd.bitbucket.io` added (`update_environment`, approved) | 0 | — | — |
| 6 | 21:59 | `S/bb` | `curl` index, img7, img8, img11, img12, `spike1.asc`, PNGs | 0 | — | Q1..Q4 2N3904/2N3906, R1 330, R2 10k, R3 100k, R4 10k, R5 33k, C1 100u, C2 2u, Vdd 3 V |
| 7 | 21:59 | harness | `verilog/rtl/chipalooza_frame.v`: analog bus, bias and switch wiring | 0 | — | buses: per-slot switches to the shared pads |
| 8 | 21:59–22:01 | — | questions to Christoph; answers: generic 2-pad slot and a no-pad variant, coupling digital and analog, LED amplifier off chip, 3.3 V devices; later: self-biased minimal neurons, fast spikes fine | — | — | — |
| 9 | 22:01–22:08 | `S` | read the conventions of `sg13cmos5l_cm_slot7`, `sg13cmos5l_cm_ip__single2diff2single` (`CLAUDE.md`, `docs/traps.md`, `docs/record-keeping.md`), notes branch `sudel_buecher` (`verbatim-chatlog-export.md`, `chatlog_tools/`); skill `xschem-analog-schematic` loaded | 0 | — | record keeping and LVS conventions taken over |
| 10 | 22:07 | `S/sim` | ngspice: HV Vgs = 0 leakage, gate capacitance | 0 | — | 3..60 fA/um (L 10..0.45 um); 4.4 fF/um2 in inversion |
| 11 | 22:11 | `S/sim/n1` | neuron v0 (bias-current stand-ins) | 0 | `neuron_v0.sp` | oscillates, 7 Hz; spike < 1 ms |
| 12 | 22:14 | `S/sim/n1` | neuron v1 (slow node from a 1 nA bias) | 0 | `v1.png` | latches: slow node stuck at 3.25 V |
| 13 | 22:15 | `S/sim/n1` | `dc_dev.py`: subthreshold mirror ratios vs W, L | 0 | — | NMOS 0.8..1.8x, PMOS 0.9..2.4x of the W/L ratio; v1 resized: 2.3 Hz/nA, spike 8 ms |
| 14 | 22:18 | `S/sim/n1` | `tbb.py`: beta-multiplier reference, start-up, enable | 0 | — | starts from leakage in 9 ms; disabled 2 pA |
| 15 | 22:19–22:21 | `testbenches/ngspice` | first `bbl.spice`; `t_first.py` | 0 | `out/first.*` | all four fire; static 117 nA |
| 16 | 22:22–22:26 | `S/sim/n1` | minimal neuron: R1, R5 PMOS gate on vss, R2 NMOS gate on vdd, R4 merged into M3, only R3 biased | 0 | `run4.py`, `v4_zoom.png` | 1.72 Hz/nA, spike 5 us; 20 pF on the membrane halves f |
| 17 | 22:27 | repo | `bbl.spice` rewritten (minimal neuron, DAC, gap junctions, pulse synapses, bias) | — | — | — |
| 18 | 22:28–22:29 | `layout/scripts` | PDK PCells in the KLayout Python module (`pdk.py`: `pya` shim, `psutil`) | 0 | — | `SG13_dev`: nmosHV, pmosHV, rhigh, ptap1, ntap1, ... |
| 19 | 22:30–22:39 | `testbenches/ngspice` | tuning runs; "timestep too small"; stale `.dat` reread (fixed: outputs deleted before each run); `uic` replaced by a 100 us supply ramp | abort | `out/tune_*.log` | — |
| 20 | 22:31–22:58 | `testbenches/ngspice` | option matrices (reltol, gmin, trtol, itl4, rshunt, method), bisection by subcircuit | mixed | `S/tb_debug/` | the pulse synapses (floating nodes kicked by out) trigger the aborts |
| 21 | 22:37 | `testbenches/ngspice` | synapse internal nodes during a spike | 0 | — | floating synapse node bootstraps to 4.4 V and kicks the presynaptic out: real design flaw |
| 22 | 23:04 | repo | synapse rewritten (3.3 V NAND of spk and en drives one long PMOS into the membrane); 2.2 pF on vcpla, vcplb | 0 | `out/bis2_*` | full core converges at 0.1 ms steps |
| 23 | 23:07–23:10 | repo | layout-friendly sizing (ng instead of m, DAC on a 2.5 nA reference, C1 10 pF, rhigh meander) | — | — | — |
| 24 | 23:09–23:20 | `testbenches/ngspice` | leak resistors, cshunt, 10 us steps | mixed | — | only a 10 us max step converges (10 min per 3 s) |
| 25 | 23:11–23:17 | repo | `lay.py`, `build.py`; DRC per cell (`verification/drc/run_drc_cells.sh`) | 0 | `S/drc_*` | first run: off-grid taps, M1.d, M3.d; after fixes all 9 cells 0 violations |
| 26 | 23:19–23:20 | repo | LVS `bbl_unit` (`run_lvs.py --run_mode=deep`); `mkcdl.py` (X -> M/R); `--disable_tap_extraction` | fail, 0 | `S/lvs_unit` | vdd/vss short (rail stubs at the same x) fixed; schematic not read as X lines (CDL needed); then match |
| 27 | 23:21–23:27 | repo | `build_slot.py` (frame `slot1_wrapper.gds`, trunk band, Metal4 columns, TopMetal1 straps); LVS both slots | fail, 0 | `S/lvs_*` | rhigh `l` (41.055 um) and `ps` (0.18 um) to the CDL; then both match |
| 28 | 23:27 | repo | DRC both slots | 0 | `S/drc_slot` | 0 violations, 0 exceptions |
| 29 | 23:28 | repo | branch `main` created, commit `6c9a972`, `git push -u origin main` | 0 | — | — |
| 30 | 23:29–23:31 | repo | kpex 2.5D (`--mode CC`) both slots | 0 | `netlist/pex/` | about 2250 coupling capacitors each, 1 min per slot |
| 31 | 23:36–23:41 | `schematic/xschem` | `gen_sheets.py`, `check_sheets.py` (xschem netlist vs source, device by device) | 0 | `netlist_check/` | stub collisions and a bias short found and fixed (vertical occupancy routing); 0 mismatches in 11 sheets; testbench sheet |
| 32 | 23:39–23:46 | `testbenches/ngspice` | campaign: aborts at the reset of a bus-coupled neuron | abort | `out/sch/*.log` | minimal repro (one neuron + pass gate + bus) runs clean |
| 33 | 23:46 | repo | `build_slot.py <harness>/gds <out> 18 pads`, `mkcdl.py --slot 18 pads`, LVS | 0 | `S/slotN` | slot_18 match |
| 34 | 23:49 | `testbenches/ngspice` | internal nodes during a spike of N0 | 0 | — | N1 jumps 0.07 -> 1.6 V in one 90 ns step: spurious solution of the regenerative loop |
| 35 | 23:51 | repo | commit `941e790` (sheets, PEX, slot_N), push | 0 | — | — |
| 36 | 23:51–00:10 | `testbenches/ngspice` | trtol, reltol, 2 us steps, bias decoupling, removal of coupling blocks | 0 | `S/tb_debug/` | with the gap junctions removed the rates are the uncoupled ones; disabled gap junctions (fA) "couple" numerically |
| 37 | 00:10–00:14 | `testbenches/ngspice` | XM3 current-limited (0.3/4 um, R4 back), C2 2.6 pF | 0 | `out/m3*` | N1/N0 1.117 (expected 1.118), N3/N2 1.094 (1.095); bus pulse 2.4 V |
| 38 | 00:18 | repo | netlist and layout updated, layouts rebuilt; LVS both slots; sheets regenerated and checked | 0 | — | match, match; 0 mismatches |
| 39 | 00:18–00:22 | repo | final DRC both slots; kpex both slots | 0 | — | 0 / 0 violations, 0 exceptions; 2245 / 2253 capacitors |
| 40 | 00:18 | `testbenches/ngspice` | `campaign.py --tag sch --jobs 3` (29 cases) | — | `out/sch/` | first results consistent (tuning, 3 / 10 pF bus load) |
| 41 | 00:22 | `testbenches/ngspice` | `campaign.py --include netlist/pex/bbl_slot_pads.pex.spice --tag pex --jobs 1 --tstop 1.5` (12 cases) | — | `out/pex/` | tune_0_1_2_3: 1.52, 2.06, 2.98 Hz (schematic 1.58, 2.14, 3.07) |
| 42 | 00:24 | repo | commit `52a174b` (current-limited M3, reports, README, run log), push | 0 | — | — |
| 43 | 00:44 | `testbenches/ngspice` | busload_30p: N2, N3 stuck at vm 0.7 V, out 2.5 V | — | `out/sch/busload_30p.dat` | with the current-limited M3 the upstroke is slow, and the reset path (slow follows out) engages at the same out level: a stable intermediate state. Both campaigns stopped |
| 44 | 00:45–00:50 | `S/sim/n1` | `run7.py`: M4, R2 sizes vs bus load 3 / 33 / 103 pF | 0 | — | strong R2: no stuck state but incomplete resets (f does not scale with C); no size fixes it |
| 45 | 00:50 | `S/sim/n1` | `run8.py`: R5 split (XMR5A nmos 0.3/100 gate vdd: fast discharge; XMR5B pmos 0.3/4 gate vin: slow recharge = refractory time) | 0 | — | complete resets at every load; 10 nA: 21.25 / 6.48 / 2.47 Hz for 3 / 33 / 103 pF (1/C prediction 6.42, 2.44) |
| 46 | 00:52 | repo | netlist, layout, sheets updated; slots rebuilt; LVS both; `check_sheets.py` | 0 | — | match, match; 0 mismatches |
| 47 | 00:53 | `testbenches/ngspice` | `campaign.py --tag sch --jobs 3` (30 cases, with tune_low 5 s) | — | `out/sch/` | see SUMMARY |
| 48 | 00:54 | repo | final DRC and kpex both slots, then the post-layout campaign (12 cases, 1.5 s) | — | `verification/`, `out/pex/` | see SUMMARY |
| 49 | 01:00 | repo | commit `746af5a` (R5 split, final DRC/LVS/PEX), push | 0 | — | — |
| 50 | 01:03 | `schematic/xschem` | agent started (Christoph's question): hand-redraw of the leaf sheets with the skill `xschem-analog-schematic`, checks `check_sheets.py` and `sheet_equiv.py` | — | — | see below |
| 51 | 01:18 | `testbenches/ngspice` | campaign results (9 cases): code 1..13 1.56..15.49 Hz unloaded; code 0 fires every 3 s (0.3 Hz); code 15 about 18 Hz | — | `out/sch/` | below the 1..20 Hz spec at both ends |
| 53 | 01:03–01:37 | `schematic/xschem` | agent (step 50) done: `bbl_neuron` (laid out like spike1.asc, original part names tagged), `bbl_syn`, `bbl_bias`, `bbl_dac`, `bbl_gap` redrawn by hand; `check_sheets.py` OK for all 11 sheets; `sheet_equiv.py` (Christoph's) equivalent for all 10 compared sheets once the reference carries the two new sizes of step 52; placement scripts in `S/hand/` (not committed); `gen_sheets.py` now skips the hand-drawn sheets | 0 | `S/sheets_ref`, `S/sheets_ref_sized` | renders in `schematic/png/` |
| 54 | 01:40 | — | Christoph away; the remaining steps run unattended in `S/finish.sh` (one approval): wait for the campaigns, plots, sheet check, chat log, commits and pushes every 2 min | — | `S/finish.log` | — |
| 52 | 01:19 | repo | recalibration: XMLP 0.3/8 -> 0.3/7 (DAC reference +14 %), XMH 0.3/9 -> 0.3/3.2 (base leg 0.75 unit); layouts rebuilt; LVS both | 0 | — | match, match; campaigns restarted (`--tag sch --jobs 3`; DRC, kpex, then `--tag pex`) |
