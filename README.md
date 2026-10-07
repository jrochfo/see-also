# See also

**[seealso.wiki](https://seealso.wiki)** — a picture from Wikipedia, with the caption somebody wrote for it. Click anywhere for another.

A small, quiet site for spontaneous discovery, built on the accidental poetry of Wikipedia image captions: the
volunteer who wrote "Tracks are sometimes non-linear" under a photo of a sailing stone, or "A whoopee cushion
awaiting a victim". Inspired by the wikipoetics and Earth-loading-screen corners of TikTok.

## Three ways to look

- **🌍 Everything** — a captioned picture from a Wikipedia article, in Wikipedia's own thumbnail frame. Opens on a
  hand-picked favourite; first-time visitors always see the sailing stones.
- **🖼️ Art** — a painting framed on a gallery wall, the frame chosen from the painting's colours, with a wall label.
- **🪶 Poetry** — one stanza from a poem's Wikipedia article, on paper on a leather desk blotter.

Each mode has **See also** topics (bottom right): Humanity, Dinosaurs, Birds, Sweets, Space, Rides… for
everything; Night, The sea, Quiet rooms, Wonders… for art; nursery rhymes and poets for poetry. Topics link
directly, e.g. [seealso.wiki/#humanity](https://seealso.wiki/#humanity), [#art/snow](https://seealso.wiki/#art/snow),
[#poetry/dickinson](https://seealso.wiki/#poetry/dickinson).

Light and dark mode follow the device. Keyboard: → / Space for the next one, ← to go back.

## How it works

Everything is live from Wikipedia's public APIs; nothing is copied or hosted except a few lists of article titles.

```
public/
  index.html         the whole site: HTML, CSS and JS in one file, no build step, no framework
  humanity.json      found captions for the Humanity topic (article + caption; some pinned images)
  art-themes.json    painting articles per art theme, from Wikidata "depicts"
  poems.json         poem articles per poetry section
  og.jpg, apple-touch-icon.png
tools/               scripts for growing and checking the content (see tools/README.md)
```

- **Everything topics** are Wikipedia searches (by infobox or category) and/or hand-picked titles, with filters
  that skip diagrams, maps, specimens and the like.
- **Humanity** is curated: captions mined from everyday-life categories and read by hand, plus finds sent in.
  Captions Wikipedia has since edited away are kept, marked *caption since edited*, linking to the old version.
- **Art themes** come from Wikidata ("paintings that depict snow…"). Art shows some non-free works under fair use;
  anything can be removed on request (`HIDE` in index.html).
- **Poetry** reads each poem's article live and picks a clean stanza at random.

## Develop

```sh
npm install
npm run dev        # http://localhost:8788, reloads on save
```

Push to `main` and Cloudflare Workers Builds deploys it (static assets, `wrangler.jsonc`) in about a minute.

Checks and content tools — `npm run a11y` (axe + keyboard walk), `npm run topics` (topic sizes and title
checks), Humanity mining, poem and art rebuilds — are documented in [tools/README.md](tools/README.md).

## Credits

Images and text: Wikipedia and Wikimedia Commons contributors, mostly CC BY-SA; each picture links to its source.
Home screen icon: [Twemoji](https://github.com/jdecked/twemoji), CC BY 4.0. Not affiliated with the Wikimedia
Foundation — if you enjoy this, [consider giving a little to Wikipedia](https://donate.wikimedia.org).

Made by [Jake Rochford](https://www.jakerochford.com/).
