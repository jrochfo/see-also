"""Check every Humanity caption is still on its Wikipedia page.

  python3 tools/humanity/verify.py           # report
  python3 tools/humanity/verify.py --prune   # also drop ones that are gone

Entries with their own "img" are skipped (they're pinned). A caption that has vanished has usually been
edited away: recover it with recover.py, or drop it.
"""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from wiki import media_list

P = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'humanity.json')
H = json.load(open(P))


def ok(h):
    return True if h.get('img') else any(h['caption'].lower() in c.lower() for c, _, _ in media_list(h['article']))


with ThreadPoolExecutor(3) as ex:
    res = list(ex.map(ok, H))
gone = [h for h, r in zip(H, res) if not r]
for h in gone:
    print('missing:', h['article'], '|', h['caption'])
print(f'{len(H) - len(gone)} of {len(H)} found')
if '--prune' in sys.argv and gone:
    json.dump([h for h, r in zip(H, res) if r], open(P, 'w'), ensure_ascii=False, indent=1)
    print('pruned', len(gone))
