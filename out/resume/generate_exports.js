const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function generateResumeExports() {
  console.log('🚀 Starting Resume PDF & PNG Generation...');

  const chromePath = path.resolve(__dirname, 'chrome/linux-154.0.8037.92/chrome-linux64/chrome');
  const indexPath = 'file://' + path.resolve(__dirname, 'index.html');

  if (!fs.existsSync(chromePath)) {
    console.error('❌ Chrome executable not found at:', chromePath);
    process.exit(1);
  }

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

  // Set viewport to A4 proportions at high DPI (e.g. 794x1123 px standard 96dpi, or 2x device scale)
  await page.setViewport({
    width: 794,
    height: 1123,
    deviceScaleFactor: 3 // High resolution (300+ DPI equivalent)
  });

  console.log('📄 Navigating to:', indexPath);
  await page.goto(indexPath, { waitUntil: 'networkidle0' });

  // Wait an extra second for web fonts to fully render
  await new Promise(r => setTimeout(r, 1000));

  // Hide toolbar for screenshot & pdf
  await page.evaluate(() => {
    const tb = document.getElementById('toolbar');
    if (tb) tb.style.display = 'none';
    document.body.style.padding = '0';
    document.body.style.backgroundColor = '#ffffff';
  });

  // Check actual element height vs A4 height
  const pageMetrics = await page.evaluate(() => {
    const el = document.getElementById('resumePage');
    return {
      scrollHeight: el.scrollHeight,
      clientHeight: el.clientHeight,
      offsetHeight: el.offsetHeight
    };
  });
  console.log('📐 Page element metrics (px):', pageMetrics);

  const pngPath = path.resolve(__dirname, 'Mahendra_Mali_Resume.png');
  const pdfPath = path.resolve(__dirname, 'Mahendra_Mali_Resume.pdf');

  // 1. Export High-Res PNG
  console.log('📸 Generating high-definition PNG...');
  const resumeElement = await page.$('#resumePage');
  await resumeElement.screenshot({
    path: pngPath,
    type: 'png'
  });
  console.log('✅ PNG generated:', pngPath);

  // 2. Export Crisp Vector PDF
  console.log('📑 Generating print-ready A4 PDF...');
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: {
      top: 0,
      bottom: 0,
      left: 0,
      right: 0
    }
  });
  console.log('✅ PDF generated:', pdfPath);

  await browser.close();

  console.log('🎉 Done! Both PDF and PNG are ready.');
}

generateResumeExports().catch(err => {
  console.error('Error generating exports:', err);
  process.exit(1);
});
