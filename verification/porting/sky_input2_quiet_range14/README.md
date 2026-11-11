# Fixed 0.8 / trim 1.4 global resistor candidate

This candidate applies one resistor network at all ten test points.
All 32 gain codes are tested at five nominal MOS corners and five previously unresolved PVT points.
Nominal bias factors remain 1, hot points use 0.9 and cold TT uses 0.85.
Two additional cold-TT endpoints at factor 0.9 replay the preceding range study.
The 322-case batch has twenty endpoint controls from that study.
These ten points are a screening subset, not all 45 PVT points.
DC-feasible codes still require same-code bandwidth, noise and stability checks.
Do not combine this variant's coverage with the original resistor network's 40/45 result.
