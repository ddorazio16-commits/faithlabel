# TODO

## Before / around launch

- [ ] **Switch the contact email to the business address.**
      [contact.html](contact.html) still shows `dorazioadelina@gmail.com`, while the three policy
      pages (Privacy, Terms, Shipping & Returns) all direct customers to `hello@faithlabelshop.com`.
      Deliberately deferred — not a bug, just not switched over yet.

      To do it: change `EMAIL` in [gen-legal.py](gen-legal.py) to the business address, then run
      `python3 gen-legal.py`. Don't edit the `.html` files directly — all four legal pages are
      generated and hand edits get overwritten. Once both addresses match, `EMAIL` and
      `POLICY_EMAIL` can collapse back into a single constant.
