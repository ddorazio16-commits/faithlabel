#!/usr/bin/env python3
"""Give every color a front+back image pair on grey concrete.
   Each color has:  <cslug>-concrete.jpg  (original) and  <cslug>-concrete-b.jpg (new second view).
   images = [hero(big design), other].  Grid card uses the hero image.
   For a handful of colors the newly generated -b image IS the big design
   (products shot only on the small-print side, plus 5 fixed odd-one-out colors),
   so -b goes first for those."""
import json, os, re

ROOT = "/Users/donatodorazio/faithlabel"
def cslug(c): return re.sub(r'[^a-z0-9]+', '-', c.lower()).strip('-')

# products where the -b (generated) image is the big/hero design for ALL colors
B_IS_HERO_PRODUCTS = {"matthew-1926-hoodie", "proverbs-35-hoodie", "psalm-231-hoodie"}
# individual (slug, colorslug) whose primary side was regenerated into -b (odd-one-out fixes)
B_IS_HERO_COLORS = {
    ("exodus-1414-hoodie-2", "forest-green"),
    ("faith-over-fear-crewneck-a", "navy"),
    ("faith-over-fear-crewneck-a", "white"),
    ("god-is-good-hoodie", "sand"),
    ("trust-in-god-hoodie", "royal"),
}

s = open(f"{ROOT}/data.js").read()
head = s[:s.index('window.PRODUCTS')]
data = json.loads(s[s.index('['):s.rindex(']')+1])

paired = missing = 0
missing_list = []
for p in data:
    slug = p["slug"]
    for col in p["colors"]:
        cs = cslug(col["name"])
        a = f"assets/products/{slug}/{cs}-concrete.jpg"      # original
        b = f"assets/products/{slug}/{cs}-concrete-b.jpg"    # generated second view
        pa = os.path.exists(f"{ROOT}/{a}")
        pb = os.path.exists(f"{ROOT}/{b}")
        if pa and pb:
            b_is_hero = slug in B_IS_HERO_PRODUCTS or (slug, cs) in B_IS_HERO_COLORS
            col["images"] = [b, a] if b_is_hero else [a, b]
            paired += 1
        elif pa:
            col["images"] = [a]
            missing += 1; missing_list.append(f"{slug}/{col['name']} (no -b)")
        else:
            missing += 1; missing_list.append(f"{slug}/{col['name']} (no concrete)")
    # grid card = first color's hero image; hover = its second image if present
    heroes = [c["images"][0] for c in p["colors"] if c.get("images")]
    if heroes:
        p["img"] = heroes[0]
        first = p["colors"][0]
        p["imgAlt"] = first["images"][1] if len(first.get("images", [])) > 1 else heroes[0]

open(f"{ROOT}/data.js", "w").write(head + "window.PRODUCTS = " + json.dumps(data, ensure_ascii=False, indent=0) + ";\n")
print(f"colors with front+back pair: {paired}; incomplete: {missing}")
if missing_list: print("INCOMPLETE:", missing_list)
