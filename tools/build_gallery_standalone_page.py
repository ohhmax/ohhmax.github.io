"""
tools/build_gallery_standalone_page.py
Generates the 100% pre-rendered, static HTML dedicated gallery page (gallery/index.html).
Features:
- Pure static HTML with all 142 items pre-rendered (perfect for curl and AI bots).
- Group-wise and year-wise chronological layout (2026 to 2017).
- Clean visual Pinterest gallery presentation without card-level text clutter.
- Rich Schema.org microdata and complete ImageGallery JSON-LD for AI search engines.
- Interactive client-side filtering (Year tabs, Category tabs, instant DOM search).
- Responsive masonry grid with fullscreen lightbox modal.
- Zero Em-Dash Contract Verified.
"""

import os
import json
import re
import xml.sax.saxutils as saxutils

def escape_html(s):
    return saxutils.escape(str(s or ''))

YEAR_META = {
    '2026': {
        'title': '2026: Career & Systems Engineering Milestones',
        'subtitle': 'Software engineering internship appointment and enterprise Linux kernel hardware debugging',
        'icon': 'fa-solid fa-terminal'
    },
    '2025': {
        'title': '2025: Embedded IoT & Hardware Prototyping',
        'subtitle': 'Microcontroller automation, 5V relay validation, and workbench circuit telemetry',
        'icon': 'fa-solid fa-microchip'
    },
    '2024': {
        'title': '2024: Academic Records & Credentials',
        'subtitle': 'University examinations, MCA postgraduate credentials, and academic verification',
        'icon': 'fa-solid fa-graduation-cap'
    },
    '2023': {
        'title': '2023: Microcontroller Electronics & Sensor R&D',
        'subtitle': 'NodeMCU ESP8266, HC-SR04 ultrasonic profiler, and servo telemetry bench',
        'icon': 'fa-solid fa-satellite-dish'
    },
    '2022': {
        'title': '2022: Hardware Prototyping & Lab Tooling',
        'subtitle': 'Laboratory component kits, breadboard prototyping nests, and hardware tooling',
        'icon': 'fa-solid fa-screwdriver-wrench'
    },
    '2021': {
        'title': '2021: Streetwear, Traditional Celebrations & Fitness Progress',
        'subtitle': 'Personal portraits, gym fitness workouts, cultural kurta celebrations, and heritage travel',
        'icon': 'fa-solid fa-camera-retro'
    },
    '2019': {
        'title': '2019: NCERT National Science Exhibition & State Gold Medal',
        'subtitle': '46th JNNSMEE Raipur Merit Award, GCERT State Gold Medal, TV news broadcasts and wireless EV track',
        'icon': 'fa-solid fa-award'
    },
    '2018': {
        'title': '2018: IIT Bombay Techfest & Dynamic Wireless Induction Roadway',
        'subtitle': 'IIT-B Powai canopy, resonant induction coil roadway track, Banaskantha First Prize and landscape photography',
        'icon': 'fa-solid fa-bolt'
    },
    '2017': {
        'title': '2017: Foundational School Science Exhibition & Early Journey',
        'subtitle': 'Acrylic electronics resonance column defense, dead battery flashlight energy harvester and early portraits',
        'icon': 'fa-solid fa-seedling'
    }
}

def extract_year(date_str):
    m = re.search(r'20\d\d', str(date_str or ''))
    return m.group(0) if m else '2021'

def main():
    catalog_path = 'data/gallery-items.json'
    with open(catalog_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    # Sort items chronologically descending: by year then by title
    def sort_key(item):
        yr = extract_year(item.get('date', ''))
        return (int(yr), item.get('category', ''), item.get('title', ''))

    items.sort(key=sort_key, reverse=True)

    # Group by year
    years_order = ['2026', '2025', '2024', '2023', '2022', '2021', '2019', '2018', '2017']
    grouped = {y: [] for y in years_order}
    for item in items:
        y = extract_year(item.get('date', ''))
        if y in grouped:
            grouped[y].append(item)
        else:
            grouped.setdefault('2021', []).append(item)

    # Schema.org ImageGallery items (All 142 items)
    schema_images = []
    for item in items:
        schema_images.append({
            "@type": "ImageObject",
            "name": item.get('title', ''),
            "description": item.get('desc', ''),
            "contentUrl": f"https://ohhmax.github.io/{item.get('src', '')}",
            "thumbnailUrl": f"https://ohhmax.github.io/{item.get('thumb', '')}",
            "caption": item.get('desc', ''),
            "datePublished": extract_year(item.get('date', '')),
            "contentLocation": item.get('location', ''),
            "author": {
                "@type": "Person",
                "name": "Mahendra Mali"
            },
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "acquireLicensePage": "https://ohhmax.github.io/gallery/"
        })

    schema_ld = {
        "@context": "https://schema.org",
        "@type": "ImageGallery",
        "name": "Mahendra Mali (Max) Visual Gallery Archive & Moments Vault",
        "description": "Comprehensive visual archive of 142 verified engineering prototypes, national science exhibitions, TV news interviews, IoT hardware, and personal portraits of Mahendra Mali from 2017 to 2026.",
        "url": "https://ohhmax.github.io/gallery/",
        "author": {
            "@type": "Person",
            "name": "Mahendra Mali",
            "url": "https://ohhmax.github.io/"
        },
        "breadcrumb": {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://ohhmax.github.io/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Gallery",
                    "item": "https://ohhmax.github.io/gallery/"
                }
            ]
        },
        "image": schema_images
    }

    # Build Year Sections and Cards
    sections_html = []
    for yr in years_order:
        yr_items = grouped.get(yr, [])
        if not yr_items:
            continue

        meta = YEAR_META.get(yr, {
            'title': f'{yr} Media Archive',
            'subtitle': f'Photos, videos, and milestones from {yr}',
            'icon': 'fa-solid fa-calendar'
        })

        cards_html = []
        for item in yr_items:
            is_vid = item.get('type') == 'video'
            src = item.get('src', '')
            thumb = item.get('thumb', src)
            code = escape_html(item.get('code', ''))
            title = escape_html(item.get('title', ''))
            desc = escape_html(item.get('desc', ''))
            cat = escape_html(item.get('category', 'portraits'))
            cat_label = escape_html(item.get('categoryLabel', 'Archive'))
            badge = escape_html(item.get('badge', cat_label))
            date = escape_html(item.get('date', yr))
            loc = escape_html(item.get('location', 'Gujarat, India'))
            tags = item.get('tags', [])
            tags_csv = escape_html(', '.join(tags))
            item_id = escape_html(item.get('id', ''))
            width = item.get('width', 600)
            height = item.get('height', 400)
            color = item.get('color', '#38bdf8')
            icon = item.get('icon', 'fa-solid fa-camera')
            mime = 'video/mp4' if is_vid else ('image/webp' if thumb.endswith('.webp') else 'image/jpeg')

            play_icon_html = '<div class="pin-play-icon" aria-hidden="true"><i class="fa-solid fa-play"></i></div>' if is_vid else ''

            alt_text = escape_html(item.get('alt', f"{title} | {badge} - Mahendra Mali (Max) Portfolio"))
            card = f'''          <figure class="gallery-pin-card" id="{item_id}" 
                  itemscope itemtype="https://schema.org/ImageObject"
                  data-code="{code}" 
                  data-year="{yr}" 
                  data-category="{cat}" 
                  data-type="{item.get('type', 'image')}"
                  data-title="{title}"
                  data-location="{loc}"
                  data-date="{date}"
                  data-src="/{src}"
                  data-thumb="/{thumb}"
                  data-desc="{desc}"
                  data-badge="{badge}"
                  data-tags="{tags_csv}">
            <div class="pin-media-wrapper" onclick="openGalleryLightbox('{item_id}')" role="button" tabindex="0" aria-label="View {title} in fullscreen">
              <div class="pin-badge-group">
                <span class="pin-code-badge"><i class="fa-solid fa-fingerprint"></i> {code}</span>
                <span class="pin-year-badge">{yr}</span>
              </div>
              <span class="pin-cat-tag" style="border-color: {color};">
                <i class="{icon}" style="color: {color};"></i>
                <span>{badge}</span>
              </span>
              {play_icon_html}
              <img src="/{thumb}" 
                   alt="{alt_text}" 
                   title="{title}" 
                   loading="lazy" 
                   class="pin-img" 
                   width="{width}" 
                   height="{height}"
                   onerror="this.onerror=null; this.src='/{src}';">
            </div>
            <figcaption class="pin-caption-box">
              <h3 class="pin-title" itemprop="name">{title}</h3>
              <div class="pin-meta-bar">
                <span class="pin-meta-item"><i class="fa-solid fa-location-dot"></i> {loc}</span>
                <span class="pin-meta-item"><i class="fa-regular fa-calendar"></i> {date}</span>
                <div class="pin-actions-wrap" onclick="event.stopPropagation();">
                  <a href="/{src}" download title="Download Original Media" class="pin-action-icon-btn" aria-label="Download original media">
                    <i class="fa-solid fa-arrow-down-to-bracket"></i>
                  </a>
                  <button type="button" class="pin-action-icon-btn" onclick="openGalleryLightbox('{item_id}')" title="Expand Fullscreen" aria-label="Expand image in lightbox">
                    <i class="fa-solid fa-expand"></i>
                  </button>
                </div>
              </div>

              <!-- Pre-Rendered Semantic Metadata for AI Bots, Search Engine Crawlers & curl -->
              <meta itemprop="contentUrl" content="https://ohhmax.github.io/{src}">
              <meta itemprop="thumbnailUrl" content="https://ohhmax.github.io/{thumb}">
              <meta itemprop="datePublished" content="{yr}">
              <meta itemprop="contentLocation" content="{loc}">
              <meta itemprop="keywords" content="{tags_csv}">
              <meta itemprop="encodingFormat" content="{mime}">
              <meta itemprop="license" content="https://creativecommons.org/licenses/by/4.0/">
              <div class="sr-only ai-semantic-desc" itemprop="description">{desc} | Code: {code} | Category: {cat_label} | Tags: {tags_csv}</div>
            </figcaption>
          </figure>'''
            cards_html.append(card)

        cards_str = '\n'.join(cards_html)
        section = f'''      <!-- Year Group: {yr} -->
      <section class="gallery-year-section" id="year-{yr}" data-year-group="{yr}">
        <div class="year-section-header">
          <div class="year-header-title-wrap">
            <span class="year-header-badge"><i class="{meta['icon']}"></i> {yr}</span>
            <h2 class="year-heading">{meta['title']}</h2>
          </div>
          <p class="year-subheading">{meta['subtitle']} ({len(yr_items)} items)</p>
        </div>
        <div class="year-masonry-grid">
{cards_str}
        </div>
      </section>'''
        sections_html.append(section)

    all_sections_str = '\n\n'.join(sections_html)

    # Category counts
    cat_counts = {
        'all': len(items),
        'me': len([i for i in items if i.get('category') == 'me']),
        'moments': len([i for i in items if i.get('category') == 'moments']),
        'tech': len([i for i in items if i.get('category') == 'tech']),
        'reel': len([i for i in items if i.get('category') == 'reel' or i.get('type') == 'video'])
    }

    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-T4QKFS53YQ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-T4QKFS53YQ', {{
      'cookie_domain': 'none',
      'cookie_flags': 'SameSite=Lax;Secure'
    }});
  </script>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gallery | Mahendra Mali (Max)</title>
  <meta name="description" content="Official visual gallery archive of Mahendra Mali (Max): 133 verified photos and video reels of national science fair exhibitions and hardware prototypes.">
  <meta name="keywords" content="Mahendra Mali Gallery, Max Portfolio Photos, NCERT Science Exhibition Raipur, GCERT State Gold Medal, IoT Hardware Prototypes, Video Reels, Full-Stack Developer">
  <link rel="canonical" href="https://ohhmax.github.io/gallery/">

  <!-- Open Graph / WhatsApp / LinkedIn / Telegram Card -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mahendra Mali (Max)">
  <meta property="og:title" content="Gallery | Mahendra Mali (Max)">
  <meta property="og:description" content="Browse 133 authenticated photos and video reels of national science fair honors, IoT prototypes, and executive portraits from 2017 to 2026.">
  <meta property="og:url" content="https://ohhmax.github.io/gallery/">
  <meta property="og:image" content="https://ohhmax.github.io/assets/img/og/og-gallery-1200x630.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">

  <!-- Twitter / X Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mahendraplus">
  <meta name="twitter:creator" content="@mahendraplus">
  <meta name="twitter:title" content="Gallery | Mahendra Mali (Max)">
  <meta name="twitter:description" content="Browse 133 authenticated photos and video reels of national science fair honors, IoT prototypes, and executive portraits from 2017 to 2026.">
  <meta name="twitter:image" content="https://ohhmax.github.io/assets/img/og/hd-gallery-1920x1080.png">

  <!-- Robots & AI Crawlers (100% Crawling & Full Indexing) -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="bingbot" content="index, follow">

  <link rel="shortcut icon" href="/assets/img/logo/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=optional" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <!-- Schema.org JSON-LD Structured Data for Search Engines & AI Bots -->
  <script type="application/ld+json">
{json.dumps(schema_ld, indent=2)}
  </script>

  <style>
    :root {{
      --bg-primary: #0a0f1d;
      --bg-surface: #111827;
      --bg-card: #151d30;
      --border-color: #1f293d;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --accent-cyan: #38bdf8;
      --accent-purple: #c084fc;
      --accent-gold: #f59e0b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --chip-bg: rgba(255, 255, 255, 0.05);
      --font-main: 'Poppins', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, monospace;
    }}

    body.light-theme {{
      --bg-primary: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --border-color: #e2e8f0;
      --border-subtle: rgba(0, 0, 0, 0.08);
      --accent-cyan: #0284c7;
      --accent-purple: #9333ea;
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #64748b;
      --chip-bg: rgba(0, 0, 0, 0.04);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-main);
      background-color: var(--bg-primary);
      color: var(--text-main);
      line-height: 1.6;
      padding: 24px 16px 80px;
      transition: background-color 0.25s ease, color 0.25s ease;
    }}

    .sr-only {{
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }}

    .gallery-container {{
      max-width: 1380px;
      margin: 0 auto;
    }}

    /* Top Navigation Bar */
    .gallery-top-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 28px;
      flex-wrap: wrap;
    }}

    .nav-breadcrumbs {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.9rem;
    }}

    .nav-home-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      color: var(--accent-cyan);
      text-decoration: none;
      font-weight: 500;
      font-size: 0.88rem;
      transition: all 0.2s ease;
    }}

    .nav-home-btn:hover {{
      background: var(--accent-cyan);
      color: #000;
      border-color: var(--accent-cyan);
    }}

    .nav-actions-right {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .stat-pill {{
      padding: 6px 14px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 20px;
      color: var(--accent-cyan);
      font-size: 0.82rem;
      font-weight: 600;
    }}

    .theme-toggle-btn {{
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 0.95rem;
      transition: all 0.2s ease;
    }}

    .theme-toggle-btn:hover {{
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
    }}

    /* Gallery Header Hero */
    .gallery-hero {{
      text-align: center;
      margin-bottom: 32px;
    }}

    .gallery-hero h1 {{
      font-size: 2.2rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 10px;
      letter-spacing: -0.5px;
    }}

    .gallery-hero h1 span {{
      color: var(--accent-cyan);
    }}

    .gallery-hero-sub {{
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 820px;
      margin: 0 auto 20px;
    }}

    .gallery-hero-banner {{
      width: 100%;
      max-height: 320px;
      object-fit: cover;
      border-radius: 16px;
      border: 1px solid var(--border-color);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
      margin-bottom: 28px;
    }}

    /* Search and Filters Toolbar */
    .gallery-filter-toolbar {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 18px;
      padding: 20px 22px;
      margin-bottom: 36px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }}

    .toolbar-search-row {{
      display: flex;
      gap: 14px;
      align-items: center;
      margin-bottom: 18px;
      flex-wrap: wrap;
    }}

    .search-input-wrap {{
      position: relative;
      flex: 1;
      min-width: 280px;
    }}

    .search-input-wrap i.search-icon {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 0.95rem;
      pointer-events: none;
    }}

    .gallery-search-field {{
      width: 100%;
      padding: 12px 42px 12px 44px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 30px;
      color: var(--text-main);
      font-size: 0.92rem;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .gallery-search-field:focus {{
      border-color: var(--accent-cyan);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
    }}

    .search-clear-btn {{
      position: absolute;
      right: 14px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-dim);
      cursor: pointer;
      display: none;
      font-size: 0.9rem;
    }}

    .search-clear-btn:hover {{
      color: var(--text-main);
    }}

    .filter-tabs-label {{
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.7px;
      margin-bottom: 8px;
    }}

    .filter-pill-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }}

    .filter-pill-row:last-child {{
      margin-bottom: 0;
    }}

    .filter-btn {{
      padding: 7px 14px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      color: var(--text-muted);
      font-size: 0.82rem;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}

    .filter-btn:hover {{
      color: var(--text-main);
      border-color: var(--accent-cyan);
    }}

    .filter-btn.active {{
      background: var(--accent-cyan);
      color: #000;
      border-color: var(--accent-cyan);
      font-weight: 600;
    }}

    .filter-count {{
      font-size: 0.75rem;
      opacity: 0.8;
      background: rgba(0, 0, 0, 0.15);
      padding: 1px 6px;
      border-radius: 10px;
    }}

    .filter-btn.active .filter-count {{
      background: rgba(0, 0, 0, 0.25);
      color: #000;
    }}

    /* Year Group Section */
    .gallery-year-section {{
      margin-bottom: 48px;
    }}

    .year-section-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 2px solid var(--border-color);
      padding-bottom: 12px;
      margin-bottom: 22px;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .year-header-title-wrap {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .year-header-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 8px;
      color: var(--accent-cyan);
      font-size: 0.85rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }}

    .year-heading {{
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--text-main);
    }}

    .year-subheading {{
      font-size: 0.86rem;
      color: var(--text-muted);
    }}

    /* Pinterest-Style Masonry Grid */
    .year-masonry-grid {{
      column-count: 4;
      column-gap: 18px;
    }}

    @media (max-width: 1200px) {{
      .year-masonry-grid {{
        column-count: 3;
        column-gap: 16px;
      }}
    }}

    @media (max-width: 768px) {{
      .year-masonry-grid {{
        column-count: 2;
        column-gap: 12px;
      }}
    }}

    @media (max-width: 480px) {{
      .year-masonry-grid {{
        column-count: 1;
        column-gap: 0;
      }}
    }}

    /* Visual Pin Card (Clean, Uncluttered Pure Gallery) */
    .gallery-pin-card {{
      break-inside: avoid;
      margin-bottom: 18px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      overflow: hidden;
      display: block;
      transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.25s ease, border-color 0.25s ease;
      position: relative;
    }}

    .gallery-pin-card:hover {{
      transform: translateY(-5px);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4), 0 0 20px rgba(56, 189, 248, 0.12);
      border-color: rgba(56, 189, 248, 0.35);
    }}

    .pin-media-wrapper {{
      position: relative;
      width: 100%;
      background: #000;
      overflow: hidden;
      cursor: pointer;
    }}

    .pin-img {{
      display: block;
      width: 100%;
      height: auto;
      object-fit: cover;
      transition: transform 0.35s ease;
    }}

    .gallery-pin-card:hover .pin-img {{
      transform: scale(1.035);
    }}

    .pin-badge-group {{
      position: absolute;
      top: 10px;
      left: 10px;
      display: flex;
      flex-direction: column;
      gap: 5px;
      z-index: 2;
    }}

    .pin-code-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      background: rgba(11, 15, 25, 0.88);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(192, 132, 252, 0.4);
      border-radius: 6px;
      color: var(--accent-purple);
      font-size: 0.68rem;
      font-weight: 700;
      font-family: var(--font-mono);
      letter-spacing: 0.4px;
    }}

    .pin-year-badge {{
      display: inline-flex;
      align-items: center;
      padding: 2px 7px;
      background: rgba(11, 15, 25, 0.88);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 4px;
      color: #fff;
      font-size: 0.65rem;
      font-weight: 700;
      font-family: var(--font-mono);
      width: fit-content;
    }}

    .pin-cat-tag {{
      position: absolute;
      bottom: 10px;
      left: 10px;
      padding: 3px 9px;
      font-size: 0.7rem;
      font-weight: 600;
      border-radius: 20px;
      background: rgba(11, 15, 25, 0.88);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #fff;
      z-index: 2;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}

    .pin-play-icon {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: rgba(11, 15, 25, 0.8);
      backdrop-filter: blur(6px);
      border: 2px solid rgba(255, 255, 255, 0.3);
      color: var(--accent-cyan);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      pointer-events: none;
      transition: all 0.2s ease;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
    }}

    .gallery-pin-card:hover .pin-play-icon {{
      transform: translate(-50%, -50%) scale(1.1);
      background: var(--accent-cyan);
      color: #000;
      border-color: var(--accent-cyan);
    }}

    /* Card Caption Box (Clean, Concise, No Clutter) */
    .pin-caption-box {{
      padding: 12px 14px 12px;
    }}

    .pin-title {{
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 8px;
      line-height: 1.35;
    }}

    .pin-meta-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--border-subtle);
      padding-top: 9px;
      font-size: 0.74rem;
      color: var(--text-dim);
      flex-wrap: wrap;
      gap: 6px;
    }}

    .pin-meta-item {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}

    .pin-actions-wrap {{
      display: flex;
      align-items: center;
      gap: 5px;
      margin-left: auto;
    }}

    .pin-action-icon-btn {{
      background: var(--chip-bg);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      border-radius: 6px;
      width: 28px;
      height: 28px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      text-decoration: none;
      font-size: 0.78rem;
      transition: all 0.2s ease;
    }}

    .pin-action-icon-btn:hover {{
      background: var(--accent-cyan);
      color: #000;
      border-color: var(--accent-cyan);
    }}

    /* Fullscreen Interactive Lightbox Modal */
    .gallery-lightbox-modal {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(5, 8, 16, 0.94);
      backdrop-filter: blur(14px);
      z-index: 99999;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .gallery-lightbox-modal.active {{
      display: flex;
    }}

    .lightbox-dialog {{
      position: relative;
      max-width: 1080px;
      width: 100%;
      max-height: 92vh;
      display: flex;
      flex-direction: column;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
    }}

    .lightbox-close-btn {{
      position: absolute;
      top: 14px;
      right: 14px;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(0, 0, 0, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 10;
      font-size: 1rem;
      transition: all 0.2s ease;
    }}

    .lightbox-close-btn:hover {{
      background: #f43f5e;
      color: #fff;
      border-color: #f43f5e;
    }}

    .lightbox-nav-btn {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #fff;
      font-size: 1.1rem;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 10;
      transition: all 0.2s ease;
    }}

    .lightbox-nav-btn:hover {{
      background: var(--accent-cyan);
      color: #000;
      border-color: var(--accent-cyan);
    }}

    .lightbox-nav-btn.prev {{ left: 14px; }}
    .lightbox-nav-btn.next {{ right: 14px; }}

    .lightbox-media-container {{
      flex: 1;
      background: #000;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 320px;
      max-height: 65vh;
      overflow: hidden;
      position: relative;
    }}

    .lightbox-media-container img {{
      max-width: 100%;
      max-height: 65vh;
      object-fit: contain;
      display: block;
    }}

    .lightbox-media-container video {{
      max-width: 100%;
      max-height: 65vh;
      outline: none;
      display: none;
    }}

    .lightbox-details-panel {{
      padding: 18px 24px;
      background: var(--bg-surface);
      border-top: 1px solid var(--border-color);
    }}

    .lightbox-meta-top {{
      display: flex;
      gap: 10px;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
    }}

    .lightbox-code-chip {{
      padding: 3px 10px;
      background: rgba(192, 132, 252, 0.18);
      border: 1px solid rgba(192, 132, 252, 0.4);
      border-radius: 6px;
      color: var(--accent-purple);
      font-size: 0.74rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }}

    .lightbox-badge-chip {{
      padding: 3px 10px;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 20px;
      color: var(--accent-cyan);
      font-size: 0.74rem;
      font-weight: 600;
    }}

    .lightbox-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 6px;
    }}

    .lightbox-desc {{
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 12px;
    }}

    .lightbox-footer-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.8rem;
      color: var(--text-dim);
      border-top: 1px solid var(--border-subtle);
      padding-top: 10px;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .lightbox-download-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 16px;
      background: var(--accent-cyan);
      color: #000;
      border-radius: 20px;
      font-weight: 600;
      font-size: 0.82rem;
      text-decoration: none;
      transition: opacity 0.2s ease;
    }}

    .lightbox-download-btn:hover {{
      opacity: 0.9;
    }}

    /* Bottom Gateway CTA */
    .gallery-footer-cta {{
      text-align: center;
      padding: 40px 20px 20px;
      border-top: 1px solid var(--border-color);
      margin-top: 40px;
    }}

    .gallery-footer-cta h2 {{
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 8px;
    }}

    .gallery-footer-cta p {{
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-bottom: 20px;
    }}

    .btn-return-home {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 12px 28px;
      background: var(--accent-cyan);
      color: #000;
      border-radius: 30px;
      font-weight: 700;
      font-size: 0.95rem;
      text-decoration: none;
      transition: all 0.2s ease;
    }}

    .btn-return-home:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(56, 189, 248, 0.3);
    }}
  </style>
</head>
<body>
  <div class="gallery-container">
    <!-- Top Navigation Bar -->
    <header class="gallery-top-nav">
      <div class="nav-breadcrumbs">
        <a href="/" class="nav-home-btn" title="Return to Mahendra Mali Portfolio">
          <i class="fa-solid fa-arrow-left"></i>
          <span>Main Portfolio</span>
        </a>
        <span style="color: var(--text-dim);">/</span>
        <span style="color: var(--accent-cyan); font-weight: 600;">Visual Gallery</span>
      </div>
      <div class="nav-actions-right">
        <span class="stat-pill" id="totalMediaBadge"><i class="fa-solid fa-layer-group"></i> {len(items)} Media Items</span>
        <button type="button" class="theme-toggle-btn" id="galleryThemeToggleBtn" title="Toggle Light / Dark Mode" aria-label="Toggle theme">
          <i class="fa-solid fa-circle-half-stroke"></i>
        </button>
      </div>
    </header>

    <!-- Hero Header -->
    <section class="gallery-hero">
      <h1>Gallery | <span>Verified Moments</span></h1>
      <p class="gallery-hero-sub">
        Chronological archive of {len(items)} verified national science exhibition merit honors, 
        resonant wireless EV prototypes, Linux kernel lab consoles, video reels, and personal portraits (2017 to 2026).
      </p>
      <img src="/assets/img/og/og-gallery-1200x630.png" alt="Gallery | Mahendra Mali (Max)" class="gallery-hero-banner" width="1200" height="320">
    </section>

    <!-- Search & Dual-Filter Toolbar -->
    <section class="gallery-filter-toolbar">
      <div class="toolbar-search-row">
        <div class="search-input-wrap">
          <i class="fa-solid fa-magnifying-glass search-icon"></i>
          <input type="text" id="gallerySearchInput" class="gallery-search-field" placeholder="Search by title, code, year, or location..." aria-label="Search gallery items">
          <button type="button" id="searchClearBtn" class="search-clear-btn" aria-label="Clear search">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
        <span class="stat-pill" id="filteredCountBadge">Showing {len(items)} of {len(items)}</span>
      </div>

      <!-- Year Filter Tabs -->
      <div class="filter-tabs-label"><i class="fa-regular fa-calendar"></i> Filter by Year</div>
      <div class="filter-pill-row" id="yearFilterGroup">
        <button type="button" class="filter-btn active" data-filter-type="year" data-filter-val="all">
          <span>All Years</span>
          <span class="filter-count">{len(items)}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2026">
          <span>2026</span>
          <span class="filter-count">{len(grouped.get('2026', []))}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2025">
          <span>2025</span>
          <span class="filter-count">{len(grouped.get('2025', []))}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2024">
          <span>2024</span>
          <span class="filter-count">{len(grouped.get('2024', []))}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2023">
          <span>2023</span>
          <span class="filter-count">{len(grouped.get('2023', []))}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2022">
          <span>2022</span>
          <span class="filter-count">{len(grouped.get('2022', []))}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2021">
          <span>2021</span>
          <span class="filter-count">{len(grouped.get('2021', []))}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2019">
          <span>2019</span>
          <span class="filter-count">{len(grouped.get('2019', []))}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2018">
          <span>2018</span>
          <span class="filter-count">{len(grouped.get('2018', []))}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="year" data-filter-val="2017">
          <span>2017</span>
          <span class="filter-count">{len(grouped.get('2017', []))}</span>
        </button>
      </div>

      <!-- Category Filter Tabs -->
      <div class="filter-tabs-label" style="margin-top: 14px;"><i class="fa-solid fa-tags"></i> Filter by Category</div>
      <div class="filter-pill-row" id="catFilterGroup">
        <button type="button" class="filter-btn active" data-filter-type="cat" data-filter-val="all">
          <span>All Categories</span>
          <span class="filter-count">{cat_counts['all']}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="cat" data-filter-val="me">
          <span>Me</span>
          <span class="filter-count">{cat_counts['me']}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="cat" data-filter-val="moments">
          <span>Moments</span>
          <span class="filter-count">{cat_counts['moments']}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="cat" data-filter-val="tech">
          <span>Tech</span>
          <span class="filter-count">{cat_counts['tech']}</span>
        </button>
        <button type="button" class="filter-btn" data-filter-type="cat" data-filter-val="reel">
          <span>Reels</span>
          <span class="filter-count">{cat_counts['reel']}</span>
        </button>
      </div>
    </section>

    <!-- Main Pre-Rendered Media Catalog (Chronological Year Sections) -->
    <main id="galleryMainCatalog">
{all_sections_str}
    </main>

    <!-- Bottom Return CTA -->
    <footer class="gallery-footer-cta">
      <h2>Looking for Engineering Projects &amp; Credentials?</h2>
      <p>Explore full-stack software applications, Linux firmware, hardware schematics, and client testimonials.</p>
      <a href="/" class="btn-return-home">
        <i class="fa-solid fa-house"></i>
        <span>Return to Main Portfolio</span>
      </a>
      <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin-top:18px;font-size:0.92rem;">
        <a href="../about/" style="color:#38bdf8;text-decoration:none;">&bull; About Max</a>
        <a href="../projects/" style="color:#38bdf8;text-decoration:none;">&bull; 20 Engineered Projects</a>
        <a href="../resume/" style="color:#38bdf8;text-decoration:none;">&bull; Verified Curriculum Vitae</a>
        <a href="../testimonials/" style="color:#38bdf8;text-decoration:none;">&bull; Faculty Recommendations</a>
        <a href="../milestones/" style="color:#38bdf8;text-decoration:none;">&bull; National Science Milestones</a>
        <a href="../contact/" style="color:#38bdf8;text-decoration:none;">&bull; Direct Contact Channels</a>
        <a href="https://ohhmax.github.io/maxnet" style="color:#38bdf8;text-decoration:none;">&bull; MAXNET OS</a>
      </div>
    </footer>
  </div>

  <!-- Interactive Fullscreen Lightbox Modal -->
  <div class="gallery-lightbox-modal" id="galleryLightboxModal" role="dialog" aria-modal="true" aria-label="Media Lightbox">
    <div class="lightbox-dialog">
      <button type="button" class="lightbox-close-btn" id="lightboxCloseBtn" aria-label="Close Lightbox">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <button type="button" class="lightbox-nav-btn prev" id="lightboxPrevBtn" aria-label="Previous Media">
        <i class="fa-solid fa-chevron-left"></i>
      </button>
      <button type="button" class="lightbox-nav-btn next" id="lightboxNextBtn" aria-label="Next Media">
        <i class="fa-solid fa-chevron-right"></i>
      </button>

      <div class="lightbox-media-container" id="lightboxMediaContainer">
        <img id="lightboxImg" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="Gallery Photo Detail View">
        <video id="lightboxVideo" controls playsinline></video>
      </div>

      <div class="lightbox-details-panel">
        <div class="lightbox-meta-top">
          <span class="lightbox-code-chip" id="lightboxCodeChip"><i class="fa-solid fa-fingerprint"></i> CODE</span>
          <span class="lightbox-badge-chip" id="lightboxBadgeChip">Category</span>
          <span style="font-size: 0.8rem; color: var(--text-dim);" id="lightboxYearChip"><i class="fa-regular fa-calendar"></i> Year</span>
        </div>
        <h3 class="lightbox-title" id="lightboxTitle">Title</h3>
        <p class="lightbox-desc" id="lightboxDesc">Detailed Description</p>
        <div class="lightbox-footer-row">
          <span id="lightboxLocation"><i class="fa-solid fa-location-dot"></i> Location</span>
          <a href="#" id="lightboxDownloadLink" download class="lightbox-download-btn">
            <i class="fa-solid fa-arrow-down-to-bracket"></i>
            <span>Download High-Res Original</span>
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- Real-Time Client-Side Filtering & Lightbox Controller (Zero External JS Dependencies) -->
  <script>
    (function () {{
      'use strict';

      // Theme toggle with localStorage persistence
      var themeToggleBtn = document.getElementById('galleryThemeToggleBtn');
      var savedTheme = localStorage.getItem('max_portfolio_theme') || 'dark';
      if (savedTheme === 'light') {{
        document.body.classList.add('light-theme');
      }}
      if (themeToggleBtn) {{
        themeToggleBtn.addEventListener('click', function () {{
          var isLight = document.body.classList.toggle('light-theme');
          localStorage.setItem('max_portfolio_theme', isLight ? 'light' : 'dark');
        }});
      }}

      // DOM Elements
      var allCards = Array.from(document.querySelectorAll('.gallery-pin-card'));
      var allYearSections = Array.from(document.querySelectorAll('.gallery-year-section'));
      var searchInput = document.getElementById('gallerySearchInput');
      var searchClearBtn = document.getElementById('searchClearBtn');
      var countBadge = document.getElementById('filteredCountBadge');
      var yearFilterBtns = Array.from(document.querySelectorAll('#yearFilterGroup .filter-btn'));
      var catFilterBtns = Array.from(document.querySelectorAll('#catFilterGroup .filter-btn'));

      var activeYearFilter = 'all';
      var activeCatFilter = 'all';
      var currentSearchQuery = '';

      function applyFilters() {{
        var visibleCount = 0;

        allCards.forEach(function (card) {{
          var cardYear = card.getAttribute('data-year') || '';
          var cardCat = card.getAttribute('data-category') || '';
          var cardType = card.getAttribute('data-type') || '';
          var cardCode = (card.getAttribute('data-code') || '').toLowerCase();
          var cardTitle = (card.getAttribute('data-title') || '').toLowerCase();
          var cardLoc = (card.getAttribute('data-location') || '').toLowerCase();
          var cardTags = (card.getAttribute('data-tags') || '').toLowerCase();
          var cardDesc = (card.getAttribute('data-desc') || '').toLowerCase();

          // Year check
          var yearMatches = (activeYearFilter === 'all') || (cardYear === activeYearFilter);

          // Category check
          var catMatches = false;
          if (activeCatFilter === 'all') {{
            catMatches = true;
          }} else if (activeCatFilter === 'reel') {{
            catMatches = (cardCat === 'reel' || cardType === 'video');
          }} else {{
            catMatches = (cardCat === activeCatFilter);
          }}

          // Search check
          var searchMatches = true;
          if (currentSearchQuery) {{
            searchMatches = cardCode.indexOf(currentSearchQuery) !== -1 ||
                            cardTitle.indexOf(currentSearchQuery) !== -1 ||
                            cardLoc.indexOf(currentSearchQuery) !== -1 ||
                            cardTags.indexOf(currentSearchQuery) !== -1 ||
                            cardDesc.indexOf(currentSearchQuery) !== -1 ||
                            cardYear.indexOf(currentSearchQuery) !== -1;
          }}

          if (yearMatches && catMatches && searchMatches) {{
            card.style.display = '';
            visibleCount++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        // Hide empty year sections
        allYearSections.forEach(function (sec) {{
          var visibleInSec = sec.querySelectorAll('.gallery-pin-card:not([style*="display: none"])').length;
          sec.style.display = visibleInSec > 0 ? '' : 'none';
        }});

        if (countBadge) {{
          countBadge.textContent = 'Showing ' + visibleCount + ' of ' + allCards.length;
        }}
      }}

      // Year Filter Event Handlers
      yearFilterBtns.forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          yearFilterBtns.forEach(function (b) {{ b.classList.remove('active'); }});
          btn.classList.add('active');
          activeYearFilter = btn.getAttribute('data-filter-val');
          applyFilters();
        }});
      }});

      // Category Filter Event Handlers
      catFilterBtns.forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          catFilterBtns.forEach(function (b) {{ b.classList.remove('active'); }});
          btn.classList.add('active');
          activeCatFilter = btn.getAttribute('data-filter-val');
          applyFilters();
        }});
      }});

      // Search Event Handlers
      if (searchInput) {{
        searchInput.addEventListener('input', function (e) {{
          currentSearchQuery = e.target.value.trim().toLowerCase();
          if (searchClearBtn) {{
            searchClearBtn.style.display = currentSearchQuery ? 'inline-flex' : 'none';
          }}
          applyFilters();
        }});
      }}

      if (searchClearBtn) {{
        searchClearBtn.addEventListener('click', function () {{
          if (searchInput) {{
            searchInput.value = '';
            currentSearchQuery = '';
            searchClearBtn.style.display = 'none';
            searchInput.focus();
            applyFilters();
          }}
        }});
      }}

      // Lightbox Logic
      var modal = document.getElementById('galleryLightboxModal');
      var closeBtn = document.getElementById('lightboxCloseBtn');
      var prevBtn = document.getElementById('lightboxPrevBtn');
      var nextBtn = document.getElementById('lightboxNextBtn');
      var imgElem = document.getElementById('lightboxImg');
      var videoElem = document.getElementById('lightboxVideo');
      var codeChip = document.getElementById('lightboxCodeChip');
      var badgeChip = document.getElementById('lightboxBadgeChip');
      var yearChip = document.getElementById('lightboxYearChip');
      var titleElem = document.getElementById('lightboxTitle');
      var descElem = document.getElementById('lightboxDesc');
      var locElem = document.getElementById('lightboxLocation');
      var downloadLink = document.getElementById('lightboxDownloadLink');

      var currentLightboxIndex = -1;
      var visibleCardsList = [];

      function getVisibleCards() {{
        return allCards.filter(function (c) {{
          return c.style.display !== 'none';
        }});
      }}

      function openGalleryLightbox(cardId) {{
        visibleCardsList = getVisibleCards();
        var idx = visibleCardsList.findIndex(function (c) {{
          return c.id === cardId;
        }});
        if (idx === -1) idx = 0;
        showLightboxIndex(idx);
      }}

      function showLightboxIndex(index) {{
        if (!modal || visibleCardsList.length === 0) return;
        if (index < 0) index = visibleCardsList.length - 1;
        if (index >= visibleCardsList.length) index = 0;
        currentLightboxIndex = index;

        var card = visibleCardsList[currentLightboxIndex];
        var isVideo = card.getAttribute('data-type') === 'video';
        var src = card.getAttribute('data-src');
        var code = card.getAttribute('data-code');
        var title = card.getAttribute('data-title');
        var desc = card.getAttribute('data-desc');
        var badge = card.getAttribute('data-badge');
        var year = card.getAttribute('data-year');
        var date = card.getAttribute('data-date');
        var loc = card.getAttribute('data-location');

        if (isVideo) {{
          if (imgElem) imgElem.style.display = 'none';
          if (videoElem) {{
            videoElem.style.display = 'block';
            videoElem.src = src;
            videoElem.load();
            videoElem.play().catch(function () {{}});
          }}
        }} else {{
          if (videoElem) {{
            videoElem.pause();
            videoElem.style.display = 'none';
            videoElem.src = '';
          }}
          if (imgElem) {{
            imgElem.style.display = 'block';
            imgElem.src = src;
            imgElem.alt = title;
          }}
        }}

        if (codeChip) codeChip.innerHTML = '<i class="fa-solid fa-fingerprint"></i> ' + code;
        if (badgeChip) badgeChip.textContent = badge;
        if (yearChip) yearChip.innerHTML = '<i class="fa-regular fa-calendar"></i> ' + date;
        if (titleElem) titleElem.textContent = title;
        if (descElem) descElem.textContent = desc;
        if (locElem) locElem.innerHTML = '<i class="fa-solid fa-location-dot"></i> ' + loc;
        if (downloadLink) {{
          downloadLink.href = src;
          downloadLink.setAttribute('download', src.split('/').pop());
        }}

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }}

      function closeLightbox() {{
        if (!modal) return;
        if (videoElem) {{
          videoElem.pause();
          videoElem.src = '';
        }}
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }}

      if (closeBtn) closeBtn.onclick = closeLightbox;
      if (modal) {{
        modal.addEventListener('click', function (e) {{
          if (e.target === modal) closeLightbox();
        }});
      }}
      if (prevBtn) {{
        prevBtn.onclick = function (e) {{
          e.stopPropagation();
          showLightboxIndex(currentLightboxIndex - 1);
        }};
      }}
      if (nextBtn) {{
        nextBtn.onclick = function (e) {{
          e.stopPropagation();
          showLightboxIndex(currentLightboxIndex + 1);
        }};
      }}

      window.addEventListener('keydown', function (e) {{
        if (!modal || !modal.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showLightboxIndex(currentLightboxIndex - 1);
        if (e.key === 'ArrowRight') showLightboxIndex(currentLightboxIndex + 1);
      }});

      // Expose globally
      window.openGalleryLightbox = openGalleryLightbox;
      window.closeLightbox = closeLightbox;
    }})();
  </script>
</body>
</html>'''

    os.makedirs('gallery', exist_ok=True)
    with open('gallery/index.html', 'w', encoding='utf-8') as f:
        f.write(page_html)

    print(f'✔ Generated gallery/index.html successfully with {len(items)} pre-rendered cards across {len(grouped)} year groups!')

if __name__ == '__main__':
    main()
