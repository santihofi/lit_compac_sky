#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
set -euo pipefail
if [[ "${PDK:-}" != sky130A ]]; then
    echo "This wrapper requires PDK=sky130A, got ${PDK:-unset}." >&2
    exit 2
fi
if [[ $# == 0 ]]; then
    echo "Usage: with_sky130_ngspice.sh command [arguments...]" >&2
    exit 2
fi
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export SPICE_USERINIT_DIR="$script_dir/ngspice"
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MPLBACKEND=Agg
exec "$@"
