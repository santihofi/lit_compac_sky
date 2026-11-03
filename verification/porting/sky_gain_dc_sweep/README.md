# Gain code swept inside ngspice

Eight DC analyses sweep the code source from 0 to 31 for the four sign combinations at 100 mV and 10 mV.
The final plot combines those captures into K100, K10 and their ratio.
Every waveform reference is plot-qualified.
scripts/audit_gain_dc_sweep.py verifies the 32 code identities, endpoint scalar anchors and agreement with 32 independent operating-point runs.

The typical-corner control agrees within the six-digit precision of the earlier saved scalars.
The one-row Chipify result represents one 32-point waveform, not 32 scalar limit verdicts.
Per-code acceptance requires separate waveform evaluation.
This reduced bench omits the full operating-point, axis-curvature and bandwidth measurements.
Its elapsed time is therefore not a like-for-like performance benchmark.
