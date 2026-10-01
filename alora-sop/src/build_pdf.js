// usage: node build_pdf.js manual.html out.pdf   (run with NODE_PATH pointing at playwright)
const { chromium } = require('playwright');
(async () => {
  const [file, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ viewport: { width: 1000, height: 1200 } })).newPage();
  await page.goto('file://' + require('path').resolve(file));
  await page.emulateMedia({ media: 'print' });
  await page.waitForTimeout(300);
  const info = await page.evaluate(() => {
    const pages = [...document.querySelectorAll('.page')];
    const over = pages.filter(p => p.scrollHeight > p.clientHeight + 2).map(p => ({ id: p.id, sh: p.scrollHeight, ch: p.clientHeight }));
    return { n: pages.length, over };
  });
  await page.pdf({ path: out, width: '8.5in', height: '11in', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log('page divs:', info.n, '| overflowing pages:', info.over.length);
  info.over.slice(0, 40).forEach(o => console.log('  OVERFLOW', o.id, o.sh, '>', o.ch));
  await browser.close();
  if (info.over.length) process.exitCode = 1;
})();
