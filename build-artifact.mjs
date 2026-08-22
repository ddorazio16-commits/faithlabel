// Builds a single self-contained HTML page for publishing as an Artifact.
// The Artifact CSP blocks all external requests, so: inline CSS + JS + data,
// embed fonts, and embed images as data URIs. To stay well under 16MB we embed
// a compact set (grid flatlays + each color's front) at a smaller size — enough
// for color-switching to work in the hosted preview. The deployable folder keeps
// the full-resolution galleries.
import fs from 'fs';
import { execSync } from 'child_process';

const DIR = '/Users/donatodorazio/faithlabel';
const TMP = '/tmp/art-embed';
fs.mkdirSync(TMP, { recursive: true });
const read = f => fs.readFileSync(`${DIR}/${f}`, 'utf8');

/* Embed EVERY gallery image so the live link shows all the pictures too.
   Compressed enough (max edge / quality below) that ~250 images stay under
   the 16MB Artifact limit. The deployable folder keeps full-res versions. */
const EMBED_PX = 620, EMBED_Q = 64;
const uriCache = new Map();
function imgURI(rel){
  if(!rel) return rel;
  if(uriCache.has(rel)) return uriCache.get(rel);
  const src = `${DIR}/${rel}`;
  if(!fs.existsSync(src)){ uriCache.set(rel, rel); return rel; }
  const out = `${TMP}/${rel.replace(/[\/]/g,'_')}`;
  try{ execSync(`sips -s format jpeg -s formatOptions ${EMBED_Q} -Z ${EMBED_PX} "${src}" --out "${out}"`, {stdio:'ignore'}); }
  catch(e){ uriCache.set(rel, rel); return rel; }
  const uri = 'data:image/jpeg;base64,' + fs.readFileSync(out).toString('base64');
  uriCache.set(rel, uri);
  return uri;
}

/* ---- fonts (latin woff2, embedded) ---- */
const fontCss = fs.readFileSync('/tmp/ffonts.css', 'utf8');
const faceRe = /\/\*\s*([\w-]+)\s*\*\/\s*@font-face\s*\{([^}]*)\}/g;
const faces = []; let fm;
while ((fm = faceRe.exec(fontCss))) {
  if (fm[1] !== 'latin') continue;
  const b = fm[2];
  faces.push({ family:/font-family:\s*'([^']+)'/.exec(b)[1], style:/font-style:\s*(\w+)/.exec(b)[1],
    weight:/font-weight:\s*(\d+)/.exec(b)[1], url:/url\(([^)]+)\)/.exec(b)[1] });
}
async function embedFonts(){
  let out='';
  for(const f of faces){
    const res = await fetch(f.url, { headers:{'User-Agent':'Mozilla/5.0 Chrome/122'} });
    const buf = Buffer.from(await res.arrayBuffer());
    out += `@font-face{font-family:'${f.family}';font-style:${f.style};font-weight:${f.weight};`
         + `font-display:swap;src:url(data:font/woff2;base64,${buf.toString('base64')}) format('woff2');}\n`;
  }
  return out;
}

/* ---- transform PRODUCTS: point every image at an embedded data URI ---- */
global.window = {};
await import(`file://${DIR}/data.js?ts=${Date.now()}`).catch(()=>{});
if(!global.window.PRODUCTS){ // data.js uses window.PRODUCTS = ... ; eval as fallback
  eval(read('data.js'));
}
const PRODUCTS = global.window.PRODUCTS;
let count = 0;
for(const p of PRODUCTS){
  p.img = imgURI(p.img); p.imgAlt = imgURI(p.imgAlt); count += 2;
  for(const c of p.colors){
    c.images = c.images.map(imgURI);   // embed the full gallery for every color
    count += c.images.length;
  }
}
console.error(`embedded ${count} image refs (${uriCache.size} unique files)`);

/* ---- assemble ---- */
const fontFaces = await embedFonts();
let css = read('styles.css').replace('url("assets/hero.jpg")', `url("${imgURI('assets/hero.jpg')}")`);
const js = read('app.js');
const dataInline = `window.PRODUCTS = ${JSON.stringify(PRODUCTS)};`;

let body = /<body[^>]*>([\s\S]*)<\/body>/.exec(read('index.html'))[1];
body = body
  .replace(/<script src="data\.js[^"]*"><\/script>/, '')
  .replace(/<script src="app\.js[^"]*"><\/script>/, '')
  // policy pages aren't embedded in the single file — point them at the live site
  .replace(/href="(privacy|terms|shipping-returns|contact)\.html"/g,
           'href="https://faithlabelshop.com/$1.html" target="_blank" rel="noopener"');

const page =
`<meta charset="utf-8">
<title>FaithLabel — Luxury Christian Apparel</title>
<style>
${fontFaces}${css}
</style>
${body}
<script>${dataInline}</script>
<script>
${js}
</script>`;

fs.writeFileSync(`${DIR}/faithlabel-artifact.html`, page);
console.error(`\nWrote faithlabel-artifact.html — ${(Buffer.byteLength(page)/1024/1024).toFixed(2)}MB`);
