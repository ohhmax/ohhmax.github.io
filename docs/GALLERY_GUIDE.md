# Media Vault & Gallery Management Guide

This guide explains how media is structured, named, and how to effortlessly add or remove photos and videos in the portfolio.

---

## 📁 Directory Architecture

All visual gallery media is stored inside `assets/img/gallery/` organized into four semantic subfolders:

```
assets/img/gallery/
├── Reel/           (Live video reels, national demonstrations, and WebP poster thumbs)
│   └── thumbs/
├── Moments/        (National and State science exhibitions, awards, certificates, campus moments)
│   └── thumbs/
├── Tech/           (IoT microcontrollers, circuits, solar EV tracks, kernel debugging, systems)
│   └── thumbs/
└── Me/             (Developer portraits, personal milestones, fitness routines)
    └── thumbs/
```

---

## Self-Describing Filename Format

Every media asset follows a predictable, self-documenting naming convention:

```
<YEAR>_<TITLE-SLUG>.<EXTENSION>
```

### Examples:
- `2026_qualcomm-enterprise-board-uart-serial-kernel-debugging-setup.jpg`
- `2026_sparks-to-ideas-official-software-internship-offer-letter.jpg`
- `2025_esp32-microcontroller-relay-driver-assembly-bench.jpg`
- `2019_doordarshan-dd-news-national-television-live-interview.mp4`
- `2019_ncert-46th-jnnsmee-grand-valedictory-award-ceremony-stage.jpg`
- `2018_gcert-gujarat-state-science-fair-gold-medal-stall-47-55.jpg`

### What Each Part Means:
1. **Year prefix (`2019_`, `2024_`, `2026_`)**: Automatically determines the date and sorts photos chronologically in file managers.
2. **Title slug (`qualcomm-enterprise-board-...`)**: Automatically converts into the user-facing title and SEO search keywords.
3. **Parent folder (`Moments/`, `Reel/`, `Tech/`, `Me/`)**: Assigns the category filter group and badge.

---

## How to Maintain Gallery Assets

1. Store media in the appropriate subfolder (`Moments/`, `Tech/`, `Reel/`, or `Me/`) using `<year>_<title-slug>.<ext>`, with a `.webp` thumbnail in its `thumbs/` subfolder.
2. Keep `data/gallery-items.json`, `gallery/index.html`, `index.html`, `sitemap.xml`, and `assets/xml/sitemap.xml` synchronized.
3. Run `npm test` to verify all media references, JSON schemas, and HTML pages pass with zero broken links.
