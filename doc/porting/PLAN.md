# SKY130A port plan

Status: characterization and schematic design in progress, no SKY130 multiplier layout has been verified.

## Scope and acceptance

The reference is lit_compac commit 3764a02d8641559aa58ec8521680424afc38a178.
The starting template is sky130A-ams-chip-template commit a84f4514d727b58cd475a67000aac230d8d367ea, aligned structurally with the IHP AMS template.
Work is on work-santi.
Pending confirmation, preserve the 1.45 to 1.65 V external supply range, 0 to 80 C specified temperature range, sixteen tiles with a 432-bit serial trim chain, the separate bandgap and all analog interfaces.
Keep the source project's low-pass filter deferred.
Prioritize multiplier accuracy, bandwidth, noise and stability, and quantify any power or area cost.
Evaluate 1.8 V separately as an alternative, never mix its results into an equal-supply comparison.

## Ordered milestones

1. Freeze provenance and reproduce the IHP baseline.
   Inventory every model family, device size, bench, characterization limit and layout result.
   Run the nominal multiplier, common-mode loop, bias chain and bandgap benches before adopting the documented numbers.
   Archive rendered decks, simulator logs, scalar tables and tool versions.
2. Build equivalent SKY130 schematics.
   Map MOS geometry, finger semantics, resistors, capacitors, BJTs and bulk ties explicitly.
   Compare symbol pin coordinates and netlisted connectivity.
   Characterize device primitives before choosing replacement resistor lengths or bandgap ratios.
   Size and verify the Gilbert core and CMFB first, then DACs, output stage, bandgap, bias channel and tile.
3. Qualify schematic performance with Chipify.
   Use the same input amplitude, load and measurement definitions for both processes.
   Run nominal and process/supply/temperature sweeps, independent passive corners where available, trim coverage, mismatch with a zero-variation control, loop gain and kick/startup benches.
   Verify reported measurements are finite, expected case counts match, every required vector exists and waveform capture succeeds.
   Record each failure and its cause.
   Do not release layout work for a block until its schematic acceptance checks pass or a specific limitation is agreed.
4. Generate layout from Python.
   Start with verified SKY130 PCells and reusable geometry helpers.
   Preserve matching, symmetry, common centroids, shared diffusion or taps where legal, guard rings and explicit well/substrate connectivity.
   Build primitive blocks, tile, then the 4 by 4 tree and separate bandgap.
   Re-harden the register against SKY130 standard cells and verify bit order.
   Keep layout dimensions and all physical interfaces in a machine-readable manifest.
5. Verify physical and extracted views.
   Run applicable KLayout and Magic DRC, LVS against the schematic, boundary/pin checks and PEX.
   Classify density and full-chip-only checks explicitly.
   Rerun the same electrical benches on extracted views, inspect parasitic budgets and fix regressions.
6. Compare and deliver.
   Produce a report covering devices, sizing, headroom, gain/linearity, PVT, mismatch, noise, bandwidth, stability, startup, power, area, routing and extracted degradation.
   Separate measured results, source-reported results, estimates and untested claims.
   Update reusable SKY130 template flow changes, validate them against the IHP template's conventions, commit and push work-santi.

## Evidence and knowledge capture

After each tool bring-up, primitive characterization, block qualification and layout milestone, distill the newly demonstrated decisions and tool limitations.
Keep circuit artifacts and complete logs here, with concise commit-pinned findings in the designated private knowledge repositories.
Do not commit PDK model files, credentials or machine-specific secrets.
Do not claim layout signoff from an empty report or schematic equivalence from a simulator return code.

## Current external dependencies

The destination repository has no remote configured yet.
The reference knowledge repository uses an HTTPS remote that needs credentials inside the container.
GitHub SSH access works after adding the container account corresponding to UID 1000.

## Checkpoint on 2026-10-30

Current IHP bare-core corners, nominal noise and CMFB stability have been reproduced.
The all-LVT, native-quad and source-degeneration SKY130 candidates remain rejected at corners.
The four-copy degeneration candidate improves nominal speed and noise at 3.63 times the bare-core supply current, with insufficient loop gain margin.
Continue with full transfer surfaces and separate slow/fast CMFB compensation.
Do not start the port layout from these rejected sizes.
The reusable template now includes measured MOS corner-identity controls and corrected skew-corner ordering.
