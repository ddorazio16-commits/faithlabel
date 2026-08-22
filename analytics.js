/* FaithLabel — Google Analytics 4 (privacy-respecting, IP anonymized).
 * To turn it on: create a free GA4 property at analytics.google.com, copy your
 * Measurement ID (looks like G-XXXXXXXXXX), and paste it below. That's it —
 * every page already loads this file, so analytics goes live everywhere.
 * Leave GA_ID empty to keep analytics off. */
window.GA_ID = ""; // e.g. "G-ABC1234XYZ"

(function () {
  if (!window.GA_ID) return;
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + window.GA_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", window.GA_ID, { anonymize_ip: true });
})();
