#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Freeze and plot the nominal CMFB and local replica return ratios."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
fig, axes = plt.subplots(2, 1, sharex=True, figsize=(8, 6), constrained_layout=True)
archive = {}
for name, project, sheet, results in [
    ("CMFB", "sky_replica_validation", "stability.yaml", "out/stability"),
    ("Tail replica", "sky_replica_stability", "nominal.yaml", "out"),
]:
    p = ROOT / "verification/porting" / project
    out = p / results
    audit(p / "datasheets" / sheet, out)
    meta = json.loads(max((out / "history").glob("*.meta.json"),
                         key=lambda f: f.stat().st_mtime).read_text())
    directory = Path(meta["analysis_dirs"]["ac"])
    if not directory.is_absolute():
        directory = out / directory
    frame = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
    if len(frame) != 1:
        raise ValueError("Expected one nominal loop result")
    row = frame.iloc[0]
    wave = pd.read_csv(directory / f"run_{row.run_id}__stability.csv")
    freq = wave["frequency"].to_numpy()
    mag = wave["ac2.tloop_mag"].to_numpy()
    phase = np.rad2deg(np.unwrap(np.deg2rad(wave["ac2.tloop_phase"].to_numpy())))
    key = name.lower().replace(" ", "_")
    archive.update({key+"_frequency": freq, key+"_magnitude": mag, key+"_phase_deg": phase})
    label = f"{name}: PM {row.pm:.1f}°, GM {row.gm_db:.1f} dB"
    axes[0].semilogx(freq, 20*np.log10(mag), label=label)
    axes[1].semilogx(freq, phase, label=name)
axes[0].axhline(0, color="black", linewidth=.7)
axes[1].axhline(-180, color="black", linewidth=.7)
axes[0].set(ylabel="Return ratio (dB)", ylim=(-60, 60))
axes[1].set(xlabel="Frequency (Hz)", ylabel="Phase (degrees)", xlim=(1, 1e10), ylim=(-300, 10))
for ax in axes:
    ax.grid(True, alpha=.25)
axes[0].legend()
fig.suptitle("SKY130 replica candidate | tt, 27 C, 1.5 V, 100 fF")
for ext in ["png", "pdf"]:
    fig.savefig(ROOT / "doc/porting/figures" / f"sky_replica_loops.{ext}", dpi=180)
np.savez_compressed(ROOT / "doc/porting/evidence/sky_replica_loop_waveforms.npz", **archive)
