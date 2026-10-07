"""Rebuild public/art-themes.json from Wikidata.

  python3 tools/art/build_themes.py

Each art theme = paintings (Wikidata P31 painting) that have an English Wikipedia article and that Wikidata
says depict (P180) any of the theme's subjects. Battle and war scenes are left out. Still life uses genre (P136).
To add a theme: add a line here with Wikidata IDs (look them up at wikidata.org; check the label, IDs are easy
to get wrong, e.g. Q1997 is carbon dioxide, not rainbow), then add a matching ART_TOPICS entry in index.html.
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from wiki import sparql

THEMES = {
    'night':   ['Q405', 'Q575', 'Q523'],                                  # moon, night, star
    'sea':     ['Q165', 'Q9430', 'Q35872', 'Q11446', 'Q40080', 'Q170483'],  # sea, ocean, boat, ship, beach, sailing ship
    'skies':   ['Q8074', 'Q527', 'Q166564', 'Q1052'],                     # cloud, sky, sunset, rainbow
    'sublime': ['Q8502', 'Q81054', 'Q34038', 'Q8072', 'Q35666', 'Q852190'],  # mountain, storm, waterfall, volcano, glacier, shipwreck
    'snow':    ['Q7561', 'Q1311', 'Q23392'],                              # snow, winter, ice
    'flowers': ['Q506', 'Q1107656', 'Q34687', 'Q171497'],                 # flower, garden, rose, sunflower
    'animals': ['Q146', 'Q144', 'Q5113', 'Q726'],                         # cat, dog, bird, horse
    'quiet':   ['Q35473', 'Q199657', 'Q133492', 'Q35197', 'Q571'],        # window, reading, letter, mirror, book
    'music':   ['Q34379', 'Q11639', 'Q638', 'Q8355', 'Q6607', 'Q180733', 'Q5994', 'Q27939'],  # instrument, dance, music, violin, guitar, lute, piano, singing
    'wonders': ['Q235113', 'Q7559', 'Q182559', 'Q7246', 'Q8028'],         # angel, dragon, mermaid, unicorn, fairy
}
NO_WAR = 'FILTER NOT EXISTS { ?p wdt:P180 ?w. VALUES ?w { wd:Q178561 wd:Q198 } } FILTER NOT EXISTS { ?p wdt:P136 wd:Q3374353 }'


def titles(where):
    q = f'''SELECT DISTINCT ?t WHERE {{ ?p wdt:P31 wd:Q3305213. {where} {NO_WAR}
      ?a schema:about ?p; schema:isPartOf <https://en.wikipedia.org/>; schema:name ?t. }}'''
    return sorted({b['t']['value'] for b in sparql(q)})


out = {}
for k, ids in THEMES.items():
    out[k] = titles('VALUES ?d { ' + ' '.join('wd:' + q for q in ids) + ' } ?p wdt:P180 ?d.')
    print(k, len(out[k]), flush=True); time.sleep(1)
out['stilllife'] = titles('?p wdt:P136 wd:Q170571.')
print('stilllife', len(out['stilllife']))
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'art-themes.json'), 'w'), ensure_ascii=False, indent=0)
