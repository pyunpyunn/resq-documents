const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const root = path.resolve(__dirname, '..');
let puppeteer;
try { puppeteer = require('puppeteer-core'); }
catch { puppeteer = require(path.join(os.tmpdir(), 'resqperation-mermaid-renderer/node_modules/puppeteer-core')); }

async function main() {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'assets/manifest.json'), 'utf8'));
  const font = fs.readFileSync(path.join(root, 'assets/Inter.ttf')).toString('base64');
  const chrome = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
  const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ['--disable-gpu'], protocolTimeout: 240000 });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 1000, deviceScaleFactor: 1 });
  await page.setContent(`<html><head><style>@font-face{font-family:Inter;src:url(data:font/ttf;base64,${font}) format('truetype');font-weight:100 900;font-style:normal}html,body{margin:0;padding:0;background:#fff}svg{display:block}text{font-optical-sizing:none}</style></head><body><div id="canvas"></div></body></html>`);
  await page.evaluate(async () => { await document.fonts.load('600 18px Inter'); await document.fonts.load('400 16px Inter'); });
  const sample = process.argv.includes('--sample');
  const selected = sample ? manifest.filter(e => e.mode === 'compact') : manifest;
  const results = [];
  const reportPath = path.join(root, 'assets', sample ? 'render-samples.json' : 'render-results.json');
  const previous = !sample && fs.existsSync(reportPath) ? JSON.parse(fs.readFileSync(reportPath, 'utf8')) : [];
  const cache = new Map(previous.filter(r => !r.error).map(r => [r.relative, r]));
  try {
    for (let index = 0; index < selected.length; index++) {
      const entry = selected[index];
      const input = path.join(root, entry.relative);
      const source = fs.readFileSync(input, 'utf8');
      const digest = crypto.createHash('sha256').update(source).digest('hex');
      let output = input.replace(/\.svg$/i, '.png');
      const cached = cache.get(entry.relative);
      if (cached && cached.hash === digest && fs.existsSync(output)) { results.push(cached); continue; }
      try {
        await page.setViewport({ width: 1400, height: 1000, deviceScaleFactor: 1 });
        const audit = await page.evaluate(async svg => {
          document.getElementById('canvas').innerHTML = svg;
          await document.fonts.ready;
          const rootSvg = document.querySelector('#canvas > svg');
          const view = rootSvg.viewBox.baseVal;
          const clipped = [];
          const tableOverflow = [];
          for (const text of rootSvg.querySelectorAll('text')) {
            if (!text.textContent.trim()) continue;
            const b = text.getBBox();
            if (b.x < 58 || b.y < 0 || b.x + b.width > view.width - 56 || b.y + b.height > view.height - 56) clipped.push(text.textContent);
            const table = text.closest('[data-kind="table"]');
            if (table) {
              const card = table.querySelector('rect');
              const x = +card.getAttribute('x'), y = +card.getAttribute('y'), w = +card.getAttribute('width'), h = +card.getAttribute('height');
              if (b.x < x - 1 || b.x + b.width > x + w + 1 || b.y < y - 1 || b.y + b.height > y + h + 1) tableOverflow.push(text.textContent);
            }
          }
          return { clipped, tableOverflow, font: document.fonts.check('600 18px Inter'), textElements: rootSvg.querySelectorAll('text').length };
        }, source);
        if (!audit.font || audit.clipped.length || audit.tableOverflow.length) throw new Error(JSON.stringify(audit));
        const scale = Math.min(3, 28000 / entry.width, 28000 / entry.height, Math.sqrt(80000000 / (entry.width * entry.height)));
        await page.setViewport({ width: 1400, height: 1000, deviceScaleFactor: scale });
        const png = await page.screenshot({ type: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: entry.width, height: entry.height }, timeout: 180000 });
        try { fs.writeFileSync(output, png); }
        catch (error) {
          if (!['UNKNOWN','EPERM','EACCES','EBUSY'].includes(error.code)) throw error;
          output = input.replace(/\.svg$/i, `_updated_${digest.slice(0, 8)}.png`);
          fs.writeFileSync(output, png);
        }
        results.push({ relative: entry.relative, hash: digest, output: output.replaceAll('\\', '/'), png_relative: path.relative(root,output).replaceAll('\\','/'), scale, width: Math.round(entry.width * scale), height: Math.round(entry.height * scale), ...audit });
        console.log(`${index + 1}/${selected.length} OK ${entry.relative}`);
      } catch (error) {
        results.push({ relative: entry.relative, error: error.message });
        console.log(`${index + 1}/${selected.length} FAILED ${entry.relative}: ${error.message.slice(0, 350)}`);
      }
      fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
    }
  } finally { await browser.close(); }
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
  const failed = results.filter(r => r.error);
  console.log(JSON.stringify({ rendered: results.length - failed.length, failed: failed.length }));
  if (failed.length) process.exitCode = 1;
}
main().catch(error => { console.error(error); process.exit(1); });
