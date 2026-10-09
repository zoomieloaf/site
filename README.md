# zoomieloaf.com

The ZoomieLoaf studio website: a landing page, the privacy policy and the terms of use.
Plain HTML and CSS, no build step, no scripts, no cookies.

## Pages

- `/`: landing page with the product list
- `/privacy/`: privacy policy for the site and every product
- `/terms/`: terms of use
- `404.html`: not-found page

## Run locally

```sh
npx serve .
```

## Deploy

Cloudflare Pages, connected to this repo: no build command, output directory `/`.
`_headers` sets the security headers.

## Keep the policy true

Before publishing a product that handles data differently (a new extension, a permission, a network call),
add or update its section in `privacy/index.html` and change the effective date on both legal pages.
The Chrome Web Store listing's privacy answers must match it.
