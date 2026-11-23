# Mahendra Mali: Executive Engineering Resume

An ultra-modern, high-impact, single-page A4 executive resume engineered for tech leadership, systems engineering, cybersecurity, on-device AI, and full-stack software development roles.

Built strictly to standard **A4 dimensions (210mm × 297mm)** with a zero-overflow guarantee, reactive modern web technologies, and a decoupled **JSON-driven architecture**.

---

## 🎯 Executive Profile & Core Strengths Analysis

Based on an exhaustive analysis of your GitHub repositories (`github.com/mahendraplus`), personal portfolio (`mahendraplus.github.io`), local project directories, and official academic/national awards:

### Where You Are Best (Your Unique Edge):
1. **Bare Metal to High-Level Systems Architect**:
   Unlike typical software developers who only write application logic, you bridge the entire stack: from Qualcomm IPQ9574 AArch64 kernel firmware compilation (`maxidu`), ESP8266/ESP32 bare-metal C++ with 400 kHz Fast I2C (`HomeMax`), up to native Android (Kotlin) and modern reactive web dashboards.
2. **Telecommunications, 5G RF & On-Device AI**:
   - `maxkit` & `CellWatchPro`: Enforcing Jio 5G Dual-Band Carrier Aggregation (n78+n28) locking with live tower telemetry and diagnostic port scanning.
   - `maxai`: On-device AI engine executing quantized LiteRT LM and GGUF models directly on mobile GPUs with zero cloud latency and built-in function calling.
3. **Cybersecurity, Reverse Engineering & Protocol Forensics**:
   - Enterprise API Reverse Engineering: Deep traffic analysis and session reconstruction of closed enterprise ERP systems (`amuldairy` / Amul AMCS).
   - Network Security & Pentesting: Burp Suite Pro workflow automation (`bmax`), wireless packet injection (`rtl8812au`), and high-star security tooling (`B4Bomber` with 69+ stars, `MAXTER` with 23+ stars).
4. **National-Level Proven Innovation**:
   - **NCERT National Science Exhibition Finalist (JNNSMEE Raipur 2019)** for your *Batteryless Electric Car* exhibit.
   - **State Science Exhibition Winner (GCERT Gandhinagar 2018)**.
   - **IIT Gandhinagar Amalthea '18 ICON** participant.

---

## 📁 Project Structure

```
/home/max/Projects/resume/
├── index.html                 # Modern reactive web resume & interactive dashboard
├── resume.json                # Single source of truth (edit this file anytime!)
├── resume-data.js             # Fallback data layer for direct file:// browsing without CORS
├── generate_exports.js        # Automated headless Chrome Puppeteer exporter
├── Mahendra_Mali_Resume.pdf   # Print-ready vector single-page A4 PDF (613 KB)
├── Mahendra_Mali_Resume.png   # Ultra-crisp 300 DPI high-definition PNG (1.2 MB)
├── photo.jpg                  # Optimized portrait avatar photo
├── package.json               # Node.js build & export scripts
└── README.md                  # Complete documentation and user guide
```

---

## 🚀 Quick Start & How to Use

### 1. View in Any Browser
Simply double-click or open `index.html` in any web browser:
```bash
# Open in your browser directly
xdg-open index.html
# Or with firefox:
firefox index.html
```

### 2. Interactive Web Toolbar Features
When viewing `index.html` on your screen, a floating toolbar provides powerful controls:
- **Download PDF**: Instant direct download of the pre-rendered vector PDF.
- **Download PNG (300 DPI)**: Instant download of the ultra-high-resolution image.
- **Browser Print**: Triggers your browser's print dialog configured with exact A4 print rules.
- **Photo: ON / OFF**: 1-click toggle to show or hide the portrait photo (automatically adjusts layout).
- **Theme Switcher**: Choose from 4 curated styles:
  - `Modern Slate (Blue)`: High-contrast executive standard
  - `Cyber Teal`: Clean modern technical aesthetic
  - `Deep Indigo`: Sophisticated dark-accent palette
  - `Monochromatic (Classic)`: Minimalist editorial black and white
- **Live Edit Mode**: Click "Edit Live" to edit any text directly on the screen, then click "Save JSON" to download your updated `resume.json`!

### 3. How to Update Your Resume Data
To update your experience, projects, skills, or contact info:
1. Open [`resume.json`](file:///home/max/Projects/resume/resume.json).
2. Edit any field, add new bullet points, or update numbers.
3. Run the export command to regenerate both the PDF and PNG automatically:
```bash
npm run export
# or
node generate_exports.js
```

---

## 📐 Strict A4 Single-Page Guarantee

- **Target Dimensions**: `210mm × 297mm` (Standard A4 portrait).
- **Page Containment**: The container height is precisely calibrated at `1123px` (`offsetHeight: 1123px`, `scrollHeight: 1123px`), ensuring **zero overflow**, no awkward split-pages, and no second blank page during export or printing.
- **Font Stack**: Clean, modern typography using Google's *Plus Jakarta Sans* for headings/body and *JetBrains Mono* for technical stacks.

---

## 📄 Export Artifacts

- [📄 Mahendra_Mali_Resume.pdf](file:///home/max/Projects/resume/Mahendra_Mali_Resume.pdf): Ready for job applications, ATS portals, and printing.
- [🖼️ Mahendra_Mali_Resume.png](file:///home/max/Projects/resume/Mahendra_Mali_Resume.png): 300 DPI high-definition image for LinkedIn, portfolio showcases, or image sharing.
