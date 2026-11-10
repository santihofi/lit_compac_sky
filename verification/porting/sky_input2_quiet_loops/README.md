# Quiet-replica nominal loop checks

Generate with scripts/prepare_input2_quiet_loops.py from the selected nominal code evidence and the quiet-replica circuit.
CMFB injection splits the OTA output from the load gates.
Local bias injection splits both main and replica tail gates from the current-reference node.
Each probe preserves DC continuity and uses voltage and current AC injection to reconstruct the return ratio.
The other loop stays closed.
Both tests use zero differential inputs, 100 fF per output and an ideal common-mode reference.
The provisional screens require phase margin from 45 to 180 degrees, gain margin at least 10 dB and exactly one unity crossing.
These local small-signal checks do not establish startup, large-signal stability, realistic reference-driver behavior or receiver-loaded loop stability.

Run scripts/analyze_input2_quiet_loops.py after the Chipify batch completes.
It checks all five selected parameter tuples and independently reconstructs six loop metrics from each captured curve.
