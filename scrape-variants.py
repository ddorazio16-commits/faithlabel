#!/usr/bin/env python3
"""Fetch every FaithLabel product's variant data from the source store's
per-product .js endpoint and normalise it into a clean catalog for the
product-detail pages (colors, sizes, per-color image galleries, prices)."""
import json, urllib.request, re, sys, html as _html

BASE = "https://w2fb1a-q3.myshopify.com/products/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"

# garment color name -> approximate swatch hex (for the color selector UI)
SWATCH = {
 "Ash":"#E4E4E2","Black":"#191919","Charcoal":"#3E4249","Clay":"#A7614A","Cocoa":"#6A4A39",
 "Dark Chocolate":"#3A2A22","Fern":"#5C6B3B","Forest Green":"#22402E","Light Blue":"#BBD6E7",
 "Light Pink":"#E9C6CE","Maroon":"#5E212A","Military Green":"#4B5320","Navy":"#232F4C",
 "Ocean":"#2E5A73","Royal":"#284C9E","Sand":"#D8C9A4","Smoke":"#8B8E90","Sport Grey":"#B7B7B4",
 "White":"#F4F3EF",
}

# slug (our local id) -> source handle, category
HANDLES = [
 ("christian-unisex-crewneck","christian-unisex-crewneck-catholic-sweatshirt-religious-gift-for-him-and-her","crewneck"),
 ("faith-over-fear-crewneck-a","christian-unisex-sweatshirt-faith-over-fear-crewneck-religious-gift-for-him-and-her","crewneck"),
 ("john-146-crewneck","christian-unisex-sweatshirt-john-14-6-crewneck-religious-gift-for-him-and-her","crewneck"),
 ("crusader-deus-vult-hoodie","crusader-deus-vult-hoodie-catholic-unisex-sweatshirt-faith-gift-for-him-and-her","hoodie"),
 ("exodus-1414-hoodie","exodus-14-14-hoodie-catholic-unisex-sweatshirt-faith-gift-for-him-and-her","hoodie"),
 ("exodus-1414-hoodie-2","exodus-14-14-hoodie-catholic-unisex-sweatshirt-faith-gift-for-him-and-her-1","hoodie"),
 ("faith-over-fear-crewneck-b","faith-over-fear-crewneck-christian-sweatshirt-religious-gift-for-him-and-her","crewneck"),
 ("faith-over-fear-hoodie","faith-over-fear-hoodie-catholic-unisex-sweatshirt-faith-gift-for-him-and-her","hoodie"),
 ("god-is-good-hoodie","god-is-good-hoodie-christian-unisex-sweatshirt-religious-gift-for-him-and-her","hoodie"),
 ("isaiah-4319-hoodie","isaiah-43-19-catholic-hoodie-christian-unisex-sweatshirt-faith-gift-for-him-and-her","hoodie"),
 ("jesus-king-of-kings-tshirt","jesus-king-of-kings-t-shirt-christian-tie-dye-tee-religious-gift-for-him-and-her","tshirt"),
 ("john-146-hoodie","john-14-6-faith-hoodie-catholic-unisex-sweatshirt-meaningful-gift-for-him-and-her","hoodie"),
 ("matthew-1926-hoodie","matthew-19-26-hoodie-catholic-unisex-sweatshirt-faith-gift-for-him-and-her","hoodie"),
 ("philippians-413-hoodie","philippians-4-13-hoodie-christian-unisex-sweatshirt-religious-gift-for-him-and-her","hoodie"),
 ("proverbs-35-hoodie","proverbs-3-5-hoodie-catholic-unisex-sweatshirt-faith-gift-for-him-and-her","hoodie"),
 ("psalm-231-hoodie","psalm-23-1-hoodie-catholic-unisex-sweatshirt-faith-gift-for-him-and-her","hoodie"),
 ("trust-in-god-hoodie","trust-in-god-christian-hoodie-catholic-unisex-sweatshirt-religious-gift-for-him-and-her","hoodie"),
 ("walk-by-faith-hoodie","walk-by-faith-hoodie-catholic-unisex-sweatshirt-faith-gift-for-him-and-her","hoodie"),
]

def fetch(handle):
    req = urllib.request.Request(BASE + handle + ".js", headers={"User-Agent": UA})
    return json.load(urllib.request.urlopen(req, timeout=30))

def norm_src(src):
    # strip query string, keep permanent cdn.shopify.com path
    return src.split("?")[0]

def clean_desc(raw):
    """Parse the source HTML description into ordered blocks:
       {t:'p'} paragraph, {t:'h'} short section header, {t:'li'} feature bullet.
       Inline dash-lists become bullets; the returns/refund blurb is dropped
       (it lives on the Shipping & Returns page instead)."""
    txt = re.sub(r"<[^>]+>", "\n", raw or "")
    txt = _html.unescape(txt).replace("**", "")
    txt = re.sub(r"\s+-\s*(?=[A-Za-z0-9])", "\n- ", txt)     # inline "-item" -> bullet line
    emoji = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\U00002B00-\U00002BFF\U00002190-\U000021FF\U0000FE0F\U00002028-\U0000202F]")
    HEADS = re.compile(r"^(product features|features|care instructions|care|details|materials?|sizing|fit)\s*:?\s*$", re.I)
    blocks, skip = [], False
    for line in txt.split("\n"):
        l = emoji.sub("", line)
        l = re.sub(r"\s+", " ", l).strip()
        if re.search(r"return policy|returns are|refund|contact us within", l, re.I):
            skip = True
        if skip or not l:
            continue
        if l.startswith("- "):
            item = l[2:].strip(" :-")
            if item:
                blocks.append({"t": "li", "x": item})
        elif HEADS.match(l) or (len(l) < 42 and l.rstrip().endswith(":")):
            h = l.rstrip(": ").strip()
            if h:
                blocks.append({"t": "h", "x": h})
        else:
            l = re.sub(r"^\s*(?:Product Overview|Overview|Product Features|Features)\s*:\s*", "", l, flags=re.I)
            if len(l) > 2:
                blocks.append({"t": "p", "x": l})
    return blocks

catalog = []
for slug, handle, cat in HANDLES:
    try:
        d = fetch(handle)
    except Exception as e:
        print(f"!! {slug}: {e}", file=sys.stderr); continue

    opt_names = [o["name"] for o in d["options"]]
    color_idx = next((i for i,n in enumerate(opt_names) if n.lower() in ("color","colour")), None)
    size_idx  = next((i for i,n in enumerate(opt_names) if n.lower()=="size"), None)

    # variant_id -> color
    vid_color = {}
    prices = []
    sizes_seen = []
    colors_order = []
    size_price = {}
    variant_ids = {}   # "Color|Size" -> Shopify variant id (for cart-permalink checkout)
    for v in d["variants"]:
        opts = v["options"]
        color = opts[color_idx] if color_idx is not None else None
        size  = opts[size_idx]  if size_idx  is not None else None
        vid_color[v["id"]] = color
        if v.get("available"): prices.append(v["price"])
        if size and size not in sizes_seen: sizes_seen.append(size)
        if color and color not in colors_order: colors_order.append(color)
        if size: size_price[size] = min(size_price.get(size, 10**9), v["price"])
        if color and size: variant_ids[f"{color}|{size}"] = v["id"]
    if not prices:
        prices = [v["price"] for v in d["variants"]]

    # images per color (via variant_ids); also generic images (no variant_ids)
    color_imgs = {c: [] for c in colors_order}
    generic = []
    # Use media (has src + not variant map) plus variants' featured_image for color mapping
    # Build from variants' featured_image first (reliable color->image)
    color_first_img = {}
    for v in d["variants"]:
        fi = v.get("featured_image")
        c = vid_color.get(v["id"])
        if fi and c and c not in color_first_img:
            color_first_img[c] = norm_src(fi["src"])
    # Full gallery per color: scan media/images with variant_ids
    imgs_full = d.get("media") or []
    for im in imgs_full:
        src = norm_src(im.get("src") or (im.get("preview_image") or {}).get("src",""))
        if not src: continue
        vids = im.get("variant_ids") or []
        cols = {vid_color.get(x) for x in vids if vid_color.get(x)}
        if cols:
            for c in cols:
                if src not in color_imgs.get(c, []): color_imgs.setdefault(c,[]).append(src)
        else:
            generic.append(src)

    # shared detail/back shots = media that is NOT any color's front image
    fronts = set(color_first_img.values())
    shared = []
    for s in generic:
        if s not in fronts and s not in shared:
            shared.append(s)
    # no cap — bring EVERY shot the source has (back print, close-ups,
    # size guide, lifestyle) so each product shows all its pictures.
    shared = shared[:20]

    colors = []
    for c in colors_order:
        front = color_first_img.get(c)
        gallery = ([front] if front else []) + [s for s in shared if s != front]
        if not gallery:
            gallery = generic[:3]
        colors.append({
            "name": c,
            "swatch": SWATCH.get(c, "#B7B7B4"),
            "images": [("https:" + g if g.startswith("//") else g) for g in gallery],
        })

    catalog.append({
        "slug": slug, "handle": handle, "category": cat,
        "title": d["title"],
        "price_min": min(prices)/100.0,
        "price_max": max(prices)/100.0,
        "sizes": sizes_seen,
        "size_prices": {s: round(p/100.0, 2) for s, p in size_price.items()},
        "variants": variant_ids,
        "desc": clean_desc(d.get("description")),
        "colors": colors,
    })
    print(f"OK {slug:26} colors={len(colors_order):2} sizes={len(sizes_seen)} "
          f"gallery_imgs={sum(len(c['images']) for c in colors)} price={min(prices)/100.0}", file=sys.stderr)

json.dump(catalog, open("/Users/donatodorazio/faithlabel/catalog.json","w"), indent=1)
print(f"\nWrote catalog.json — {len(catalog)} products", file=sys.stderr)
