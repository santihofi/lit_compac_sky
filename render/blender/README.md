# Blender Renders

This folder is reserved for 3D renders of the `chip_top` layout.

The layout will be rendered with [Blender](https://www.blender.org/) in the future, and the resulting figures will be stored here. The 2D renders that `make render-gds` produces today are written to [`../img/`](../img/).

Until then the KLayout 2.5D view is the closest thing. It extrudes the drawn layers to the heights of the sky130 stack, from the substrate through `li1` and `met1` to `met5` with their vias, and it comes with the PDK in `$PDKPATH/libs.tech/klayout/d25/sky130.lyd25`. Open a layout and pick the `D25 View` entry of the `Efabless sky130` menu:

```sh
ke layout/chip_top_logo_fill.gds.gz
```

The view needs a display session, so it belongs in the container desktop and not in a batch shell. A full chip is a lot of geometry for it, start on a macro such as `macros/inverter/layout/inverter.gds`.
