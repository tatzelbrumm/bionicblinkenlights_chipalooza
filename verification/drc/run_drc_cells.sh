#!/bin/bash
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Run the PDK KLayout DRC (no density) on every top cell of a GDS; summary per cell.
# usage: run_drc_cells.sh <gds> <outdir> <cell> [<cell> ...]
GDS=$(realpath "$1"); OUT=$2; shift 2
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=ihp-sg13cmos5l
export KLAYOUT_PATH=$PDK_ROOT/$PDK/libs.tech/klayout
DRC=$KLAYOUT_PATH/tech/drc/run_drc.py
mkdir -p "$OUT"
for c in "$@"; do
  ( python3 $DRC --path=$GDS --topcell=$c --run_dir=$OUT/$c --no_density > $OUT/$c.log 2>&1
    n=$(python3 - "$OUT/$c" <<'PY'
import sys, glob, xml.etree.ElementTree as ET
f = glob.glob(sys.argv[1] + '/*_full.lyrdb')
if not f:
    print('NO_REPORT'); sys.exit()
items = ET.parse(f[0]).getroot().find('items')
cats = {}
for it in items:
    k = it.find('category').text.strip("'"); cats[k] = cats.get(k, 0) + 1
print(sum(cats.values()), ' '.join(f'{k}:{v}' for k, v in sorted(cats.items())))
PY
)
    exc=$(grep -c -i "exception" $OUT/$c.log)
    echo "$c violations: $n exceptions: $exc" ) &
  while [ $(jobs -r | wc -l) -ge 3 ]; do sleep 1; done
done
wait
