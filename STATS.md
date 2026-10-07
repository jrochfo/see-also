# See also: project stats

Snapshot taken 2026-10-07, when the project was put on the back burner.

## Time
- Elapsed: ~25 hours (2026-10-06 11:42 → 2026-10-07 12:42, US Central)
- Active work: ~7.5 hours (stretches with no gap over 20 minutes)
- Commits landed across 9 distinct clock hours

## Conversation and compute
- Messages from Jake: ~100
- Model calls: ~500, all Claude Opus 5.5
- Tool uses: ~490 (≈385 shell commands, ≈100 file/screenshot reads)
- Tokens (≈ ¾ of a word each):
  - Output written: ~460,000
  - Cache reads: ~205 million (each step re-reads the conversation so far)
  - Cache writes: ~3.4 million
- Background jobs: several hours of slow, rate-limited Wikipedia surveys (poems, poets, 3 Humanity
  mining passes, 2 topic-quality samples)

## Code
- 40 commits at the time of the snapshot
- ~20,700 lines added, ~500 removed (mostly data and tools)
- The site: one 969-line `public/index.html`
- 33 tracked files

## Content
- Humanity: 437 captions (44 featured), from ~3,000 mined candidates read by hand across 3 passes
- Poetry: 367 poems in 17 sections (12 poets + 5 others)
- Art: 2,287 paintings in 11 themes
- Everything: 16 topics

## Shipped
seealso.wiki: three modes (everything, art, poetry) with See also topics; a Humanity collection including an
archive of edited-away captions; link-preview card and home-screen icon; light/dark following the device;
accessibility at zero automated issues; a `tools/` folder for mining, checking and rebuilding content.

## How these were measured
- Git: `git rev-list --count HEAD`, `git log --shortstat`
- Session log: `~/.claude/projects/-Users-jrochford/115b8d8a-6f29-475e-88e4-fdcb08ababe4.jsonl`
  (timestamps, per-call token usage, tool calls)
