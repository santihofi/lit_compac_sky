#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Prove drawn candidate connectivity and parameters against the rendered deck."""
import argparse
import json
from pathlib import Path
import re

import numpy as np


def circuits(text):
    if "IS MISSING" in text:
        raise ValueError("Unresolved schematic symbol")
    text = re.sub(r"\n\+\s*", " ", text)
    result = {}
    for cell, ports, body in re.findall(
            r"^\.subckt (\w+) ([^\n]*)\n(.*?)^\.ends[^\n]*", text, re.M | re.S | re.I):
        devices = {}
        for line in body.splitlines():
            tokens = line.lower().split()
            if not tokens or tokens[0][0] not in "xr":
                continue
            if tokens[0][0] == "r":
                devices[tokens[0]] = (tokens[1:3], "resistor", {"value": tokens[3]})
            else:
                stop = next((i for i, t in enumerate(tokens) if "=" in t), len(tokens))
                props = dict(t.split("=", 1) for t in tokens[stop:])
                if tokens[stop-1].startswith("sky130_fd_pr__"):
                    props.setdefault("m", "1")
                devices[tokens[0]] = (tokens[1:stop-1], tokens[stop-1], props)
        result[cell.lower()] = (ports.lower().split(), devices)
    return result


def numeric(value):
    units = {"m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15}
    suffix = value[-1]
    return float(value[:-1]) * units[suffix] if suffix in units else float(value)


def compare(golden, drawn):
    report = {}
    for cell, (ports, devices) in golden.items():
        if cell not in drawn:
            raise ValueError("Missing drawn subcircuit " + cell)
        actual_ports, actual = drawn[cell]
        if ports != actual_ports:
            raise ValueError(f"{cell}: port order differs")
        if devices.keys() != actual.keys():
            raise ValueError(f"{cell}: instance differences {devices.keys() ^ actual.keys()}")
        mapping = dict(zip(ports, ports))
        reverse = dict(mapping)
        for name, (nodes, model, props) in devices.items():
            actual_nodes, actual_model, actual_props = actual[name]
            if model != actual_model or len(nodes) != len(actual_nodes):
                raise ValueError(f"{cell}/{name}: model or pin count differs")
            if props.keys() != actual_props.keys():
                raise ValueError(f"{cell}/{name}: parameter set differs {props.keys() ^ actual_props.keys()}")
            for key, value in props.items():
                if not np.isclose(numeric(value), numeric(actual_props[key]), rtol=2e-12, atol=1e-18):
                    raise ValueError(f"{cell}/{name}/{key}: {value} != {actual_props[key]}")
            for expected, observed in zip(nodes, actual_nodes):
                if expected in mapping and mapping[expected] != observed:
                    raise ValueError(f"{cell}/{name}: {expected} maps to both {mapping[expected]} and {observed}")
                if observed in reverse and reverse[observed] != expected:
                    raise ValueError(f"{cell}/{name}: short between {expected} and {reverse[observed]}")
                mapping[expected] = observed
                reverse[observed] = expected
        report[cell] = {"devices": len(devices), "nets": len(mapping), "ports": len(ports)}
    return {"status": "equivalent", "cells": report}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("golden", type=Path)
    parser.add_argument("drawn", type=Path, nargs="+")
    args = parser.parse_args()
    result = compare(circuits(args.golden.read_text()),
                     circuits("\n".join(p.read_text() for p in args.drawn)))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
