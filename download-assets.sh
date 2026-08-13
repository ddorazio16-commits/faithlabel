#!/usr/bin/env bash
# Downloads the real FaithLabel product mockups (concrete backgrounds) into assets/products/
# so the site is fully self-contained and never depends on the temporary Shopify dev store.
set -euo pipefail
cd "$(dirname "$0")"
CDN="https://w2fb1a-q3.myshopify.com/cdn/shop/files"
W="width=1000"
DIR="assets/products"
mkdir -p "$DIR"

# format: slug|primary_file|alt_file
items=(
"christian-unisex-crewneck|20260515182945-1f1508c0-c33b-6ea0-8a3c-42eb6282f2bc.png|20260308060846-1f11ab54-45d0-69ec-baf5-0eea887c3cf9.png"
"faith-over-fear-crewneck-a|20260515173606-1f150848-d206-68a4-84d2-6a710bcbbfe3.png|20260302232044-1f1168e7-0189-628e-88ae-46ffd1b82ce1.png"
"john-146-crewneck|20260515182454-1f1508b5-ed2b-6450-ab96-7a0f1fb71c58.png|20260308062502-1f11ab78-a19b-6bc2-b318-0eea887c3cf9.png"
"crusader-deus-vult-hoodie|20260515173928-1f150850-599b-68ee-bb54-469dd08d68e5.png|20260302232748-1f1168f6-c756-6bec-950b-82ce8b945f9e.png"
"exodus-1414-hoodie|20260504203234-1f147f86-1cb0-625c-974e-e2aec25ea8ad.png|20260302230822-1f1168cb-5861-6744-807d-82ce8b945f9e.png"
"faith-over-fear-crewneck-b|20260308093529-1f11ad22-53c9-6ccc-b71e-6e959b62645e.png|20260302202231-1f116758-a872-625c-a328-6e703700052a.png"
"faith-over-fear-hoodie|20260308090407-1f11acdc-37c8-6b04-b6b3-1e453086ceb1.png|20260302175022-1f116604-90be-6e80-9965-eec1f394ab12.png"
"god-is-good-hoodie|20260515175705-1f150877-bc7a-6984-9cb9-92ca0abd6c08.png|20260305041238-1f118498-c2bf-6dd2-a458-d6ebe8611f23.png"
"isaiah-4319-hoodie|20260308092822-1f11ad12-674f-6716-8df5-8ebcb801a8ed.png|20260302155501-1f116502-bf18-681a-a8b8-d2f16ff77e32.png"
"jesus-king-of-kings-tshirt|20260320032746-1f1240cc-3c71-6f0a-92f5-769259c4e595.png|20260320032754-1f1240cc-830a-6052-9b9f-d2ba25705abd.png"
"john-146-hoodie|20260504202759-1f147f7b-e2fb-6d5e-a9e2-2e5d780a8e79.png|20260308085336-1f11acc4-b106-6272-832c-32eddb289ad1.png"
"matthew-1926-hoodie|20260504203519-1f147f8c-41d0-6dd8-8759-aece7a7d7c9e.png|20260302201620-1f11674a-d5e0-6fc6-9afe-1289e00b6ea2.png"
"philippians-413-hoodie|20260515181814-1f1508a7-054b-61d4-95bb-c2f79ebd8dc1.png|20260305044917-1f1184ea-ab7b-6e62-8d3f-8e3fafc33b1d.png"
"proverbs-35-hoodie|20260515181126-1f150897-cc8f-6372-99f7-2e7f25ad732b.png|20260305043014-1f1184c0-133a-6006-bde2-1e62f732020c.png"
"psalm-231-hoodie|20260515175247-1f15086e-1f06-6c60-90bd-6a710bcbbfe3.png|20260302233601-1f116909-2c5c-691c-8d7e-9ada144e9a70.png"
"trust-in-god-hoodie|20260515180110-1f150880-d82d-6448-b1f6-7a0f1fb71c58.png|20260308065421-1f11abba-294f-6b36-bfa2-2ea26e8f940f.png"
"walk-by-faith-hoodie|20260504221058-1f148062-0e10-65f8-8d71-46d71a06a235.png|20260302203142-1f11676d-2a60-61ce-9902-86d7dfe453cc.png"
)

for row in "${items[@]}"; do
  IFS='|' read -r slug primary alt <<< "$row"
  echo "-> $slug"
  curl -sfL "${CDN}/${primary}?${W}" -o "${DIR}/${slug}.png"
  curl -sfL "${CDN}/${alt}?${W}"     -o "${DIR}/${slug}-alt.png"
done

# Optimise for the web: PNG (~1.4MB) -> JPG (~200KB), max 900px, quality 82.
# Uses macOS `sips`; swap for ImageMagick (`convert`) on Linux if needed.
echo "Optimising images…"
for f in "$DIR"/*.png; do
  sips -s format jpeg -s formatOptions 82 -Z 900 "$f" --out "${f%.png}.jpg" >/dev/null 2>&1
  rm "$f"
done

echo "Ready — $(ls -1 "$DIR" | wc -l | tr -d ' ') optimised images ($(du -sh "$DIR" | cut -f1))."
