# Like, Share & Subscribe Embed

**Status:** Backlog idea — captured 2026-03-11
**Origin:** Built like/share/subscribe natively into fullstackpm.tech blog; realized the pattern is useful for any content site.

---

## The Problem

Every blog, newsletter, and content site needs the same three engagement primitives:
- **Like** — lightweight social signal, no account required
- **Share** — one-click to LinkedIn, X, copy link
- **Subscribe** — email capture with newsletter hook

Most sites either build this from scratch (time-consuming, reinvented every time) or use heavy third-party platforms (Disqus, ConvertKit widgets) that are slow, ugly, hard to style, and own your data.

There's no clean, embeddable, self-hostable widget that handles all three with a single script tag.

---

## The Solution

A lightweight embeddable widget — drop one `<script>` tag into any HTML page and get a fully functional like/share/subscribe bar, styled to match the host site.

```html
<script src="https://engage.fullstackpm.tech/widget.js"
        data-site-id="your-site-id"
        data-page-id="your-post-slug">
</script>
```

Widget renders inline:

```
❤️ 12 Likes    [LinkedIn] [X] [Copy Link]    [Subscribe ___________] [→]
```

---

## Inputs & Outputs

**Inputs (from host site):**
- `site-id` — identifies the customer/property
- `page-id` — identifies the specific piece of content
- Optional: `theme` (light/dark/auto), `accent-color`, `subscribe-placeholder`

**Outputs (to host site):**
- Rendered widget matching the page's color scheme
- Real-time like count (HTMX or lightweight JS polling)
- Share URLs auto-constructed from current page URL
- Email capture POSTed to the embed service's newsletter store

**Data returned to customer:**
- Dashboard: likes per page, shares tracked, subscriber list export
- Webhook on new subscriber (connect to Mailchimp, ConvertKit, etc.)

---

## Technical Approach

**Phase 1 — Hosted widget (SaaS)**
- Central API handles likes, shares, subscribers per `site-id + page-id`
- Widget JS served from CDN, renders via HTMX or vanilla JS
- Anonymous visitor dedup via first-party cookie (same pattern as fullstackpm.tech)
- SQLite → Postgres as it scales

**Phase 2 — Self-hostable**
- Docker image customers can deploy on their own infra
- Same API, no data leaves their server
- Useful for privacy-conscious publishers, enterprise

**Phase 3 — Analytics dashboard**
- Per-page engagement metrics
- Subscriber growth over time
- Top-shared content

---

## Why It Matters

**Who needs it:**
- Independent bloggers and newsletter writers (Substack refugees who want their own domain)
- Small SaaS companies with content marketing blogs
- Developer tools and documentation sites
- Portfolio sites like fullstackpm.tech

**Why now:**
- Creator economy is decentralizing off big platforms — people want owned audiences
- Third-party comment/engagement widgets (Disqus etc.) are dying or getting bloated
- Privacy regulations make third-party tracking harder — first-party embeds are the right direction
- The fullstackpm.tech implementation already proved the pattern works

**Differentiation from existing tools:**
- Disqus — comments only, heavy, ad-supported, ugly
- ConvertKit forms — subscribe only, not embeddable as a bar, no likes/shares
- AddThis / ShareThis — dead or dying, privacy nightmare, no likes
- This — all three primitives, lightweight, styleable, data ownership

---

## Smallest Viable Version

1. Hosted API (FastAPI, same stack as fullstackpm.tech)
2. One JS file (~5KB) that renders the widget
3. Like toggle (anonymous, cookie-deduped)
4. Share buttons (LinkedIn, X, copy)
5. Email capture → stored in DB, exportable as CSV
6. One dashboard page: subscriber list + like counts per page

No auth required for widget users. Site owners log in to see their dashboard.

---

## Business Model Options

- **Free tier:** Up to 1 site, 1,000 likes/month, 100 subscribers stored
- **Pro ($9/month):** Unlimited sites, unlimited likes, 10,000 subscribers, webhooks
- **Self-hosted (one-time $49):** Docker image, run on own infra

---

## Next Steps

1. Validate demand — post the idea, see if anyone asks for it
2. Scope the MVP (widget JS + API + basic dashboard)
3. Build on top of fullstackpm.tech's existing likes/newsletter infrastructure
4. Ship as a standalone subdomain: `engage.fullstackpm.tech` or new domain
