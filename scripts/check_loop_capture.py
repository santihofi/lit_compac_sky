#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Anchor captured return ratios to independently exported ngspice margins."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from check_chipify_results import audit


def margins(wave, prefix="ac2.tloop"):
    frequency = wave["frequency"].to_numpy()
    magnitude = wave[prefix + "_mag"].to_numpy()
    phase = np.rad2deg(np.unwrap(np.deg2rad(wave[prefix + "_phase"].to_numpy())))
    if not np.all(np.diff(frequency) > 0) or not np.all(magnitude > 0):
        raise ValueError("Nonmonotonic frequency or nonpositive loop magnitude")
    db = 20 * np.log10(magnitude)
    crossings = np.flatnonzero(((db[:-1] >= 0) & (db[1:] < 0)) |
                              ((db[:-1] < 0) & (db[1:] >= 0)))
    candidates = []
    for i in crossings:
        fraction = db[i] / (db[i] - db[i+1])
        candidates.append((180 + phase[i] + fraction * (phase[i+1] - phase[i]),
                           frequency[i] * (frequency[i+1] / frequency[i]) ** fraction))
    pm, fu = min(candidates) if candidates else (999, 0)
    if (not len(crossings) and db[0] > 0) or np.cos(np.deg2rad(phase[0])) < 0:
        pm = -999
    crossing180 = np.flatnonzero((phase[:-1] > -180) & (phase[1:] <= -180))
    gm_db, f180 = 999, 0
    if len(crossing180):
        i = crossing180[0]
        fraction = (phase[i] + 180) / (phase[i] - phase[i+1])
        gm_db = -(db[i] + fraction * (db[i+1] - db[i]))
        f180 = frequency[i] * (frequency[i+1] / frequency[i]) ** fraction
    return dict(pm=pm, fu=fu, gm_db=gm_db, f180=f180, t0_db=db[0],
                ncross=len(crossings))


def check(sheet, out):
    integrity = audit(sheet, out)
    meta = json.loads(max((out / "history").glob("*.meta.json"),
                         key=lambda p: p.stat().st_mtime).read_text())
    directory = Path(meta["analysis_dirs"]["ac"])
    if not directory.is_absolute():
        directory = out / directory
    frame = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
    archive = {}
    for _, row in frame.iterrows():
        wave = pd.read_csv(directory / f"run_{row.run_id}__stability.csv")
        measured = margins(wave)
        for name, value in measured.items():
            if not np.isclose(value, row[name], rtol=5e-5, atol=1e-4):
                raise ValueError(f"{row.run_id}: {name} curve={value}, scalar={row[name]}")
        archive[row.run_id] = wave.to_numpy()
        archive["columns"] = wave.columns.to_numpy(dtype=str)
    return {"status": "valid", "cases": integrity["cases"],
            "anchored_loop_curves": len(frame)}, archive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("datasheet", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    result, _ = check(args.datasheet, args.out)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
