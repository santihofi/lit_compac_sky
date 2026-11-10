# Quiet-replica exhaustive gain-code PVT screen

This is the six-copy quiet-replica circuit with 1.41 um fixed loads.
All 32 gain codes are evaluated at five MOS corners, three temperatures and three supplies.
The earlier per-MOS ideal bias currents remain fixed across supply and temperature.
Passives are nominal, and gate and reference drivers are ideal.
The screen finds common gain and diagonal-shape codes, not full-spec coverage.
Alternative bias settings remain available when no gain code passes.
Use scripts/analyze_trim_code_coverage.py --candidate quiet --grid pvt --gain-tolerance-percent 1 after completion.
