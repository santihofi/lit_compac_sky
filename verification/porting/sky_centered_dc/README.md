# Fixed-code calibrated PVT control

Each MOS corner uses its nearest measured K100 magnitude to 10 per volt at 27 C and 1.5 V.
The selected gain code then stays fixed over the supply and temperature grid.
The SKY130 design also retains its earlier fixed per-corner ideal current settings.
Nominal resistors are used throughout.
This is neither temperature compensation nor a real bias-DAC qualification.
scripts/prepare_calibrated_pvt.py generates the project from retained source decks and calibration evidence.
