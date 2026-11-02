#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Draw the characterized replica candidate as a separate, unqualified view."""
from pathlib import Path
import json
import re

import yaml
from jinja2 import Environment, StrictUndefined

from port_core_schematic import attr, components

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "verification/porting/sky_replica_tail"
DEST = ROOT / "verification/porting/sky_replica_schematic"
SCHEMATIC = DEST / "schematic"
SCHEMATIC.mkdir(parents=True, exist_ok=True)
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
config = yaml.safe_load((SOURCE / "datasheets/nominal.yaml").read_text())
parameters = {k: v[0] if isinstance(v, list) else 0 if k == "seed" else v
              for k, v in config["parameters"].items()}
golden = Environment(undefined=StrictUndefined).from_string(
    (SOURCE / "tb/replica.spice").read_text()).render(**parameters)
definitions = {}
for cell, body in re.findall(r"^\.subckt (\w+) (.*?)^\.ends", golden, re.M | re.S):
    lines = re.sub(r"\n\+\s*", " ", body).splitlines()
    definitions[cell] = {line.split()[0]: line for line in lines[1:]
                         if line and line[0] in "XxR"}
(DEST / "golden.spice").write_text(golden)
(DEST / "parameters.json").write_text(json.dumps(parameters, indent=2) + "\n")


def properties(line):
    tokens = line.split()
    name = tokens[0]
    if name.startswith("R"):
        return "devices/res.sym", f"name={name}\nvalue={tokens[3]}\nm=1"
    index = next(i for i, t in enumerate(tokens) if t.startswith("sky130_fd_pr__"))
    model = tokens[index].removeprefix("sky130_fd_pr__")
    props = dict(t.split("=", 1) for t in tokens[index+1:])
    if float(props["m"]) != float(props["mult"]):
        raise ValueError("Symbol cannot represent different m and mult")
    del props["m"]
    text = f"name={name[1:]}\n" + "\n".join(f"{k}={v}" for k, v in props.items())
    return "sky130_fd_pr/" + model + ".sym", text + f"\nmodel={model}\nspiceprefix=X"


def instance(line, x, y, rotation=0, flip=0):
    sym, props = properties(line)
    return f"C {{{sym}}} {x} {y} {rotation} {flip} {{{props}\n}}\n"


serial = 0
def label(x, y, net, rotation=0, flip=0):
    global serial
    serial += 1
    return (f"C {{devices/lab_pin.sym}} {x} {y} {rotation} {flip} "
            f"{{name=candidate_label{serial} sig_type=std_logic lab={net}}}\n")


def wire(x1, y1, x2, y2):
    return f"N {x1} {y1} {x2} {y2} {{}}\n"


def stretch(text):
    def ymap(y):
        value = int(y)
        return value - (160 if value < -240 else 0) - (80 if value < -400 else 0)
    for m, end, a in reversed(list(components(text))):
        sym, x, y, r, f = m.groups()
        text = text[:m.start()] + f"C {{{sym}}} {x} {ymap(y)} {r} {f} {{{a}}}" + text[end:]
    text = re.sub(r"^N (-?\d+) (-?\d+) (-?\d+) (-?\d+) (.*)$",
                  lambda m: f"N {m[1]} {ymap(m[2])} {m[3]} {ymap(m[4])} {m[5]}",
                  text, flags=re.M)
    text = re.sub(r"^(T \{(?:[^{}]|\n)*\} -?\d+) (-?\d+)( [0-3] [01] .*)$",
                  lambda m: f"{m[1]} {ymap(m[2])}{m[3]}", text, flags=re.M)
    # Group boxes are reconstructed by the inherited circuit's wires.
    text = re.sub(r"^P .*\n", "", text, flags=re.M)
    return text


for cell in ["gilbert_cell", "ota", "gain_trim"]:
    macro = "ota" if cell == "ota" else "gilbert_cell"
    source = ROOT / "macros" / macro / "schematic/xschem" / (cell + ".sch")
    text = source.read_text()
    # Remove inherited IHP sizing and layout claims before adding candidate notes.
    text = re.sub(r"^T \{([^{}]*)\} [^\n]*$", lambda m: "" if len(m[1]) > 130 else m[0],
                  text, flags=re.M)
    if cell == "gilbert_cell":
        text = re.sub(r"T \{Layout plan.*?\} -?\d+ -?\d+ .*?\n", "", text, flags=re.S)
        text = re.sub(r"T \{RD1/RD2:.*?\} -?\d+ -?\d+ .*?\n", "", text, flags=re.S)
        text += "T {Experimental geometry, not released to layout.\nResistor lengths still need manufacturing-grid quantization.\nDummy placement and matching need a new physical design.} -660 610 0 0 0.3 0.3 {}\n"

    for m, end, a in reversed(list(components(text))):
        sym, x, y, r, f = m.groups()
        name = attr(a, "name", "")
        if "annotate_fet_params" in sym or (cell == "gilbert_cell" and name in ["M14", "p13"]):
            text = text[:m.start()] + text[end:]
            continue
        key = name if name.startswith("Rtap") else "X" + name
        if key in definitions[cell]:
            text = text[:m.start()] + instance(definitions[cell][key], x, y, r, f).rstrip() + text[end:]
        elif sym.endswith("gain_trim.sym"):
            ref = "lit_compac_sky/verification/porting/sky_replica_schematic/schematic/gain_trim.sym"
            text = text[:m.start()] + f"C {{{ref}}} {x} {y} {r} {f} {{{a}}}" + text[end:]
    if cell == "gilbert_cell":
        removed = [
            "N -590 -700 -590 -570", "N -590 -510 -590 -490",
            "N -590 -540 -530 -540", "N -630 -540 -630 -490",
            "N -630 -490 -590 -490",
        ]
        for prefix in removed:
            text, count = re.subn("^" + re.escape(prefix) + r" .*\n", "", text, flags=re.M)
            if count != 1:
                raise ValueError("Missing reference wire: " + prefix)
        text = stretch(text)
        # Source resistors occupy the new space between the pair and its tail.
        for number, x in [(1, -260), (2, -60)]:
            prefix = f"N {x} -660 {x} -530"
            text, count = re.subn("^" + re.escape(prefix) + r" .*\n", "", text, flags=re.M)
            assert count == 1, prefix
            text += instance(definitions[cell][f"XRP{number}"], x, -600, 2)
            text += wire(x, -660, x, -630) + wire(x, -570, x, -530)
            text += label(x, -570, f"ps{number}", 1)
            text += wire(x+20, -600, x+40, -600) + label(x+40, -600, "ptap", flip=1)
        # Each quad branch gets its own modeled source resistor.
        for number, x in [(7, 150), (8, 350), (9, 550), (10, 750)]:
            prefix = f"N {x} -420 {x} -240"
            text, count = re.subn("^" + re.escape(prefix) + r" .*\n", "", text, flags=re.M)
            assert count == 1, prefix
            text += instance(definitions[cell][f"XRdegen{number}"], x, -350, 2)
            text += wire(x, -420, x, -380) + wire(x, -320, x, -240)
            text += label(x, -380, f"qd{number}", 1)
            text += wire(x+20, -350, x+30, -350) + label(x+30, -350, "ptap", flip=1)
        # Replica reference: one eighth of the input pair, with eight series units.
        text += "T {Tail reference replica, one eighth of the input pair} -1580 -1490 0 0 0.4 0.4 {}\n"
        text += instance(definitions[cell]["XM14"], -1260, -1300)
        text += wire(-1240, -1330, -1240, -1400) + label(-1240, -1400, "vdd", 1)
        text += wire(-1240, -1300, -1180, -1300) + label(-1180, -1300, "ntap", flip=1)
        text += wire(-1280, -1300, -1540, -1300) + wire(-1540, -1300, -1540, -400)
        text += wire(-1240, -1270, -1240, -1200) + label(-1240, -1200, "rvcm1", 1)
        text += wire(-1440, -1200, -1240, -1200) + wire(-1240, -1200, -1040, -1200)
        for number, x, flip, gate in [(1, -1440, 0, "in1n"), (2, -1040, 1, "in1p")]:
            for index in range(8):
                y = -1150 + 80*index
                text += instance(definitions[cell][f"XRrep{number}_{index}"], x, y, 2)
                text += wire(x, y-30, x, y-50)
                if index:
                    text += label(x, y-50, f"rp{number}_{index}", 1)
                text += wire(x+20, y, x+40, y) + label(x+40, y, "ptap", flip=1)
            text += wire(x, -560, x, -510) + label(x, -560, f"rps{number}", 1)
            origin = x-20 if not flip else x+20
            text += instance(definitions[cell][f"XMrep{number}"], origin, -480, 0, flip)
            direction = -1 if not flip else 1
            text += wire(x+direction*40, -480, x+direction*80, -480)
            text += label(x+direction*80, -480, gate, flip=flip)
            text += wire(x, -480, x-direction*60, -480)
            text += label(x-direction*60, -480, "ntap", flip=1-flip)
            text += wire(x, -450, x, -400)
        text += wire(-1540, -400, -1440, -400) + wire(-1440, -400, -1040, -400)
        text += label(-1540, -400, "ibias")
        text += "T {Experimental replica candidate, schematic qualification in progress} -650 -1280 0 0 0.6 0.6 {}\n"
    if cell == "ota":
        old_columns = [760+80*i for i in range(12)]
        for m, end, a in reversed(list(components(text))):
            sym, x, y, rotation, flip = m.groups()
            name = attr(a, "name", "")
            if re.fullmatch(r"RS\d+", name):
                number = int(name[2:])
                text = text[:m.start()] + instance(
                    definitions[cell]["X"+name], 800+100*(number-1), 80, 3).rstrip() + text[end:]
            elif "lab_pin.sym" in sym and (
                (int(x) in old_columns and int(y) in [30, 130]) or
                (int(x)+20 in old_columns and int(y) == 80)):
                text = text[:m.start()] + text[end:]
        for x in old_columns:
            for y1, y2 in [(30, 50), (110, 130)]:
                pattern = rf"^N {x} {y1} {x} {y2} .*\n|^N {x} {y2} {x} {y1} .*\n"
                text, count = re.subn(pattern, "", text, flags=re.M)
                if count != 1:
                    raise ValueError(f"Missing OTA resistor stub {x} {y1} {y2}")
        for index in range(12):
            x = 800+100*index
            text += wire(x, 100, x, 140)
            if index < 11:
                text += wire(x+30, 80, x+70, 80)
                text += label(x+50, 80, f"rs{index+1}", 1)
        text += wire(800, 140, 1900, 140) + label(800, 140, "ptap")
        text += wire(730, 80, 770, 80) + label(730, 80, "sa")
        text += wire(1930, 80, 1970, 80) + label(1970, 80, "sb", flip=1)
        text += "T {Fast-loop degeneration, twelve series resistor units} 760 -180 0 0 0.4 0.4 {}\n"
    (SCHEMATIC / (cell + ".sch")).write_text(text)
    symbol = source.with_suffix(".sym").read_text()
    if "spectre_format=" not in symbol:
        symbol = symbol.replace('format="@name @pinlist @symname"',
                                'format="@name @pinlist @symname"\nspectre_format="@name ( @pinlist ) @symname"')
    (SCHEMATIC / (cell + ".sym")).write_text(symbol)

(SCHEMATIC / "xschemrc").write_text(header +
    "source $env(PDK_ROOT)/sky130A/libs.tech/xschem/xschemrc\n"
    "set candidate_dir [file dirname [file normalize [info script]]]\n"
    "set XSCHEM_LIBRARY_PATH $candidate_dir:$XSCHEM_LIBRARY_PATH\n"
    "append XSCHEM_LIBRARY_PATH :/foss/designs\n"
    "set spiceprefix 1\n")
print(DEST)
