# pmos4 trim-switch control

This retains the original replica transistors and current calibration.
Load and trim resistance scale together by 1.7, with no separate doubling of trim segments.
The pmos4 variant uses 4 parallel PMOS copies per inherited switch unit.
PMOS wells connect to the core ntap supply.
Ideal complementary gate drivers preserve the original code polarity.
These drivers represent static control levels, not qualified physical inverters.
The retained NMOS switches in tg2 form transmission gates.
Endpoint bracketing is only a screen before matched-gain shape, speed and loop checks.
