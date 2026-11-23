# Social Share Assets & Thumbnail Production Guide
**Portfolio of Mahendra Mali (Max)**

This directory (`assets/img/social-share/`) is the central repository for all social sharing preview banners, video teasers, and brand assets across platforms.

---

## Required Assets Checklist

| Asset File Name | Resolution & Aspect Ratio | Target Social Media / Platform |
| :--- | :--- | :--- |
| `og-universal-1200x630.png` | 1200 x 630 px (1.91:1) | WhatsApp, Telegram, LinkedIn, Facebook, Discord, Slack |
| `twitter-large-card-1200x675.png` | 1200 x 675 px (16:9) | Twitter / X Large Summary Cards |
| `instagram-square-1080x1080.png` | 1080 x 1080 px (1:1) | Instagram Feed, Threads, Facebook Square Posts |
| `instagram-story-reel-1080x1920.png` | 1080 x 1920 px (9:16) | Instagram Stories, Reels, YouTube Shorts, TikTok |
| `youtube-thumb-1280x720.png` | 1280 x 720 px (16:9) | YouTube Portfolio Walkthrough & Demo Reel |
| `github-repo-banner-1280x640.png` | 1280 x 640 px (2:1) | GitHub Profile Readme & Repository Social Previews |
| `whatsapp-telegram-avatar-800x800.png` | 800 x 800 px (1:1) | WhatsApp & Telegram Profile / Channel Avatar |
| `video-teaser-reel.mp4` | 1080 x 1920 or 1920 x 1080 | Runway / Kling AI 5 to 8 second looping motion teaser |
| `brand-cyber-mascot-logo-1024x1024.png`| 1024 x 1024 px (1:1) | MaxHive 3D Robot Mascot Icon & App Seal |
| `project-maxai-ondevice-ai-1200x675.png` | 1200 x 675 px (16:9) | MaxAI On-Device AI Project Showcase Banner |
| `project-celllock5g-1200x675.png` | 1200 x 675 px (16:9) | CellLock5G Modem Diagnostics Banner |
| `project-maxter-termux-1200x675.png` | 1200 x 675 px (16:9) | MAXTER Termux Developer Suite Banner |
| `project-goportproxy-1200x675.png` | 1200 x 675 px (16:9) | Go Port Proxy 10k Concurrency Router Banner |
| `project-homemax-50relay-1200x675.png` | 1200 x 675 px (16:9) | HomeMax 50-Relay Industrial Automation Banner |

---

## Prompts Dataset

All AI prompts, negative prompts, aspect ratios, and tool suggestions are saved in:
* File: `assets/img/social-share/social-prompts-data.json`

---

## Production Steps for Generated Images
1. Copy the prompt from `assets/img/social-share/social-prompts-data.json`.
2. Generate in **Midjourney v6.1**, **Flux.1 Pro**, or **DALL-E 3**.
3. Save the resulting image with the exact target filename listed above in `assets/img/social-share/`.
4. Run image optimization (e.g. TinyPNG or `oxipng`) to keep file size under 350KB for lightning-fast social preview loading.
