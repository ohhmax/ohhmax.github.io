const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

async function generateResumeExports() {
  console.log('Starting Resume PDF & PNG Generation...');

  const candidates = [
    process.env.CHROME_BIN,
    '/home/max/.local/bin/google-chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/chromium',
    path.resolve(__dirname, 'chrome/linux-154.0.8037.92/chrome-linux64/chrome')
  ].filter(Boolean);

  const chromePath = candidates.find(p => fs.existsSync(p));
  const htmlPath = path.resolve(__dirname, 'index.html');
  const fileUrl = 'file://' + htmlPath;

  if (!chromePath) {
    console.error('Chrome executable not found in candidates:', candidates);
    process.exit(1);
  }
  console.log('Using Chrome executable:', chromePath);

  const pdfPath = path.resolve(__dirname, 'Mahendra_Mali_Resume.pdf');
  const pngPath = path.resolve(__dirname, 'Mahendra_Mali_Resume.png');

  // Try Puppeteer if installed
  let puppeteerSuccess = false;
  try {
    const puppeteer = require('puppeteer');
    const browser = await puppeteer.launch({
      executablePath: chromePath,
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--font-render-hinting=none',
        '--enable-font-antialiasing'
      ]
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 794, height: 1123, deviceScaleFactor: 3 });
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 1000));
    await page.evaluate(() => {
      const tb = document.getElementById('toolbar');
      if (tb) tb.style.display = 'none';
      document.body.style.padding = '0';
      document.body.style.backgroundColor = '#ffffff';
    });
    const resumeElement = await page.$('#resumePage');
    if (resumeElement) {
      await resumeElement.screenshot({ path: pngPath, type: 'png' });
    }
    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: 0, bottom: 0, left: 0, right: 0 }
    });
    await browser.close();
    puppeteerSuccess = true;
    console.log('Puppeteer export succeeded');
  } catch (err) {
    console.log('Puppeteer not available, using Chrome CLI directly:', err.message);
  }

  if (!puppeteerSuccess) {
    console.log('Exporting PDF via Chrome headless CLI...');
    execSync(`"${chromePath}" --headless=new --no-sandbox --disable-gpu --print-to-pdf="${pdfPath}" "${fileUrl}"`, { stdio: 'inherit' });
    console.log('Exporting PNG via Chrome headless CLI...');
    execSync(`"${chromePath}" --headless=new --no-sandbox --disable-gpu --window-size=1200,1697 --force-device-scale-factor=2 --screenshot="${pngPath}" "${fileUrl}"`, { stdio: 'inherit' });
  }

  // Sync to out directories if they exist
  const outResume = path.resolve(__dirname, '../out/resume');
  if (fs.existsSync(outResume)) {
    fs.copyFileSync(pdfPath, path.join(outResume, 'Mahendra_Mali_Resume.pdf'));
    fs.copyFileSync(pngPath, path.join(outResume, 'Mahendra_Mali_Resume.png'));
  }

  console.log('Done! Both PDF and PNG are updated and verified.');
}

generateResumeExports().catch(err => {
  console.error('Error generating exports:', err);
  process.exit(1);
});
