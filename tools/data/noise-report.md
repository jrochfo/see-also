# Topic noise report (2026-10-06)

~30 real pictures per "everything" topic (tools/topics/sample.mjs), graded by eye on contact sheets.
good = a picture of the thing, nice to look at · flat = on topic but dull · off = wrong or unpleasant.

| Topic | Before | After fixes | What the off ones were / what fixed it |
|---|---|---|---|
| Dinosaurs | 40% good, 33% off | ~87% good | skull diagrams, bone drawings, maps → only accept restoration/skeleton/mount captions |
| Fruits & vegetables | 31% good, 41% off | ~55% → est. 75–80% | flowers, trees, chemistry → hand-picked list of ~110 + skip seeds/trees/stews |
| Space | 44% good | ~65% → est. 80% | light curves, maps, survey frames → famous-object list + skips |
| Birds | 72% | ~92% | museum eggs, a rabbit → famous list + skip egg/specimen/skull |
| Bugs | 62% | ~85% | pinned specimens, all bees → famous list + skips |
| Sea creatures | 82% | ~90% | charts, fossil jaws, all turtles → famous list |
| Sweets | 68% | ~75% → est. 85% | boxes, cake pans, factories, shops → skips |
| Toys | 50% | ~80% | packaging, stores, companies → skips |
| Weather | 73% | ~77% → est. 90% | radar maps, instruments, lab demos → skips |
| Trains / Mushrooms / Instruments / Towers / Waterfalls | 70–89% | similar | stray diagrams, a medal, a death poem (Kegon Falls) → shared filter |

Lessons:
- Size doesn't matter past a few hundred articles; what you show from each article does. Science articles' random captioned
  picture is often a diagram, so animal/food topics use `lead: true` (first captioned picture) and famous lists.
- One shared caption filter (TOPIC_SKIP) removes most "off" pictures everywhere. Per-topic `skip`, `want`, `notDesc` handle the rest.
- Re-run this after any topic change: node --use-system-ca tools/topics/sample.mjs && python3 tools/topics/sheets.py tools/data/samples.json
