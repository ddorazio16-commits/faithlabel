#!/usr/bin/env python3
"""Turn catalog.json into:
   - data.js         : the PRODUCTS array the site consumes (variants + local image paths)
   - dl-manifest.tsv : url<TAB>localpath list for the image downloader
Local images live at assets/products/<slug>/<basename>.jpg
"""
import json, os

ROOT = "/Users/donatodorazio/faithlabel"
cat = json.load(open(f"{ROOT}/catalog.json"))
# {slug: {image-stem: color}} from the vision classification (build-colormap.py)
colormap = json.load(open(f"{ROOT}/color-map.json"))
def _stem(u): return os.path.splitext(os.path.basename(u))[0]

VERSE = {
 "christian-unisex-crewneck":"Faithful","faith-over-fear-crewneck-a":"Faith over Fear",
 "john-146-crewneck":"John 14:6","crusader-deus-vult-hoodie":"Deus Vult",
 "exodus-1414-hoodie":"Exodus 14:14","exodus-1414-hoodie-2":"Exodus 14:14",
 "faith-over-fear-crewneck-b":"Faith over Fear","faith-over-fear-hoodie":"Faith over Fear",
 "god-is-good-hoodie":"God is Good","isaiah-4319-hoodie":"Isaiah 43:19",
 "jesus-king-of-kings-tshirt":"King of Kings","john-146-hoodie":"John 14:6",
 "matthew-1926-hoodie":"Matthew 19:26","philippians-413-hoodie":"Philippians 4:13",
 "proverbs-35-hoodie":"Proverbs 3:5","psalm-231-hoodie":"Psalm 23:1",
 "trust-in-god-hoodie":"Trust in God","walk-by-faith-hoodie":"Walk by Faith",
}

def basename_jpg(url):
    b = url.split("/")[-1].split("?")[0]
    return os.path.splitext(b)[0] + ".jpg"

manifest = {}   # url -> localpath (dedup)
products = []
for p in cat:
    slug = p["slug"]
    cmap = colormap.get(slug, {})
    # Union of every image for this product (first-seen order) + each color's
    # featured flat-mockup, so we can regroup images by their true garment color.
    union, featured_url = [], {}
    for col in p["colors"]:
        if col["images"]:
            featured_url[col["name"]] = col["images"][0]
        for url in col["images"]:
            if url not in union:
                union.append(url)
    grouped = {c["name"]: [] for c in p["colors"]}
    for url in union:
        c = cmap.get(_stem(url))
        if c in grouped:
            grouped[c].append(url)
    colors = []
    for col in p["colors"]:
        name = col["name"]
        urls = grouped[name][:]
        fu = featured_url.get(name)          # flat mockup leads the gallery
        if fu:
            if fu in urls: urls.remove(fu)
            urls = [fu] + urls
        local = []
        for url in urls:
            fn = basename_jpg(url)
            lp = f"assets/products/{slug}/{fn}"
            manifest[url] = lp
            local.append(lp)
        colors.append({"name": name, "swatch": col["swatch"], "images": local})
    default = colors[0]["images"] if colors else []
    # Grid cards keep the curated concrete-background flatlay when we have it,
    # so the grid stays visually consistent; the PDP shows full color galleries.
    flat = f"assets/products/{slug}.jpg"
    flat_alt = f"assets/products/{slug}-alt.jpg"
    has_flat = os.path.exists(f"{ROOT}/{flat}")
    grid_img = flat if has_flat else (default[0] if default else "")
    grid_alt = flat_alt if os.path.exists(f"{ROOT}/{flat_alt}") else (default[1] if len(default) > 1 else grid_img)
    products.append({
        "slug": slug,
        "title": p["title"],
        "cat": p["category"],
        "price": p["price_min"],
        "sizePrices": p.get("size_prices", {}),
        "desc": p.get("desc", []),
        "verse": VERSE.get(slug, "Faithful"),
        "sizes": p["sizes"],
        "colors": colors,
        "img":    grid_img,
        "imgAlt": grid_alt,
    })

with open(f"{ROOT}/data.js", "w") as f:
    f.write("/* Auto-generated from the source store — 18 products with full variants.\n")
    f.write("   Regenerate: python3 scrape-variants.py && python3 gen-data.py */\n")
    f.write("window.PRODUCTS = " + json.dumps(products, ensure_ascii=False, indent=0) + ";\n")

with open(f"{ROOT}/dl-manifest.tsv", "w") as f:
    for url, lp in manifest.items():
        f.write(f"{url}\t{lp}\n")

print(f"products: {len(products)}")
print(f"distinct images to download: {len(manifest)}")
print("category counts:", {c: sum(1 for x in products if x['cat']==c) for c in ('hoodie','crewneck','tshirt')})
