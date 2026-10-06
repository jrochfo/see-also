# See also

A StumbleUpon-style microsite for spontaneous discovery, built on Wikipedia.
Inspired by wikipoetics / Earth loading screen on TikTok: the poetry of
Wikipedia image captions.

- Single file: public/index.html (HTML, CSS, JS inline, no build step, no dependencies)
- Hosted on Cloudflare Workers (static assets): wrangler.jsonc serves public/;
  pushing to main on github.com/jrochfo/see-also deploys automatically
- Three modes: everything (Wikipedia thumb box + caption), art (framed on a
  gallery wall), poetry (one stanza on paper on a leather desk blotter; mockup stage)
- Poetry reads public/poems.json (hand-picked poem articles plus whole poets'
  "Poetry by X" categories, by section = POETRY_TOPICS) and pulls a random clean stanza live (stanzasIn)
- Topics (TOPICS) filter "everything"; picked from a Wikipedia-style "See also"
  panel (bottom right, also holds About). Each topic is search queries and/or
  hand-picked titles; #topic in the URL links straight to one
- Art topics (ART_TOPICS) read public/art-themes.json: enwiki painting titles that
  Wikidata says depict each theme's subjects (P180), pulled once via SPARQL
- No albums/movies. Art does show non-free (fair use) images by Jake's choice;
  HIDE lists titles to never show, for takedown requests
- Click anywhere advances; every image links to its source article
- Images come live from the Wikipedia API. "Everything" mixes a curated SEEDS
  list with random articles, filtered by SKIP_FILE and caption length
- Keep it extremely simple: one centered visual, minimal chrome
- The "everything" mode should stay faithful to Wikipedia's thumbnail look