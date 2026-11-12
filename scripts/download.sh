#!/bin/sh
# Download the WMT24 general-task files this project reads, at a pinned commit.
# Source: https://github.com/wmt-conference/wmt24-news-systems (no license stated).
# Everything lands in data/ (git-ignored). Nothing downloaded is committed.
#   sh scripts/download.sh
set -eu
REPO=https://github.com/wmt-conference/wmt24-news-systems
COMMIT=fabe1f81d65449b3e3f9f8d37da280fa6cf3650a   # 2025-11-20
cd "$(dirname "$0")/.."
if [ ! -d data/.git ]; then
  git clone --quiet --filter=blob:none --no-checkout "$REPO" data
fi
cd data
PATTERNS="/humeval/esa_generalMT2024_wave*.csv /humeval/annotator_mapping.json /humeval/merge_to_jsonl.py"
for p in en-cs en-es en-hi en-is en-ja en-ru en-uk en-zh; do
  PATTERNS="$PATTERNS /txt/sources/$p.txt /txt/references/$p.* /txt/documents/$p.docs /txt/metadata/$p.jsonl /txt/system-outputs/$p/"
done
set -f; git sparse-checkout set --no-cone $PATTERNS; set +f
git checkout --quiet "$COMMIT"
echo "data/ at $(git rev-parse HEAD)"; du -sh . | cut -f1
