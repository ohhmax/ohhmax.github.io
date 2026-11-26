"""
tools/generate-image-sitemap.py - Generates sitemap.xml with image entries.
"""

import os
import json
import re
import xml.sax.saxutils as saxutils

def escape_xml(s):
    return saxutils.escape(str(s or ''))

def main():
    with open('data/gallery-items.json', 'r', encoding='utf-8') as fp:
        gallery_items = json.load(fp)

    # Read project IDs from assets/js/projects-data.js
    with open('assets/js/projects-data.js', 'r', encoding='utf-8') as fp:
        pdata_raw = fp.read()
    
    # Extract project names/slugs
    names = re.findall(r'"name":\s*"([^"]+)"', pdata_raw)
    slug_map = {
        'MaxAI': 'maxai',
        'CellLock 5G': 'celllock5g',
        'HomeMax': 'homemax',
        'CellWatchPro': 'cellwatchpro',
        'Amul Dairy Platform': 'amul-dairy-platform',
        'MaxFit': 'maxfit',
        'MaxHive OSINT': 'maxhive-osint',
        'IPCAI Studio': 'ipcai-studio',
        'LuCI Cyber Theme': 'luci-cyber-theme',
        'ADB on OpenWrt': 'adb-on-wrt',
        'Go Port Proxy': 'go-port-proxy',
        'MAXTER': 'maxter',
        'Qualcomm Kernel': 'qualcomm-custom-kernel',
        'MaxKit Android': 'maxkit-android',
        'SDX65 Pipeline': 'sdx65-modem-pipeline',
        'Safety Interlock': 'alcohol-safety-interlock',
        'Ultrasonic Profiler': 'ultrasonic-profiler',
        'Developer Cheatsheets': 'developer-cheatsheets',
        'GSRTC Transit': 'gsrtc-transit-platform'
    }

    project_slugs = []
    for n in names:
        matched = False
        for k, slug in slug_map.items():
            if k.lower() in n.lower():
                project_slugs.append(slug)
                matched = True
                break
        if not matched:
            project_slugs.append(re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-'))

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
        '  <url>',
        '    <loc>https://ohhmax.github.io/</loc>',
        '    <lastmod>2026-10-30T00:00:00+00:00</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://ohhmax.github.io/gallery/</loc>',
        '    <lastmod>2026-10-30T00:00:00+00:00</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.95</priority>'
    ]

    # Add all gallery media items to /gallery/ URL entry with Google Image Sitemap schema (images only, skip videos)
    for item in gallery_items:
        src = item.get('src', '')
        if not src or src.lower().endswith('.mp4'):
            continue
        full_url = f'https://ohhmax.github.io/{src}'
        title = escape_xml(item.get('title', ''))
        desc = escape_xml(item.get('desc', ''))
        xml_lines.append('    <image:image>')
        xml_lines.append(f'      <image:loc>{full_url}</image:loc>')
        if title:
            xml_lines.append(f'      <image:title>{title}</image:title>')
        if desc:
            xml_lines.append(f'      <image:caption>{desc}</image:caption>')
        xml_lines.append('    </image:image>')

    xml_lines.append('  </url>')

    # Standard section landing pages
    sections = [
        ('about', '0.95', 'monthly'),
        ('projects', '1.0', 'weekly'),
        ('resume', '0.95', 'monthly'),
        ('testimonials', '0.95', 'monthly'),
        ('milestones', '0.90', 'monthly'),
        ('contact', '0.90', 'monthly'),
    ]

    for sname, prio, freq in sections:
        xml_lines.extend([
            '  <url>',
            f'    <loc>https://ohhmax.github.io/{sname}/</loc>',
            '    <lastmod>2026-10-30T00:00:00+00:00</lastmod>',
            f'    <changefreq>{freq}</changefreq>',
            f'    <priority>{prio}</priority>',
            '  </url>',
            '  <url>',
            f'    <loc>https://ohhmax.github.io/#{sname}</loc>',
            '    <lastmod>2026-10-30T00:00:00+00:00</lastmod>',
            f'    <changefreq>{freq}</changefreq>',
            f'    <priority>{round(float(prio) - 0.05, 2)}</priority>',
            '  </url>'
        ])

    # Hash for gallery
    xml_lines.extend([
        '  <url>',
        '    <loc>https://ohhmax.github.io/#gallery</loc>',
        '    <lastmod>2026-10-30T00:00:00+00:00</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>'
    ])

    # Project deep links
    for pid in project_slugs:
        xml_lines.extend([
            '  <url>',
            f'    <loc>https://ohhmax.github.io/#project-{pid}</loc>',
            '    <lastmod>2026-10-30T00:00:00+00:00</lastmod>',
            '    <changefreq>weekly</changefreq>',
            '    <priority>0.85</priority>',
            '  </url>'
        ])

    xml_lines.append('</urlset>')

    sitemap_content = '\n'.join(xml_lines) + '\n'
    with open('sitemap.xml', 'w', encoding='utf-8') as fp:
        fp.write(sitemap_content)

    print(f'✔ Generated sitemap.xml with {len(gallery_items)} indexed image entries!')

if __name__ == '__main__':
    main()
