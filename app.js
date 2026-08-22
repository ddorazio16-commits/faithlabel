/* ============================================================
   FaithLabel — storefront logic
   Data comes from data.js (window.PRODUCTS) — 18 products, each with
   colors (swatch + gallery) and sizes.
   Features: friendly filter, product-detail modal (color/size/gallery),
   variant-aware cart, weekly verse, Shopify checkout handoff (Printify fulfils).
   ============================================================ */

document.documentElement.classList.add('js');

/* On refresh/return, always start at the very top so the first thing the
   visitor sees is the verse bar and the hero — not a restored scroll spot. */
if('scrollRestoration' in history){ history.scrollRestoration = 'manual'; }
window.scrollTo(0, 0);
window.addEventListener('load', () => window.scrollTo(0, 0));
window.addEventListener('pageshow', () => window.scrollTo(0, 0));

const PRODUCTS = window.PRODUCTS || [];
const CAT_LABEL = { hoodie:'Hoodie', crewneck:'Crewneck', tshirt:'T-Shirt' };
/* Shopify store that handles payment + Printify fulfillment. Checkout hands
   the cart off here via a cart permalink. Change this if you move to a custom
   domain (e.g. 'faithlabel.com'). */
const SHOP = 'w2fb1a-q3.myshopify.com';

/* ---- helpers ---- */
const $  = (s, r=document) => r.querySelector(s);
const $$ = (s, r=document) => [...r.querySelectorAll(s)];
const money = n => '$' + Number(n).toFixed(2);
const escHtml = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const escAttr = escHtml;
const bySlug = s => PRODUCTS.find(p => p.slug === s);
const colorOf = (p, name) => p.colors.find(c => c.name === name) || p.colors[0];
/* exact price for a size (larger sizes cost more); falls back to base price */
const priceFor = (p, size) => (p && p.sizePrices && p.sizePrices[size]) || (p && p.price) || 0;
/* render a product description (blocks of {t:'p'|'h'|'li'}) to safe HTML */
function renderDesc(blocks){
  if(!blocks || !blocks.length) return '';
  let html = '', inList = false;
  const closeList = () => { if(inList){ html += '</ul>'; inList = false; } };
  for(const b of blocks){
    if(b.t === 'li'){ if(!inList){ html += '<ul>'; inList = true; } html += `<li>${escHtml(b.x)}</li>`; }
    else { closeList(); html += b.t === 'h' ? `<h4>${escHtml(b.x)}</h4>` : `<p>${escHtml(b.x)}</p>`; }
  }
  closeList();
  return html;
}

/* keep broken images from showing a broken-image icon on a luxury page */
document.addEventListener('error', e => {
  const t = e.target;
  if(t && t.tagName === 'IMG' && !t.dataset.err){ t.dataset.err = '1'; t.style.opacity = '0'; console.warn('[FaithLabel] image failed to load:', t.src); }
}, true);

/* focus containment: make the page chrome inert while a modal is open */
let lastFocus = null;
function lockBg(){ ['#announce','#header','#top','.footer'].forEach(s => { const e = $(s); if(e) e.setAttribute('inert',''); }); }
function unlockBg(){ ['#announce','#header','#top','.footer'].forEach(s => { const e = $(s); if(e) e.removeAttribute('inert'); }); }
function splitTitle(t){
  const [main, ...rest] = t.split('|');
  return { main: main.trim(), sub: rest.join('|').trim() };
}

/* ============================================================
   Grid
   ============================================================ */
const grid = $('#grid');

function cardHTML(p){
  const { main, sub } = splitTitle(p.title);
  return `
  <article class="card reveal" data-open="${p.slug}" data-cat="${p.cat}"
           data-search="${(p.title + ' ' + p.verse).toLowerCase().replace(/"/g,'&quot;')}">
    <div class="card__media">
      <span class="card__tag">${CAT_LABEL[p.cat]}</span>
      <img class="card__img card__img--main" src="${p.img}" alt="${escAttr(main)}" loading="lazy" decoding="async" />
      <img class="card__img card__img--alt" data-alt="${p.imgAlt}" alt="" loading="lazy" decoding="async" aria-hidden="true" />
      <span class="card__quick">Select Options</span>
    </div>
    <div class="card__body">
      <span class="card__verse">${escHtml(p.verse)}</span>
      <h3 class="card__title">${escHtml(main)}</h3>
      ${sub ? `<p class="card__sub">${escHtml(sub)}</p>` : ''}
      <div class="card__foot">
        <span class="card__price"><span>From</span> ${money(p.price)}</span>
        <span class="card__add">View
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </span>
      </div>
    </div>
  </article>`;
}

grid.innerHTML = PRODUCTS.map(cardHTML).join('');
grid.addEventListener('click', e => {
  const card = e.target.closest('.card[data-open]');
  if(card) openPDP(card.dataset.open);
});
/* load each card's hover image only when it's actually needed (saves ~2MB) */
function loadAltImage(e){
  const card = e.target.closest('.card'); if(!card) return;
  const alt = card.querySelector('.card__img--alt');
  if(alt && !alt.getAttribute('src') && alt.dataset.alt) alt.src = alt.dataset.alt;
}
grid.addEventListener('mouseover', loadAltImage);
grid.addEventListener('focusin', loadAltImage);

/* counts */
const counts = PRODUCTS.reduce((a,p)=>{ a.all++; a[p.cat]=(a[p.cat]||0)+1; return a; }, {all:0});
$('#cAll').textContent = counts.all;
$('#cHoodie').textContent = counts.hoodie || 0;
$('#cCrewneck').textContent = counts.crewneck || 0;
$('#cTshirt').textContent = counts.tshirt || 0;

/* ============================================================
   Filtering — pills + search, with FLIP motion
   ============================================================ */
const state = { cat:'all', query:'' };
const filters = $('#filters');
const pills = $$('.pill', filters);
const pillBg = $('#pillBg');
const empty = $('#empty');

function movePill(){
  const active = filters.querySelector('.pill.is-active');
  if(!active) return;
  pillBg.style.width = active.offsetWidth + 'px';
  pillBg.style.transform = `translateX(${active.offsetLeft - 4}px)`;
}
function setCat(cat){
  state.cat = cat;
  pills.forEach(p=>{
    const on = p.dataset.filter === cat;
    p.classList.toggle('is-active', on);
    p.setAttribute('aria-selected', on);
  });
  movePill();
  applyFilter();
}
function applyFilter(){
  const cat = state.cat, q = state.query.trim().toLowerCase();
  const cards = [...grid.children];
  const first = new Map();
  cards.forEach(c => { if(c.style.display !== 'none') first.set(c, c.getBoundingClientRect()); });

  let visible = 0;
  cards.forEach(c => {
    const match = (cat === 'all' || c.dataset.cat === cat) &&
                  (q === '' || c.dataset.search.includes(q));
    c.dataset.match = match;
    if(match){
      visible++;
      if(c.style.display === 'none') c.style.display = '';
      // a re-matched card may still be mid-hide — cancel it and un-hide,
      // otherwise rapid filter changes leave cards stuck invisible.
      clearTimeout(c._hideT); c.classList.remove('is-hiding');
    }
  });

  const last = new Map();
  cards.forEach(c => { if(c.dataset.match === 'true') last.set(c, c.getBoundingClientRect()); });

  last.forEach((lr, c) => {
    const fr = first.get(c);
    if(fr){
      const dx = fr.left - lr.left, dy = fr.top - lr.top;
      if(dx || dy){
        c.style.transition = 'none';
        c.style.transform = `translate(${dx}px, ${dy}px)`;
        requestAnimationFrame(() => { c.style.transition = ''; c.style.transform = ''; });
      }
    } else {
      c.classList.add('is-hiding');
      requestAnimationFrame(() => c.classList.remove('is-hiding'));
    }
  });
  cards.forEach(c => {
    if(c.dataset.match !== 'true' && c.style.display !== 'none'){
      c.classList.add('is-hiding');
      clearTimeout(c._hideT);
      c._hideT = setTimeout(() => { if(c.dataset.match !== 'true'){ c.style.display = 'none'; c.classList.remove('is-hiding'); } }, 460);
    }
  });
  empty.hidden = visible > 0;
}
pills.forEach(p => p.addEventListener('click', () => setCat(p.dataset.filter)));

/* search */
const searchInput = $('#searchInput');
const searchClear = $('#searchClear');
searchInput.addEventListener('input', () => {
  state.query = searchInput.value;
  searchClear.hidden = !searchInput.value;
  applyFilter();
});
searchClear.addEventListener('click', () => {
  searchInput.value = ''; state.query = ''; searchClear.hidden = true;
  applyFilter(); searchInput.focus();
});

/* deep links with data-filter (footer) */
$$('[data-filter]').forEach(el => {
  if(el.classList.contains('pill')) return;
  el.addEventListener('click', e => {
    if(el.tagName === 'A'){ e.preventDefault(); $('#collection').scrollIntoView({ behavior:'smooth' }); }
    setCat(el.dataset.filter); closeMobileNav();
  });
});
window.addEventListener('resize', movePill);
window.addEventListener('load', movePill);
setTimeout(movePill, 300);

/* ============================================================
   Product detail (PDP)
   ============================================================ */
const pdp = $('#pdp'), pdpOverlay = $('#pdpOverlay');
let pdpState = { slug:null, color:null, size:null, qty:1 };
let pdpSwapTimer = null;
const hasVariant = (p, color, size) => !!(p && p.variants && p.variants[`${color}|${size}`]);

function setPdpPrice(p){
  $('#pdpPrice').innerHTML = pdpState.size
    ? money(priceFor(p, pdpState.size))
    : `<span>From</span> ${money(p.price)}`;
}

/* size buttons reflect real availability: some color+size combos don't exist
   as variants, so they're disabled (and can never reach a broken checkout). */
function renderSizes(p){
  $('#pdpSizes').innerHTML = p.sizes.map(s => {
    const ok = hasVariant(p, pdpState.color, s);
    const active = s === pdpState.size ? ' is-active' : '';
    return `<button class="size-btn${ok ? '' : ' is-unavailable'}${active}" data-size="${s}"`
         + `${ok ? '' : ' disabled aria-disabled="true" title="Unavailable in this color"'}>${s}</button>`;
  }).join('');
}

/* one place to swap the main image — cancels any pending swap (no race),
   crossfades, and clears a prior load-error opacity so it never stays blank. */
function setMainImage(src, alt){
  const mainImg = $('#pdpMainImg');
  clearTimeout(pdpSwapTimer);
  mainImg.classList.add('is-swapping');
  pdpSwapTimer = setTimeout(() => {
    if(src) mainImg.src = src;
    if(alt != null) mainImg.alt = alt;
    mainImg.style.opacity = '';
    delete mainImg.dataset.err;
    mainImg.classList.remove('is-swapping');
  }, 140);
}

function openPDP(slug){
  const p = bySlug(slug);
  if(!p) return;
  if(!p.colors || !p.colors.length){ toast('Details for this piece are unavailable right now.'); return; }
  lastFocus = document.activeElement;
  pdpState = { slug, color: p.colors[0].name, size:null, qty:1 };
  const { main, sub } = splitTitle(p.title);

  $('#pdpVerse').textContent = p.verse;
  $('#pdpTitle').textContent = main;
  $('#pdpSub').textContent = sub;
  setPdpPrice(p);
  $('#pdpDesc').innerHTML = renderDesc(p.desc);
  $('#pdpQtyVal').textContent = '1';
  $('#pdpSizeHint').hidden = true;

  $('#pdpSwatches').innerHTML = p.colors.map(c =>
    `<button class="swatch${c.name===pdpState.color?' is-active':''}" style="background:${c.swatch}"
             data-color="${c.name}" title="${c.name}" aria-label="${c.name}"></button>`).join('');
  $('#pdpColorName').textContent = pdpState.color;

  renderSizes(p);
  setGallery(p, pdpState.color);

  pdpOverlay.hidden = false;
  requestAnimationFrame(() => pdpOverlay.classList.add('is-open'));
  pdp.classList.add('is-open'); pdp.setAttribute('aria-hidden','false');
  pdp.querySelector('.pdp__info').scrollTop = 0;
  document.body.style.overflow = 'hidden';
  lockBg();
  requestAnimationFrame(() => $('#pdpClose').focus());
}

function setGallery(p, colorName){
  const c = colorOf(p, colorName);
  const imgs = (c && c.images && c.images.length) ? c.images : [p.img].filter(Boolean);
  setMainImage(imgs[0], `${splitTitle(p.title).main} — ${colorName}`);
  $('#pdpThumbs').innerHTML = imgs.map((src,i) =>
    `<button class="${i===0?'is-active':''}" data-img="${src}" aria-label="View image ${i+1}"><img src="${src}" alt="" loading="lazy" decoding="async"></button>`).join('');
}

function closePDP(){
  pdpOverlay.classList.remove('is-open');
  pdp.classList.remove('is-open'); pdp.setAttribute('aria-hidden','true');
  if(!cartEl.classList.contains('is-open')){ document.body.style.overflow = ''; unlockBg(); }
  setTimeout(() => pdpOverlay.hidden = true, 450);
  if(lastFocus && !cartEl.classList.contains('is-open')){ lastFocus.focus?.(); }
}

pdp.addEventListener('click', e => {
  const sw = e.target.closest('.swatch');
  if(sw){
    pdpState.color = sw.dataset.color;
    $$('.swatch', pdp).forEach(x => x.classList.toggle('is-active', x===sw));
    $('#pdpColorName').textContent = pdpState.color;
    const p = bySlug(pdpState.slug);
    if(pdpState.size && !hasVariant(p, pdpState.color, pdpState.size)){ pdpState.size = null; setPdpPrice(p); }
    renderSizes(p);
    setGallery(p, pdpState.color);
    return;
  }
  const sz = e.target.closest('.size-btn');
  if(sz){
    if(sz.disabled || sz.classList.contains('is-unavailable')) return;
    pdpState.size = sz.dataset.size;
    $$('.size-btn', pdp).forEach(x => x.classList.toggle('is-active', x===sz));
    setPdpPrice(bySlug(pdpState.slug));
    $('#pdpSizeHint').hidden = true;
    return;
  }
  const th = e.target.closest('#pdpThumbs button');
  if(th){
    setMainImage(th.dataset.img);
    $$('#pdpThumbs button', pdp).forEach(x => x.classList.toggle('is-active', x===th));
    return;
  }
  const q = e.target.closest('[data-q]');
  if(q){
    pdpState.qty = Math.min(20, Math.max(1, pdpState.qty + Number(q.dataset.q)));
    $('#pdpQtyVal').textContent = pdpState.qty;
    return;
  }
});
$('#pdpAdd').addEventListener('click', () => {
  const p = bySlug(pdpState.slug);
  if(!pdpState.size){ $('#pdpSizeHint').hidden = false; toast('Please choose a size.'); return; }
  if(!hasVariant(p, pdpState.color, pdpState.size)){ toast('That size is sold out in this color.'); return; }
  addToCart(pdpState.slug, pdpState.color, pdpState.size, pdpState.qty);
  closePDP();
  openCart();
});
$('#pdpClose').addEventListener('click', closePDP);
pdpOverlay.addEventListener('click', closePDP);

/* size guide */
const sizeguide = $('#sizeguide');
function openSizeGuide(){ sizeguide.hidden = false; sizeguide.setAttribute('aria-hidden','false'); pdp.setAttribute('inert',''); requestAnimationFrame(()=> $('#sizeguideClose').focus()); }
function closeSizeGuide(){ sizeguide.hidden = true; sizeguide.setAttribute('aria-hidden','true'); pdp.removeAttribute('inert'); $('#sizeGuide').focus?.(); }
$('#sizeGuide').addEventListener('click', openSizeGuide);
$('#sizeguideClose').addEventListener('click', closeSizeGuide);
sizeguide.addEventListener('click', e => { if(e.target === sizeguide){ closeSizeGuide(); } });

/* ============================================================
   Cart (variant-aware)
   ============================================================ */
const CART_KEY = 'faithlabel_cart_v2';
let cart = loadCart();
const keyOf = l => `${l.slug}::${l.color}::${l.size}`;

function loadCart(){
  let raw;
  try{ raw = JSON.parse(localStorage.getItem(CART_KEY)); }
  catch(e){ console.warn('[FaithLabel] cart could not be read, starting empty', e); return []; }
  if(!Array.isArray(raw)) return [];
  // Drop lines whose product/color/size no longer exist (e.g. after the
  // catalog is regenerated) so a stale cart can never crash render or checkout.
  const clean = raw.filter(l => {
    const p = l && bySlug(l.slug);
    return p && hasVariant(p, l.color, l.size)
      && Number.isFinite(l.qty) && l.qty > 0;
  });
  if(clean.length !== raw.length){
    console.warn('[FaithLabel] removed cart items that are no longer available');
    try{ localStorage.setItem(CART_KEY, JSON.stringify(clean)); }catch{}
  }
  return clean;
}
function saveCart(){ try{ localStorage.setItem(CART_KEY, JSON.stringify(cart)); }catch{} }

function addToCart(slug, color, size, qty=1){
  const line = cart.find(l => l.slug===slug && l.color===color && l.size===size);
  if(line) line.qty += qty; else cart.push({ slug, color, size, qty });
  saveCart(); renderCart(); bumpCart();
  const p = bySlug(slug);
  toast(`Added — ${splitTitle(p.title).main} · ${color}, ${size}`);
}
function changeQty(key, delta){
  const line = cart.find(l => keyOf(l) === key);
  if(!line) return;
  line.qty = Math.min(20, line.qty + delta);
  if(line.qty <= 0) cart = cart.filter(l => keyOf(l) !== key);
  saveCart(); renderCart();
}
function removeLine(key){ cart = cart.filter(l => keyOf(l) !== key); saveCart(); renderCart(); }

const cartItems = $('#cartItems'), cartEmpty = $('#cartEmpty'), cartFoot = $('#cartFoot');

function renderCart(){
  const count = cart.reduce((n,l)=>n+l.qty, 0);
  const badge = $('#cartCount');
  badge.textContent = count; badge.hidden = count === 0;
  $('#cartHeadCount').textContent = count ? `· ${count}` : '';

  if(!cart.length){ cartItems.innerHTML = ''; cartEmpty.style.display = 'flex'; cartFoot.hidden = true; return; }
  cartEmpty.style.display = 'none'; cartFoot.hidden = false;

  cartItems.innerHTML = cart.map(l => {
    const p = bySlug(l.slug); const { main } = splitTitle(p.title);
    const img = colorOf(p, l.color).images[0]; const key = keyOf(l);
    return `
    <div class="cart-line">
      <img class="cart-line__img" src="${img}" alt="${escAttr(main)}" />
      <div>
        <div class="cart-line__title">${main}</div>
        <div class="cart-line__meta">${l.color} · ${l.size} · ${money(priceFor(p, l.size))}</div>
        <div class="cart-line__qty">
          <button data-dec="${key}" aria-label="Decrease quantity">−</button>
          <span>${l.qty}</span>
          <button data-inc="${key}" aria-label="Increase quantity">+</button>
        </div>
      </div>
      <div class="cart-line__right">
        <span class="cart-line__price">${money(priceFor(p, l.size) * l.qty)}</span>
        <button class="cart-line__remove" data-remove="${key}">Remove</button>
      </div>
    </div>`;
  }).join('');

  $('#cartSubtotal').textContent = money(cart.reduce((s,l)=> s + priceFor(bySlug(l.slug), l.size) * l.qty, 0));
}

cartItems.addEventListener('click', e => {
  const inc = e.target.closest('[data-inc]'); if(inc){ changeQty(inc.dataset.inc, 1); return; }
  const dec = e.target.closest('[data-dec]'); if(dec){ changeQty(dec.dataset.dec, -1); return; }
  const rm  = e.target.closest('[data-remove]'); if(rm){ removeLine(rm.dataset.remove); return; }
});

/* cart open/close */
const cartEl = $('#cart'), overlay = $('#overlay');
function openCart(){
  lastFocus = document.activeElement;
  overlay.hidden = false; requestAnimationFrame(()=> overlay.classList.add('is-open'));
  cartEl.classList.add('is-open'); cartEl.setAttribute('aria-hidden','false');
  document.body.style.overflow = 'hidden';
  lockBg();
  requestAnimationFrame(()=> $('#cartClose').focus());
}
function closeCart(){
  overlay.classList.remove('is-open'); cartEl.classList.remove('is-open');
  cartEl.setAttribute('aria-hidden','true'); document.body.style.overflow = ''; unlockBg();
  setTimeout(()=> overlay.hidden = true, 450);
  lastFocus?.focus?.();
}
$('#cartToggle').addEventListener('click', openCart);
$('#cartClose').addEventListener('click', closeCart);
overlay.addEventListener('click', closeCart);
$('#cartEmptyShop').addEventListener('click', () => { closeCart(); $('#collection').scrollIntoView({behavior:'smooth'}); });
document.addEventListener('keydown', e => {
  if(e.key === 'Escape'){
    if(!sizeguide.hidden){ closeSizeGuide(); return; }
    if(pdp.classList.contains('is-open')){ closePDP(); return; }
    closeCart(); closeMobileNav();
  }
});
function bumpCart(){
  $('#cartToggle').animate([{transform:'scale(1)'},{transform:'scale(1.18)'},{transform:'scale(1)'}], {duration:360, easing:'ease-out'});
}

/* ============================================================
   Checkout — hands off to the Shopify cart, which takes payment
   and triggers Printify fulfillment. Builds a cart permalink:
   https://<shop>/cart/<variantId>:<qty>,<variantId>:<qty>
   ============================================================ */
function shopifyCheckoutURL(){
  const parts = [];
  const missing = [];
  for(const l of cart){
    const p = bySlug(l.slug);
    const vid = p && p.variants && p.variants[`${l.color}|${l.size}`];
    if(vid) parts.push(`${vid}:${l.qty}`);
    else missing.push(`${splitTitle(p ? p.title : l.slug).main} (${l.color}/${l.size})`);
  }
  return { url: parts.length ? `https://${SHOP}/cart/${parts.join(',')}` : null, missing };
}

$('#checkoutBtn').addEventListener('click', () => {
  if(!cart.length){ toast('Your cart is empty.'); return; }
  const { url, missing } = shopifyCheckoutURL();
  // never silently drop an item — if anything is unavailable, stop and say so
  if(missing.length){
    console.warn('[FaithLabel] no variant id for:', missing);
    toast(`Unavailable: ${missing[0]}. Please remove it to check out.`);
    return;
  }
  if(!url){ toast('Sorry — we couldn’t start checkout for these items.'); return; }
  $('#checkoutBtn').textContent = 'Taking you to checkout…';
  window.location.href = url;
});

/* ============================================================
   Toast
   ============================================================ */
const toastEl = $('#toast');
let toastTimer;
function toast(msg){
  toastEl.textContent = msg; toastEl.classList.add('is-show');
  clearTimeout(toastTimer); toastTimer = setTimeout(()=> toastEl.classList.remove('is-show'), 2600);
}

/* ============================================================
   Weekly verse
   ============================================================ */
const VERSES = [
  {t:'The Lord is my light and my salvation; whom shall I fear?', r:'Psalm 27:1'},
  {t:'I can do all things through Christ who strengthens me.', r:'Philippians 4:13'},
  {t:'Trust in the Lord with all your heart, and lean not on your own understanding.', r:'Proverbs 3:5'},
  {t:'Be strong and courageous. Do not be afraid; the Lord your God will be with you wherever you go.', r:'Joshua 1:9'},
  {t:'The Lord will fight for you; you need only to be still.', r:'Exodus 14:14'},
  {t:'For I know the plans I have for you, plans to prosper you and not to harm you.', r:'Jeremiah 29:11'},
  {t:'The Lord is my shepherd; I shall not want.', r:'Psalm 23:1'},
  {t:'We walk by faith, not by sight.', r:'2 Corinthians 5:7'},
  {t:'And we know that in all things God works for the good of those who love him.', r:'Romans 8:28'},
  {t:'She is clothed with strength and dignity; she laughs without fear of the future.', r:'Proverbs 31:25'},
  {t:'Cast all your anxiety on him because he cares for you.', r:'1 Peter 5:7'},
  {t:'Let all that you do be done in love.', r:'1 Corinthians 16:14'},
  {t:'Jesus said, I am the way and the truth and the life.', r:'John 14:6'},
  {t:'With God all things are possible.', r:'Matthew 19:26'},
  {t:'Behold, I am doing a new thing; now it springs forth, do you not perceive it?', r:'Isaiah 43:19'},
  {t:'The joy of the Lord is your strength.', r:'Nehemiah 8:10'},
  {t:'Give thanks to the Lord, for he is good; his love endures forever.', r:'Psalm 107:1'},
  {t:'Come to me, all you who are weary, and I will give you rest.', r:'Matthew 11:28'},
  {t:'The name of the Lord is a strong tower; the righteous run to it and are safe.', r:'Proverbs 18:10'},
  {t:'Let your light shine before others, that they may see your good deeds.', r:'Matthew 5:16'},
];
(function setWeeklyVerse(){
  const week = Math.floor(Date.now() / (7*24*60*60*1000));
  const v = VERSES[week % VERSES.length];
  const el = $('#verseText');
  if(el) el.textContent = `“${v.t}” — ${v.r}`;
})();

/* ============================================================
   Header scroll + hero parallax
   ============================================================ */
const header = $('#header'), controls = $('#controls'), heroImg = $('#heroImg');
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
let ticking = false;
let headerH = readHeaderH();
function readHeaderH(){ return parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 72; }
window.addEventListener('resize', () => { headerH = readHeaderH(); });
function onScroll(){
  if(ticking) return; ticking = true;
  requestAnimationFrame(() => {
    const y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 12);                       // always (works with reduced motion)
    controls.classList.toggle('is-stuck', controls.getBoundingClientRect().top <= headerH + 10);
    if(!reduceMotion && y < window.innerHeight){ heroImg.style.transform = `translateY(${y * 0.28}px) scale(1.06)`; }
    ticking = false;
  });
}
window.addEventListener('scroll', onScroll, { passive:true });

/* ============================================================
   Reveal on scroll
   ============================================================ */
const io = new IntersectionObserver((entries) => {
  entries.forEach(en => { if(en.isIntersecting){ en.target.classList.add('is-in'); io.unobserve(en.target); } });
}, { threshold:0.12, rootMargin:'0px 0px -40px 0px' });
$$('.reveal').forEach((el,i) => {
  if(el.classList.contains('card')) el.style.transitionDelay = (Math.min(i,8) * 45) + 'ms';
  io.observe(el);
});
window.addEventListener('load', () => {
  setTimeout(() => $$('.reveal:not(.is-in)').forEach(el => { if(el.getBoundingClientRect().top < innerHeight) el.classList.add('is-in'); }), 600);
});

/* ============================================================
   Mobile nav + newsletter
   ============================================================ */
const navToggle = $('#navToggle');
function closeMobileNav(){ header.classList.remove('nav-open'); navToggle.setAttribute('aria-expanded','false'); }
navToggle.addEventListener('click', () => {
  const open = header.classList.toggle('nav-open'); navToggle.setAttribute('aria-expanded', open);
});
$$('#mobileNav a').forEach(a => a.addEventListener('click', closeMobileNav));

/* Clicking the FaithLabel wordmark / cross returns to the very top of the
   page (verse bar + hero), same as a refresh — closing any open panels. */
$('a.brand')?.addEventListener('click', e => {
  e.preventDefault();
  if(pdp.classList.contains('is-open')) closePDP();
  if(cartEl.classList.contains('is-open')) closeCart();
  closeMobileNav();
  window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
});

$('#signupForm').addEventListener('submit', e => {
  e.preventDefault(); $('#signupForm').reset(); $('#signupNote').hidden = false;
  toast('Welcome to the fold');
});

/* init */
renderCart();
const HASH_CAT = { hoodies:'hoodie', crewnecks:'crewneck', tshirts:'tshirt', all:'all' };
setCat(HASH_CAT[location.hash.replace('#','')] || 'all');
