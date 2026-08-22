#!/usr/bin/env python3
"""Build the concrete-flatlay work-list: for each product color, pick the best
real source photo (prefer a spread flat that shows the design; else the color's
featured image). Output /tmp/worklist.json = [{slug,color,src,url}]."""
import json, os

ROOT="/Users/donatodorazio/faithlabel"
BASE="https://faithlabelshop.com/"
data=json.loads((s:=open(f"{ROOT}/data.js").read())[s.index('['):s.rindex(']')+1])
manifest=json.load(open("/tmp/shots/manifest.json"))

# index->type per product (from the shot-type classification pass)
CLS={
 "christian-unisex-crewneck":{str(i):"flat" for i in range(16)},
 "faith-over-fear-crewneck-a":{"0":"flat","1":"closeup","2":"model","3":"flat","4":"model","5":"flat","6":"flat","7":"closeup"},
 "john-146-crewneck":{"0":"model","1":"flat","2":"flat","3":"model","4":"model","5":"flat","6":"model","7":"flat","8":"model","9":"closeup"},
 "crusader-deus-vult-hoodie":{"0":"model","1":"closeup","2":"model","3":"closeup","4":"flat","5":"model","6":"closeup"},
 "exodus-1414-hoodie":{"0":"flat","1":"model","2":"flat","3":"model","4":"flat","5":"model","6":"model","7":"model","8":"model","9":"flat","10":"model","11":"flat","12":"closeup","13":"model"},
 "exodus-1414-hoodie-2":{"0":"closeup","1":"flat","2":"flat","3":"closeup","4":"model","5":"closeup","6":"closeup","7":"flat","8":"model","9":"flat","10":"closeup","11":"flat","12":"closeup","13":"model","14":"flat"},
 "faith-over-fear-crewneck-b":{"0":"flat","1":"closeup","2":"flat","3":"model","4":"model","5":"model","6":"flat","7":"closeup","8":"flat","9":"model","10":"flat","11":"model","12":"flat","13":"model","14":"flat","15":"model"},
 "faith-over-fear-hoodie":{"0":"flat","1":"closeup","2":"flat","3":"closeup","4":"model","5":"flat","6":"closeup"},
 "god-is-good-hoodie":{"0":"model","1":"flat","2":"closeup","3":"flat","4":"flat","5":"flat","6":"closeup","7":"flat"},
 "isaiah-4319-hoodie":{"0":"flat","1":"model","2":"model","3":"model","4":"model","5":"flat","6":"model","7":"model","8":"flat","9":"model"},
 "jesus-king-of-kings-tshirt":{"0":"flat","1":"flat","2":"flat","3":"flat"},
 "john-146-hoodie":{"0":"closeup","1":"flat","2":"closeup","3":"flat","4":"closeup","5":"flat","6":"closeup","7":"flat","8":"flat","9":"flat","10":"closeup","11":"flat","12":"closeup","13":"flat","14":"model","15":"flat"},
 "matthew-1926-hoodie":{"0":"flat","1":"model","2":"flat","3":"model","4":"flat","5":"model","6":"flat","7":"model","8":"flat","9":"model","10":"flat","11":"model"},
 "philippians-413-hoodie":{"0":"flat","1":"model","2":"flat","3":"model","4":"flat","5":"model","6":"flat","7":"model","8":"flat","9":"model","10":"flat"},
 "proverbs-35-hoodie":{**{str(i):"flat" for i in range(16)},"8":"model","9":"model"},
 # batch 5 (hand-classified): folded fronts -> "closeup" (not preferred), spread flats -> "flat"
 "psalm-231-hoodie":{"0":"closeup","1":"closeup","2":"closeup","3":"model","4":"closeup","5":"model","6":"closeup","7":"model","8":"closeup","9":"flat","10":"model","11":"closeup","12":"model"},
 "trust-in-god-hoodie":{"0":"closeup","1":"flat","2":"closeup","3":"flat","4":"closeup","5":"flat","6":"flat","7":"model","8":"model","9":"closeup","10":"flat","11":"closeup","12":"flat"},
 "walk-by-faith-hoodie":{"0":"closeup","1":"flat","2":"flat","3":"closeup","4":"flat","5":"closeup","6":"flat","7":"model","8":"closeup","9":"flat","10":"closeup","11":"model","12":"closeup","13":"flat"},
}
# stem -> type per product
stemtype={}
for slug,m in manifest.items():
    stems=m["images"]; cls=CLS.get(slug,{})
    stemtype[slug]={stems[int(i)]:t for i,t in cls.items() if int(i)<len(stems)}

work=[]; fallback=[]
for p in data:
    slug=p["slug"]; st=stemtype.get(slug,{})
    for col in p["colors"]:
        imgs=col["images"]
        stem=lambda pth: os.path.splitext(os.path.basename(pth))[0]
        flats=[im for im in imgs if st.get(stem(im))=="flat"]
        src = flats[0] if flats else (imgs[0] if imgs else None)
        if not src: continue
        if not flats: fallback.append(f"{slug}/{col['name']}")
        work.append({"slug":slug,"color":col["name"],"src":src,"url":BASE+src})
json.dump(work, open("/tmp/worklist.json","w"), indent=1)
print(f"work items (colors): {len(work)}")
print(f"colors with a real flat source: {len(work)-len(fallback)}; fell back to featured (no flat): {len(fallback)}")
print("fallbacks:", fallback)
PY
