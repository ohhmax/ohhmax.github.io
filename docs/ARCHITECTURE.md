# Portfolio System Architecture & Directory Organization

Technical overview of the project structure and directory architecture for **Mahendra Mali (Max)** portfolio.

---

## 🏛️ Directory Layout

```
MyPortfolio-2026/
├── assets/                  Static media assets
│   ├── img/                 Images, avatars, moments, and media vault
│   │   ├── gallery/         Organized folders (Me, Moments, Reel, Tech) with thumbs
│   │   ├── moments/         About section innovation slider moments (.webp)
│   │   ├── logo/            Brand icons and favicons
│   │   └── og/              Social Open Graph preview banners
│   ├── video/               Core video assets and highlights
│   ├── vendor/              Third-party libraries (FontAwesome)
│   └── xml/                 Sitemaps and search engine schemas
├── backend/                 Cloudflare Worker telemetry and contact gateway
├── css/                     Modular stylesheets and minified bundles
│   ├── style.css            Primary global design system and animations
│   ├── gallery.css          Media vault grid and vertical Reels explorer
│   └── maxhive-nav.css      Bottom floating glass dock and expandable drawer
├── js/                      Frontend controllers, datasets, and minified bundles
│   ├── script.js            Core SPA navigation, theme toggle, and modals
│   ├── portfolio-gallery.js Real-time 1:1 vertical Reels explorer and folder filters
│   ├── maxhive-nav.js       Bottom dock gestures, drawer, and breadcrumbs
│   ├── moments-data.js      Innovation slider moments data
│   ├── projects-data.js     Engineering projects dataset
│   └── testimonials.js      Client testimonials and review cards
├── pages/                   Static section endpoints and standalone documents
│   └── cv-resume-latest-info.html Complete text-searchable curriculum vitae
├── resume/                  Print-ready A4 HTML, PDF, and PNG resume exports
├── data/                    Structured JSON configurations and schemas
│   ├── gallery-items.json   Master catalog of 133 verified media assets
│   ├── resume-data.js       Resume JavaScript data mirror
│   └── resume.json          JSON Resume standardized data format
├── docs/                    Documentation and architectural guides
│   ├── ARCHITECTURE.md      System architecture and directory layout
│   └── GALLERY_GUIDE.md     Media vault management and naming conventions
├── about/ contact/ gallery/ milestones/ projects/ testimonials/ Dedicated SEO route pages
├── portfolio-monitor/       Companion Android intelligence app source & build script
├── index.html               Primary single-page portfolio application
├── 404.html                 Error fallback page
├── maxconf.json             Runtime configuration with encrypted notification fields
├── robots.txt               Crawler rules for Googlebot, Bingbot, and AI agents
├── sitemap.xml              Canonical XML sitemap with image namespace
├── llms.txt                 LLM summary dossier for AI agent grounding
├── llms-full.txt            Extended LLM dossier and credential reference
├── ai.txt                   AI crawler capabilities manifest
└── package.json             NPM scripts and project metadata
```

---

## Architecture Principles

1. **Pre-Rendered Static HTML**:
   All projects, 8 testimonials, and 133 gallery assets are pre-rendered into HTML markup. This guarantees immediate readability for `curl` requests, web scrapers, and AI search engines with zero client-side JavaScript execution required.

2. **Self-Describing Media Files**:
   Media files encode their year, category, and descriptive title directly into their filename and subfolder path.

3. **100% Asset Integrity**:
   Every referenced asset in HTML and CSS maps to an existing file on disk, verified by `npm test`.

4. **Zero-Dash Typography**:
   Strict adherence to standard punctuation, eliminating em-dashes and en-dashes across all files.
