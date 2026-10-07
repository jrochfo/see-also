// Check the site's topics: article counts per topic, and every hand-picked title (exists? redirect? disambiguation? duplicate?).
//   node --use-system-ca tools/topics/check.mjs
import fs from 'fs';
import { fileURLToPath } from 'url';
const root = fileURLToPath(new URL('../../', import.meta.url));
const html = fs.readFileSync(root + 'public/index.html', 'utf8');
const i = html.indexOf('const sp = c =>'), j = html.indexOf('// Never show articles');
const { TOPICS } = new Function(html.slice(i, j) + '\nreturn { TOPICS };')();
const H = { 'User-Agent': 'SeeAlso-tools (seealso.wiki)' };
const sleep = ms => new Promise(r => setTimeout(r, ms));
const api = async q => {   // retries with backoff: Wikipedia answers bursts with "too many requests"
  for (let i = 0; ; i++) {
    const r = await fetch('https://en.wikipedia.org/w/api.php?format=json&formatversion=2&' + q, { headers: H });
    const text = await r.text();
    try { await sleep(800); return JSON.parse(text); } catch (e) { if (i > 7) throw e; await sleep(6000 * (i + 1)); }
  }
};
for (const [k, t] of Object.entries(TOPICS)) {
  if (t.humanity) continue;
  let n = 0;
  for (const s of t.search || []) n += (await api('action=query&list=search&srlimit=1&srsearch=' + encodeURIComponent(s))).query.searchinfo.totalhits;
  const titles = t.titles || [], dupes = titles.filter((x, i) => titles.indexOf(x) !== i), problems = [];
  for (let a = 0; a < titles.length; a += 45) {
    const q = (await api('action=query&redirects=1&prop=pageprops&ppprop=disambiguation&titles=' + encodeURIComponent(titles.slice(a, a + 45).join('|')))).query;
    for (const p of q.pages) if (p.missing !== undefined) problems.push('missing: ' + p.title); else if (p.pageprops) problems.push('disambiguation: ' + p.title);
  }
  console.log(`${t.label.padEnd(26)} ${String(n).padStart(6)} articles + ${titles.length} hand-picked` + (dupes.length ? `  DUPES: ${dupes}` : '') + (problems.length ? `  ${problems.join('; ')}` : ''));
}
