"""Mine Wikipedia captions for the Humanity topic.

  python3 tools/humanity/mine.py                 # mines every category in categories.txt not mined before
  python3 tools/humanity/mine.py "Breakfast foods" "Bathing"   # or just these

Writes tools/data/humanity-candidates-<date>.txt: one "Article|caption" per line, for reading by hand.
Copy the keepers into public/humanity.json as {"article": ..., "caption": ...}. Then run verify.py.

Filters aim at the found-poetry feel: short, plain, literal, everyday.
"""
import json, os, re, sys, datetime
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from wiki import category_members, media_list

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
SEEN = os.path.join(HERE, '..', 'data', 'humanity-mined-articles.txt')   # articles already mined, so reruns skip them

MIN, MAX = 12, 62
SKIP_FILE = re.compile(r'\.svg|map|logo|diagram|chart', re.I)
DRY = re.compile(r'\d|museum|collection|exhibit|logo|poster|advert|patent|portrait|statue|illustration|engraving|painting|diagram|'
                 r'map\b|chart|cover|label|stamp|coin|brand|packag|cross[- ]section|schematic|structure|production|factory|'
                 r'manufactur|species|genus|commercial|sold|sale|price|market|scan|graph|brain|cortex|neuron', re.I)


def plain(c):
    if not (MIN <= len(c) <= MAX) or DRY.search(c):
        return False
    # a capitalised word after the first usually means a specific place/person/product: reads as documentation
    return not any(w[:1].isupper() and w != 'I' for w in c.split()[1:])


def main():
    cats = sys.argv[1:] or [l.strip() for l in open(os.path.join(HERE, 'categories.txt')) if l.strip() and not l.startswith('#')]
    seen_articles = set(open(SEEN).read().splitlines()) if os.path.exists(SEEN) else set()
    have = {h['caption'].lower() for h in json.load(open(os.path.join(ROOT, 'public', 'humanity.json')))}
    arts = sorted({a for c in cats for a in category_members(c) if not a.startswith('List of')} - seen_articles)
    print(len(arts), 'new articles to mine', flush=True)
    with ThreadPoolExecutor(2) as ex:       # two at a time: Wikipedia throttles bursts
        results = list(ex.map(lambda t: (t, media_list(t)), arts))
    out, dupe = [], set(have)
    for t, caps in results:
        for c, f, _ in caps:
            c = re.sub(r'\[\d+\]', '', c).strip()
            if SKIP_FILE.search(f) or not plain(c) or c.lower() in dupe:
                continue
            dupe.add(c.lower()); out.append(f'{t}|{c}')
    path = os.path.join(HERE, '..', 'data', f'humanity-candidates-{datetime.date.today()}.txt')
    open(path, 'w').write('\n'.join(out) + '\n')
    open(SEEN, 'a').write(''.join(a + '\n' for a in arts))
    print(len(out), 'candidates ->', os.path.relpath(path, ROOT))


if __name__ == '__main__':
    main()
