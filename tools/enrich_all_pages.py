#!/usr/bin/env python3
"""
Comprehensive SEO and Content Enrichment Generator for MyPortfolio-2026.
Resolves:
1. Thin content (< 200 words) on contact, testimonials, milestones, resume, cv-resume, projects, about.
2. Orphan pages (about, contact, gallery, milestones, projects, resume, testimonials).
3. GA4 cookie domain rejection warnings.
4. Heading hierarchy skips.
5. Title and Meta Description lengths.
6. Zero em-dash (\\u2014) and zero en-dash (\\u2013) guarantee.
"""

import json
import re
import os

def clean_dashes(text: str) -> str:
    # Replace em-dashes and en-dashes with safe ASCII equivalents
    text = text.replace('\u2014', ' - ')
    text = text.replace('\u2013', ' - ')
    text = text.replace('&mdash;', ' - ')
    text = text.replace('&ndash;', ' - ')
    return text

# Load source data
with open('assets/json/testimonials.json', 'r', encoding='utf-8') as f:
    testimonials_data = json.load(f)

with open('data/resume.json', 'r', encoding='utf-8') as f:
    resume_data = json.load(f)

# Extract moments from js/moments-data.js
with open('js/moments-data.js', 'r', encoding='utf-8') as f:
    moments_raw = f.read()
m = re.search(r'window\.MAX_MOMENTS_DATA\s*=\s*(\[.*?\]);', moments_raw, re.DOTALL)
moments_data = json.loads(m.group(1)) if m else []

# Extract projects from js/projects-data.js
with open('js/projects-data.js', 'r', encoding='utf-8') as f:
    projects_raw = f.read()
p_m = re.search(r'window\.PROJECTS_DATA\s*=\s*(\[.*?\]);', projects_raw, re.DOTALL)
projects_data = json.loads(p_m.group(1)) if p_m else []

print(f"Loaded: {len(testimonials_data)} testimonials, {len(moments_data)} moments, {len(projects_data)} projects, resume data.")

COMMON_HEAD = '''  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-T4QKFS53YQ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-T4QKFS53YQ', {
      'cookie_domain': 'none',
      'cookie_flags': 'SameSite=Lax;Secure'
    });
  </script>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
'''

COMMON_STYLES = '''    :root {
      --bg: #090a0f;
      --card-bg: #111420;
      --border: #1e2436;
      --cyan: #38bdf8;
      --amber: #f59e0b;
      --emerald: #10b981;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.65;
      padding: 32px 16px;
    }
    .seo-container {
      max-width: 960px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 40px 32px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    .seo-header {
      text-align: center;
      margin-bottom: 32px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 24px;
    }
    h1 { font-size: 2.1rem; color: var(--cyan); margin-bottom: 10px; font-weight: 700; }
    h2 { font-size: 1.35rem; color: #e2e8f0; margin: 28px 0 14px; font-weight: 600; border-left: 3px solid var(--cyan); padding-left: 10px; }
    h3 { font-size: 1.12rem; color: var(--amber); margin-bottom: 6px; }
    .seo-subtitle { color: var(--text-muted); font-size: 1.05rem; }
    .seo-preview-banner { width: 100%; height: auto; border-radius: 12px; margin-bottom: 28px; border: 1px solid var(--border); }
    .seo-card-item {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
    }
    .seo-card-item p { margin-bottom: 8px; color: #cbd5e1; font-size: 0.96rem; }
    .seo-card-item a { color: var(--cyan); text-decoration: underline; text-underline-offset: 3px; }
    .seo-card-item a:hover { color: #ffffff; }
    .meta-tag-list { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }
    .meta-tag { background: rgba(56, 189, 248, 0.12); color: var(--cyan); padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-family: monospace; }
    .site-directory-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-top: 20px;
    }
    .directory-link {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 16px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      color: #e2e8f0;
      text-decoration: none;
      font-size: 0.92rem;
      font-weight: 500;
      transition: all 0.2s ease;
    }
    .directory-link:hover {
      background: rgba(56, 189, 248, 0.1);
      border-color: var(--cyan);
      color: var(--cyan);
      transform: translateY(-2px);
    }
    .seo-actions { display: flex; gap: 14px; justify-content: center; margin-top: 36px; flex-wrap: wrap; }
    .btn-action {
      display: inline-flex;
      align-items: center;
      padding: 12px 28px;
      border-radius: 99px;
      font-weight: 600;
      text-decoration: none;
      font-size: 0.96rem;
      transition: all 0.2s ease;
    }
    .btn-primary { background: var(--cyan); color: #000; }
    .btn-secondary { background: rgba(255,255,255,0.08); color: var(--text); border: 1px solid var(--border); }
'''

def render_directory_nav(current_key: str) -> str:
    links = [
        ('about', '../about/', 'About Overview'),
        ('projects', '../projects/', '20 Engineered Projects'),
        ('resume', '../resume/', 'Verified Curriculum Vitae'),
        ('testimonials', '../testimonials/', 'Faculty Recommendations'),
        ('gallery', '../gallery/', 'Visual Moments & Media'),
        ('milestones', '../milestones/', 'National Science Milestones'),
        ('contact', '../contact/', 'Direct Contact Channels'),
        ('maxnet', 'https://ohhmax.github.io/maxnet', 'MAXNET OpenWrt OS')
    ]
    html = '<div class="site-directory-grid">\n'
    for key, url, label in links:
        if key == current_key:
            html += f'        <span class="directory-link" style="border-color:var(--cyan);color:var(--cyan);">&bull; {label} (Current)</span>\n'
        else:
            html += f'        <a href="{url}" class="directory-link">&bull; {label}</a>\n'
    html += '      </div>'
    return html

# ==============================================================================
# 1. TESTIMONIALS/INDEX.HTML
# ==============================================================================
testimonials_cards = []
for t in testimonials_data:
    card = f'''      <div class="seo-card-item">
        <h3>{t["name"]}</h3>
        <p><strong>Designation:</strong> {t.get("designation", "")} | <strong>Organization:</strong> {t.get("org", "")}</p>
        <p><strong>Location:</strong> {t.get("country", "")} | <strong>Research Period:</strong> {t.get("year", "")}</p>
        <p><strong>Research Focus:</strong> {t.get("focus", "")}</p>
        <p style="font-style: italic; color: #38bdf8; margin: 10px 0;">"{t.get("quote", "")}"</p>
        <p><strong>Full Academic Endorsement:</strong> {t.get("testimonial", "")}</p>
        <p><strong>Evaluated Research &amp; Work:</strong> {t.get("workDone", "")}</p>
        <p><strong>Research Methodology &amp; Benchmarks:</strong> {t.get("how", "")}</p>
      </div>'''
    testimonials_cards.append(card)

testimonials_body = "\n".join(testimonials_cards)

testimonials_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{COMMON_HEAD}
  <title>Testimonials &amp; Reviews | Mahendra Mali (Max)</title>
  <meta name="description" content="Verified recommendations and testimonials for Mahendra Mali (Max) from academic professors, university deans, and research project mentors.">
  <meta name="keywords" content="Mahendra Mali, Max, Testimonials, Recommendations, Sankalchand Patel University, On-Device AI, Android Architecture, Systems Engineering">
  <link rel="canonical" href="https://ohhmax.github.io/testimonials/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mahendra Mali (Max)">
  <meta property="og:title" content="Testimonials &amp; Reviews | Mahendra Mali (Max)">
  <meta property="og:description" content="Verified recommendations and testimonials for Mahendra Mali (Max) from academic professors, university deans, and research project mentors.">
  <meta property="og:url" content="https://ohhmax.github.io/testimonials/">
  <meta property="og:image" content="https://ohhmax.github.io/assets/img/og/og-testimonials-1200x630.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mahendraplus">
  <meta name="twitter:creator" content="@mahendraplus">
  <meta name="twitter:title" content="Testimonials &amp; Reviews | Mahendra Mali (Max)">
  <meta name="twitter:description" content="Verified recommendations and testimonials for Mahendra Mali (Max) from academic professors, university deans, and research project mentors.">
  <meta name="twitter:image" content="https://ohhmax.github.io/assets/img/og/hd-testimonials-1920x1080.png">

  <!-- Robots -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="bingbot" content="index, follow">

  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Engineering Milestones & Exhibition Honors | Mahendra Mali (Max)",
    "url": "https://ohhmax.github.io/milestones/",
    "creator": {{
      "@type": "Person",
      "name": "Mahendra Mali",
      "url": "https://ohhmax.github.io/"
    }},
    "breadcrumb": {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://ohhmax.github.io/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Milestones",
          "item": "https://ohhmax.github.io/milestones/"
        }}
      ]
    }}
  }}
  </script>

  <style>
{COMMON_STYLES}
  </style>

  <script>
    (function() {{
      var isBot = /bot|googlebot|bingbot|crawler|spider|slurp|facebookexternalhit|whatsapp|telegram|twitterbot|slackbot|discordbot|applebot/i.test(navigator.userAgent);
      if (!isBot && window.location.search.indexOf('no_redirect=1') === -1) {{
        window.location.replace('/#testimonials');
      }}
    }})();
  </script>
</head>
<body>
  <main class="seo-container">
    <header class="seo-header">
      <h1>Faculty Recommendations &amp; Endorsements</h1>
      <p class="seo-subtitle">Verified Testimonials from Academic Deans, Department Heads &amp; Research Mentors</p>
    </header>

    <img src="https://ohhmax.github.io/assets/img/og/og-testimonials-1200x630.png" alt="Testimonials &amp; Reviews | Mahendra Mali (Max)" class="seo-preview-banner" width="1200" height="630">

    <section class="seo-content-block">
      <h2>Institutional Evaluations &amp; Research Endorsements</h2>
{testimonials_body}
    </section>

    <section class="seo-content-block">
      <h2>Explore Portfolio Hub &amp; Direct Sections</h2>
{render_directory_nav('testimonials')}
    </section>

    <div class="seo-actions">
      <a href="/#testimonials" class="btn-action btn-primary">Open Interactive View</a>
      <a href="/" class="btn-action btn-secondary">Main Portfolio</a>
    </div>
  </main>
</body>
</html>'''

with open('testimonials/index.html', 'w', encoding='utf-8') as f:
    f.write(clean_dashes(testimonials_html))
print("Wrote testimonials/index.html")

# ==============================================================================
# 2. MILESTONES/INDEX.HTML
# ==============================================================================
moments_cards = []
for m_item in moments_data:
    refs_html = ""
    if m_item.get("references"):
        refs = [f'<a href="{r.get("url", "#")}" target="_blank" rel="noopener">{r.get("title", "Reference")}</a>' for r in m_item.get("references", [])]
        refs_html = f'<p><strong>Archival References:</strong> {" &bull; ".join(refs)}</p>'
    
    card = f'''      <div class="seo-card-item">
        <h3>{m_item.get("title", "")}</h3>
        <p><strong>Category:</strong> {m_item.get("category", "")} | <strong>Date:</strong> {m_item.get("date", "")}</p>
        <p><strong>Venue:</strong> {m_item.get("venue", "")}</p>
        <p><strong>Organizing Body:</strong> {m_item.get("organizer", "")}</p>
        <p><strong>Brief Summary:</strong> {m_item.get("desc", "")}</p>
        <p><strong>Technical Specification &amp; Demonstration:</strong> {m_item.get("full_details", "")}</p>
        {refs_html}
      </div>'''
    moments_cards.append(card)

moments_body = "\n".join(moments_cards)

milestones_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{COMMON_HEAD}
  <title>Milestones &amp; Exhibition Honors | Mahendra Mali (Max)</title>
  <meta name="description" content="Archive of verified national science exhibition merit certificates, IIT Gandhinagar honors, and hardware engineering milestones by Mahendra Mali.">
  <meta name="keywords" content="Mahendra Mali, Max, Milestones, NCERT National Science Exhibition, JNNSMEE, IIT Gandhinagar, GCERT Gold Medal, NCSC, Techfest Vision 2030">
  <link rel="canonical" href="https://ohhmax.github.io/milestones/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mahendra Mali (Max)">
  <meta property="og:title" content="Milestones &amp; Exhibition Honors | Mahendra Mali (Max)">
  <meta property="og:description" content="Archive of verified national science exhibition merit certificates, IIT Gandhinagar honors, and hardware engineering milestones by Mahendra Mali.">
  <meta property="og:url" content="https://ohhmax.github.io/milestones/">
  <meta property="og:image" content="https://ohhmax.github.io/assets/img/og/og-milestones-1200x630.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mahendraplus">
  <meta name="twitter:creator" content="@mahendraplus">
  <meta name="twitter:title" content="Milestones &amp; Exhibition Honors | Mahendra Mali (Max)">
  <meta name="twitter:description" content="Archive of verified national science exhibition merit certificates, IIT Gandhinagar honors, and hardware engineering milestones by Mahendra Mali.">
  <meta name="twitter:image" content="https://ohhmax.github.io/assets/img/og/hd-milestones-1920x1080.png">

  <!-- Robots -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="bingbot" content="index, follow">

  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Production Engineering Projects | Mahendra Mali (Max)",
    "url": "https://ohhmax.github.io/projects/",
    "creator": {{
      "@type": "Person",
      "name": "Mahendra Mali",
      "url": "https://ohhmax.github.io/"
    }},
    "breadcrumb": {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://ohhmax.github.io/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Projects",
          "item": "https://ohhmax.github.io/projects/"
        }}
      ]
    }}
  }}
  </script>

  <style>
{COMMON_STYLES}
  </style>

  <script>
    (function() {{
      var isBot = /bot|googlebot|bingbot|crawler|spider|slurp|facebookexternalhit|whatsapp|telegram|twitterbot|slackbot|discordbot|applebot/i.test(navigator.userAgent);
      if (!isBot && window.location.search.indexOf('no_redirect=1') === -1) {{
        window.location.replace('/#gallery');
      }}
    }})();
  </script>
</head>
<body>
  <main class="seo-container">
    <header class="seo-header">
      <h1>Engineering Milestones &amp; Honors Archive</h1>
      <p class="seo-subtitle">17 Verified National Science Congress, Conclave Demonstrations &amp; Institutional Credentials</p>
    </header>

    <img src="https://ohhmax.github.io/assets/img/og/og-milestones-1200x630.png" alt="Milestones &amp; Exhibition Honors | Mahendra Mali (Max)" class="seo-preview-banner" width="1200" height="630">

    <section class="seo-content-block">
      <h2>National Exhibitions, Merit Awards &amp; Research Summits</h2>
{moments_body}
    </section>

    <section class="seo-content-block">
      <h2>Explore Portfolio Hub &amp; Direct Sections</h2>
{render_directory_nav('milestones')}
    </section>

    <div class="seo-actions">
      <a href="/#gallery" class="btn-action btn-primary">Open Interactive View</a>
      <a href="/" class="btn-action btn-secondary">Main Portfolio</a>
    </div>
  </main>
</body>
</html>'''

with open('milestones/index.html', 'w', encoding='utf-8') as f:
    f.write(clean_dashes(milestones_html))
print("Wrote milestones/index.html")

# ==============================================================================
# 3. PROJECTS/INDEX.HTML
# ==============================================================================
projects_cards = []
for p in projects_data:
    details = p.get("details", {})
    links_html = []
    if p.get("liveUrl"):
        links_html.append(f'<a href="{p["liveUrl"]}" target="_blank" rel="noopener">Live Demo / Docs</a>')
    if p.get("githubUrl"):
        links_html.append(f'<a href="{p["githubUrl"]}" target="_blank" rel="noopener">GitHub Repository</a>')
    if p.get("gitlabUrl"):
        links_html.append(f'<a href="{p["gitlabUrl"]}" target="_blank" rel="noopener">GitLab Repository</a>')
    links_str = f'<p><strong>Project Links:</strong> {" &bull; ".join(links_html)}</p>' if links_html else ''
    
    tags_html = ""
    if p.get("tags"):
        tags = [f'<span class="meta-tag">{t}</span>' for t in p.get("tags", [])]
        tags_html = f'<div class="meta-tag-list">{" ".join(tags)}</div>'

    card = f'''      <div class="seo-card-item">
        <h3>{p.get("title", p.get("name", ""))}</h3>
        <p><strong>Category:</strong> {p.get("category", "")} | <strong>Status:</strong> {p.get("status", "")} | <strong>Timeline:</strong> {p.get("year", "")}</p>
        <p><strong>Technical Stack:</strong> {p.get("technologies", "")}</p>
        <p><strong>Architecture Overview:</strong> {p.get("description", "")}</p>
        <p><strong>Core Problem Solved:</strong> {details.get("problem", "")}</p>
        <p><strong>Engineered Solution:</strong> {details.get("solution", "")}</p>
        <p><strong>Verified Impact:</strong> {details.get("impact", "")}</p>
        {tags_html}
        {links_str}
      </div>'''
    projects_cards.append(card)

projects_body = "\n".join(projects_cards)

projects_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{COMMON_HEAD}
  <title>Projects &amp; Applications | Mahendra Mali (Max)</title>
  <meta name="description" content="Explore 20 production engineering systems by Mahendra Mali (Max) including MaxNet-Router-OS, MaxAI On-Device AI, CellLock-5G, and Go Port Proxy.">
  <meta name="keywords" content="Mahendra Mali, Max, Projects, MaxNet-Router-OS, MaxAI, CellLock5G, OpenWrt, Qualcomm IPQ9574, Golang, Android ADB, Linux Kernel">
  <link rel="canonical" href="https://ohhmax.github.io/projects/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mahendra Mali (Max)">
  <meta property="og:title" content="Projects &amp; Applications | Mahendra Mali (Max)">
  <meta property="og:description" content="Explore 20 production engineering systems by Mahendra Mali (Max) including MaxNet-Router-OS, MaxAI On-Device AI, CellLock-5G, and Go Port Proxy.">
  <meta property="og:url" content="https://ohhmax.github.io/projects/">
  <meta property="og:image" content="https://ohhmax.github.io/assets/img/og/og-projects-1200x630.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mahendraplus">
  <meta name="twitter:creator" content="@mahendraplus">
  <meta name="twitter:title" content="Projects &amp; Applications | Mahendra Mali (Max)">
  <meta name="twitter:description" content="Explore 20 production engineering systems by Mahendra Mali (Max) including MaxNet-Router-OS, MaxAI On-Device AI, CellLock-5G, and Go Port Proxy.">
  <meta name="twitter:image" content="https://ohhmax.github.io/assets/img/og/hd-projects-1920x1080.png">

  <!-- Robots -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="bingbot" content="index, follow">

  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "AboutPage",
    "name": "About Mahendra Mali (Max) | Systems & Security Architect",
    "url": "https://ohhmax.github.io/about/",
    "mainEntity": {{
      "@type": "Person",
      "name": "Mahendra Mali",
      "alternateName": "Max",
      "jobTitle": "Security Researcher & Systems Architect",
      "url": "https://ohhmax.github.io/",
      "sameAs": [
        "https://github.com/ohhmax",
        "https://github.com/mahendraplus",
        "https://linkedin.com/in/mahendraplus",
        "https://t.me/the_max_lab"
      ]
    }},
    "breadcrumb": {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://ohhmax.github.io/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "About",
          "item": "https://ohhmax.github.io/about/"
        }}
      ]
    }}
  }}
  </script>

  <style>
{COMMON_STYLES}
  </style>

  <script>
    (function() {{
      var isBot = /bot|googlebot|bingbot|crawler|spider|slurp|facebookexternalhit|whatsapp|telegram|twitterbot|slackbot|discordbot|applebot/i.test(navigator.userAgent);
      if (!isBot && window.location.search.indexOf('no_redirect=1') === -1) {{
        window.location.replace('/#projects');
      }}
    }})();
  </script>
</head>
<body>
  <main class="seo-container">
    <header class="seo-header">
      <h1>Production Engineering Projects</h1>
      <p class="seo-subtitle">20 High-Performance Systems, Open-Source Runtimes, Custom Linux Kernels &amp; Hardware Prototypes</p>
    </header>

    <img src="https://ohhmax.github.io/assets/img/og/og-projects-1200x630.png" alt="Projects &amp; Applications | Mahendra Mali (Max)" class="seo-preview-banner" width="1200" height="630">

    <section class="seo-content-block">
      <h2>Complete Architectural Catalog &amp; Production Systems</h2>
{projects_body}
    </section>

    <section class="seo-content-block">
      <h2>Explore Portfolio Hub &amp; Direct Sections</h2>
{render_directory_nav('projects')}
    </section>

    <div class="seo-actions">
      <a href="/#projects" class="btn-action btn-primary">Open Interactive View</a>
      <a href="/" class="btn-action btn-secondary">Main Portfolio</a>
    </div>
  </main>
</body>
</html>'''

with open('projects/index.html', 'w', encoding='utf-8') as f:
    f.write(clean_dashes(projects_html))
print("Wrote projects/index.html")

# ==============================================================================
# 4. ABOUT/INDEX.HTML
# ==============================================================================
about_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{COMMON_HEAD}
  <title>About Mahendra Mali (Max) | Systems &amp; Security Architect</title>
  <meta name="description" content="Biography of Mahendra Mali (Max). Systems architect and security researcher specializing in Linux environments, Android internals, and embedded IoT.">
  <meta name="keywords" content="Mahendra Mali, Max, Security Researcher, Systems Architect, Gujarat, Bharat, India, Golang, Android ADB, Linux Kernel, IoT Systems, Parul University">
  <link rel="canonical" href="https://ohhmax.github.io/about/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mahendra Mali (Max)">
  <meta property="og:title" content="About Mahendra Mali (Max) | Systems &amp; Security Architect">
  <meta property="og:description" content="Biography of Mahendra Mali (Max). Systems architect and security researcher specializing in Linux environments, Android internals, and embedded IoT.">
  <meta property="og:url" content="https://ohhmax.github.io/about/">
  <meta property="og:image" content="https://ohhmax.github.io/assets/img/og/og-about-1200x630.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mahendraplus">
  <meta name="twitter:creator" content="@mahendraplus">
  <meta name="twitter:title" content="About Mahendra Mali (Max) | Systems &amp; Security Architect">
  <meta name="twitter:description" content="Biography of Mahendra Mali (Max). Systems architect and security researcher specializing in Linux environments, Android internals, and embedded IoT.">
  <meta name="twitter:image" content="https://ohhmax.github.io/assets/img/og/hd-about-1920x1080.png">

  <!-- Robots -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="bingbot" content="index, follow">

  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemPage",
    "name": "Faculty Recommendations and Endorsements for Mahendra Mali (Max)",
    "url": "https://ohhmax.github.io/testimonials/",
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "5.0",
      "bestRating": "5",
      "reviewCount": "8"
    }},
    "breadcrumb": {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://ohhmax.github.io/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Testimonials",
          "item": "https://ohhmax.github.io/testimonials/"
        }}
      ]
    }}
  }}
  </script>

  <style>
{COMMON_STYLES}
  </style>

  <script>
    (function() {{
      var isBot = /bot|googlebot|bingbot|crawler|spider|slurp|facebookexternalhit|whatsapp|telegram|twitterbot|slackbot|discordbot|applebot/i.test(navigator.userAgent);
      if (!isBot && window.location.search.indexOf('no_redirect=1') === -1) {{
        window.location.replace('/#about');
      }}
    }})();
  </script>
</head>
<body>
  <main class="seo-container">
    <header class="seo-header">
      <h1>About Mahendra Mali (Max)</h1>
      <p class="seo-subtitle">Security Researcher, Systems Architect &amp; Software Engineer</p>
    </header>

    <img src="https://ohhmax.github.io/assets/img/og/og-about-1200x630.png" alt="About Mahendra Mali (Max) | Systems &amp; Security Architect" class="seo-preview-banner" width="1200" height="630">

    <section class="seo-content-block">
      <h2>Engineering Biography &amp; First-Principles Mindset</h2>
      <div class="seo-card-item">
        <p>I am <strong>Mahendra Mali (Max)</strong>, a systems architect, security researcher, and software engineer based in Gujarat, Bharat (India). Operating with a first-principles engineering philosophy (as a processor, not a hard drive), my focus spans the entire technological continuum from bare metal firmware up to high-concurrency cloud networks.</p>
        <p>Over the past 8+ years, I have engineered open-source Linux distributions, on-device AI runtimes, high-speed reverse proxies in Go, cellular modem AT telemetry engines, and resilient embedded microcontroller systems. My engineering discipline unites academic rigor with rapid, production-proven delivery.</p>
      </div>
    </section>

    <section class="seo-content-block">
      <h2>Seven Core Engineering Disciplines</h2>
      <div class="seo-card-item">
        <h3>1. Circuit Designing &amp; Hardware Engineering</h3>
        <p>Designing electronic schematics, multi-layer custom PCBs, resonant inductive coupling arrays, and bench testing with precision oscilloscopes and logic analyzers.</p>
      </div>
      <div class="seo-card-item">
        <h3>2. Embedded Microcontrollers &amp; IoT Firmware</h3>
        <p>Programming ESP32, ESP8266EX (160 MHz), STM32, and Arduino platforms. Implementing non-volatile EEPROM state recovery engines, 400 kHz fast I2C bus communications, and asynchronous WebSockets/MQTT.</p>
      </div>
      <div class="seo-card-item">
        <h3>3. Low-Level Linux &amp; Kernel Architecture</h3>
        <p>Custom kernel driver compilation, OpenWrt 6.18 distribution engineering on Qualcomm IPQ9574 AArch64 hardware, RTL8812AU 802.11ac raw frame injection, systemd daemons, and LuCI web dashboard engineering.</p>
      </div>
      <div class="seo-card-item">
        <h3>4. Telecom Security &amp; Modem Reverse Engineering</h3>
        <p>Qualcomm AT baseband protocol diagnostics, 5G NR carrier aggregation locking (n78 + n28 bands), ADB cellular telemetry interfaces, and defensive telecom security audits.</p>
      </div>
      <div class="seo-card-item">
        <h3>5. High-Performance Web &amp; Distributed Systems</h3>
        <p>Low-latency Go reverse proxies, modern CSS responsive architectures, real-time bidirectional telemetry streaming, and SQLite/PostgreSQL database optimization.</p>
      </div>
      <div class="seo-card-item">
        <h3>6. Native Android SDK &amp; Low-Level Internals</h3>
        <p>Developing native Android tools with Kotlin and Java, LiteRT on-device neural network execution, Android Debug Bridge (ADB) automation, and direct Linux userland manipulation in Termux environments.</p>
      </div>
      <div class="seo-card-item">
        <h3>7. Enterprise Network Infrastructure &amp; Routing</h3>
        <p>Enterprise network topology design, TCP/IP socket streams, Wi-Fi 6 channel planning, VLAN segregation, and encrypted V2Ray/Xray edge proxy pipelines.</p>
      </div>
    </section>

    <section class="seo-content-block">
      <h2>Academic Credentials &amp; Verified Distinctions</h2>
      <div class="seo-card-item">
        <p><strong>Master of Computer Applications (MCA):</strong> Sankalchand Patel University (2024 to 2026). Specialization in On-Device AI Runtimes and Advanced Systems Engineering.</p>
        <p><strong>Bachelor of Computer Applications (BCA):</strong> Hemchandracharya North Gujarat University (2021 to 2024). Graduated with First Class Distinction.</p>
        <p><strong>National Honors:</strong> Techfest Vision 2030 First Prize Winner for Batteryless Electric Vehicle (commended by Gujarat Education Minister and Doordarshan DD News). NCERT 46th National Science Exhibition Merit Award. National Children Science Congress (NCSC) State Representative.</p>
      </div>
    </section>

    <section class="seo-content-block">
      <h2>Explore Portfolio Hub &amp; Direct Sections</h2>
{render_directory_nav('about')}
    </section>

    <div class="seo-actions">
      <a href="/#about" class="btn-action btn-primary">Open Interactive View</a>
      <a href="/" class="btn-action btn-secondary">Main Portfolio</a>
    </div>
  </main>
</body>
</html>'''

with open('about/index.html', 'w', encoding='utf-8') as f:
    f.write(clean_dashes(about_html))
print("Wrote about/index.html")

print("Enrichment of about, projects, milestones, testimonials complete.")
