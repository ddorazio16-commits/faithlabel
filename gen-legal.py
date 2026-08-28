#!/usr/bin/env python3
"""Generate the policy subpages (privacy, terms, shipping-returns, contact)
   sharing the site's styles. The three policy pages carry the copy supplied
   by FaithLabel verbatim; edit it here, not in the generated HTML."""
import os
ROOT = "/Users/donatodorazio/faithlabel"
V = "1787529800"
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='7' fill='%23163BA1'/%3E%3Cpath d='M16 6v20M9 13h14' "
           "stroke='%23C8A24C' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E")
UPDATED = "August 13, 2026"
EMAIL = "dorazioadelina@gmail.com"
# The three policy pages cite the business address; contact.html still uses EMAIL.
POLICY_EMAIL = "hello@faithlabelshop.com"
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

privacy = f"""
<p>FaithLabel respects your privacy and is committed to protecting your personal information. This Privacy Policy explains how we collect, use, disclose, and protect information when you visit <strong>faithlabelshop.com</strong>, make a purchase, contact us, or otherwise interact with our services.</p>
<p>By using our website, you acknowledge the practices described in this Privacy Policy.</p>

<h2>1. Information We Collect</h2>
<p>We may collect personal information that you voluntarily provide to us, including:</p>
<ul>
  <li>Name</li>
  <li>Billing and shipping address</li>
  <li>Email address</li>
  <li>Phone number</li>
  <li>Order and transaction information</li>
  <li>Customer service communications</li>
  <li>Information you provide when subscribing to marketing communications</li>
</ul>
<p>When you make a purchase, payment information is processed by our payment providers. FaithLabel does not directly store complete credit or debit card information.</p>
<p>We may also automatically collect certain information when you visit our website, such as your IP address, browser and device information, pages viewed, referring URLs, and interactions with our website.</p>

<h2>2. How We Use Your Information</h2>
<p>We may use your information to:</p>
<ul>
  <li>Process, fulfill, and deliver orders</li>
  <li>Process payments and refunds</li>
  <li>Communicate with you regarding your order</li>
  <li>Respond to customer service requests</li>
  <li>Prevent fraud and protect the security of our website</li>
  <li>Improve our website, products, and customer experience</li>
  <li>Send promotional communications when you have opted in to receive them</li>
  <li>Comply with applicable legal and regulatory requirements</li>
</ul>

<h2>3. Shopify and Service Providers</h2>
<p>Our store uses Shopify and other third-party service providers to support our e-commerce operations.</p>
<p>These providers may process personal information as necessary to provide services such as website hosting, payment processing, order fulfillment, shipping, analytics, fraud prevention, and marketing.</p>
<p>These third parties process information according to their own terms and privacy practices.</p>

<h2>4. Cookies and Similar Technologies</h2>
<p>FaithLabel and our service providers may use cookies and similar technologies to operate the website, remember preferences, understand website usage, improve performance, prevent fraud, and, where applicable, provide advertising or marketing functionality.</p>
<p>Depending on your location, you may have options to manage certain cookies or data-sharing preferences through our website&rsquo;s privacy controls or your browser settings.</p>

<h2>5. How We Share Information</h2>
<p>We may share personal information with service providers when reasonably necessary to operate our business, including providers involved in:</p>
<ul>
  <li>Website and e-commerce hosting</li>
  <li>Payment processing</li>
  <li>Order production and fulfillment</li>
  <li>Shipping and delivery</li>
  <li>Analytics</li>
  <li>Marketing and communications</li>
  <li>Fraud prevention and security</li>
</ul>
<p>We may also disclose information when required by law, to respond to lawful requests, to protect our rights or the safety of others, or in connection with a merger, acquisition, sale, or transfer of all or part of our business.</p>
<p>We do not sell your personal information for money.</p>
<p>Certain privacy laws define &ldquo;sale&rdquo; or &ldquo;sharing&rdquo; more broadly, particularly in connection with targeted advertising or analytics. Where required by applicable law, eligible customers may exercise available opt-out rights through the privacy controls provided on our website.</p>

<h2>6. Data Retention</h2>
<p>We retain personal information for as long as reasonably necessary to fulfill the purposes described in this Privacy Policy, maintain business and transaction records, resolve disputes, enforce agreements, and comply with legal obligations.</p>

<h2>7. Data Security</h2>
<p>We use reasonable administrative, technical, and organizational safeguards designed to protect personal information. However, no method of electronic transmission or storage can be guaranteed to be completely secure.</p>

<h2>8. Your Privacy Rights</h2>
<p>Depending on where you live, you may have certain rights concerning your personal information, including the right to request access to, correction of, or deletion of certain personal information, or to opt out of certain uses of your information.</p>
<p>To submit a privacy-related request, contact us at <a href="mailto:{POLICY_EMAIL}">{POLICY_EMAIL}</a></p>
<p>We may need to verify your identity before completing certain requests.</p>

<h2>9. Marketing Communications</h2>
<p>If you subscribe to promotional emails, you may unsubscribe at any time by using the unsubscribe link included in those communications.</p>
<p>You may still receive non-promotional communications necessary to complete transactions or provide customer service, such as order confirmations and shipping updates.</p>

<h2>10. Children&rsquo;s Privacy</h2>
<p>Our website is not intended for children under 13, and we do not knowingly collect personal information from children under 13.</p>
<p>If you believe a child has provided personal information to us, please contact us so that we can take appropriate action.</p>

<h2>11. Third-Party Links</h2>
<p>Our website may contain links to third-party websites or services. FaithLabel is not responsible for the privacy, security, or content practices of third-party websites.</p>

<h2>12. Changes to This Privacy Policy</h2>
<p>We may update this Privacy Policy periodically to reflect changes to our business practices, technology, legal requirements, or services.</p>
<p>The date at the top of this page indicates when this Privacy Policy was last updated.</p>

<h2>13. Contact Us</h2>
<p>For questions about this Privacy Policy or your personal information, please contact:</p>
<ul>
  <li><strong>Email:</strong> <a href="mailto:{POLICY_EMAIL}">{POLICY_EMAIL}</a></li>
  <li><strong>Instagram DM:</strong> <a href="{IG}" target="_blank" rel="noopener">@faithlabelshop</a></li>
</ul>
"""

terms = f"""
<p>Welcome to FaithLabel. These Terms of Service govern your use of <strong>faithlabelshop.com</strong> and any purchases made through our website.</p>
<p>Throughout these Terms, &ldquo;FaithLabel,&rdquo; &ldquo;we,&rdquo; &ldquo;us,&rdquo; and &ldquo;our&rdquo; refer to FaithLabel. By accessing our website or purchasing from us, you agree to these Terms. If you do not agree, please do not use our website.</p>

<h2>1. Online Store Terms</h2>
<p>You may use our website and products only for lawful purposes and in accordance with these Terms.</p>
<p>You may not use the website in a way that violates applicable laws, infringes upon the rights of others, interferes with the operation or security of the website, or attempts to gain unauthorized access to our systems.</p>

<h2>2. Products</h2>
<p>We make reasonable efforts to display our products, colors, designs, descriptions, and images as accurately as possible.</p>
<p>However, colors and appearance may vary depending on your screen, device settings, lighting, production process, and other factors.</p>
<p>Because some FaithLabel products may be produced or fulfilled on demand, minor variations may occur between products.</p>
<p>We reserve the right to modify or discontinue products at any time without prior notice.</p>

<h2>3. Pricing</h2>
<p>All prices are displayed in the currency indicated on our website and are subject to change without notice.</p>
<p>We reserve the right to correct pricing, product descriptions, promotions, or other errors. If an error affects an order you have already placed, we may contact you to provide available options, including cancellation and a refund when appropriate.</p>
<p>Applicable taxes and shipping charges may be added during checkout.</p>

<h2>4. Orders</h2>
<p>Submitting an order does not guarantee acceptance.</p>
<p>We reserve the right to refuse, limit, or cancel an order when reasonably necessary, including in cases involving suspected fraud, pricing or inventory errors, payment issues, unauthorized resale activity, or other circumstances that may affect our ability to fulfill the order.</p>
<p>If we cancel an order after payment has been collected, we will issue an appropriate refund.</p>
<p>You are responsible for providing accurate billing, shipping, and contact information when placing an order.</p>

<h2>5. Shipping, Returns, and Refunds</h2>
<p>Shipping, delivery, returns, replacements, and refunds are governed by our <a href="shipping-returns.html"><strong>Shipping &amp; Returns Policy</strong></a>, which is incorporated into these Terms by reference.</p>
<p>Please review that policy before making a purchase.</p>
<p>Customers are responsible for providing a complete and accurate shipping address. FaithLabel is not responsible for delivery problems resulting from incorrect information provided by the customer, except as otherwise required by law.</p>

<h2>6. Intellectual Property</h2>
<p>Unless otherwise stated, the FaithLabel name, branding, logos, original designs, graphics, photographs, written content, website content, and other original materials are owned by or licensed to FaithLabel and are protected by applicable intellectual property laws.</p>
<p>You may not copy, reproduce, distribute, modify, commercially exploit, or create derivative works from our protected content without prior written permission.</p>
<p>Purchasing a FaithLabel product does not transfer ownership of any intellectual property associated with its design or branding.</p>

<h2>7. User Submissions</h2>
<p>If you voluntarily submit reviews, photographs, feedback, comments, or other content to FaithLabel, you represent that you have the right to provide that content and that it does not violate the rights of another person.</p>
<p>We may use feedback you voluntarily provide to improve our products and services.</p>
<p>We will obtain any permissions required by applicable law before using customer-created content for purposes that require additional consent.</p>

<h2>8. Third-Party Services</h2>
<p>Our website may rely on or provide access to third-party platforms, payment processors, fulfillment providers, shipping providers, applications, or websites.</p>
<p>We are not responsible for third-party websites or services that we do not own or control. Your use of third-party services may also be governed by their respective terms and policies.</p>

<h2>9. Prohibited Uses</h2>
<p>You may not use our website to:</p>
<ul>
  <li>Engage in unlawful or fraudulent activity</li>
  <li>Infringe intellectual property or other legal rights</li>
  <li>Transmit malicious code or interfere with website security</li>
  <li>Attempt unauthorized access to accounts, systems, or information</li>
  <li>Scrape, copy, or exploit website content for unauthorized commercial purposes</li>
  <li>Harass, threaten, or abuse others</li>
  <li>Misrepresent your identity or transaction information</li>
</ul>
<p>We reserve the right to restrict access to our services for violations of these Terms.</p>

<h2>10. Disclaimer of Warranties</h2>
<p>To the fullest extent permitted by applicable law, our website and services are provided on an &ldquo;as available&rdquo; basis.</p>
<p>We do not guarantee that the website will always be uninterrupted, error-free, or completely secure.</p>
<p>Nothing in these Terms excludes warranties or consumer rights that cannot legally be excluded.</p>

<h2>11. Limitation of Liability</h2>
<p>To the fullest extent permitted by applicable law, FaithLabel will not be liable for indirect, incidental, special, consequential, or punitive damages arising from your use of the website, services, or products.</p>
<p>Nothing in these Terms limits liability that cannot legally be limited or excluded.</p>

<h2>12. Indemnification</h2>
<p>To the extent permitted by applicable law, you agree to indemnify and hold FaithLabel harmless from claims, damages, liabilities, and reasonable expenses resulting from your unlawful use of the website, your violation of these Terms, or your infringement of another person&rsquo;s rights.</p>

<h2>13. Privacy</h2>
<p>Your use of our website is also subject to our <a href="privacy.html"><strong>Privacy Policy</strong></a>, which explains how personal information is collected, used, and disclosed.</p>

<h2>14. Changes to These Terms</h2>
<p>We may update these Terms periodically. Changes become effective when the revised Terms are posted on our website unless otherwise stated.</p>
<p>Your continued use of the website after updated Terms are posted constitutes acceptance of those Terms to the extent permitted by applicable law.</p>

<h2>15. Severability</h2>
<p>If any provision of these Terms is determined to be unlawful or unenforceable, the remaining provisions will remain in effect to the fullest extent permitted by law.</p>

<h2>16. Entire Agreement</h2>
<p>These Terms, together with our <a href="privacy.html">Privacy Policy</a>, <a href="shipping-returns.html">Shipping &amp; Returns Policy</a>, and other policies displayed on our website, constitute the agreement between you and FaithLabel concerning your use of the website and purchases from us.</p>

<h2>17. Contact</h2>
<p>Questions regarding these Terms may be sent to:<br />
Email: <a href="mailto:{POLICY_EMAIL}">{POLICY_EMAIL}</a></p>
"""

shipping = f"""
<p>Thank you for supporting FaithLabel, a small faith-driven brand. Because each piece is made especially for you, please review the following information before placing your order.</p>

<h2>Made to Order</h2>
<p>Each FaithLabel item is printed individually after your order is placed. Because our pieces are made to order rather than shipped from pre-stocked inventory, please allow time for production before your order ships.</p>

<h2>Shipping Times &amp; Costs</h2>
<ul>
  <li>Shipping costs and estimated delivery times are displayed at checkout based on your order and delivery location.</li>
  <li>Once your order ships, you&rsquo;ll receive a confirmation email with tracking information.</li>
  <li>Delivery estimates are not guaranteed and may be affected by carrier delays, weather, holidays, or other circumstances outside of our control.</li>
</ul>

<h2>Returns, Refunds &amp; Replacements</h2>
<p>Because each FaithLabel piece is made to order, <strong>we do not accept returns or exchanges for buyer&rsquo;s remorse, change of mind, or incorrectly selected sizes.</strong> Please review the size guide provided on each product page carefully before placing your order.</p>
<p>We want you to receive your FaithLabel piece exactly as intended. If your item arrives <strong>damaged, defective, or misprinted</strong>, please contact us within 7 days of delivery at <a href="mailto:{POLICY_EMAIL}">{POLICY_EMAIL}</a> with your order number, a description of the issue, and clear photos showing the problem. We will review the issue and, when eligible, arrange an appropriate replacement or refund.</p>

<h2>Lost Packages</h2>
<p>If your package appears to be lost in transit, please contact us at <a href="mailto:{POLICY_EMAIL}">{POLICY_EMAIL}</a> with your order number. We&rsquo;ll review the tracking information and work with the shipping provider or fulfillment partner to determine the appropriate next steps.</p>
<p>FaithLabel is not responsible for packages marked as delivered by the carrier that are subsequently lost or stolen, except where otherwise required by law.</p>

<h2>Incorrect or Incomplete Addresses</h2>
<p>Customers are responsible for providing a complete and accurate shipping address at checkout.</p>
<p>If an order cannot be delivered or is returned because of an incorrect or incomplete address provided at checkout, additional shipping costs may apply before the order can be resent.</p>

<h2>Order Issues</h2>
<p>If you experience an issue with your order, please contact:</p>
<p><a href="mailto:{POLICY_EMAIL}">{POLICY_EMAIL}</a></p>
<p>Please include your order number so we can assist you as quickly as possible.</p>
<p>Nothing in this policy limits any rights you may have under applicable consumer protection laws.</p>
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

# Each policy carries its own revision date, so updating one page doesn't restamp the others.
PAGES = {
  "privacy.html":         ("Privacy Policy", "Legal", "How FaithLabel collects, uses, and protects your information.", privacy, "August 24, 2026"),
  "terms.html":           ("Terms of Service", "Legal", "The terms for using FaithLabel and buying our products.", terms, "August 24, 2026"),
  "shipping-returns.html":("Shipping & Returns", "Help", "Production times, shipping, and our returns and replacement policy.", shipping, "August 28, 2026"),
  "contact.html":         ("Contact Us", "Help", "Get in touch with the FaithLabel team.", contact, UPDATED),
}

for fn, (title, eyebrow, desc, body, updated) in PAGES.items():
    html = HEAD.format(title=title, desc=desc, eyebrow=eyebrow, updated=updated) + body + FOOT
    open(os.path.join(ROOT, fn), "w", encoding="utf-8").write(html)
    print("wrote", fn)
