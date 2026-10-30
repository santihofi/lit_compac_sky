#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Explore the mapped CMFB's degeneration with the actual loop-gain bench."""
from pathlib import Path
import re,yaml
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'verification/porting/sky_core_validation'
s=(p/'tb/stability.spice').read_text()
s=re.sub(r'^(XRS\d+ .*?\bL=)22.705',r'\1{{22.705*cmfb_rscale}}',s,flags=re.M)
(p/'tb/stability_sizing.spice').write_text(s)
d=yaml.safe_load((p/'datasheets/stability.yaml').read_text())
d['parameters'].update(cmfb_rscale=[1,1.5,2,3],c_load=['30f','100f'])
d['tests']={'stability_sizing':d['tests']['stability']}
(p/'datasheets/stability_sizing.yaml').write_text('# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'+yaml.safe_dump(d,sort_keys=False))

# Separate the integrating loop from the fast loop before moving the latter.
s=re.sub(r'(^XMC .*?)(?=^Rtap_R2)',lambda m:m[0].replace('1.0*power_m','cmfb_cscale*power_m').replace('1*power_m','cmfb_cscale*power_m'),s,flags=re.M|re.S)
q=ROOT/'verification/porting/sky_cmfb_options'
(q/'tb').mkdir(parents=True,exist_ok=True)
(q/'datasheets').mkdir(exist_ok=True)
(q/'tb/stability_sizing.spice').write_text(s)
d['parameters'].update(cmfb_rscale=[0.5,1,1.5],cmfb_cscale=[4,16],c_load=['30f','100f'])
(q/'datasheets/stability_sizing.yaml').write_text((p/'datasheets/stability_sizing.yaml').read_text().split('parameters:')[0]+yaml.safe_dump(d,sort_keys=False))
(q/'settings.json').write_text('{"num_cores": 4, "sim_timeout_sec": 180}'+chr(10))
