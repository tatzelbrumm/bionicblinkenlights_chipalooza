<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Run log: Bionic Blinkenlights slot for the Chipalooza sg13cmos5l harness

Cloud session, 2026-11-08 (UTC). Repositories: this one (`/home/user/bionicblinkenlights_chipalooza`), the
harness `tatzelbrumm/sg13cmos5l_ocd_chipalooza` (read only, `/home/user/sg13cmos5l_ocd_chipalooza`),
`tatzelbrumm/claude-cloud-config` (environment). Scratch work in the session scratchpad (not committed).

## Tool versions (once)

| tool | version |
|---|---|
| ngspice | ngspice-47 (`/foss/tools`, claude-cloud-config archive) |
| xschem | 3.4.8RC |
| KLayout | 0.30.12 (Debian package and Python module) |
| klayout-pex | 0.6.8 |
| magic | 8.3.685 |
| netgen | 1.5.324 |
| PDK | `/foss/pdks/ihp-sg13cmos5l` (IHP-Open-PDK iic-jku fork `df4c5054`) |

## Steps

| # | time | cwd | command / action | exit | log / output | result |
|---|---|---|---|---|---|---|
| 1 | 21:56 | `/foss` | read `/foss/setup.log` | 0 | — | setup script stopped after `APT_OK`: no `PIP_OK`, `OSDI_OK`, `CACE_OK`, `SETUP_DONE` |
| 2 | 21:57 | `/` | the missing steps of `setup-cloud.sh` by hand: OSDI copy, tool symlinks, `pip install klayout==0.30.12 klayout-pex==0.6.8`, kpex wrapper | 0 | — | tools on `PATH`; CACE not installed (not needed so far) |
| 3 | 21:58–22:05 | harness checkout | read `README`, `config.txt`, `gds/slot*_wrapper.gds`, `verilog/rtl/chipalooza_frame.v` | 0 | — | slot 537.15 x 273 um; shared pins identical in all 18 wrappers; pad pins differ |
| 4 | 22:00 | — | fetch `cmucsd.bitbucket.io/bionicblinkenlights` | fail | proxy 403 | host not in the environment's allowlist |
| 5 | 22:01 | — | environment `sg13cmos5l`: allowed host `cmucsd.bitbucket.io` added (approved by the user) | 0 | — | — |
| 6 | 22:02 | scratchpad `bb/` | `curl` index, img7, img8, img11, img12, `spike1.asc`, PNGs | 0 | — | 4-transistor neuron: Q1..Q4 2N3904/2N3906, R1 330, R2 10k, R3 100k, R4 10k, R5 33k, C1 100u, C2 2u, Vdd 3 V |
| 7 | 22:03 | scratchpad | user's questions answered: generic 2-pad slot and a no-pad variant; coupling digital + analog; LED amplifier off-chip; 3.3 V devices | — | — | — |
| 8 | 22:05–22:08 | scratchpad | read the conventions of `sg13cmos5l_cm_slot7`, `sg13cmos5l_cm_ip__single2diff2single` (`CLAUDE.md`, `docs/traps.md`, `docs/record-keeping.md`), notes branch `sudel_buecher` (`verbatim-chatlog-export.md`, `chatlog_tools/`) | 0 | — | record-keeping rules taken over |
| 9 | 22:11 | scratchpad `sim/` | ngspice: HV MOSFET Vgs = 0 leakage and gate-capacitance density | 0 | — | 3..60 fA/um (L 10..0.45 um); 4.4 fF/um2 in inversion |
| 10 | 22:13 | scratchpad `sim/n1` | neuron v0 (bias-current stand-ins for every resistor) | 0 | `neuron_v0.sp` | oscillates, 7 Hz; spike < 1 ms |
| 11 | 22:15 | scratchpad `sim/n1` | neuron v1 (slow-node sink/pull-up from a 1 nA bias) | 0 | `tb1.sp`, `v1.png` | latches: slow node stuck at 3.25 V (W = 0.3 um PMOS ratio 1.8x geometric) |
| 12 | 22:16 | scratchpad `sim/n1` | `dc_dev.py`: subthreshold mirror ratios vs W, L | 0 | — | NMOS 0.8..1.8x, PMOS 0.9..2.4x of W/L ratio |
| 13 | 22:17 | scratchpad `sim/n1` | neuron v1 resized (MR5a 0.3/2.5, MR5b 0.3/20) | 0 | `v2.png` | 2.3 Hz/nA, spike 8 ms |
| 14 | 22:18 | scratchpad `sim/n1` | `tbb.py`: beta-multiplier reference, start-up, enable | 0 | — | starts from leakage in 9 ms; off 2 pA; R 400 um rhigh chosen |
| 15 | 22:20 | `testbenches/ngspice` | `t_first.py` (first full core) | 0 | `out/first.*` | all 4 fire; static 117 nA (median), the 2.9 uA mean was sample-weighted |
| 16 | 22:31 | scratchpad `sim/n1` | user: neurons minimal; fast spikes fine. Neuron v3: R1, R5 PMOS gate to vss, R2 NMOS gate to vdd, R4 merged into M3, only R3 biased | 0 | `run4.py`, `v4_zoom.png` | 1.72 Hz/nA, spike 5 us; 20 pF on the membrane halves f; membrane + 20 pF reach 3.3 V in 1 us |
| 17 | 22:34 | `netlist/source` | `bbl.spice` rewritten (minimal neuron, DAC, gap junctions, pulse synapses, bias) | — | — | — |
| 18 | 22:35 | `testbenches/ngspice` | `t_tune.py` codes (0,5,10,15) and (1,2,4,8) | 0 / abort | `out/tune_*.log` | (1,2,4,8): 2.67, 4.21, 6.50, 12.66 Hz; (0,5,10,15) aborted at 1.095 s, "timestep too small" at bus0 (chgtol 1e-17) |
| 19 | 22:47 | `testbenches/ngspice` | options relaxed (reltol 1e-3, abstol 1e-14, default chgtol, rshunt 1e15), abort check added; DAC unit legs L 15 -> 20 um | — | — | rerun started |
