# Tools

Scripts and notes for growing and refining See also. Nothing here is published (the site is `public/`).
Run everything from the project root. Python 3 (no packages needed) and Node 22+.

**Working from the work laptop:** Zscaler intercepts HTTPS. Python's urllib is fine; Node needs
`node --use-system-ca …`. Wikipedia rate-limits bursts ("You are making too many requests"): the tools pace
themselves and retry, so let them run; don't run two at once.

## Humanity (found captions) — `public/humanity.json`

Each entry is `{"article", "caption"}`: the site finds that caption on the live page. Optional:
`featured` (Jake's originals: open the main page, 8% of picks), `img` + `oldid` (caption since edited away;
shown with "caption since edited"), `live: true` (pinned image but caption still current).

1. **Mine** — `python3 tools/humanity/mine.py` mines every category in `tools/humanity/categories.txt`
   (or pass category names). Skips articles already mined (`tools/data/humanity-mined-articles.txt`).
   Filters for short (12–62 chars), plain, everyday captions: no numbers, no proper nouns mid-caption, no
   museum/species/brand words, no diagrams/maps/logos. Output: `tools/data/humanity-candidates-<date>.txt`.
2. **Read by hand** — the step that matters; about 1 in 8 survive. Keep understatement that turns tender or
   funny ("Some amount of time later"), accidental philosophy ("Oranges, like apples, grow on trees."), small
   human moments ("A couple holds hands on their fiftieth anniversary"). People-focused ones land best.
   Skip clinical, sexual, flat, or sad-without-tender. Past passes, with ✓ on keepers:
   `tools/data/humanity-candidates-pass1.txt`, `-pass2.txt`, `-pass3.txt`.
3. **Add** keepers to `public/humanity.json`.
4. **Verify** — `python3 tools/humanity/verify.py` (add `--prune` to drop vanished ones).
5. **Recover** an edited-away caption — `python3 tools/humanity/recover.py "Whoopee cushion" "awaiting a victim"`
   prints the old revision and image URL to pin.

## Poetry — `public/poems.json`

Sections = See also topics (`POETRY_TOPICS` in index.html; a new poet needs an entry with `poet:` for the credit).
- `python3 tools/poetry/check.py --poet "Wallace Stevens"` — every poem article by a poet, with clean-stanza counts.
- `python3 tools/poetry/check.py "Ozymandias"` — specific articles.
- Results so far: `tools/data/poet-survey.md`. Original hand list with sample stanzas and ✂︎ notes: `tools/data/poems-draft.md`.
- Taste notes: heavier poems are fine (Jake: poetry treats them poetically); cut untranslated pages and slurs.

## Art themes — `public/art-themes.json`

`python3 tools/art/build_themes.py` rebuilds every theme from Wikidata ("paintings with an enwiki article that
depict X", battle scenes excluded). Add a theme there + an `ART_TOPICS` entry in index.html. Double-check
Wikidata IDs by label. To hide one painting (takedowns, installation photos), add its title to `HIDE`.

## Everything topics — `TOPICS` in index.html

Each topic: `search` (CirrusSearch queries) and/or `titles` (hand-picked, ~60% of picks when both),
plus `lead` (first captioned picture only), `want` (caption must match), `skip` (caption/title must not
match), `notDesc` (skip by article description). Shared: `TOPIC_SKIP`, `TITLE_SKIP`, `SKIP_FILE`.
- `node --use-system-ca tools/topics/check.mjs` — article counts per topic, and every hand-picked title
  checked (missing / disambiguation / duplicate). Run after editing any list.
- `node --use-system-ca tools/topics/sample.mjs [topic…]` then `python3 tools/topics/sheets.py tools/data/samples.json`
  — ~30 real pictures per topic as contact sheets in `tools/data/sheets/`, to grade by eye.
  Last report: `tools/data/noise-report.md`.

## Visual QA

`tools/qa.sh "#art" light desktop` (or `dark`/`device`, `phone`/`ipad`) screenshots the local dev server
(`npm run dev`) into `tools/data/qa/`. Headless Chrome follows the Mac's appearance; `light` forces light.
Safari/iPad can't be tested this way; avoid CSS 3D transforms (Safari dropped the old 3D gallery floor).

## Link preview — `public/og.jpg`

`tools/og/og.html` is the 1200×630 card. Screenshot it:
`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1200,630 --screenshot=og.png tools/og/og.html`,
save as JPEG to `public/og.jpg`. The photo (sailing stones, Jon Sullivan) is public domain.

## Deploy

Push to `main` → Cloudflare Workers Builds deploys in ~1 minute. Check it's live:
`curl -s "https://seealso.wiki/?v=$RANDOM" | diff -q - public/index.html`

## Accessibility check

`npm run a11y` (dev server running).
Runs axe (WCAG 2.1 A/AA + best practice) on every mode in light and dark, with nothing open, See also open,
and About open, then walks the page with Tab and checks the keyboard Next button and screen-reader announcement.
Last run 2026-10-07: 0 issues in all 18 states.
What's in place: caption as alt text, a polite live region announcing each picture/poem, a "Next picture" /
"Previous picture" pair that appears only on keyboard focus (first stops after the top bar), visible focus
outlines, focus moves into See also when it opens, a hidden h1, landmarks, text contrast ≥ 4.5:1 (the hint's
breathing is kept above it), reduced motion respected.
