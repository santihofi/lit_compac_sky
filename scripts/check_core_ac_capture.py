#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Match exported core AC curves to independently captured gain and bandwidth."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from check_chipify_results import audit


def check_curve(data, prefix, gain, bandwidth_mhz):
    frequency = data["frequency"].to_numpy()
    magnitude = data[prefix + "_mag"].to_numpy()
    if not np.all(np.diff(frequency) > 0) or not np.all(magnitude > 0):
        raise ValueError("AC curve has a nonmonotonic scale or nonpositive magnitude")
    db = 20 * np.log10(magnitude / magnitude[0])
    crossing = np.flatnonzero((db[:-1] > -3) & (db[1:] <= -3))
    if len(crossing) == 0:
        raise ValueError("AC curve has no downward 3 dB crossing")
    i = crossing[0]
    measured = (frequency[i] + (-3 - db[i]) *
                (frequency[i+1] - frequency[i]) / (db[i+1] - db[i])) / 1e6
    if not np.isclose(magnitude[0], gain, rtol=5e-5):
        raise ValueError(f"{prefix} gain {magnitude[0]} differs from scalar {gain}")
    if not np.isclose(measured, bandwidth_mhz, rtol=5e-5):
        raise ValueError(f"{prefix} bandwidth {measured} differs from scalar {bandwidth_mhz}")
    return abs(measured / bandwidth_mhz - 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("datasheet", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    integrity = audit(args.datasheet, args.out, False)
    spec = yaml.safe_load(args.datasheet.read_text())
    meta_path = max((args.out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime)
    meta = json.loads(meta_path.read_text())
    directory = Path(meta["analysis_dirs"]["ac"])
    if not directory.is_absolute():
        directory = args.out / directory
    frame = pd.read_csv(args.out / "simulation_results.csv", dtype={"run_id": str})
    checked = 0
    max_error = 0
    for tb, test in spec["tests"].items():
        if test.get("ac_signals") != ["ac1.gd", "ac2.gd"]:
            continue
        for _, row in frame.iterrows():
            wave = pd.read_csv(directory / f"run_{row.run_id}__{tb}.csv")
            for number in [1, 2]:
                error = check_curve(wave, f"ac{number}.gd", row[f"acgain_in{number}"],
                                    row[f"bw_in{number}_mhz"])
                max_error = max(max_error, error)
                checked += 1
    if not checked:
        raise ValueError("No supported core AC capture declarations found")
    print(json.dumps({"status": "valid", "cases": integrity["cases"],
                      "anchored_curves": checked,
                      "maximum_relative_bandwidth_difference": max_error}))


if __name__ == "__main__":
    main()
