#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Anchor replica kick captures and compare the two integration time steps."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
project = ROOT / "verification/porting/sky_replica_kick"
out = project / "out"
result = audit(project / "datasheets/kick.yaml", out, False)
meta = json.loads(max((out / "history").glob("*.meta.json"),
                     key=lambda p: p.stat().st_mtime).read_text())
directory = out / meta["analysis_dirs"]["transient"]
data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
records, arrays, cases = [], {}, {}
fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
for _, row in data.iterrows():
    wave = pd.read_csv(directory / ("run_" + row.run_id + "__kick.csv"))
    t = wave.time.to_numpy()
    if not (np.all(np.diff(t) > 0) and abs(t[-1] - 1e-6) < 1e-12):
        raise ValueError("Incomplete or nonmonotonic transient")
    key = f"{row.kick_node}_{'positive' if row.kick_current > 0 else 'negative'}_{row.maxstep}"
    arrays[key] = wave.to_numpy()
    cases[(row.kick_node, row.kick_current, row.maxstep)] = wave
    peak_mask = (t >= 100e-9) & (t <= 900e-9)
    late = t >= 900e-9
    measured = {
        "peak_mv": float(abs(wave.err[peak_mask]).max() * 1000),
        "residual_mv": float(abs(wave.err[late]).max() * 1000),
        "bias_residual_mv": float(abs(wave.bias_err[late]).max() * 1000),
    }
    for name, value in measured.items():
        if not np.isclose(value, row[name], rtol=3e-5, atol=1e-8):
            raise ValueError(f"{key}: scalar/capture mismatch for {name}")
    record = {"case": key, **measured}
    for signal in ["err", "bias_err"]:
        outside = np.flatnonzero((t >= 120.2e-9) & (abs(wave[signal]) > 1e-3))
        finish = (float(t[outside[-1]+1]) if len(outside) and outside[-1] < len(t)-1
                  else (120.2e-9 if not len(outside) else None))
        record[signal + "_settle_1mv_ns"] = (
            None if finish is None else (finish - 120.2e-9) * 1e9)
        record[signal + "_late_pp_uv"] = float(np.ptp(wave[signal][late]) * 1e6)
    records.append(record)
    col = 0 if row.kick_node == "vbias" else 1
    style = "--" if row.maxstep == "50p" else "-"
    label = f"{row.kick_current*1e6:+g} uA, {row.maxstep}"
    axes[0, col].plot(t*1e9, wave.err*1e3, style, linewidth=1, label=label)
    axes[1, col].plot(t*1e9, wave.bias_err*1e3, style, linewidth=1, label=label)
comparisons = []
for node in ["vbias", "ibias"]:
    for current in [-40e-6, 40e-6]:
        coarse = cases[(node, current, "100p")]
        fine = cases[(node, current, "50p")]
        report = {"kick_node": node, "kick_current_a": current}
        for signal in ["err", "bias_err"]:
            aligned = np.interp(coarse.time, fine.time, fine[signal])
            report[signal + "_maximum_difference_mv"] = float(
                np.max(abs(coarse[signal] - aligned)) * 1000)
        comparisons.append(report)
for col, title in enumerate(["CMFB load-gate kick", "Replica tail-gate kick"]):
    axes[0, col].set(title=title, ylabel="Output CM error (mV)")
    axes[1, col].set(ylabel="Tail-gate error (mV)")
    axes[0, col].legend(fontsize=8)
for ax in axes.flat:
    ax.set(xlabel="Time (ns)", xlim=(90, 500))
    ax.grid(alpha=.25)
evidence = ROOT / "doc/porting/evidence"
data.to_csv(evidence / "sky_replica_kick.csv", index=False)
np.savez_compressed(evidence / "sky_replica_kick_waveforms.npz", **arrays)
summary = {"audit": result, "columns": wave.columns.tolist(),
           "cases": records, "step_comparison": comparisons}
(evidence / "sky_replica_kick_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
for ext in ["png", "pdf"]:
    fig.savefig(ROOT / "doc/porting/figures" / ("sky_replica_kick." + ext), dpi=180)
print(json.dumps(summary, indent=2))
