# Media Vault & Gallery Management Guide

This guide explains how media is structured, named, and how to effortlessly add or remove photos and videos in the portfolio.

---

## 📁 Directory Architecture

All visual gallery media is stored inside `assets/img/gallery/` organized into six semantic subfolders:

```
assets/img/gallery/
├── videos/         (Live video reels, national demonstrations, and video projects)
│   └── thumbs/     (WebP poster thumbnails for instant loading)
├── honors/         (National and State science exhibitions, trophies, certificates)
│   └── thumbs/
├── hardware-iot/   (IoT microcontrollers, circuits, solar EV roadway tracks)
│   └── thumbs/
├── tech-lab/       (Kernel debugging, Linux matrices, internship appointment letters)
│   └── thumbs/
├── fitness/        (Gym workouts, training routines, and fitness milestones)
│   └── thumbs/
└── portraits/      (Developer portraits, campus moments, travel landscapes)
    └── thumbs/
```

---

## 🏷️ Self-Describing Filename Format

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
3. **Parent folder (`honors/`, `videos/`, etc.)**: Automatically assigns the category filter tab and badge.

---

## ⚡ How to Add New Photos or Videos

To add a new photo or video in the future:
1. Choose the appropriate subfolder (`honors/`, `hardware-iot/`, `tech-lab/`, `videos/`, `fitness/`, or `portraits/`).
2. Name your file using the `<year>_<title-slug>.<ext>` pattern.
   Example: `assets/img/gallery/honors/2026_national-coding-hackathon-first-prize.jpg`.
3. Run the generator script:
   ```bash
   python3 tools/reorganize_gallery_media.py
   python3 tools/build_portfolio_reels_gallery.py
   python3 tools/build_gallery_standalone_page.py
   python3 tools/generate-image-sitemap.py
   npm test
   ```
4. Done! The gallery, Schema.org metadata, sitemap, and vertical Reels explorer will update automatically.

---

## 🗑️ How to Delete Photos or Videos

1. Simply delete the file from `assets/img/gallery/<group>/`.
2. Run:
   ```bash
   python3 tools/reorganize_gallery_media.py
   python3 tools/build_portfolio_reels_gallery.py
   python3 tools/build_gallery_standalone_page.py
   python3 tools/generate-image-sitemap.py
   npm test
   ```
3. The deleted photo is automatically purged from the JSON catalog, HTML pages, and sitemaps.
