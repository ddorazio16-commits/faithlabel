# FaithLabel — Luxury Christian Apparel

A fast, self-contained storefront for the FaithLabel brand. Rebuilt from the
original Shopify store into a polished, deployable site — same color scheme,
same pricing, same product mockups (each on its original concrete backdrop),
with a cinematic hero, smooth scroll motion, a super-friendly filter, and full
product pages with color / size selection.

Built as plain HTML/CSS/JS — no build step, no framework, no dependencies.

**Features**
- **18 products** (all items from the source store, titles verbatim), filterable by Hoodies / Crewnecks / T-Shirts with live search.
- **Real product pages** — click any item to open a detail view: image gallery, color swatches (switching a color updates the gallery), size selector (S–5XL), quantity, size guide, and Add to Cart.
- **Variant-aware cart** — each line remembers its color + size; persists across visits.
- **Verse of the Week** in the top bar — rotates automatically each week through a curated list.
- **Printify-ready** checkout seam (see below).

```
faithlabel/
├── index.html            # markup (incl. product-detail modal + size guide)
├── styles.css            # design system (royal-blue + antique-gold)
├── app.js                # filter/search, product pages, variant cart, Printify seam
├── data.js               # generated product data (18 products, colors, sizes, images)
├── scrape-variants.py    # pulls variant data from the source store  → catalog.json
├── gen-data.py           # catalog.json → data.js + dl-manifest.tsv
├── download-variants.sh  # downloads + optimises all gallery images
├── download-assets.sh    # (original) re-fetches the grid flatlays
└── assets/
    ├── hero.jpg          # heavenly-light hero (Unsplash, free license)
    └── products/
        ├── <slug>.jpg    # concrete-flatlay grid image (+ -alt hover)
        └── <slug>/       # per-product color gallery images
```

## Refreshing the catalog

```bash
python3 scrape-variants.py   # fetch colors/sizes/images from the source store
python3 gen-data.py          # build data.js + the image download manifest
./download-variants.sh       # download + optimise every gallery image
```

## Run it locally

Any static server works. For example:

```bash
cd faithlabel
python3 -m http.server 8712
```

Then open <http://localhost:8712>.

## Deploy it

It's a static folder — drop it on any host:

- **Netlify / Vercel / Cloudflare Pages:** drag the folder in, or connect the repo. No build command; publish directory is the folder root.
- **GitHub Pages:** push the folder and enable Pages on the branch.
- **Your own domain:** upload the folder to any web root.

## Design notes

- **Palette** is built on the brand's exact colors — sky `#E9F2F7`, royal-blue ink `#163BA1` — plus one disciplined **antique-gold** accent (`#C8A24C`) drawn from gilded religious art (illuminated manuscripts, gold-leaf icons).
- **Type:** Cormorant Garamond (display) + Inter (body), loaded from Google Fonts with a system-serif fallback so it degrades gracefully offline.
- **Motion:** scroll-reveal, hero parallax, hover image-swap on cards, a sliding gold indicator on the filter pills, and a FLIP animation so the grid re-flows smoothly when you filter. All of it respects `prefers-reduced-motion`.
- **Titles & pricing** are preserved verbatim from the source store. (The one duplicate "Exodus 14:14 Hoodie" listing was consolidated into a single product.)

## Editing the catalog

All products live in the `PRODUCTS` array at the top of [`app.js`](app.js).
Each entry:

```js
{ slug:'psalm-231-hoodie', cat:'hoodie', price:52.99, verse:'Psalm 23:1',
  title:'Psalm 23:1 Hoodie | Catholic Unisex Sweatshirt, Faith Gift for Him and Her',
  printifyId:'' }
```

- `cat` drives the filter — one of `hoodie` / `crewneck` / `tshirt`.
- Images are looked up by `slug`: `assets/products/<slug>.jpg` (main) and
  `<slug>-alt.jpg` (hover). Filter counts update automatically.

## Checkout (live — via Shopify)

Checkout hands the cart off to the connected Shopify store, which takes
payment and triggers Printify fulfillment. No backend or API keys live in
this site.

**How it works:** each product in `data.js` carries a `variants` map of
`"Color|Size" → Shopify variant id` (pulled by `scrape-variants.py`). When a
shopper clicks **Proceed to Checkout**, `app.js` builds a Shopify *cart
permalink* and redirects there:

```
https://<SHOP>/cart/<variantId>:<qty>,<variantId>:<qty>
```

Shopify adds the items, runs its secure checkout, and (because the store has
Printify connected) the paid order is produced and shipped automatically.

**Config:** the store domain is the `SHOP` constant near the top of `app.js`:

```js
const SHOP = 'w2fb1a-q3.myshopify.com';
```

If you move Shopify to a custom domain (e.g. `faithlabel.com`), update `SHOP`
to that domain and redeploy. If products change, re-run
`scrape-variants.py && gen-data.py` to refresh the variant ids.

## Refreshing the product images

`download-assets.sh` re-fetches the mockups from the source store and optimises
them (PNG → ~200KB JPG, max 900px). Uses macOS `sips`; on Linux swap in
ImageMagick's `convert`.

## Image credit

Hero photograph via [Unsplash](https://unsplash.com) (free to use, no
attribution required).
