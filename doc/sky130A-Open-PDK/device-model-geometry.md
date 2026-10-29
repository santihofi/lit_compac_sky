# SKY130 geometry and model coverage

Checked in IIC-OSIC-TOOLS 2026.10 on 2026-10-29.
A layout generator's minimum width and length do not establish the simulator model's supported geometry range.

## Native NMOS has discrete model bins

The installed `sky130_fd_pr__nfet_03v3_nvt.pm3.spice` defines nine narrow geometry bins.
The centers below are in micrometres, and each bound extends 0.005 um from its center.

| Finger width | Supported lengths |
| ---: | --- |
| 10.0 | 0.5 |
| 4.0 | 0.5 |
| 1.0 | 0.5, 0.6 |
| 0.7 | 0.5, 0.6 |
| 0.42 | 0.5, 0.6, 0.8 |

A probe using 5 um fingers failed with `could not find a valid modelname` even though the length exceeded the layout generator's minimum.
Using 4 um fingers at L=0.5 um ran successfully.
Check the installed model before any geometry sweep, because a mathematically interpolated size can fall outside every model bin.

The Xschem total width is `W = nf × finger_width`.
For sixteen 4 um fingers, write W=64, nf=16 and L=0.5.
The KLayout PCell's `w` is the finger width, so the corresponding PCell parameters use w=4, nf=16 and l=0.5.

## Keep the parasitic geometry in step

The stock Xschem MOS symbols derive drain/source diffusion area and perimeter from the integer number of diffusion regions.
For odd finger counts, use the same integer expressions as the symbol, rather than nf/2.
The displayed width alone does not update handwritten ad/as/pd/ps values.
The symbols also use nrd=nrs=0.29/W.
Recompute those values when a handwritten sizing deck changes W.

## Select a device through the PCell type

The `skywater130` KLayout library exposes `nfet` and `pfet` PCells with a `type` parameter.
Low-threshold devices are supported choices, including `sky130_fd_pr__nfet_01v8_lvt` and `sky130_fd_pr__pfet_01v8_lvt`.
The native `sky130_fd_pr__nfet_03v3_nvt` is another nfet type.
There is no separately named low-threshold PCell to look up.
The library's `bulk` choice controls a tie or guard ring, not an automatic isolated source-tied well.

These checks establish model coverage and generator interfaces.
Each generated device still requires DRC, extraction and LVS before use in a verified macro.
