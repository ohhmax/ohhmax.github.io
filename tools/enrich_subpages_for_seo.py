#!/usr/bin/env python3
"""
Enrich subpages with rich, authentic content to resolve 'Thin content' and 'Orphan page' warnings.
Strict Zero Em-Dash & En-Dash Contract Verified.
"""
import json
import re

# ==============================================================================
# 1. ENRICH CONTACT/INDEX.HTML
# ==============================================================================
contact_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
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
  <title>Contact Mahendra Mali (Max) | Security &amp; Systems Engineer</title>
  <meta name="description" content="Get in touch with Mahendra Mali (Max) for security research, systems architecture, full-stack development, and embedded IoT consulting inquiries.">
  <meta name="keywords" content="Mahendra Mali, Max, Security Researcher, Systems Architect, All-Rounder Engineer, Golang, Android ADB, Linux Kernel, IoT Systems, Gujarat, India">
  <link rel="canonical" href="https://ohhmax.github.io/contact/">

  <!-- Open Graph / Social Preview -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mahendra Mali (Max)">
  <meta property="og:title" content="Contact Mahendra Mali (Max) | Security &amp; Systems Engineer">
  <meta property="og:description" content="Get in touch with Mahendra Mali (Max) for security research, systems architecture, full-stack development, and embedded IoT consulting inquiries.">
  <meta property="og:url" content="https://ohhmax.github.io/contact/">
  <meta property="og:image" content="https://ohhmax.github.io/assets/img/og/og-contact-1200x630.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">

  <!-- Twitter / X Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mahendraplus">
  <meta name="twitter:creator" content="@mahendraplus">
  <meta name="twitter:title" content="Contact Mahendra Mali (Max) | Security &amp; Systems Engineer">
  <meta name="twitter:description" content="Get in touch with Mahendra Mali (Max) for security research, systems architecture, full-stack development, and embedded IoT consulting inquiries.">
  <meta name="twitter:image" content="https://ohhmax.github.io/assets/img/og/hd-contact-1920x1080.png">

  <!-- Robots & AI Crawlers -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="bingbot" content="index, follow">

  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "ContactPage",
    "name": "Contact Mahendra Mali (Max)",
    "url": "https://ohhmax.github.io/contact/",
    "mainEntity": {
      "@type": "Person",
      "name": "Mahendra Mali",
      "email": "ohmaxgit@gmail.com",
      "telephone": "+919824584454",
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
          "name": "Contact",
          "item": "https://ohhmax.github.io/contact/"
        }
      ]
    }
  }
  </script>

  <style>
    :root {
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
    h2 { font-size: 1.4rem; color: #e2e8f0; margin: 28px 0 14px; font-weight: 600; border-left: 3px solid var(--cyan); padding-left: 10px; }
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
    .seo-card-item a { color: var(--cyan); text-decoration: none; }
    .seo-card-item a:hover { text-decoration: underline; }
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
  </style>

  <!-- Instant Browser Redirect to Full Interactive Single-Page App -->
  <script>
    (function() {
      var isBot = /bot|googlebot|bingbot|crawler|spider|slurp|facebookexternalhit|whatsapp|telegram|twitterbot|slackbot|discordbot|applebot/i.test(navigator.userAgent);
      if (!isBot && window.location.search.indexOf('no_redirect=1') === -1) {
        window.location.replace('/#contact');
      }
    })();
  </script>
</head>
<body>
  <main class="seo-container">
    <header class="seo-header">
      <h1>Get in Touch with Mahendra Mali (Max)</h1>
      <p class="seo-subtitle">Security Researcher, Systems Architect &amp; Software Engineer</p>
    </header>

    <img src="https://ohhmax.github.io/assets/img/og/og-contact-1200x630.png" alt="Contact Mahendra Mali (Max) | Security Researcher and Systems Architect" class="seo-preview-banner" width="1200" height="630">

    <section class="seo-content-block">
      <h2>Primary Engineering &amp; Research Channels</h2>
      <div class="seo-card-item">
        <p><strong>Direct Email:</strong> <a href="mailto:ohmaxgit@gmail.com">ohmaxgit@gmail.com</a></p>
        <p><strong>Secondary Academic Email:</strong> <a href="mailto:mahendrakumarganpatbhaimali@gmail.com">mahendrakumarganpatbhaimali@gmail.com</a></p>
        <p><strong>Direct Telegram:</strong> <a href="https://t.me/mahendraplus" target="_blank" rel="noopener">t.me/mahendraplus</a></p>
        <p><strong>Telegram Research Channel:</strong> <a href="https://t.me/the_max_lab" target="_blank" rel="noopener">t.me/the_max_lab</a></p>
        <p><strong>Official GitHub:</strong> <a href="https://github.com/ohhmax" target="_blank" rel="noopener">github.com/ohhmax</a></p>
        <p><strong>Developer Profile:</strong> <a href="https://github.com/mahendraplus" target="_blank" rel="noopener">github.com/mahendraplus</a></p>
        <p><strong>LinkedIn Professional:</strong> <a href="https://linkedin.com/in/mahendraplus" target="_blank" rel="noopener">linkedin.com/in/mahendraplus</a></p>
        <p><strong>Physical Base:</strong> Gujarat, Bharat (India) &bull; Available for Global Remote, Hybrid, and On-Site Engineering Deployments</p>
      </div>
    </section>

    <section class="seo-content-block">
      <h2>Technical Consultation &amp; System Collaboration Areas</h2>
      <div class="seo-card-item">
        <h3>1. Embedded Systems, Microcontrollers &amp; IoT Firmware</h3>
        <p>Architecting custom hardware schematics, resonant wireless power coupling, automated safety interlocks, and non-volatile EEPROM state recovery engines across ESP32, ESP8266, and Arduino Mega platforms.</p>
      </div>
      <div class="seo-card-item">
        <h3>2. Low-Level Linux, OpenWrt &amp; Qualcomm Kernel Engineering</h3>
        <p>Kernel configuration, AOSP device tree bringup, Qualcomm IPQ9574 AArch64 and MSM8916 custom kernels, OpenWrt 6.18 distribution engineering, and LuCI network telemetry interfaces.</p>
      </div>
      <div class="seo-card-item">
        <h3>3. Telecom Security, Cellular Modem Telemetry &amp; Reverse Engineering</h3>
        <p>Qualcomm AT baseband protocol automation, 5G NR Standalone (SA) and Non-Standalone (NSA) carrier aggregation locking, cellular failover daemons, and RF spectrum diagnostics.</p>
      </div>
      <div class="seo-card-item">
        <h3>4. High-Performance Full-Stack Systems &amp; Concurrency</h3>
        <p>Low-latency Go reverse proxies, real-time WebSocket telemetry pipelines, responsive CSS architectural systems, and SQLite/PostgreSQL database tuning.</p>
      </div>
    </section>

    <section class="seo-content-block">
      <h2>Coordinated Vulnerability Disclosure &amp; Security Audits</h2>
      <div class="seo-card-item">
        <p>All reverse engineering, hardware security testing, and modem protocol diagnostics conducted by Mahendra Mali (Max) operate under standard defensive security research and authorized academic testing methodologies. Security inquiries, coordinated vulnerability disclosures (CVD), and firmware audit requests receive priority response within 24 hours.</p>
      </div>
    </section>

    <section class="seo-content-block">
      <h2>Explore Portfolio Hub &amp; Direct Sections</h2>
      <div class="site-directory-grid">
        <a href="../about/" class="directory-link">&bull; About Overview</a>
        <a href="../projects/" class="directory-link">&bull; 20 Engineered Projects</a>
        <a href="../resume/" class="directory-link">&bull; Verified Curriculum Vitae</a>
        <a href="../testimonials/" class="directory-link">&bull; Faculty Recommendations</a>
        <a href="../gallery/" class="directory-link">&bull; Visual Moments &amp; Media</a>
        <a href="../milestones/" class="directory-link">&bull; National Science Milestones</a>
      </div>
    </section>

    <div class="seo-actions">
      <a href="/#contact" class="btn-action btn-primary">Open Interactive View</a>
      <a href="/" class="btn-action btn-secondary">Main Portfolio</a>
    </div>
  </main>
</body>
</html>'''

with open('contact/index.html', 'w', encoding='utf-8') as f:
    f.write(contact_html)
print('Updated contact/index.html with rich content and internal links.')
