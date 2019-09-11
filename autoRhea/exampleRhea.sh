#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
INPUT="$DIR/input"
OUTDIR="$DIR/output"
mkdir -p "$OUTDIR"
rm "$OUTDIR"/*.*

set -euo pipefail


OTU="$INPUT/otutab.tsv"
TREE="$INPUT/pruned.tree"
META="$INPUT/mapping_auto.tsv"
NORM="$OUTDIR/otutab-norm.tab"


echo "[0] Check input files"
if [ ! -e "$OTU" ];then echo "Missing $OTU"; exit 1; fi



set -euxo pipefail
echo "[1] Normalize"
Rscript --vanilla normalize.R "$OTU" "$OUTDIR" 2> "$OUTDIR/norm.log"

echo "[2] Alpha diversity"
Rscript --vanilla alpha.R "$NORM" "$OUTDIR" 2> "$OUTDIR/alpha.log"

if [ ! -e "$TREE" ];then echo "Missing $TREE"; exit 1; fi
if [ ! -e "$META" ];then echo "Missing $META"; exit 1; fi

echo "[3] Beta"
#OTUTAB_NORMALIZED METADATA TREE CATEGORY OUTPUT_DIR
Rscript --vanilla beta.R "$NORM" "$META" "$TREE" "Treatment" "$OUTDIR" 2> "$OUTDIR/beta.R"
