import puppeteer from 'puppeteer-core';
import fs from 'fs';
import { createRequire } from 'module';
const axe = fs.readFileSync(createRequire(import.meta.url).resolve('axe-core/axe.min.js'), 'utf8');
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
const views = [['everything','',  'light'], ['everything','', 'dark'], ['art','#art','light'], ['art','#art','dark'], ['poetry','#poetry','light'], ['poetry','#poetry','dark']];
const all = {};
for (const [name, hash, theme] of views) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: theme }]);
  await page.goto('http://localhost:8788/' + hash, { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('#stage.in img, #stage.in .verse', { timeout: 30000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 1500));
  // states to test: base, See also open, About open
  for (const state of ['base', 'seealso', 'about']) {
    if (state === 'seealso') await page.evaluate(() => document.getElementById('seeBtn').click());
    if (state === 'about') await page.evaluate(() => { openSee(false); document.getElementById('aboutBtn').click(); });
    await new Promise(r => setTimeout(r, 400));
    await page.evaluate(axe);
    const r = await page.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] })).violations
      .map(v => ({ id: v.id, impact: v.impact, help: v.help, n: v.nodes.length, ex: v.nodes.slice(0, 3).map(n => n.target.join(' ') + ' :: ' + (n.failureSummary || '').split('\n').slice(1, 2).join('')) })));
    all[`${name}-${theme}-${state}`] = r;
  }
  // keyboard walk (base state)
  if (theme === 'light') {
    await page.close();
    const p2 = await browser.newPage(); await p2.setViewport({ width: 1280, height: 800 });
    await p2.goto('http://localhost:8788/' + hash, { waitUntil: 'networkidle2' }); var kp = p2;
    await kp.waitForSelector('#stage.in', { timeout: 30000 }).catch(() => {}); await new Promise(r => setTimeout(r, 2000));
    const order = [];
    for (let i = 0; i < 9; i++) {
      await kp.keyboard.press('Tab');
      order.push(await kp.evaluate(() => { const a = document.activeElement; const r = a.getBoundingClientRect();
        return `${a.tagName.toLowerCase()}${a.id ? '#' + a.id : ''} "${(a.getAttribute('aria-label') || a.textContent || '').trim().slice(0, 30)}" ${r.width > 2 ? 'visible' : 'HIDDEN'} outline=${getComputedStyle(a).outlineStyle}`; }));
    }
    const before = await kp.evaluate(() => document.querySelector('#announce').textContent);
    await kp.evaluate(() => document.getElementById('nextBtn').focus()); await kp.keyboard.press('Enter');
    await new Promise(r => setTimeout(r, 6000));
    const after = await kp.evaluate(() => document.querySelector('#announce').textContent);
    all[`${name}-keyboard`] = { order, nextButtonAdvances: before !== after, announced: after.slice(0, 120) };
    await kp.close(); continue;
  }
  await page.close();
}
await browser.close();
fs.writeFileSync(new URL('../data/a11y-results.json', import.meta.url), JSON.stringify(all, null, 1));
for (const [k, v] of Object.entries(all)) {
  if (Array.isArray(v)) { console.log(`\n## ${k}: ${v.length} issue types`); v.forEach(x => console.log(`  [${x.impact}] ${x.id} (${x.n}) ${x.help}\n     e.g. ${x.ex[0]}`)); }
  else console.log(`\n## ${k}\n  ` + v.order.join('\n  ') + `\n  next button advances: ${v.nextButtonAdvances}\n  announced: ${v.announced}`);
}
