"""Small helpers for talking to Wikipedia / Wikimedia politely (user agent, retries, gentle pacing)."""
import json, time, urllib.request, urllib.parse

UA = {'User-Agent': 'SeeAlso-tools (seealso.wiki; jake.rochford@gmail.com)'}
API = 'https://en.wikipedia.org/w/api.php'
REST = 'https://en.wikipedia.org/api/rest_v1/'


def get(url, tries=4, timeout=40, headers=None):
    """GET a JSON URL, retrying with backoff (Wikipedia rate-limits bursts)."""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={**UA, **(headers or {})})
            return json.load(urllib.request.urlopen(req, timeout=timeout))
        except Exception:
            if i == tries - 1:
                return {}
            time.sleep(2 + 3 * i)


def api(**params):
    params.update(format='json', formatversion=2)
    return get(API + '?' + urllib.parse.urlencode(params))


def search_count(query):
    """How many articles a CirrusSearch query matches (hastemplate:, incategory:, deepcat: ...)."""
    return api(action='query', list='search', srsearch=query, srlimit=1).get('query', {}).get('searchinfo', {}).get('totalhits', 0)


def category_members(cat):
    """Articles directly in a category (no subcategories)."""
    out, cont = [], {}
    while True:
        d = api(action='query', list='categorymembers', cmtitle='Category:' + cat, cmnamespace=0, cmlimit=500, **cont)
        out += [m['title'] for m in d.get('query', {}).get('categorymembers', [])]
        if 'continue' not in d:
            return out
        cont = {'cmcontinue': d['continue']['cmcontinue']}


def media_list(title):
    """Every image in an article, with its caption: [(caption, file, image_url)]. Same source the site uses."""
    d = get(REST + 'page/media-list/' + urllib.parse.quote(title.replace(' ', '_'), safe=''))
    out = []
    for i in d.get('items', []):
        if i.get('type') == 'image' and i.get('caption') and i.get('srcset'):
            src = i['srcset'][-1]['src']
            out.append((i['caption']['text'], i.get('title', ''), 'https:' + src if src.startswith('//') else src))
    return out


def sparql(query):
    """Run a Wikidata SPARQL query; returns the bindings list."""
    d = get('https://query.wikidata.org/sparql?query=' + urllib.parse.quote(query),
            headers={'Accept': 'application/sparql-results+json'}, timeout=120)
    return d.get('results', {}).get('bindings', [])
