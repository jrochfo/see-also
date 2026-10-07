# See also

A quiet discovery site built on the accidental poetry of Wikipedia image captions (wikipoetics). Live at
seealso.wiki. README.md is the overview; tools/README.md documents every content and check process.

## Shape
- Single file: public/index.html (HTML, CSS, JS inline, no build step, no dependencies). Keep it that way.
- Cloudflare Workers static assets (wrangler.jsonc serves public/). Push to main on github.com/jrochfo/see-also
  deploys in ~1 min; confirm with `curl -s "https://seealso.wiki/?v=$RANDOM" | diff -q - public/index.html`.
- `npm run dev` → localhost:8788 with live reload.

## Modes and topics
- everything (Wikipedia thumb box + caption; must stay faithful to Wikipedia's look), art (frame chosen by
  frameFor from the painting's colours, gallery room, wall label), poetry (stanza on paper on a leather blotter).
- See also panel (bottom right) lists the current mode's topics: TOPICS / ART_TOPICS / POETRY_TOPICS. Links:
  #topic for everything, #art/topic, #poetry/topic. Old #produce/#toys/#instruments redirect.
- TOPICS entries: search (CirrusSearch) and/or titles (hand-picked, ~60% of picks), lead (first captioned picture
  only), want / skip / notDesc filters. Shared filters: TOPIC_SKIP, TITLE_SKIP, SKIP_FILE. Avoid deepcat: on broad
  trees (deepcat:"Amusement rides" reached a band's article).
- Plain everything mixes HUMANITY_RATE Humanity, SEED_RATE SEEDS (hand-picked articles) and random articles.
- Humanity: public/humanity.json. featured = Jake's picks (main page opener; FEATURED_SHARE of Humanity picks);
  jake = sent by Jake (hidden #found review view); img + oldid = caption edited away ("caption since edited");
  live = pinned image, caption still current; url = non-Wikipedia link (Wiktionary). First-time visitors (no
  localStorage "visited") always open on INTRO (Sailing stones).
- Art: art-themes.json from Wikidata (tools/art/build_themes.py). Shows non-free art by Jake's choice; HIDE lists
  titles never to show (takedowns, installation photos). NOT_THE_WORK skips "work in a room" lead images.
- Poetry: poems.json sections = POETRY_TOPICS; stanzasIn picks clean English stanzas live.
- Link preview: public/og.jpg (source tools/og/og.html; sailing stones photo is public domain).

## Taste (Jake)
- Extremely simple: one centred visual, minimal chrome. Plain, friendly copy; curly quotes.
- No albums/movies/music (non-free media); no "Did you know" (too close to Wikipedia's own features).
- Humanity: people-focused, tender, understated captions land best. Ask before cutting content.
- Poetry may hold heavier poems; cut untranslated pages and slurs.

## Practical
- Behind Zscaler: Node needs --use-system-ca; Python urllib is fine. Wikipedia rate-limits bursts; pace requests.
- No CSS 3D transforms (Safari/iPad dropped the old 3D floor).
- Accessibility: keep `npm run a11y` at 0 issues (alt text, live announcements, keyboard Next button, contrast ≥ 4.5:1).
