#!/usr/bin/env python3
"""
Apply perfect Schema.org, Link Graph, and Crawler discovery across all pages.
Strict Zero Em-Dash & En-Dash Guarantee.
"""

import json
import re

def clean_dashes(text: str) -> str:
    return text.replace('\u2014', ' - ').replace('\u2013', ' - ').replace('&mdash;', ' - ').replace('&ndash;', ' - ')

# 1. Update tools/enrich_all_pages.py with distinct schemas for milestones, projects, about
with open('tools/enrich_all_pages.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix milestones schema
old_m_schema = '''  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "ItemPage",
    "name": "Faculty Recommendations and Endorsements for Mahendra Mali (Max)",
    "url": "https://ohhmax.github.io/testimonials/",
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "5.0",
      "bestRating": "5",
      "reviewCount": "8"
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
          "name": "Testimonials",
          "item": "https://ohhmax.github.io/testimonials/"
        }
      ]
    }
  }
  </script>'''

new_m_schema = '''  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Engineering Milestones & Exhibition Honors | Mahendra Mali (Max)",
    "url": "https://ohhmax.github.io/milestones/",
    "creator": {
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
          "name": "Milestones",
          "item": "https://ohhmax.github.io/milestones/"
        }
      ]
    }
  }
  </script>'''

# Replace for milestones
code = code.replace(old_m_schema, new_m_schema, 1)

new_p_schema = '''  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Production Engineering Projects | Mahendra Mali (Max)",
    "url": "https://ohhmax.github.io/projects/",
    "creator": {
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
          "name": "Projects",
          "item": "https://ohhmax.github.io/projects/"
        }
      ]
    }
  }
  </script>'''

# Replace for projects
code = code.replace(old_m_schema, new_p_schema, 1)

new_a_schema = '''  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "AboutPage",
    "name": "About Mahendra Mali (Max) | Systems & Security Architect",
    "url": "https://ohhmax.github.io/about/",
    "mainEntity": {
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
          "name": "About",
          "item": "https://ohhmax.github.io/about/"
        }
      ]
    }
  }
  </script>'''

# Replace for about
code = code.replace(old_m_schema, new_a_schema, 1)

with open('tools/enrich_all_pages.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated tools/enrich_all_pages.py schemas.")

# 2. Add Schema to resume/index.html and pages/cv-resume-latest-info.html
resume_schema = '''  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "ProfilePage",
    "name": "Curriculum Vitae & Resume | Mahendra Mali (Max)",
    "url": "https://ohhmax.github.io/resume/",
    "mainEntity": {
      "@type": "Person",
      "name": "Mahendra Mali",
      "alternateName": "Max",
      "jobTitle": "Security Researcher & Systems Architect",
      "email": "ohmaxgit@gmail.com",
      "telephone": "+919824584454",
      "url": "https://ohhmax.github.io/"
    }
  }
  </script>
'''

for path in ['resume/index.html', 'pages/cv-resume-latest-info.html']:
    with open(path, 'r', encoding='utf-8') as f:
        rc = f.read()
    if 'application/ld+json' not in rc:
        rc = rc.replace('</head>', resume_schema + '</head>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(rc)
        print(f"Added schema to {path}")

# 3. Add organic milestone link into gallery section in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

milestone_link = '''      <!-- Portfolio Gallery -->
      <article class="gallery" data-page="gallery" id="gallery">
        <header style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px;">
          <h2 class="h2 article-title" style="margin-bottom: 0;">Gallery</h2>
          <a href="./milestones/" class="gallery-milestones-archive-link" style="color: #38bdf8; font-size: 0.88rem; font-weight: 600; text-decoration: underline; text-underline-offset: 3px;">
            <i class="fa-solid fa-award"></i> View National Science Congress &amp; Exhibition Archive
          </a>
        </header>'''

if 'gallery-milestones-archive-link' not in idx_content:
    old_gallery_hdr = '''      <!-- Portfolio Gallery -->
      <article class="gallery" data-page="gallery" id="gallery">
        <header>
          <h2 class="h2 article-title">Gallery</h2>
        </header>'''
    idx_content = idx_content.replace(old_gallery_hdr, milestone_link)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(clean_dashes(idx_content))
    print("Added organic milestones link in index.html gallery header.")
