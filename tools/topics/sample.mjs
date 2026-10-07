// Sample ~30 real pictures per "everything" topic, using the site's own topic code.
//   node --use-system-ca tools/topics/sample.mjs [topic ...] > /dev/null    (--use-system-ca needed behind Zscaler)
// Writes tools/data/samples.json; then: python3 tools/topics/sheets.py tools/data/samples.json  -> contact sheets to grade by eye.
import fs from 'fs';
import { fileURLToPath } from 'url';
const root = fileURLToPath(new URL('../../', import.meta.url));
const html = fs.readFileSync(root + 'public/index.html', 'utf8');
const code = html.slice(html.indexOf('/* ————————————————— config'), html.indexOf('/* ————————————————— queue'));
const _fetch = globalThis.fetch;
globalThis.fetch = (u, o = {}) => _fetch(u, { ...o, headers: { 'User-Agent': 'SeeAlso-tools (seealso.wiki)' } });
globalThis.DOMParser = class { parseFromString() { return { querySelectorAll: () => [] }; } };
const { TOPICS, fetchTopic } = new Function(code + '\nreturn { TOPICS, fetchTopic };')();
const want = process.argv.slice(2), out = {};
for (const key of Object.keys(TOPICS)) {
  if (TOPICS[key].humanity || (want.length && !want.includes(key))) continue;
  const items = [], seen = new Set();
  for (let tries = 0; tries < 14 && items.length < 30; tries++) {
    try { for (const i of await fetchTopic(key)) if (!seen.has(i.img)) { seen.add(i.img); items.push({ title: i.title, caption: i.caption, img: i.img }); } }
    catch (e) { await new Promise(r => setTimeout(r, 3000)); }
  }
  out[key] = items.slice(0, 30);
  console.error(key, out[key].length);
  fs.writeFileSync(root + 'tools/data/samples.json', JSON.stringify(out, null, 1));
}
