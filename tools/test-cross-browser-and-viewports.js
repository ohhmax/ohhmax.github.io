/**
 * Cross-Browser & Multi-Viewport Verification Suite
 * Generates verified visual artifacts and tests all dynamic interactions
 */

const puppeteer = require('puppeteer');
const path = require('path');

const ARTIFACT_DIR = '/home/max/.gemini/antigravity-cli/brain/a6bcb143-c8e6-4c2f-b521-bc5443868afe';
const TARGET_URL = 'http://localhost:3333';

async function run() {
  console.log('Launching browser test runner...');
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/home/max/Projects/resume/chrome/linux-154.0.8037.92/chrome-linux64/chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const page = await browser.newPage();

  // 1. Desktop Dark Mode
  console.log('Testing Desktop 1280x800 (Dark Mode)...');
  await page.setViewport({ width: 1280, height: 850, deviceScaleFactor: 2 });
  await page.goto(TARGET_URL, { waitUntil: 'networkidle0' });
  await page.screenshot({ path: path.join(ARTIFACT_DIR, 'v4_desktop_dark.png') });

  // 2. Nickname Modal Test
  console.log('Testing Nickname Modal interaction...');
  await page.click('#maxNicknameBadge');
  await page.waitForSelector('#maxNicknameModal.active', { visible: true });
  await page.screenshot({ path: path.join(ARTIFACT_DIR, 'v4_nickname_modal.png') });
  await page.click('#maxNicknameGotItBtn');
  await new Promise(r => setTimeout(r, 400));

  // 3. Photo Highlights Banner & Timeline Gallery Test
  console.log('Testing Photo Highlights & Gallery Timeline Modal...');
  await page.click('#photoHighlightsBanner');
  await page.waitForSelector('#galleryTimelineModal.active', { visible: true });
  await page.screenshot({ path: path.join(ARTIFACT_DIR, 'v4_gallery_timeline.png') });

  // 4. Fullscreen Photo Lightbox Test
  console.log('Testing Fullscreen Photo Lightbox...');
  await page.click('[data-moment-index="1"]');
  await page.waitForSelector('#photoFullscreenLightbox.active', { visible: true });
  await page.screenshot({ path: path.join(ARTIFACT_DIR, 'v4_fullscreen_lightbox.png') });
  await page.click('#photoLightboxCloseBtn');
  await new Promise(r => setTimeout(r, 300));
  await page.click('#galleryTimelineCloseBtn');
  await new Promise(r => setTimeout(r, 400));

  // 5. Mobile Portrait Viewport (390x844 - iPhone / Modern Android)
  console.log('Testing Mobile 390x844...');
  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: path.join(ARTIFACT_DIR, 'v4_mobile_dark.png') });

  // 6. Mobile Unified Bottom Nav Expansion Test
  console.log('Testing Mobile Unified Bottom Nav Dock Expansion...');
  await page.evaluate(() => {
    const btn = document.getElementById('maxhiveMascotBtn');
    if (btn) btn.click();
  });
  await page.waitForSelector('#maxhiveBottomNav.expanded', { visible: true });
  await page.screenshot({ path: path.join(ARTIFACT_DIR, 'v4_mobile_unified_nav_expanded.png') });

  // 7. MaxAI Project Modal on Mobile
  console.log('Testing Projects Navigation & MaxAI Modal...');
  await page.evaluate(() => {
    const link = document.querySelector('[data-drawer-navigate="projects"]');
    if (link) link.click();
  });
  await new Promise(r => setTimeout(r, 600));
  await page.evaluate(() => {
    const card = document.querySelector('.project-card-box');
    if (card) {
      card.scrollIntoView({ behavior: 'instant', block: 'center' });
      card.click();
    }
  });
  await page.waitForSelector('#projectModal.active', { visible: true });
  await page.screenshot({ path: path.join(ARTIFACT_DIR, 'v4_mobile_maxai_project_modal.png') });
  await page.evaluate(() => {
    const close = document.getElementById('projectModalCloseBtn');
    if (close) close.click();
  });
  await new Promise(r => setTimeout(r, 400));

  // 8. Desktop Light Mode Test
  console.log('Testing Light Mode...');
  await page.setViewport({ width: 1280, height: 850, deviceScaleFactor: 2 });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.evaluate(() => {
    const themeBtn = document.getElementById('headerThemeToggleBtn');
    if (themeBtn) themeBtn.click();
  });
  await new Promise(r => setTimeout(r, 400));
  await page.screenshot({ path: path.join(ARTIFACT_DIR, 'v4_desktop_light.png') });

  await browser.close();
  console.log('✔ All multi-viewport tests and visual artifacts created successfully!');
}

run().catch(err => {
  console.error('Test run failed:', err);
  process.exit(1);
});
