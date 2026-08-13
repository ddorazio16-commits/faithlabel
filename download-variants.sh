#!/usr/bin/env bash
# Downloads + optimises every variant gallery image listed in dl-manifest.tsv.
set -uo pipefail
cd "$(dirname "$0")"
UA="Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/122.0 Safari/537.36"
n=0; ok=0; fail=0
while IFS=$'\t' read -r url local; do
  [ -z "$url" ] && continue
  n=$((n+1))
  mkdir -p "$(dirname "$local")"
  [ -s "$local" ] && { ok=$((ok+1)); continue; }   # already downloaded
  tmp="/tmp/flv-$$.png"
  if curl -sfL -A "$UA" "$url" -o "$tmp" 2>/dev/null; then
    if sips -s format jpeg -s formatOptions 86 -Z 1200 "$tmp" --out "$local" >/dev/null 2>&1; then
      ok=$((ok+1))
    else fail=$((fail+1)); echo "sips-fail $local"; fi
    rm -f "$tmp"
  else fail=$((fail+1)); echo "curl-fail $url"; fi
done < dl-manifest.tsv
echo "DONE total=$n ok=$ok fail=$fail size=$(du -sh assets/products | cut -f1)"
