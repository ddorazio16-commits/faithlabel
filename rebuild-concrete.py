#!/usr/bin/env python3
"""Point every product color at its new grey-concrete flat-lay mockup
   (assets/products/<slug>/<colorslug>-concrete.jpg) if it exists on disk.
   Rewrites data.js. Grid card uses the first color's concrete image."""
import json, os, re

ROOT="/Users/donatodorazio/faithlabel"
def cslug(c): return re.sub(r'[^a-z0-9]+','-',c.lower()).strip('-')
s=open(f"{ROOT}/data.js").read()
head=s[:s.index('window.PRODUCTS')]
data=json.loads(s[s.index('['):s.rindex(']')+1])

updated=missing=0; missing_list=[]
for p in data:
    slug=p["slug"]
    for col in p["colors"]:
        cpath=f"assets/products/{slug}/{cslug(col['name'])}-concrete.jpg"
        if os.path.exists(f"{ROOT}/{cpath}") and os.path.getsize(f"{ROOT}/{cpath}")>10000:
            col["images"]=[cpath]; updated+=1
        else:
            missing+=1; missing_list.append(f"{slug}/{col['name']}")
    # grid card image = first color's concrete; hover = second color's if present
    imgs=[c["images"][0] for c in p["colors"] if c["images"]]
    if imgs:
        p["img"]=imgs[0]; p["imgAlt"]=imgs[1] if len(imgs)>1 else imgs[0]

open(f"{ROOT}/data.js","w").write(head+"window.PRODUCTS = "+json.dumps(data,ensure_ascii=False,indent=0)+";\n")
print(f"colors set to concrete: {updated}; missing (kept old): {missing}")
if missing_list: print("MISSING:", missing_list)
