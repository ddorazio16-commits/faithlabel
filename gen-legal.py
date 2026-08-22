#!/usr/bin/env python3
"""Generate the policy subpages (privacy, terms, shipping-returns, contact)
   sharing the site's styles. Content is a solid starting point for a
   print-on-demand apparel store — review before launch."""
import os
ROOT = "/Users/donatodorazio/faithlabel"
V = "1787442796"
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='7' fill='%23163BA1'/%3E%3Cpath d='M16 6v20M9 13h14' "
           "stroke='%23C8A24C' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E")
UPDATED = "August 13, 2026"
EMAIL = "dorazioadelina@gmail.com"
IG = "https://www.instagram.com/faithlabelshop"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — FaithLabel</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#163BA1" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="FaithLabel" />
  <meta property="og:title" content="{title} — FaithLabel" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://faithlabelshop.com/assets/og-image.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css?v=%s" />
  <link rel="icon" href="%s" />
  <script src="analytics.js?v=%s" defer></script>
</head>
<body>
  <header class="legal-header">
    <div class="legal-header__in">
      <a class="brand" href="index.html" aria-label="FaithLabel home">
        <span class="brand__mark" aria-hidden="true"><svg viewBox="0 0 32 32" width="24" height="24"><path d="M16 4v24M8 12h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg></span>
        <span class="brand__word">FaithLabel</span>
      </a>
      <a class="legal-back" href="index.html">&larr; Back to shop</a>
    </div>
  </header>
  <main class="legal-wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <p class="updated">Last updated {updated}</p>
""" % (V, FAVICON, V)

FOOT = """  </main>
  <footer class="legal-foot">
    &copy; 2026 FaithLabel &middot;
    <a href="privacy.html">Privacy</a> &middot;
    <a href="terms.html">Terms</a> &middot;
    <a href="shipping-returns.html">Shipping &amp; Returns</a> &middot;
    <a href="contact.html">Contact</a>
  </footer>
</body>
</html>
"""

REVIEW_NOTE = ('<p class="legal-note">This page is a general starting point provided for '
               'convenience and is not legal advice. Please review and adapt it — ideally with '
               'a qualified professional — before you begin selling.</p>')

privacy = f"""
<p>FaithLabel (&ldquo;we,&rdquo; &ldquo;us&rdquo;) respects your privacy. This policy explains what we collect when you visit our store or place an order, how we use it, and the choices you have.</p>

<h2>Information we collect</h2>
<ul>
  <li><strong>Order details</strong> — your name, shipping address, email, and the items you buy, so we can make and deliver your order.</li>
  <li><strong>Payment information</strong> — payments are processed by our payment provider. We never see or store your full card number.</li>
  <li><strong>Contact &amp; marketing</strong> — the email address you give us if you subscribe to updates.</li>
  <li><strong>Usage data</strong> — basic, mostly anonymous information about how the site is used, to keep it working well.</li>
</ul>

<h2>How we use it</h2>
<ul>
  <li>To process, produce, and ship your orders and send order updates.</li>
  <li>To respond to your questions and provide support.</li>
  <li>To send occasional updates if you&rsquo;ve opted in (you can unsubscribe anytime).</li>
  <li>To improve the store and meet legal obligations.</li>
</ul>

<h2>Who we share it with</h2>
<p>We do <strong>not</strong> sell your personal information. We share it only with the partners needed to run the store: our print-and-ship fulfillment partner (Printify and its print providers), our payment processor, and service providers such as email or analytics tools. We may disclose information when required by law.</p>

<h2>Cookies</h2>
<p>We use a small number of cookies to keep the site functioning (for example, remembering your cart) and to understand general usage. You can control cookies through your browser settings.</p>

<h2>Your choices</h2>
<ul>
  <li>Ask us to access, correct, or delete your personal information.</li>
  <li>Unsubscribe from marketing emails at any time.</li>
</ul>

<h2>Data security &amp; children</h2>
<p>We take reasonable steps to protect your information, though no method of transmission is completely secure. Our store is not directed to children, and we do not knowingly collect information from anyone under 13.</p>

<h2>Changes</h2>
<p>We may update this policy from time to time; the date above shows the latest revision.</p>

<h2>Contact</h2>
<p>Questions about your privacy? Email us at <a href="mailto:{EMAIL}">{EMAIL}</a> or message us on <a href="{IG}" target="_blank" rel="noopener">Instagram</a>.</p>
{REVIEW_NOTE}
"""

terms = f"""
<p>Welcome to FaithLabel. By using our store or placing an order, you agree to these terms. Please read them carefully.</p>

<h2>Our products</h2>
<p>Every FaithLabel piece is <strong>made to order</strong> and printed just for you. Because screens vary, actual colors may differ slightly from what you see, and each print may have small, natural variations. Scripture is quoted from public sources; our artwork, designs, and store content are owned by FaithLabel and may not be copied or resold.</p>

<h2>Orders &amp; pricing</h2>
<ul>
  <li>Prices are in U.S. dollars and may change at any time before an order is placed.</li>
  <li>Prices vary by size (larger sizes may cost more); the price shown at checkout is the price you pay.</li>
  <li>We may refuse or cancel an order — for example, if an item is mispriced or unavailable — and will refund any payment taken.</li>
  <li>Applicable taxes and shipping are calculated at checkout.</li>
</ul>

<h2>Shipping &amp; returns</h2>
<p>Production and delivery timelines, and our returns policy for defective or misprinted items, are described on our <a href="shipping-returns.html">Shipping &amp; Returns</a> page and form part of these terms.</p>

<h2>Acceptable use</h2>
<p>Please don&rsquo;t misuse the site, attempt to disrupt it, or use our content without permission.</p>

<h2>Disclaimers &amp; liability</h2>
<p>The store and its products are provided &ldquo;as is.&rdquo; To the fullest extent permitted by law, FaithLabel is not liable for indirect or incidental damages, and our total liability for any order is limited to the amount you paid for it.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of the State of New York, United States, without regard to conflict-of-law rules.</p>

<h2>Changes &amp; contact</h2>
<p>We may update these terms; the date above shows the latest revision. Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
{REVIEW_NOTE}
"""

shipping = f"""
<p>Thank you for supporting a small faith-driven brand. Here&rsquo;s what to expect after you order.</p>

<h2>Made to order</h2>
<p>Each item is printed for you individually, so orders aren&rsquo;t shipped from a warehouse shelf — there&rsquo;s a short production time before your order ships.</p>

<h2>Shipping times &amp; cost</h2>
<ul>
  <li>Shipping cost and estimated delivery are shown at checkout, based on the item and your location.</li>
  <li>You&rsquo;ll receive tracking by email as soon as your order is on its way.</li>
</ul>

<h2>Returns &amp; replacements</h2>
<p>Because every piece is made to order, we don&rsquo;t accept returns for buyer&rsquo;s remorse or an incorrectly chosen size — please use the size guide on each product page before ordering. However, your satisfaction matters:</p>
<ul>
  <li>If your item arrives <strong>damaged, defective, or misprinted</strong>, contact us with a photo and your order number and we&rsquo;ll make it right.</li>
  <li>If a package is lost in transit, reach out and we&rsquo;ll help track it down.</li>
  <li>Orders returned due to an incorrect address provided at checkout may require reshipping at additional cost.</li>
</ul>

<h2>Start a claim</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> or message us on <a href="{IG}" target="_blank" rel="noopener">Instagram</a> with your order number and a photo (for damaged items). We&rsquo;re a small team and reply as quickly as we can.</p>
"""

contact = f"""
<p>We&rsquo;d love to hear from you &mdash; whether it&rsquo;s a question about an order, sizing help, or a word of encouragement.</p>

<h2>Reach us</h2>
<ul>
  <li><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
  <li><strong>Instagram:</strong> <a href="{IG}" target="_blank" rel="noopener">@faithlabelshop</a> &mdash; DMs welcome</li>
</ul>

<h2>Order questions</h2>
<p>If your message is about an existing order, please include your <strong>order number</strong> (and a photo, if something arrived damaged) so we can help right away. See our <a href="shipping-returns.html">Shipping &amp; Returns</a> page for our replacement policy.</p>

<h2>Response time</h2>
<p>We&rsquo;re a small, faith-driven team and reply as soon as we can. Thank you for your patience &mdash; and for wearing your faith boldly.</p>
"""

PAGES = {
  "privacy.html":         ("Privacy Policy", "Legal", "How FaithLabel collects and uses your information.", privacy),
  "terms.html":           ("Terms of Service", "Legal", "The terms for using FaithLabel and buying our products.", terms),
  "shipping-returns.html":("Shipping & Returns", "Help", "Production times, shipping, and our replacement policy.", shipping),
  "contact.html":         ("Contact Us", "Help", "Get in touch with the FaithLabel team.", contact),
}

for fn, (title, eyebrow, desc, body) in PAGES.items():
    html = HEAD.format(title=title, desc=desc, eyebrow=eyebrow, updated=UPDATED) + body + FOOT
    open(os.path.join(ROOT, fn), "w").write(html)
    print("wrote", fn)
