"""Find a caption that has been edited out of an article, in the article's history.

  python3 tools/humanity/recover.py "Whoopee cushion" "awaiting a victim"

Prints the old revision (oldid), the image file it captioned, and a 960px image URL. Add it to
public/humanity.json as {"article", "caption", "img", "oldid"} and the site shows "caption since edited".
If the caption is still live but the image sits in a gallery the live lookup can't read, add "live": true.
"""
import os, re, sys, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from wiki import api, get

title, phrase = sys.argv[1], sys.argv[2]
cont = {}
for _ in range(80):    # up to 4,000 revisions back
    d = api(action='query', prop='revisions', titles=title, rvprop='ids|timestamp|content', rvslots='main', rvlimit=50, **cont)
    pages = d.get('query', {}).get('pages', [])
    for r in (pages[0].get('revisions', []) if pages else []):
        txt = r.get('slots', {}).get('main', {}).get('content', '')
        i = txt.lower().find(phrase.lower())
        if i < 0:
            continue
        files = re.findall(r'(?:File|Image):([^|\]\n]+)', txt[max(0, i - 400):i])
        print('oldid:', r['revid'], ' date:', r['timestamp'])
        if files:
            f = files[-1].strip()
            info = get('https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&prop=imageinfo'
                       '&iiprop=url&iiurlwidth=960&titles=' + urllib.parse.quote('File:' + f))
            pg = info.get('query', {}).get('pages', [{}])[0]
            print('file:', f)
            print('img:', (pg.get('imageinfo') or [{}])[0].get('thumburl', '(not on Commons; check enwiki)').split('?')[0])
        sys.exit()
    if 'continue' not in d:
        break
    cont = {'rvcontinue': d['continue']['rvcontinue']}
print('not found in history')
