#!/usr/bin/env python3
"""Merge the 5 vision-classification results into color-map.json
   ({slug: {image-stem: color}}), validated against each product's real
   color list and the featured-image anchors."""
import json, os

CLS = {
 "christian-unisex-crewneck": {"0":"Ash","1":"Dark Chocolate","2":"Light Pink","3":"Royal","4":"Ash","5":"Navy","6":"White","7":"Black","8":"Sand","9":"Dark Chocolate","10":"Light Pink","11":"Navy","12":"Sand","13":"White","14":"Black","15":"Royal"},
 "faith-over-fear-crewneck-a": {"0":"Ash","1":"Ash","2":"Navy","3":"White","4":"Black","5":"Navy","6":"White","7":"Black"},
 "john-146-crewneck": {"0":"Ash","1":"Light Blue","2":"Ash","3":"White","4":"Sand","5":"Light Pink","6":"Light Blue","7":"Light Pink","8":"Sand","9":"White"},
 "crusader-deus-vult-hoodie": {"0":"Charcoal","1":"Black","2":"Black","3":"White","4":"Charcoal","5":"White","6":"Black"},
 "exodus-1414-hoodie": {"0":"Charcoal","1":"Navy","2":"Navy","3":"White","4":"Maroon","5":"Charcoal","6":"Forest Green","7":"Forest Green","8":"Black","9":"Maroon","10":"Navy","11":"White","12":"Black","13":"Forest Green"},
 "exodus-1414-hoodie-2": {"0":"Charcoal","1":"Maroon","2":"Navy","3":"White","4":"Black","5":"Sand","6":"Charcoal","7":"Light Pink","8":"Maroon","9":"Navy","10":"Sand","11":"White","12":"Black","13":"Forest Green","14":"Light Pink"},
 "faith-over-fear-crewneck-b": {"0":"Ash","1":"White","2":"Light Pink","3":"Dark Chocolate","4":"Black","5":"Royal","6":"Ash","7":"Sand","8":"Navy","9":"Dark Chocolate","10":"Light Pink","11":"Navy","12":"Sand","13":"White","14":"Black","15":"Royal"},
 "faith-over-fear-hoodie": {"0":"Navy","1":"White","2":"Black","3":"Black","4":"Navy","5":"White","6":"Black"},
 "god-is-good-hoodie": {"0":"Sand","1":"Light Pink","2":"Sand","3":"Black","4":"Military Green","5":"Black","6":"Light Pink","7":"Military Green"},
 "isaiah-4319-hoodie": {"0":"Sand","1":"Sand","2":"Sand","3":"White","4":"Military Green","5":"Sport Grey","6":"Sport Grey","7":"White","8":"Sport Grey","9":"Military Green"},
 "jesus-king-of-kings-tshirt": {"0":"Clay","1":"Ocean","2":"Smoke","3":"Fern"},
 "john-146-hoodie": {"0":"Charcoal","1":"White","2":"Black","3":"Sand","4":"Maroon","5":"Forest Green","6":"Charcoal","7":"Navy","8":"Light Pink","9":"Maroon","10":"Navy","11":"Sand","12":"White","13":"Black","14":"Forest Green","15":"Light Pink"},
 "matthew-1926-hoodie": {"0":"Cocoa","1":"Forest Green","2":"Cocoa","3":"Charcoal","4":"Maroon","5":"Navy","6":"Black","7":"Charcoal","8":"Maroon","9":"Navy","10":"Black","11":"Forest Green"},
 "philippians-413-hoodie": {"0":"Charcoal","1":"Charcoal","2":"Royal","3":"Maroon","4":"Navy","5":"Black","6":"Maroon","7":"Navy","8":"Royal","9":"Black","10":"Forest Green"},
 "proverbs-35-hoodie": {"0":"Charcoal","1":"Maroon","2":"White","3":"Black","4":"Sand","5":"Forest Green","6":"Charcoal","7":"Navy","8":"Light Pink","9":"Maroon","10":"Navy","11":"Sand","12":"White","13":"Black","14":"Forest Green","15":"Light Pink"},
 "psalm-231-hoodie": {"0":"Charcoal","1":"White","2":"Sand","3":"Forest Green","4":"Navy","5":"Light Pink","6":"Maroon","7":"Navy","8":"Sand","9":"White","10":"Black","11":"Forest Green","12":"Light Pink"},
 "trust-in-god-hoodie": {"0":"Charcoal","1":"Royal","2":"Royal","3":"Black","4":"Maroon","5":"Forest Green","6":"Charcoal","7":"Navy","8":"Maroon","9":"Navy","10":"Royal","11":"Black","12":"Forest Green"},
 "walk-by-faith-hoodie": {"0":"Charcoal","1":"Black","2":"White","3":"Maroon","4":"Forest Green","5":"Charcoal","6":"Royal","7":"Maroon","8":"Royal","9":"Sand","10":"White","11":"Black","12":"Forest Green","13":"Light Pink"},
}

manifest = json.load(open("/tmp/sheets/manifest.json"))
colormap, issues = {}, []
for slug, cls in CLS.items():
    m = manifest[slug]
    stems = [os.path.splitext(b)[0] for b in m["images"]]
    valid = set(m["colors"])
    cmap = {}
    for i_str, color in cls.items():
        i = int(i_str)
        if color not in valid and color != "generic":
            issues.append(f"{slug}: '{color}' NOT in {sorted(valid)}")
        if i < len(stems): cmap[stems[i]] = color
    # anchors: featured index must map to its color
    for color, idx in m["featured"].items():
        st = stems[idx]
        if cmap.get(st) != color:
            issues.append(f"{slug}: anchor {color}@{idx} was '{cmap.get(st)}' -> forced")
            cmap[st] = color
    if len(cmap) != m["n"]: issues.append(f"{slug}: covered {len(cmap)}/{m['n']}")
    missing = valid - set(cmap.values())
    if missing: issues.append(f"{slug}: colors with NO image: {sorted(missing)}")
    colormap[slug] = cmap

json.dump(colormap, open("/Users/donatodorazio/faithlabel/color-map.json","w"), indent=1)
print(f"color-map.json written for {len(colormap)} products")
print("ISSUES:" if issues else "no issues — all colors covered, all anchors consistent")
for x in issues: print("  -", x)
