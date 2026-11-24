/**
 * ============================================================================
 * PORTFOLIO VERSION BUMPER & AUTO-INCREMENT ENGINE
 * Designed for Mahendra Mali (Max) Portfolio
 *
 * Capabilities:
 * 1. Default: Increments patch version (e.g. 3.9.0 -> 3.9.1) in package.json,
 *    stamps index.html (<meta name="portfolio-version">, window.PORTFOLIO_VERSION,
 *    and asset query strings ?v=X.Y.Z), and updates backend/src/index.js.
 * 2. --stamp-only: Reads version from package.json and synchronizes index.html
 *    and backend/src/index.js without incrementing patch number.
 * 3. --ci <run_number>: Stamps CI build number into index.html for live tracking.
 * ============================================================================
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const PKG_PATH = path.join(ROOT_DIR, 'package.json');
const HTML_PATH = path.join(ROOT_DIR, 'index.html');
const BACKEND_PATH = path.join(ROOT_DIR, 'backend', 'src', 'index.js');

function bumpVersion() {
  if (!fs.existsSync(PKG_PATH)) {
    console.error('package.json not found');
    process.exit(1);
  }

  const args = process.argv.slice(2);
  const isStampOnly = args.includes('--stamp-only');
  const ciIndex = args.indexOf('--ci');
  const ciRunNumber = (ciIndex !== -1 && args[ciIndex + 1]) ? args[ciIndex + 1] : null;

  const pkg = JSON.parse(fs.readFileSync(PKG_PATH, 'utf8'));
  let currentVersion = pkg.version || '3.9.0';
  let newVersion = currentVersion;

  if (!isStampOnly && !ciRunNumber) {
    const parts = currentVersion.split('.').map(n => parseInt(n, 10));
    if (parts.length === 3 && !isNaN(parts[2])) {
      parts[2] = parts[2] + 1; // Increment patch
    } else {
      parts.push(1);
    }
    newVersion = parts.join('.');
    pkg.version = newVersion;
    fs.writeFileSync(PKG_PATH, JSON.stringify(pkg, null, 2) + '\n', 'utf8');
    console.log(`[Version Bump] package.json -> ${newVersion}`);
  } else {
    console.log(`[Version Sync] package.json current version -> ${currentVersion}`);
  }

  const vTag = `v${newVersion}`;
  const displayVersion = ciRunNumber ? `${vTag}+b${ciRunNumber}` : vTag;

  // 1. Update index.html
  if (fs.existsSync(HTML_PATH)) {
    let html = fs.readFileSync(HTML_PATH, 'utf8');

    // Meta tag
    if (html.includes('name="portfolio-version"')) {
      html = html.replace(/<meta name="portfolio-version" content="[^"]*">/, `<meta name="portfolio-version" content="${displayVersion}">`);
    } else {
      html = html.replace('</head>', `  <meta name="portfolio-version" content="${displayVersion}">\n</head>`);
    }

    // window.PORTFOLIO_VERSION
    if (html.includes('window.PORTFOLIO_VERSION')) {
      html = html.replace(/window\.PORTFOLIO_VERSION\s*=\s*['"][^'"]*['"]/, `window.PORTFOLIO_VERSION = '${displayVersion}'`);
    } else {
      html = html.replace('window.__pageStartTime = performance.now();', `window.__pageStartTime = performance.now();\n    window.PORTFOLIO_VERSION = '${displayVersion}';`);
    }

    // Asset query strings
    html = html.replace(/(href="\.\/css\/[a-zA-Z0-9_-]+\.css)(\?v=[^"]*)?/g, `$1?v=${newVersion}`);
    html = html.replace(/(src="\.\/js\/[a-zA-Z0-9_-]+\.js)(\?v=[^"]*)?/g, `$1?v=${newVersion}`);

    fs.writeFileSync(HTML_PATH, html, 'utf8');
    console.log(`[Version Bump] index.html stamped with ${displayVersion}`);
  }

  // 2. Update backend/src/index.js
  if (fs.existsSync(BACKEND_PATH)) {
    let backendCode = fs.readFileSync(BACKEND_PATH, 'utf8');
    if (backendCode.includes('PORTFOLIO_VERSION')) {
      backendCode = backendCode.replace(/const PORTFOLIO_VERSION = ['"][^'"]*['"]/, `const PORTFOLIO_VERSION = '${displayVersion}'`);
    } else {
      backendCode = backendCode.replace('const CORS_HEADERS = {', `const PORTFOLIO_VERSION = '${displayVersion}';\n\nconst CORS_HEADERS = {`);
    }
    fs.writeFileSync(BACKEND_PATH, backendCode, 'utf8');
    console.log(`[Version Bump] backend/src/index.js stamped with ${displayVersion}`);
  }

  return displayVersion;
}

if (require.main === module) {
  bumpVersion();
}

module.exports = { bumpVersion };
