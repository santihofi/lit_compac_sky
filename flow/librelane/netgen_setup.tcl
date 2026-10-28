#---------------------------------------------------------------
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
#
# Setup file for netgen LVS of chip_top, selected with NETGEN_SETUP in config.yaml.
#
# It is the sky130A setup of the PDK plus the physical-only cells. The PDK setup ignores the fill, tap and
# fake diode cells only when MAGIC_EXT_USE_GDS is set, that is when Magic extracts the layout from the GDS.
# This chip is extracted from the DEF, because Magic cannot read the GDS of the OpenRAM SRAM macro (see
# the comment in config.yaml), and in that flow every cell is a black box whose well pins VPB and VNB have
# no connection to follow: the layout side then shows one isolated net per cell while the netlist side has
# them on VPWR and VGND. The cells below carry no logic, so ignoring them costs no coverage, and every
# cell that does carry logic is still compared. The tie cell conb_1 is in the list for the same reason:
# its only pins besides HI and LO are the supplies and the two well pins, so the isolated well net of the
# layout side has nothing to match against. Its HI and LO nets stay and are compared.
#---------------------------------------------------------------

source $::env(PDK_ROOT)/$::env(PDK)/libs.tech/netgen/sky130A_setup.tcl

set physical_only {
    {sky130_fd_sc_[^_]+__decap_[[:digit:]]+}
    {sky130_fd_sc_[^_]+__fill_[[:digit:]]+}
    {sky130_fd_sc_[^_]+__fillerhd_[[:digit:]]+}
    {sky130_fd_sc_[^_]+__tapvpwrvgnd_[[:digit:]]+}
    {sky130_fd_sc_[^_]+__tap_[[:digit:]]+}
    {sky130_ef_sc_[^_]+__decap_[[:digit:]]+}
    {sky130_ef_sc_[^_]+__fakediode_[[:digit:]]+}
    {sky130_fd_sc_[^_]+__conb_[[:digit:]]+}
}

foreach pattern $physical_only {
    foreach cell $cells1 {
        if {[regexp $pattern $cell match]} {
            ignore class "-circuit1 $cell"
        }
    }
    foreach cell $cells2 {
        if {[regexp $pattern $cell match]} {
            ignore class "-circuit2 $cell"
        }
    }
}
