"""Which poem articles quote clean, showable stanzas?

  python3 tools/poetry/check.py --poet "Wallace Stevens"        # every poem in "Poetry by / Poems by <poet>"
  python3 tools/poetry/check.py "Ozymandias" "The Kraken"       # specific articles

For each article prints how many clean stanzas it has and the first one. Clean = 2-10 lines, no line over
70 characters, English (no non-Latin script, few French/German/Latin function words), labels like "Chorus"
and line references like "(lines 1-9)" stripped. The site applies the same rules live (stanzasIn in index.html).
Add keepers to a section of public/poems.json; a new poet needs a POETRY_TOPICS entry too.

Survey from 2026-10-06 (clean poems / poem articles): Stevens 70/84, Coleridge 26/36, Yeats 21/44, Burns 19/30,
Blake 16/25, Tennyson 16/40, Carroll 11/14, Dickinson 11/12, Byron 11/29, Housman 6/9, Longfellow 6/17,
Brontë 4/7, Cowper 4/6. Skipped as mostly quote-free: Auden 0/12, Swinburne 0/8, Browning 1/12,
Heaney 1/12, W. C. Williams 1/12, Rossetti 1/6, Wordsworth 2/12. More in tools/data/poet-survey.md.
"""
import html, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from wiki import api, category_members

LABEL = re.compile(r'^(chorus|refrain|verse \d+|(literal |english )?translation|original|middle english|modern english)[:.]?$', re.I)
NOT_ENGLISH = re.compile(r'[Ͱ-ϿЀ-ӿ֐-ۿऀ-෿぀-鿿가-힯Ā-ſǍ-ǜ]')
FOREIGN = re.compile(r'\b(le|la|les|des|et|une|du|und|der|die|das|den|dem|ein|eine|nicht|ich|wir|est|qui|pour|sur|dans|que|mit|sie|wie|nec|quem|quam|tibi|mihi)\b', re.I)


def stanzas(page_html):
    out = []
    for m in re.finditer(r'<blockquote[^>]*>(.*?)</blockquote>|<div[^>]*class="poem"[^>]*>(.*?)</div>', page_html, re.S):
        raw = re.sub(r'<sup.*?</sup>', '', m.group(1) or m.group(2), flags=re.S).replace('\n', ' ')
        raw = re.sub(r'</p>|</dd>|</div>', '\n\n', re.sub(r'<br\s*/?>', '\n', raw))
        text = html.unescape(re.sub(r'<[^>]+>', '', raw))
        for block in re.split(r'\n\s*\n', text):
            lines = [re.sub(r'\s*\((lines? )?[\d.]+[–-][\d.]+\)$|^\d+\.\s+', '', re.sub(r'[\s\xa0]+', ' ', l).strip()) for l in block.split('\n')]
            lines = [l for l in lines if l and not LABEL.match(l) and not re.match(r'^[—―–]', l) and not re.match(r'^([IVXLC]+|\d+)\.?$', l)]
            s = '\n'.join(lines)
            if 2 <= len(lines) <= 10 and all(len(l) <= 70 for l in lines) and not NOT_ENGLISH.search(s) and len(FOREIGN.findall(s)) < 2 and s not in out:
                out.append(s)
    return out


def check(title):
    p = api(action='parse', page=title, prop='text', redirects=1)
    return title, (stanzas(p['parse']['text']) if 'parse' in p else None)


if __name__ == '__main__':
    args = sys.argv[1:]
    titles = sorted(set(category_members('Poetry by ' + args[1]) + category_members('Poems by ' + args[1]))) if args[:1] == ['--poet'] else args
    with ThreadPoolExecutor(2) as ex:
        for t, st in ex.map(check, titles):
            mark = 'MISSING' if st is None else f'{len(st)} clean'
            print(f'== {t}  [{mark}]')
            if st:
                print('   ' + st[0].replace('\n', '\n   '))
