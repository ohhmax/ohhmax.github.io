# Portfolio System Architecture & Directory Organization

Technical overview of the project structure and directory architecture for **Mahendra Mali (Max)** portfolio.

---

## 🏛️ Directory Layout

```
MyPortfolio-2026/
├── assets/                  Static media assets
│   ├── img/                 Images, avatars, moments, and media vault
│   │   ├── gallery/         Organized groupwise folders (honors, iot, videos, lab, fitness, portraits)
│   │   ├── moments/         About section innovation slider moments
│   │   ├── logo/            Brand icons and favicons
│   │   └── og/              Social Open Graph preview banners
│   ├── video/               Core video assets and highlights
│   ├── vendor/              Third-party libraries (FontAwesome, Ionicons)
│   └── xml/                 Sitemaps and search engine schemas
├── css/                     Modular stylesheets
│   ├── style.css            Primary global design system and animations
│   ├── gallery.css          Media vault grid and vertical Reels explorer
│   └── maxhive-nav.css      Bottom floating glass dock and expandable drawer
├── js/                      Frontend controllers and datasets
│   ├── script.js            Core SPA navigation, theme toggle, and modals
│   ├── portfolio-gallery.js Real-time 1:1 vertical Reels explorer and folder filters
│   ├── maxhive-nav.js       Bottom dock gestures, drawer, and breadcrumbs
│   ├── moments-data.js      Innovation slider moments data
│   ├── projects-data.js     Engineering projects dataset
│   └── testimonials.js      Client testimonials and review cards
├── pages/                   Static section endpoints and standalone documents
│   └── cv-resume-latest-info.html Complete text-searchable curriculum vitae
├── components/              Reusable HTML UI snippets and modal blueprints
├── data/                    Structured JSON configurations and schemas
│   ├── gallery-items.json   Master catalog of 130 verified media assets
│   ├── projects.json        19 software and hardware systems dataset
│   └── resume.json          JSON Resume standardized data format
├── docs/                    Documentation, architectural specs, and guides
│   ├── ARCHITECTURE.md      System architecture and directory layout
│   └── GALLERY_GUIDE.md     Media vault management and self-describing filename format
├── tools/                   Automation, testing, build, and audit tools
│   ├── audit-portfolio-seo-and-quality.js Strict SEO, asset, and DOM quality test suite
│   ├── vault-server.js      Zero-dependency local HTTP testing server
│   └── build_portfolio_reels_gallery.py Static HTML media card generator
├── index.html               Primary single-page portfolio application
├── 404.html                 Error fallback page
├── robots.txt               Crawler rules for Googlebot, Bingbot, and AI agents
├── sitemap.xml              Canonical XML sitemap with image namespace
├── llms.txt                 LLM summary dossier for AI agent grounding
└── package.json             NPM scripts and project metadata
```

---

## 🎯 Architecture Principles

1. **Pre-Rendered Static HTML**:
   All 19 projects, 8 testimonials, and 130 gallery assets are pre-rendered into HTML markup. This guarantees immediate readability for `curl` requests, web scrapers, and AI search engines with zero client-side JavaScript execution required.

2. **Self-Describing Media Files**:
   Media files encode their year, category, and descriptive title directly into their filename and subfolder path.

3. **100% Asset Integrity**:
   Every referenced asset in HTML and CSS maps to an existing file on disk, verified by `npm test`.

4. **Zero-Dash Typography**:
   Strict adherence to standard punctuation, eliminating em-dashes and en-dashes across all files.
