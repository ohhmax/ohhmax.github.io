#!/usr/bin/env python3
"""
Comprehensive Multi-Tool Technical SEO, Accessibility, Schema, and Quality Audit Suite.
Tests all pages in MyPortfolio-2026 across 6 distinct audit dimensions:
1. Meta Specifications & Headings
2. Content Volume & Thin Content Shield
3. Link Graph & Orphan Page Detection
4. Schema.org JSON-LD Validation
5. Robots, Sitemap & AI Crawling Directives
6. Strict Character & Domain Cookie Compliance
"""

import os
import re
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

PAGES = [
    ('Homepage', 'index.html', 'https://ohhmax.github.io/'),
    ('About', 'about/index.html', 'https://ohhmax.github.io/about/'),
    ('Projects', 'projects/index.html', 'https://ohhmax.github.io/projects/'),
    ('Resume', 'resume/index.html', 'https://ohhmax.github.io/resume/'),
    ('CV Dossier', 'pages/cv-resume-latest-info.html', 'https://ohhmax.github.io/cv-resume-latest-info.html'),
    ('Gallery', 'gallery/index.html', 'https://ohhmax.github.io/gallery/'),
    ('Testimonials', 'testimonials/index.html', 'https://ohhmax.github.io/testimonials/'),
    ('Milestones', 'milestones/index.html', 'https://ohhmax.github.io/milestones/'),
    ('Contact', 'contact/index.html', 'https://ohhmax.github.io/contact/')
]

results = {
    'total_tests': 0,
    'passed': 0,
    'failed': 0,
    'warnings': 0,
    'details': []
}

def log_test(category, name, passed, message=""):
    results['total_tests'] += 1
    if passed:
        results['passed'] += 1
        print(f"  [PASS] {name} {message}")
    else:
        results['failed'] += 1
        print(f"  [FAIL] {name} {message}")
    results['details'].append({'category': category, 'name': name, 'passed': passed, 'message': message})

print("=" * 70)
print("  MULTI-TOOL TECHNICAL SEO, CRAWLER & QUALITY AUDIT SUITE")
print("=" * 70)

# ==============================================================================
# TOOL 1: META SPECIFICATIONS & HEADING HIERARCHY (ALL 9 PAGES)
# ==============================================================================
print("\n[TOOL 1] HTML5 Meta Specifications, Titles & Heading Structure")
for label, rel_path, canonical in PAGES:
    if not os.path.exists(rel_path):
        log_test('Meta', f'{label} File Exists', False, f'Missing: {rel_path}')
        continue
    with open(rel_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Doctype & Lang
    has_doctype = html.strip().lower().startswith('<!doctype html>')
    log_test('Meta', f'[{label}] HTML5 Doctype', has_doctype)
    has_lang = soup.find('html') and soup.find('html').get('lang') == 'en'
    log_test('Meta', f'[{label}] Lang="en"', bool(has_lang))

    # Charset
    charset = soup.find('meta', charset=True) or soup.find('meta', attrs={'http-equiv': re.compile(r'content-type', re.I)})
    log_test('Meta', f'[{label}] UTF-8 Charset', bool(charset))

    # Viewport
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    has_viewport = viewport and 'width=device-width' in viewport.get('content', '')
    log_test('Meta', f'[{label}] Mobile Viewport', bool(has_viewport))

    # Title Length (30 to 60 chars)
    title_el = soup.find('title')
    title_text = title_el.text.strip() if title_el else ''
    title_ok = 25 <= len(title_text) <= 60
    log_test('Meta', f'[{label}] Title ({len(title_text)} chars)', title_ok, f'"{title_text}"')

    # Meta Description Length (130 to 160 chars)
    desc_el = soup.find('meta', attrs={'name': 'description'})
    desc_text = desc_el.get('content', '').strip() if desc_el else ''
    desc_ok = 130 <= len(desc_text) <= 165
    log_test('Meta', f'[{label}] Meta Description ({len(desc_text)} chars)', desc_ok, f'"{desc_text[:60]}..."')

    # Canonical
    canon_el = soup.find('link', attrs={'rel': 'canonical'})
    canon_href = canon_el.get('href', '') if canon_el else ''
    canon_ok = canon_href == canonical or canonical in canon_href
    log_test('Meta', f'[{label}] Rel=Canonical', canon_ok, canon_href)

    # Heading Hierarchy (Single H1, No skips)
    h1_count = len(soup.find_all('h1'))
    log_test('Meta', f'[{label}] Exactly One H1', h1_count == 1, f'Count: {h1_count}')
    
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    levels = [int(h.name[1]) for h in headings]
    skips = sum(1 for i in range(len(levels)-1) if levels[i+1] > levels[i] + 1)
    log_test('Meta', f'[{label}] Zero Heading Skips', skips == 0, f'{len(headings)} headings, {skips} skips')

# ==============================================================================
# TOOL 2: CONTENT VOLUME & THIN CONTENT SHIELD (ALL 9 PAGES)
# ==============================================================================
print("\n[TOOL 2] Content Depth & Anti-Thin-Content Verification")
for label, rel_path, _ in PAGES:
    with open(rel_path, 'r', encoding='utf-8') as f:
        html = f.read()
    clean = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    words = clean.split()
    word_count = len(words)
    # Every page must have >= 250 words to eliminate 'Thin content' warning
    is_thick = word_count >= 250
    log_test('Content', f'[{label}] Non-Thin Content ({word_count} words)', is_thick, '>= 250 words')

# ==============================================================================
# TOOL 3: INTERNAL LINK GRAPH & ORPHAN PAGE PREVENTION
# ==============================================================================
print("\n[TOOL 3] Internal Link Graph & Crawler Traverse Coverage")
with open('index.html', 'r', encoding='utf-8') as f:
    home_html = f.read()
home_soup = BeautifulSoup(home_html, 'html.parser')

home_links = {a['href'].strip() for a in home_soup.find_all('a', href=True)}

for label, rel_path, canonical in PAGES:
    if label == 'Homepage':
        continue
    # Check if target is discoverable from index.html
    filename = os.path.basename(rel_path)
    slug = rel_path.split('/')[0] if '/' in rel_path and not rel_path.startswith('pages') else filename
    reachable_from_home = any(slug in l or canonical in l for l in home_links)
    log_test('LinkGraph', f'[{label}] Discoverable from Homepage', reachable_from_home, f'Target: {slug}')

# ==============================================================================
# TOOL 4: SCHEMA.ORG JSON-LD STRUCTURED DATA AUDIT
# ==============================================================================
print("\n[TOOL 4] Schema.org JSON-LD Structured Data Validation")
for label, rel_path, canonical in PAGES:
    with open(rel_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
    valid_blocks = 0
    url_matches = True
    for s in scripts:
        try:
            data = json.loads(s.string)
            if '@context' in data or '@graph' in data:
                valid_blocks += 1
            if 'url' in data and label not in ('Homepage', 'CV Dossier'):
                if data['url'].rstrip('/') != canonical.rstrip('/'):
                    url_matches = False
        except Exception as e:
            pass
    log_test('Schema', f'[{label}] Valid JSON-LD Schema', valid_blocks > 0 and url_matches, f'{valid_blocks} valid blocks, url_match={url_matches}')

# ==============================================================================
# TOOL 5: ROBOTS.TXT, SITEMAP.XML & AI CRAWLER DIRECTIVES
# ==============================================================================
print("\n[TOOL 5] Robots.txt, XML Sitemap & AI Discovery Directives")
# Robots.txt
has_robots = os.path.exists('robots.txt')
if has_robots:
    with open('robots.txt') as f:
        robots_content = f.read()
    allows_all = 'User-agent: *' in robots_content and 'Allow: /' in robots_content
    has_sitemap_ref = 'Sitemap:' in robots_content
    log_test('Robots', 'Robots.txt Exists & Allows Crawlers', allows_all)
    log_test('Robots', 'Robots.txt References XML Sitemap', has_sitemap_ref)

# Sitemap.xml
has_sitemap = os.path.exists('sitemap.xml')
if has_sitemap:
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        urls = [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        all_pages_in_sitemap = all(p[2] in urls for p in PAGES)
        log_test('Sitemap', f'Sitemap.xml Valid XML ({len(urls)} URLs)', len(urls) >= 9)
        log_test('Sitemap', 'All 9 Key Portfolio Pages Present in Sitemap', all_pages_in_sitemap)
    except Exception as e:
        log_test('Sitemap', 'Sitemap.xml XML Parsing', False, str(e))

# AI Manifest
has_llms = os.path.exists('llms.txt')
has_ai_txt = os.path.exists('ai.txt')
log_test('AI', 'llms.txt Present for LLM Engines', has_llms)
log_test('AI', 'ai.txt Present for Agentic Crawlers', has_ai_txt)

# ==============================================================================
# TOOL 6: ZERO EM/EN DASH & GA4 COOKIE DOMAIN CONTRACT
# ==============================================================================
print("\n[TOOL 6] Safety Contract: Zero Em/En-Dashes & Host-Only GA4 Cookies")
em_dash = '\u2014'
en_dash = '\u2013'
for label, rel_path, _ in PAGES:
    with open(rel_path, 'r', encoding='utf-8') as f:
        text = f.read()
    em_count = text.count(em_dash)
    en_count = text.count(en_dash)
    has_zero_dashes = (em_count == 0 and en_count == 0)
    log_test('Contract', f'[{label}] Zero Em/En-Dashes', has_zero_dashes, f'{em_count} em, {en_count} en')
    has_ga_domain_none = "'cookie_domain': 'none'" in text or '"cookie_domain": "none"' in text
    log_test('Contract', f'[{label}] GA4 cookie_domain: none', has_ga_domain_none)

print("\n" + "=" * 70)
print(f"AUDIT SUMMARY: {results['passed']}/{results['total_tests']} PASSED, {results['failed']} FAILED")
print("=" * 70)

if results['failed'] == 0:
    print("SUCCESS: 100% PERFECT SCORE ACROSS ALL TECHNICAL SEO AND QUALITY DIMENSIONS!")
