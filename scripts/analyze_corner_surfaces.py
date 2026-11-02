#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit every corner surface and separate product gain from shape error."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]


def fit_surface(data):
    x = data["v(vdin1)"].to_numpy()
    y = data["v(vdin2)"].to_numpy()
    z = data["outdiff"].to_numpy()
    if len(data) != 1681 or len(set(zip(x, y))) != 1681:
        raise ValueError("Expected 1681 unique coordinates")
    for axis in (x, y):
        if not np.allclose(np.unique(axis), np.linspace(-.1, .1, 41), atol=1e-12):
            raise ValueError("Wrong input sweep grid")
    matrix = np.column_stack([np.ones_like(x), x, y, x*y])
    coef = np.linalg.lstsq(matrix, z, rcond=None)[0]
    residual = z - matrix @ coef
    fullscale = abs(coef[3] * .01)
    if fullscale < 1e-9:
        raise ValueError("Product gain is absent")
    return dict(fit_offset_v=coef[0], fit_input1_feedthrough=coef[1],
                fit_input2_feedthrough=coef[2], fit_product_gain_per_v=coef[3],
                peak_residual_percent_fullscale=abs(residual).max()/fullscale*100,
                rms_residual_percent_fullscale=np.sqrt(np.mean(residual**2))/fullscale*100,
                vocm_min_v=data.vocm.min(), vocm_max_v=data.vocm.max())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--folder", default="surface_corners")
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    p = ROOT / "verification/porting" / args.project
    reports, audits, archive = [], {}, {}
    for sheet in sorted((p / "datasheets" / args.folder).glob("*.yaml")):
        out = p / "out" / sheet.stem
        audits[sheet.name] = audit(sheet, out)
        meta = json.loads(max((out / "history").glob("*.meta.json"),
                             key=lambda f: f.stat().st_mtime).read_text())
        directory = Path(meta["analysis_dirs"]["dc"])
        if not directory.is_absolute():
            directory = out / directory
        frame = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
        for _, row in frame.iterrows():
            wave = pd.read_csv(directory / f"run_{row.run_id}__transfer.csv")
            result = row.to_dict()
            result.update(datasheet=sheet.name, **fit_surface(wave))
            reports.append(result)
            archive[sheet.stem + "_" + row.run_id] = wave.to_numpy()
            archive["columns"] = wave.columns.to_numpy(dtype=str)
    if not reports:
        raise ValueError("No surface datasheets found")
    evidence = ROOT / "doc/porting/evidence"
    data = pd.DataFrame(reports)
    data.to_csv(evidence / (args.label + ".csv"), index=False)
    (evidence / (args.label + "_audit.json")).write_text(json.dumps(audits, indent=2) + "\n")
    np.savez_compressed(evidence / (args.label + "_waveforms.npz"), **archive)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.7), constrained_layout=True)
    for corner, frame in data.groupby("corner_mos"):
        frame = frame.sort_values("temp")
        axes[0].plot(frame.temp, frame.fit_product_gain_per_v, "o-", label=corner)
        axes[1].plot(frame.temp, frame.peak_residual_percent_fullscale, "o-", label=corner)
    axes[0].set(ylabel="Fitted product gain (1/V)")
    axes[1].set(ylabel="Peak residual (% fitted full scale)")
    for ax in axes:
        ax.set(xlabel="Temperature (C)")
        ax.grid(True, alpha=.25)
    axes[1].legend(title="Raw MOS corner")
    fig.suptitle(args.label.replace("_", " ") + " | 1.5 V, CM 0.75 V, code 13")
    for ext in ["png", "pdf"]:
        fig.savefig(ROOT / "doc/porting/figures" / (args.label + "." + ext), dpi=180)
    print(data[["corner_mos", "temp", "fit_product_gain_per_v",
                "peak_residual_percent_fullscale", "rms_residual_percent_fullscale"]].to_string(index=False))


if __name__ == "__main__":
    main()
