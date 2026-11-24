#!/usr/bin/env python3
"""Point data.js at the canonical mockup files.

Every color of every product has exactly two grey-concrete flat-lays:
    assets/products/<slug>/<colorslug>-front.jpg
    assets/products/<slug>/<colorslug>-back.jpg

Image order mirrors the Shopify store: each product leads with the side Shopify
uses for its main product image (HERO side), and the grid card shows the same
color Shopify shows first (HERO color). The PDP opens on that color too.

Run after adding/replacing mockup files:  python3 rebuild-mockups.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
def cslug(c): return re.sub(r'[^a-z0-9]+', '-', c.lower()).strip('-')

# slug -> (side shown first, color shown on the grid card)  — taken from each product's first Shopify image
HERO = {
    "christian-unisex-crewneck":   ("front", "Dark Chocolate"),
    "faith-over-fear-crewneck-a":  ("back",  "Ash"),
    "john-146-crewneck":           ("front", "Light Blue"),
    "crusader-deus-vult-hoodie":   ("back",  "Black"),
    "exodus-1414-hoodie":          ("back",  "Navy"),
    "exodus-1414-hoodie-2":        ("back",  "Maroon"),
    "faith-over-fear-crewneck-b":  ("back",  "White"),
    "faith-over-fear-hoodie":      ("back",  "White"),
    "god-is-good-hoodie":          ("back",  "Light Pink"),
    "isaiah-4319-hoodie":          ("back",  "Sand"),
    "jesus-king-of-kings-tshirt":  ("front", "Smoke"),
    "john-146-hoodie":             ("back",  "White"),
    "matthew-1926-hoodie":         ("front", "Forest Green"),
    "philippians-413-hoodie":      ("front", "Charcoal"),
    "proverbs-35-hoodie":          ("front", "Maroon"),
    "psalm-231-hoodie":            ("front", "Forest Green"),
    "trust-in-god-hoodie":         ("front", "Royal"),
    "walk-by-faith-hoodie":        ("back",  "Black"),
}

s = open(f"{ROOT}/data.js").read()
head = s[:s.index('window.PRODUCTS')]
data = json.loads(s[s.index('['):s.rindex(']') + 1])

problems = []
for p in data:
    slug = p["slug"]
    first, hero_color = HERO[slug]
    order = [first, "back" if first == "front" else "front"]
    p["sides"] = order                      # which side each gallery image shows, in order
    for col in p["colors"]:
        cs = cslug(col["name"])
        imgs = []
        for side in order:
            rel = f"assets/products/{slug}/{cs}-{side}.jpg"
            if not os.path.exists(f"{ROOT}/{rel}") or os.path.getsize(f"{ROOT}/{rel}") < 20000:
                problems.append(rel)
            imgs.append(rel)
        col["images"] = imgs
    names = [c["name"] for c in p["colors"]]
    if hero_color not in names:
        problems.append(f"{slug}: hero color {hero_color!r} not in {names}")
        hero_color = names[0]
    p["heroColor"] = hero_color
    hero = next(c for c in p["colors"] if c["name"] == hero_color)
    p["img"], p["imgAlt"] = hero["images"][0], hero["images"][1]

if problems:
    print("MISSING / INVALID:"); [print("  ", x) for x in problems]; sys.exit(1)

open(f"{ROOT}/data.js", "w").write(head + "window.PRODUCTS = " + json.dumps(data, ensure_ascii=False, indent=0) + ";\n")
n = sum(len(p["colors"]) for p in data)
print(f"OK: {len(data)} products, {n} colors, {n*2} mockups (front + back each)")
