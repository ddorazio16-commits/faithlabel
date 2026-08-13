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

## Connecting Printify (later, with API keys)

The frontend is already wired for it — the checkout builds a real order payload;
you just add the backend that talks to Printify.

**Important:** a Printify API token must **never** live in this frontend. Keep it
server-side. The site calls *your* endpoint, and your endpoint calls Printify.

1. **Get your keys.** In Printify → *My Profile → Connections*, create a
   Personal Access Token. Note your **Shop ID** (Printify API `/v1/shops.json`).

2. **Add each product's Printify id.** Put the Printify product id in the
   `printifyId` field for every entry in the `PRODUCTS` array in `app.js`.

3. **Stand up a tiny backend** (serverless function is fine) that receives the
   cart payload the site already sends and creates the order. The frontend POSTs
   this to `PRINTIFY.checkoutEndpoint` (default `/api/printify/checkout`):

   ```json
   { "line_items": [ { "slug": "...", "color": "Navy", "size": "XL",
                       "quantity": 2, "printify_product_id": "..." } ],
     "subtotal": 148.97 }
   ```

   Your function calls Printify with your token
   (`Authorization: Bearer <token>`), e.g. `POST /v1/shops/{shop_id}/orders.json`,
   and returns `{ "checkout_url": "https://…" }`.

   > Many stores route fulfilment through Shopify/Etsy connected to Printify
   > rather than raw order creation — either way, this endpoint is the seam.

4. **Flip the switch.** In `app.js`, set:

   ```js
   const PRINTIFY = { connected: true, checkoutEndpoint: '/api/printify/checkout', shopId: 'YOUR_SHOP_ID' };
   ```

   Until `connected` is `true`, the checkout button explains that keys aren't
   connected yet (and logs the exact payload it *would* send to the console).

## Refreshing the product images

`download-assets.sh` re-fetches the mockups from the source store and optimises
them (PNG → ~200KB JPG, max 900px). Uses macOS `sips`; on Linux swap in
ImageMagick's `convert`.

## Image credit

Hero photograph via [Unsplash](https://unsplash.com) (free to use, no
attribution required).
