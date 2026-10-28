#!/bin/bash
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
#
# Chip top finishing script: Logo addition and fill pattern generation
# Input is a top GDS without filling
# Output is a top GDS with the logo added and filling on all layers
# Usage: ./add_logo_fill.sh <top cell>, make add-logo-fill passes TOP from the Makefile

# Abort on the first failing step instead of reporting success at the end.
set -eo pipefail

DESIGN="$1"
if [ -z "$DESIGN" ]; then
    echo "[ERROR] Usage: ./add_logo_fill.sh <top cell>"
    exit 1
fi
SCRIPTS_DIR="../flow/artistic/scripts"
GDS_DIR="../layout"
IMG_DIR="../flow/logo"
TOP_METAL_LAYER=72       # met5
TOP_METAL_DATATYPE=20    # drawing, sky130 uses 72/20 and the ArtistIC scripts default to datatype 0

# Floorplan coordinates in um
DIE_LLX=0      # Die lower-left X coordinate (layout origin)
DIE_LLY=0      # Die lower-left Y coordinate (layout origin)
DIE_URX=1600   # Die upper-right X coordinate
DIE_URY=1600   # Die upper-right Y coordinate
CORE_LLX=300   # Core lower-left X coordinate
CORE_LLY=300   # Core lower-left Y coordinate
CORE_URX=1300  # Core upper-right X coordinate
CORE_URY=1300  # Core upper-right Y coordinate

# Logo placement relative to the core lower-left corner in um
LOGO_CORE_MARGIN_LEFT=100
LOGO_CORE_MARGIN_BOTTOM=230

# meerkat.py expects die-relative margins from layout origin (0,0)
LOGO_MARGIN_LEFT=$((CORE_LLX + LOGO_CORE_MARGIN_LEFT))
LOGO_MARGIN_BOTTOM=$((CORE_LLY + LOGO_CORE_MARGIN_BOTTOM))

GDS_IN="${GDS_DIR}/${DESIGN}.gds.gz"
GDS_M5="${GDS_DIR}/${DESIGN}_m5.gds"
GDS_LOGO="${GDS_DIR}/${DESIGN}_logo.gds"
GDS_OUT="${GDS_DIR}/${DESIGN}_logo.gds.gz"
GDS_OUT_FILL="${GDS_DIR}/${DESIGN}_logo_fill.gds.gz"
LOGO_IMG="${IMG_DIR}/chip_logo_mono.png"

# ─── Logo sizing guide ────────────────────────────────────────────────────────
# meerkat.py maps each image pixel to one GDS pixel of size PIXSZ = 2 µm.
# The logo image must therefore satisfy:
#
#   img_width  [px] = logo_width  [µm] / 2 ≤ (die_width  - 2 * die_margin_left)   / 2
#   img_height [px] = logo_height [µm] / 2 ≤ (die_height - 2 * die_margin_bottom) / 2
#
# This uses symmetric margins on both sides:
#   left margin = right margin = die_margin_left
#   bottom margin = top margin = die_margin_bottom
#
# Core-relative margins are converted to die-relative margins using:
#   die_margin_left   = CORE_LLX + LOGO_CORE_MARGIN_LEFT
#   die_margin_bottom = CORE_LLY + LOGO_CORE_MARGIN_BOTTOM
#
# For this chip (die = 1600 x 1600 µm, core LL = (300,300) µm,
# logo core-relative margins = (100,230) µm):
#
#   die margins = (LOGO_MARGIN_LEFT, LOGO_MARGIN_BOTTOM) = (400,530) µm
#   max img_width  = (1600 - 2*400) / 2 = 400 px → 800 µm on-chip
#   max img_height = (1600 - 2*530) / 2 = 270 px → 540 µm on-chip
#
# Current image (chip_logo_mono.png): 400x270 px → 800x540 µm on-chip
#   placed symmetrically with die margins (left,right,bottom,top)
#   = (400,400,530,530) µm
# ─────────────────────────────────────────────────────────────────────────────

echo "[INFO] Adding logo and fill to ${GDS_IN}"

# Export top metal layer met5
# meerkat_interface.py arguments:
#   -i  Input GDS (vanilla chip without logo)
#   -m  Output top-metal-only GDS used as mask for logo placement
#   -g  Output logo GDS (will be written by meerkat.py)
#   -o  Merged output GDS (chip + logo)
#   -w  Work directory for the generated meerkat_design.py interface file
#   -l  Logo layer number (met5 = 72)
#   -d  Logo datatype (met5 drawing = 20)
#   -n  Name of the new merged top-level cell in the output GDS
python3 "${SCRIPTS_DIR}/meerkat_interface.py" \
    -i "$GDS_IN" \
    -m "$GDS_M5" \
    -g "$GDS_LOGO" \
    -o "$GDS_OUT" \
    -w "$PWD" \
    -l "$TOP_METAL_LAYER" \
    -d "$TOP_METAL_DATATYPE" \
    -n "${DESIGN}_logo_fill" \
    > /dev/null
klayout -zz -rm "${SCRIPTS_DIR}/export_top_metal.py"

# export_top_metal.py exits 0 when the layer is not in the GDS, so check the file itself.
[ -f "$GDS_M5" ] || { echo "[ERROR] no ${TOP_METAL_LAYER}/${TOP_METAL_DATATYPE} shapes in ${GDS_IN}"; exit 1; }

# Transform logo to GDS
# meerkat.py arguments:
#   -m  Logo placement margins in um from die origin (0,0): left,bottom
#       (computed from core-relative placement variables above)
#   -i  Input logo image (monochrome PNG, 1-bit b/w)
#   -g  Top-metal GDS used as mask (existing metal is excluded from logo)
#   -l  Target layer number for the logo geometry
#   -d  Target datatype for the logo geometry
#   -n  Name of the logo cell written into the output GDS
#   -o  Output logo GDS file
python3 "${SCRIPTS_DIR}/meerkat.py" \
    -m "${LOGO_MARGIN_LEFT},${LOGO_MARGIN_BOTTOM}" \
    -i "$LOGO_IMG" \
    -g "$GDS_M5" \
    -l "$TOP_METAL_LAYER" \
    -d "$TOP_METAL_DATATYPE" \
    -n "$DESIGN" \
    -o "$GDS_LOGO" \
    > /dev/null

# Merge logo into chip
klayout -zz -rm "${SCRIPTS_DIR}/merge_logo.py"

echo "[INFO] Logo added. Now adding fill patterns..."

# Add fill patterns with the PDK fill generator. sky130 has no fill keep-out layer, the generator keeps
# its distance to every drawn shape itself, so the logo needs no exclusion rectangles around it.
# generate_fill.py runs Magic tile by tile (700 um squares) on a copy of the layout in a work folder
# and writes <design>_fill_pattern.gds.gz next to it, which is then placed into the chip GDS.
FILL_DIR="${PWD}/fill_work"
rm -rf "$FILL_DIR"
mkdir -p "$FILL_DIR"
gunzip -c "$GDS_OUT" > "${FILL_DIR}/${DESIGN}_logo.gds"
# generate_fill.py starts Magic on the sky130A-GDS tech, and the PDK magicrc loads sky130A.tech over it
# and quits. Magic reads $HOME/.magicrc, so the run gets a home of its own with an empty one.
echo '# empty, keeps the -T tech generate_fill.py asks for' > "${FILL_DIR}/.magicrc"
(cd "$FILL_DIR" && HOME="$FILL_DIR" python3 "${PDKPATH}/libs.tech/magic/generate_fill.py" "${DESIGN}_logo.gds" > generate_fill.log 2>&1) || {
    echo "[ERROR] generate_fill.py failed, see ${FILL_DIR}/generate_fill.log"; exit 1; }
FILL_GDS="${FILL_DIR}/${DESIGN}_logo_fill_pattern.gds.gz"
[ -f "$FILL_GDS" ] || { echo "[ERROR] generate_fill.py wrote no ${FILL_GDS}"; exit 1; }

klayout -zz \
    -rd "design=$GDS_OUT" \
    -rd "fill=$FILL_GDS" \
    -rd "out=$GDS_OUT_FILL" \
    -r merge_gds.py

# Cleanup intermediate files
rm -rf "$FILL_DIR"
rm -f "$GDS_M5" "$GDS_LOGO" "$GDS_OUT" meerkat_design.py

echo "[INFO] Finished. Output GDS: ${GDS_OUT_FILL}"
