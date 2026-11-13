# SKY130A port plan

Status: characterization and schematic design in progress, no SKY130 multiplier layout has been verified.

## Scope and acceptance

The user clarified on 2026-11-03 that each PVT corner needs at least one code satisfying all applicable specifications simultaneously.
The passing code may differ between PVT corners.
Unused codes may fail without disqualifying the circuit.
Keep circuit geometry fixed across corners and record every selected gain and bias code.
Fixed-code sweeps measure drift without recalibration and cannot establish that a corner has no feasible code.
Endpoint bracketing is only a preliminary screen.
A DC-feasible code still needs bandwidth, noise, stability and loading verification at that same code.
The numerical gain-error tolerance remains to be confirmed, so tolerance sweeps are explicitly provisional.

The electrical baseline was frozen at lit_compac commit 3764a02d8641559aa58ec8521680424afc38a178.
The system architecture now follows source revision 93ff95680bd88ea07e60e80863d4a75e9d8106df, observed on 2026-11-02.
The multiplier, gain-trim and OTA schematic blobs are unchanged between those revisions.
The starting template is sky130A-ams-chip-template commit a84f4514d727b58cd475a67000aac230d8d367ea, aligned structurally with the IHP AMS template.
Work is on work-santi.
Pending confirmation, preserve the 1.45 to 1.65 V external supply range, 0 to 80 C specified temperature range, sixteen tiles with a 512-bit serial trim chain, the separate bandgap and the latest analog interfaces.
The updated source adds idac_ostg in each bias channel, extends each register from 27 to 32 bits and removes the external vb_ostg tree pin.
The five new bits drive active-low readout DAC switches through register-output inverters.
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

The destination now has a configured upstream, lit_compac_sky/work-santi.
The reference knowledge repository uses an HTTPS remote that needs credentials inside the container.
GitHub SSH access works after adding the container account corresponding to UID 1000.

## Checkpoint on 2026-10-30

Current IHP bare-core corners, nominal noise and CMFB stability have been reproduced.
The all-LVT, native-quad and source-degeneration SKY130 candidates failed their tested corner settings.
Those screens do not exhaust per-corner calibration choices.
The four-copy degeneration candidate improves nominal speed and noise at 3.63 times the bare-core supply current, with insufficient loop gain margin.
Continue with full transfer surfaces and separate slow/fast CMFB compensation.
Do not start the port layout from these unqualified sizes.
The reusable template now includes measured MOS corner-identity controls and corrected skew-corner ordering.

## Further characterization on 2026-10-30

Full nominal transfer surfaces now distinguish gain from shape error.
The first source-degenerated candidate has 2.35 percent peak fitted residual against IHP 1.38 percent.
Explicit convergence controls reduce its dense sweep from a timeout to a valid 58-second run.
Large-signal CMFB traces expose the slow-capacitor settling cost, and load geometry offers a separate compensation path.
Five quantized bias settings pass the nominal process-corner diagonal ratio screen at the original supply, with supply/temperature and full-surface checks still pending.
A separately labeled 1.8 V, 0.9 V common-mode branch remains exploratory.
See REPRODUCE.md for project identities and execution rules.

## Checkpoint on 2026-11-01

The compact two-copy candidate improves nominal full-surface shape and all matched core-to-core bandwidth paths, with input capacitance below the current IHP core.
The fixed-current PVT sweep passes 36 of 45 diagonal-curvature cases, so it remains unqualified.
The remaining experiments separate folding-mirror headroom, input-pair body effect and tail output conductance.
New waveform checks compare AC captures with independent scalar anchors after a reproducible wrong-curve capture in Chipify.
Template controls and design results are committed incrementally.


## Publishing checkpoint on 2026-11-02

The SKY130 template work-santi branch now pushes successfully.
The latest published template update records model-bin channel-length limits and file hashes.
The destination design still has no configured remote, and the private reference repository still requires HTTPS credentials.

## Replica checkpoint on 2026-11-02

The transistor-replica tail candidate is the first to pass the 45-case diagonal-curvature screen with fixed per-corner current codes.
Its nominal full-surface error improves over IHP and both CMFB and local replica loops pass their provisional margins.
The 45-case bandwidth and both feedback-loop sweeps now have independent waveform audits.
Both loops pass their provisional margin limits, but input-2 bandwidth is lower than IHP in some corners.
Fifteen nominal-supply full surfaces and the nominal receiver-load comparison are complete, with the mixed shape and speed results recorded in COMPARISON.md.
The separate drawn experimental schematic passes electrical comparison and nominal simulation replay.
The wider trim network now brackets gain 10 at 22/27 C in all five MOS corners and is monotonic across all 32 codes at 27 C.
Its nearest-code residual reaches 0.64 percent versus IHP's 0.44 percent.
Fixed calibrated-code PVT checks expose limitations of the wider resistor network: 40 of 45 shape passes, and input-2 bandwidth below IHP in every matched case.
These measurements do not exhaust alternative codes at each PVT corner and therefore do not prove infeasibility under per-corner calibration.
An independent trim-gate rail control confirms substantial switch-drive sensitivity.
Further switch and resistor-distribution controls must preserve the nominal gain while recovering speed and shape.
The original replica also passes eight nominal loop-current kick controls with independently checked waveforms.
Supply-extreme full surfaces, passive corners, calibrated loop margins, startup, mismatch and real bias circuitry remain open.
The main macro folders have not been promoted to an accepted replacement.

## Joint nominal code coverage, 2026-11-09

The transmission-gate candidate has DC-feasible codes in all five nominal MOS corners at a provisional one-percent gain tolerance.
All fourteen such codes have valid and independently anchored AC measurements.
Only sf code 9 matches both IHP bandwidths, with just 0.055 percent input-2 margin.
The other four corners need a bias or circuit change to meet the matched-bandwidth screen at this tolerance.
These results do not exhaust bias-code choices.
The completed 1440-case gain-code sweep covers 34 of 45 points under the provisional DC screen at retained bias settings, with nominal passive models.
Retain gain, shape, speed and loop results keyed to the same complete calibration setting before declaring corner coverage.

## Input-2 candidate progress, 2026-11-09

Narrow fixed loads improve slow-corner bandwidth by eleven percent at unchanged current.
Six exact parallel copies then pass gain, shape and both fixed-load bandwidth screens at all five nominal MOS corners, at about three times the original two-copy supply current.
Five-copy results are diagnostic because the inherited replica nf expression truncates a fractional finger count.
Actual receiver loading leaves one six-copy slow-corner shortfall.
Biasing the replica gates from an explicit common-mode reference closes that loaded case without a material DC change at the measured point.
The five-corner common-mode-replica extension passes the nominal joint gain, shape, bare and receiver-loaded bandwidth screen after selecting SS code 16.
No full-PVT, noise, loop or layout acceptance is claimed.
The older two-copy gain-code PVT sweep completed ff, fs and sf before the Chipify upgrade interrupted ss.
SS and TT completed on release 0.2.3 after an unchanged-control replay.

## Next qualification, 2026-11-10

Both CMFB and local replica-bias loops now pass the nominal small-signal screens at ff=12, fs=29, sf=10, ss=16 and tt=6 on the six-copy quiet replica, with ten independently anchored curves.
Then qualify real reference impedance, full surfaces, noise and per-PVT code coverage before promoting the schematic or generating multiplier layout.
The one-percent gain tolerance remains provisional.

The quiet-replica 1440-case DC PVT code search completed with 32/45 points covered at retained bias currents. The completed 150-case bias-sensitivity screen recovers six points, giving 38/45 DC-covered points. Completed fine calibration recovers two more points, giving 40/45 observed DC-covered points. The completed resistor-range screen identifies a 0.8 fixed-load / 1.4 trim candidate with target-bracketing endpoints at nine of ten points. The completed 322-case all-code search finds DC-feasible codes at all ten test points for this global network. All eight nominal DC-feasible codes completed AC checks. Only FF and SF have joint DC/bandwidth-feasible codes, so a resistance-matched narrow trim-poly control was tested. The 2.85 um trim family recovers both FS nominal codes, and the completed five-corner comparison gives joint nominal coverage in FF, FS, SF and TT. SS remains below both input-2 bandwidth references. The completed 160-case nominal SS gain/current grid has four DC-feasible settings at factors 0.9 and 1.0. All four completed AC and fail the input-2 speed comparison. The smaller active-pair candidate recovers gain at codes 20/21, and both pass the matched-gain bare and loaded bandwidth screens at nominal SS. A twenty-case global endpoint screen is running before requalifying its other corners.
