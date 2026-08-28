#!/usr/bin/env node
/* Regression test: the product modal must never hide content out of reach.
   Drives real Chrome (headless) against a running static server — no npm deps.
   Usage:  python3 -m http.server 8712 &  node test-pdp-scroll.mjs           */
import { execFileSync } from 'node:child_process';
import { writeFileSync, unlinkSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const ORIGIN  = process.env.ORIGIN || 'http://localhost:8712';
const CHROME  = process.env.CHROME ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const HARNESS = `test-pdp-scroll.harness.${process.pid}.html`;

/* Same-origin iframe harness: opens the first product, then measures the modal.
   It lives in the doc root only for the duration of the run. */
writeFileSync(HARNESS, `<!doctype html><meta charset="utf-8"><title>t</title>
<style>html,body{margin:0}iframe{border:0;display:block}</style>
<pre id="out">pending</pre><iframe id="f" src="/index.html"></iframe><script>
const q=new URLSearchParams(location.search),f=document.getElementById('f'),out=document.getElementById('out');
f.style.width=q.get('w')+'px'; f.style.height=q.get('h')+'px';
f.addEventListener('load',()=>setTimeout(()=>{
  const d=f.contentDocument;
  d.querySelector('[data-open]').click();
  setTimeout(()=>{
    const g=s=>d.querySelector(s), B=e=>e.getBoundingClientRect();
    const pdp=g('.pdp'),inner=g('.pdp__inner'),info=g('.pdp__info'),gal=g('.pdp__gallery'),desc=g('.pdp__desc');
    const stage=g('.pdp__stage'),thumbs=g('.pdp__thumbs');
    /* scroll every scroller to its end, then check the description really ends inside the modal */
    for(const el of [inner,info,gal]) el.scrollTop=1e6;
    out.textContent=JSON.stringify({
      descEndsInsideModal: B(desc).bottom <= B(pdp).bottom+1,
      stageStaysSquare: Math.abs(B(stage).width - B(stage).height) <= 2,
      thumbsEndInsideModal: B(thumbs).bottom <= B(pdp).bottom+1,
      galleryEndsInsideModal: B(gal).bottom <= B(pdp).bottom+1,
      infoOverflows: info.scrollHeight > info.clientHeight+1,
      infoScrolledToEnd: info.scrollTop >= info.scrollHeight-info.clientHeight-1,
      innerScrolledToEnd: inner.scrollTop >= inner.scrollHeight-inner.clientHeight-1,
      modalFitsViewport: B(pdp).height <= f.contentWindow.innerHeight+1
    });
  },1500);
},1500));
</script>`);

const measure = (w, h) => {
  /* A fresh profile per launch, and a hard timeout — a wedged Chrome should fail
     the run loudly rather than hang it forever. */
  const args = ['--headless', '--disable-gpu', '--no-sandbox',
    `--user-data-dir=${mkdtempSync(join(tmpdir(), 'pdp-test-'))}`,
    '--no-first-run', '--no-default-browser-check', '--disable-background-networking',
    `--window-size=${w + 60},${h + 100}`, '--virtual-time-budget=20000', '--dump-dom',
    `${ORIGIN}/${HARNESS}?w=${w}&h=${h}`];
  const opts = { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 90000, killSignal: 'SIGKILL' };
  let dom;
  try { dom = execFileSync(CHROME, args, opts); }
  catch (err) {
    /* --dump-dom prints the DOM and then, now and again, simply declines to exit.
       The measurement is already complete when that happens, so the timeout is
       only a real failure if nothing came back on stdout. */
    if (!err.stdout || !err.stdout.includes('<pre id="out">')) throw err;
    dom = err.stdout;
  }
  const m = dom.match(/<pre id="out">([\s\S]*?)<\/pre>/);
  if (!m || m[1] === 'pending') throw new Error(`harness produced no measurement at ${w}x${h}`);
  return JSON.parse(m[1]);
};

/* Each case: viewport, plus the invariants that must hold there. */
const CASES = [
  { name: 'desktop 1440x900',      w: 1440, h: 900,  expect: ['descEndsInsideModal', 'galleryEndsInsideModal', 'thumbsEndInsideModal', 'stageStaysSquare', 'modalFitsViewport', 'infoOverflows', 'infoScrolledToEnd'] },
  { name: 'desktop short 1600x650',w: 1600, h: 650,  expect: ['descEndsInsideModal', 'galleryEndsInsideModal', 'thumbsEndInsideModal', 'stageStaysSquare', 'modalFitsViewport', 'infoOverflows', 'infoScrolledToEnd'] },
  { name: 'laptop 1280x660',       w: 1280, h: 660,  expect: ['descEndsInsideModal', 'galleryEndsInsideModal', 'thumbsEndInsideModal', 'stageStaysSquare', 'modalFitsViewport', 'infoOverflows', 'infoScrolledToEnd'] },
  { name: 'desktop tall 1440x1300',w: 1440, h: 1300, expect: ['descEndsInsideModal', 'galleryEndsInsideModal', 'thumbsEndInsideModal', 'stageStaysSquare', 'modalFitsViewport'] },
  { name: 'mobile 390x844',        w: 390,  h: 844,  expect: ['descEndsInsideModal', 'stageStaysSquare', 'modalFitsViewport', 'innerScrolledToEnd'] },
];

let failed = 0;
try {
  for (const c of CASES) {
    const r = measure(c.w, c.h);
    const bad = c.expect.filter(k => !r[k]);
    if (bad.length) { failed++; console.log(`FAIL  ${c.name}  →  ${bad.join(', ')}\n      ${JSON.stringify(r)}`); }
    else console.log(`pass  ${c.name}`);
  }
} finally { unlinkSync(HARNESS); }

console.log(failed ? `\n${failed} failing case(s)` : '\nall cases pass');
process.exit(failed ? 1 : 0);
