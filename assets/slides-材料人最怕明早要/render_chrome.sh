#!/bin/bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML="file://${DIR}/render.html"

for n in 1 2 3 4 5 6 7 8; do
  out=$(printf "%s/%02d.png" "$DIR" "$n")
  tmp=$(printf "%s/.tmp-%02d.png" "$DIR" "$n")
  "$CHROME" \
    --headless=new \
    --disable-gpu \
    --hide-scrollbars \
    --force-device-scale-factor=1 \
    --window-size=1080,1440 \
    --screenshot="$tmp" \
    "${HTML}?n=${n}" \
    >/dev/null 2>&1
  # Chrome sometimes writes slightly different sizes; normalize with sips
  sips -z 1440 1080 "$tmp" --out "$out" >/dev/null
  rm -f "$tmp"
  echo "ok $out"
done
