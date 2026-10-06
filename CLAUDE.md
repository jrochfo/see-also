# See also

A StumbleUpon-style microsite for spontaneous discovery, built on Wikipedia.
Inspired by wikipoetics / Earth loading screen on TikTok: the poetry of
Wikipedia image captions.

- Single file: public/index.html (HTML, CSS, JS inline, no build step, no dependencies)
- Hosted on Cloudflare Workers (static assets): wrangler.jsonc serves public/;
  pushing to main on github.com/jrochfo/see-also deploys automatically
- Two modes: everything (Wikipedia thumb box + caption), art (framed on a
  gallery wall)
- Topics (TOPICS) filter "everything"; picked from a Wikipedia-style "See also"
  panel (bottom right, also holds About). Each topic is search queries and/or
  hand-picked titles; #topic in the URL links straight to one
- No albums/movies: their images are non-free (fair use), the rest is PD/CC
- Click anywhere advances; every image links to its source article
- Images come live from the Wikipedia API. "Everything" mixes a curated SEEDS
  list with random articles, filtered by SKIP_FILE and caption length
- Keep it extremely simple: one centered visual, minimal chrome
- The "everything" mode should stay faithful to Wikipedia's thumbnail look