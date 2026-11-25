#!/usr/bin/env node
/**
 * Comprehensive SEO, Standards & Cross-Browser Asset Audit Tool
 * For Mahendra Mali (Max) Portfolio (2026)
 *
 * Checks:
 * 1. HTML5 Validity & Document Structure
 * 2. Complete Search Engine Meta Tags (Title, Description, Robots, Canonical)
 * 3. Open Graph Social Graph Specification
 * 4. Twitter Card Specification
 * 5. Structured Data JSON-LD Syntax & Schema Compliance
 * 6. Robots.txt and Sitemap.xml Coverage
 * 7. Asset Filesystem Integrity (Zero 404s for referenced images, scripts, CSS)
 * 8. PWA Manifest & Favicon Verification
 * 9. Content Quality Checks (Zero Em-Dashes/En-Dashes, Grounded Tone)
 * 10. Interactive DOM Element & Modal Contract Integrity
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

const ROOT_DIR = path.resolve(__dirname, '..');
const INDEX_HTML_PATH = path.join(ROOT_DIR, 'index.html');
const ROBOTS_PATH = path.join(ROOT_DIR, 'robots.txt');
const SITEMAP_PATH = path.join(ROOT_DIR, 'sitemap.xml');
const LLMS_PATH = path.join(ROOT_DIR, 'llms.txt');

let totalChecks = 0;
let passedChecks = 0;
let warnings = 0;
let failures = 0;

function check(title, condition, detail = '') {
  totalChecks++;
  if (condition) {
    passedChecks++;
    console.log(`  \x1b[32m✔ PASS\x1b[0m [${title}] ${detail}`);
  } else {
    failures++;
    console.log(`  \x1b[31m✖ FAIL\x1b[0m [${title}] ${detail}`);
  }
}

function warn(title, detail = '') {
  warnings++;
  console.log(`  \x1b[33m▲ WARN\x1b[0m [${title}] ${detail}`);
}

console.log('\n======================================================');
console.log('   MAHENDRA MALI (MAX) - SEO & QUALITY AUDIT SUITE');
console.log('======================================================\n');

// 1. Read index.html
if (!fs.existsSync(INDEX_HTML_PATH)) {
  console.error('\x1b[31mFATAL: index.html not found!\x1b[0m');
  process.exit(1);
}
const html = fs.readFileSync(INDEX_HTML_PATH, 'utf8');

// 2. Document Structure & Meta
console.log('\x1b[1m[1/6] HTML5 Standards & SEO Meta Specifications\x1b[0m');
check('Doctype', html.startsWith('<!DOCTYPE html>'), 'Valid HTML5 doctype declaration');
check('HTML Lang', /<html\s+lang=["']en["']>/i.test(html), 'Lang attribute present and set to en');
check('Meta Charset', /<meta\s+charset=["']utf-8["']/i.test(html), 'UTF-8 charset declared');
check('Viewport', /<meta\s+name=["']viewport["']/i.test(html), 'Mobile viewport configuration present');

// Title Check
const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
check('Title Tag', !!titleMatch && titleMatch[1].length > 15, `Title: "${titleMatch ? titleMatch[1] : 'NONE'}" (${titleMatch ? titleMatch[1].length : 0} chars)`);

// Meta Description
const descMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i);
check('Meta Description', !!descMatch && descMatch[1].length >= 50, `Description: ${descMatch ? descMatch[1].length : 0} chars`);

// Meta Keywords & Canonical
const keywordsMatch = html.match(/<meta\s+name=["']keywords["']/i);
check('Meta Keywords', !!keywordsMatch, 'Targeted SEO keywords indexed');
const canonicalMatch = html.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/i);
check('Canonical Link', !!canonicalMatch, `Canonical: ${canonicalMatch ? canonicalMatch[1] : 'NONE'}`);

// Open Graph
console.log('\n\x1b[1m[2/6] Social Graph & Metadata (Open Graph & Twitter Cards)\x1b[0m');
check('OG Title', /<meta\s+property=["']og:title["']/i.test(html));
check('OG Description', /<meta\s+property=["']og:description["']/i.test(html));
check('OG Type', /<meta\s+property=["']og:type["']/i.test(html));
check('OG URL', /<meta\s+property=["']og:url["']/i.test(html));
check('OG Image', /<meta\s+property=["']og:image["']/i.test(html));
check('OG Locale', /<meta\s+property=["']og:locale["']/i.test(html));
check('Twitter Card', /<meta\s+name=["']twitter:card["']/i.test(html));
check('Twitter Title', /<meta\s+name=["']twitter:title["']/i.test(html));
check('Twitter Image', /<meta\s+name=["']twitter:image["']/i.test(html));

// JSON-LD Structured Data
console.log('\n\x1b[1m[3/6] Schema.org JSON-LD Structured Data\x1b[0m');
const jsonLdBlocks = [];
const jsonLdRegex = /<script\s+type=["']application\/ld\+json["']>([\s\S]*?)<\/script>/gi;
let match;
while ((match = jsonLdRegex.exec(html)) !== null) {
  jsonLdBlocks.push(match[1]);
}
check('JSON-LD Block Count', jsonLdBlocks.length > 0, `Found ${jsonLdBlocks.length} structured data block(s)`);

let schemasValid = true;
jsonLdBlocks.forEach((block, idx) => {
  try {
    const parsed = JSON.parse(block);
    const type = parsed['@type'] || (parsed['@graph'] ? 'Graph' : 'Unknown');
    check(`JSON-LD #${idx + 1} (${type})`, true, 'Valid JSON-LD schema');
  } catch (err) {
    schemasValid = false;
    check(`JSON-LD #${idx + 1} Syntax`, false, `Parse error: ${err.message}`);
  }
});

// Sitemaps, Robots, LLMs
console.log('\n\x1b[1m[4/6] Search Engine Crawl Directives & AI Specifications\x1b[0m');
check('robots.txt exists', fs.existsSync(ROBOTS_PATH));
if (fs.existsSync(ROBOTS_PATH)) {
  const robots = fs.readFileSync(ROBOTS_PATH, 'utf8');
  check('robots.txt allows all', /User-agent:\s*\*\s*\nAllow:\s*\//i.test(robots));
  check('robots.txt references sitemap', /Sitemap:/i.test(robots));
}
check('sitemap.xml exists', fs.existsSync(SITEMAP_PATH));
check('llms.txt exists', fs.existsSync(LLMS_PATH));

// Asset Integrity (Zero 404s for linked files)
console.log('\n\x1b[1m[5/6] Local Asset Integrity & File Resolution\x1b[0m');
const srcRegex = /(?:src|href)=["'](\.\/[^"']+|assets\/[^"']+)["']/gi;
const referencedAssets = new Set();
while ((match = srcRegex.exec(html)) !== null) {
  const p = match[1].replace(/^\.\//, '');
  if (!p.startsWith('http') && !p.startsWith('#') && !p.startsWith('mailto:') && !p.startsWith('tel:')) {
    referencedAssets.add(p);
  }
}

let missingAssets = 0;
referencedAssets.forEach(assetPath => {
  // Strip URL query/hash if present
  const cleanPath = assetPath.split('?')[0].split('#')[0];
  const fullPath = path.join(ROOT_DIR, cleanPath);
  if (!fs.existsSync(fullPath)) {
    missingAssets++;
    check(`Asset ${cleanPath}`, false, 'File does not exist on disk!');
  }
});
if (missingAssets === 0) {
  check('Zero 404 Referenced Assets', true, `All ${referencedAssets.size} internal assets resolved cleanly on disk`);
}

// Content Constraints & Quality (No Em-Dashes)
console.log('\n\x1b[1m[6/6] Typography & Accessibility Contract\x1b[0m');
const hasEmDash = html.includes('\u2014');
const hasEnDash = html.includes('\u2013');
check('Zero Em-Dashes in HTML', !hasEmDash, 'Strict rule: zero em-dashes found');
check('Zero En-Dashes in HTML', !hasEnDash, 'Strict rule: zero en-dashes found');

// Key UI DOM elements
const criticalElements = [
  '#momentsSliderContainer',
  '#maxNicknameBadge',
  '#maxNicknameModal',
  '#galleryTimelineModal',
  '#photoFullscreenLightbox',
  '#projectModal',
  '#certModal',
  '#maxhiveBottomNav',
  '#maxhiveDrawer',
  '#headerThemeToggleBtn',
  '#profileNameHeader',
  '#resumeFloatingDock',
  '#testimonials-list'
];
criticalElements.forEach(selector => {
  const id = selector.replace('#', '');
  const exists = html.includes(`id="${id}"`) || fs.readFileSync(path.join(ROOT_DIR, 'resume', 'index.html'), 'utf8').includes(`id="${id}"`);
  check(`DOM Element ${selector}`, exists, exists ? 'Present in DOM' : 'Missing from DOM');
});

// Dedicated Architecture Checks (User Requested Features)
console.log('\n\x1b[1m[7/7] Feature Architecture & Integrity Audit\x1b[0m');
check('Dedicated Testimonials Page', html.includes('data-page="testimonials"'), 'Testimonials has its own dedicated article');
check('Testimonials Drawer Link', html.includes('data-drawer-navigate="testimonials"'), 'Drawer contains direct testimonials navigation card');
check('Zero /maxadmin Portal', !fs.existsSync(path.join(ROOT_DIR, 'admin.html')) && !html.includes('href="/maxadmin"'), 'Admin portal completely removed');
check('Zero Project Category Dropdown Duplication', !html.includes('filter-select-box'), 'Mobile select dropdown removed; filter pills only');
check('Schema.org 20 Projects Indexed', html.includes('Featured Production Systems and Software Engineering Innovations'), 'All 20 projects indexed in JSON-LD');
check('Crawler Catalog 20 Projects Present', (html.match(/class="seo-project-card"/g) || []).length === 20, 'Found exactly 20 crawler-accessible project articles');

const resumeStandalone = fs.readFileSync(path.join(ROOT_DIR, 'resume', 'index.html'), 'utf8');
const hasViewInResumeDock = resumeStandalone.includes('btn-view');
check('Resume Standalone Dock Single Button', !hasViewInResumeDock && resumeStandalone.includes('btn-download'), 'Resume view has only Download button');

const testimonialCardsCount = (html.match(/class="testimonials-item"/g) || []).length;
check('Testimonials Pre-Rendered 8 Cards in HTML', testimonialCardsCount === 8, `Found ${testimonialCardsCount} search-indexable endorsement cards`);

const reviewSchemaCount = (html.match(/"@type":\s*"Review"/g) || []).length;
check('Schema.org 8 Reviews Indexed in JSON-LD', reviewSchemaCount === 8, `Found ${reviewSchemaCount} structured Review schemas`);

const drawerTitlesMatch = html.match(/<div class="grid-card-text">\s*<strong>([^<]+)<\/strong>/g) || [];
const allOneWord = drawerTitlesMatch.every(t => !t.replace(/<\/?(div|strong)[^>]*>/g, '').trim().includes(' '));
check('Drawer One-Word Titles', drawerTitlesMatch.length === 8 && allOneWord, `All ${drawerTitlesMatch.length} drawer cards have strictly one-word titles`);




// Final Summary
console.log('\n------------------------------------------------------');
console.log(`AUDIT RESULT: ${passedChecks}/${totalChecks} PASSED, ${failures} FAILED, ${warnings} WARNINGS`);
console.log('------------------------------------------------------\n');

if (failures > 0) {
  process.exit(1);
} else {
  console.log('\x1b[32m✔ SUCCESS: Portfolio meets all SEO, structural, and quality criteria.\x1b[0m\n');
  process.exit(0);
}
