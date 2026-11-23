#!/usr/bin/env python3
"""
tools/rebuild_gallery_folders.py
Rebuilds gallery metadata and markup according to the user's updated gallery folder structure:
- 4 Folders: Me (56), Moments (20), Tech (30), Reel (27) = 133 items
- Filter pills: Me (default active), Moments, Tech, Reels (No "All" filter)
- Album order: Me -> Moments -> Tech -> Reel
- Seamless Next / Previous transitions across all albums
- Zero Em-Dash & En-Dash verification
"""

import os
import json
import re
import shutil
import xml.sax.saxutils as saxutils

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GALLERY_DIR = os.path.join(ROOT_DIR, 'assets', 'img', 'gallery')
FOLDERS = ['Me', 'Moments', 'Tech', 'Reel']

def escape_html(s):
    return saxutils.escape(str(s or ''))

def clean_no_dashes(text):
    if not text:
        return ""
    return str(text).replace('\u2014', ' - ').replace('\u2013', ' - ')

def main():
    old_items_file = os.path.join(ROOT_DIR, 'data', 'gallery-items.json')
    with open(old_items_file, 'r', encoding='utf-8') as f:
        old_items = json.load(f)

    # Index old items by filename
    items_by_filename = {}
    for it in old_items:
        fname = it.get('filename') or os.path.basename(it.get('src', ''))
        items_by_filename[fname] = it

    new_items = []
    
    for folder in FOLDERS:
        fdir = os.path.join(GALLERY_DIR, folder)
        if not os.path.exists(fdir):
            print(f"Warning: {fdir} not found!")
            continue
        
        files = sorted(os.listdir(fdir))
        for fname in files:
            if fname == 'thumbs' or fname.startswith('.'):
                continue
            
            fpath = os.path.join(fdir, fname)
            if not os.path.isfile(fpath):
                continue

            is_video = fname.endswith('.mp4')
            base_name = os.path.splitext(fname)[0]
            existing = items_by_filename.get(fname, {})

            # Clean titles & descriptions without any em-dashes
            raw_title = existing.get('title') or re.sub(r'^[0-9]+_', '', base_name).replace('-', ' ').replace('_', ' ').title()
            title = clean_no_dashes(raw_title)
            desc = clean_no_dashes(existing.get('desc') or title)
            loc = clean_no_dashes(existing.get('location') or 'Gujarat, India')
            
            # Tags
            tags = [clean_no_dashes(t) for t in existing.get('tags', [folder])]
            
            src = f"assets/img/gallery/{folder}/{fname}"
            if is_video:
                thumb = f"assets/img/gallery/Reel/thumbs/thumb_{base_name}.webp"
            else:
                thumb = src

            # Verify thumb exists for videos
            if is_video and not os.path.exists(os.path.join(ROOT_DIR, thumb)):
                print(f"Warning: Missing thumb for video {src}: {thumb}")

            group = folder.lower() # 'me', 'moments', 'tech', 'reel'
            m_year = re.search(r'20\d\d', fname)
            year = m_year.group(0) if m_year else str(existing.get('year') or '2024')
            date_str = existing.get('date') or year

            if folder == 'Me':
                icon = 'fa-solid fa-user'
                badge = 'Me'
            elif folder == 'Moments':
                icon = 'fa-solid fa-trophy'
                badge = 'Moments'
            elif folder == 'Tech':
                icon = 'fa-solid fa-microchip'
                badge = 'Tech'
            else:
                icon = 'fa-solid fa-clapperboard'
                badge = 'Reels'

            item_obj = {
                "id": existing.get('id') or f"gallery-{group}-{base_name}",
                "code": existing.get('code') or f"{group[:3].upper()}-{base_name[:8]}",
                "filename": fname,
                "src": src,
                "thumb": thumb,
                "type": "video" if is_video else "image",
                "category": group,
                "categoryLabel": folder if folder != 'Reel' else 'Reels',
                "badge": badge,
                "icon": icon,
                "color": existing.get('color', '#38bdf8'),
                "title": title,
                "desc": desc,
                "location": loc,
                "date": date_str,
                "width": existing.get('width', 1080 if is_video else 1920),
                "height": existing.get('height', 1920 if is_video else 1080),
                "aspectRatio": existing.get('aspectRatio', 0.5625 if is_video else 1.333),
                "tags": tags,
                "sizeBytes": os.path.getsize(fpath),
                "folder": folder if folder != 'Reel' else 'Reels',
                "group": group,
                "alt": f"{title} | {folder} - Mahendra Mali (Max) Portfolio",
                "year": year
            }
            new_items.append(item_obj)

    # Sort items: Album sequence order (Me -> Moments -> Tech -> Reel), and within each album year descending
    album_order = {'me': 0, 'moments': 1, 'tech': 2, 'reel': 3}
    def sort_key(it):
        grp_rank = album_order.get(it.get('group'), 99)
        try:
            yr = int(it.get('year') or 2024)
        except:
            yr = 2024
        return (grp_rank, -yr, it.get('title', ''))

    new_items_sorted = sorted(new_items, key=sort_key)

    print(f"Total curated items in 4 folders: {len(new_items_sorted)}")
    counts = {}
    for it in new_items_sorted:
        counts[it['group']] = counts.get(it['group'], 0) + 1
    print(f"Counts: {counts}")

    # 1. Write data/gallery-items.json
    with open(old_items_file, 'w', encoding='utf-8') as f:
        json.dump(new_items_sorted, f, indent=2, ensure_ascii=False)
    print("Updated data/gallery-items.json")

    # 2. Write js/gallery-data.js
    gallery_data_js = f"""/**
 * js/gallery-data.js
 * Auto-generated gallery media catalog for Mahendra Mali (Max) portfolio.
 * Curated Folders: Me (56), Moments (20), Tech (30), Reel (27).
 * Total items: {len(new_items_sorted)}
 * Strict Zero Em-Dash & En-Dash Contract Verified.
 */
window.GALLERY_ITEMS = {json.dumps(new_items_sorted, indent=2, ensure_ascii=False)};
"""
    with open(os.path.join(ROOT_DIR, 'js', 'gallery-data.js'), 'w', encoding='utf-8') as f:
        f.write(gallery_data_js)
    print("Updated js/gallery-data.js")

    # 3. Build Card HTML for index.html
    cards_html = []
    for idx, it in enumerate(new_items_sorted):
        item_id = it['id']
        code = it['code']
        title = it['title']
        desc = it['desc']
        cat = it['category']
        group = it['group']
        folder_label = it['folder']
        item_type = it['type']
        src = it['src']
        thumb = it['thumb']
        date_str = it['date']
        loc = it['location']
        tags_str = ' '.join(f'#{t.replace(" ", "")}' for t in it['tags'][:5])
        alt_text = it['alt']

        media_badge = '<span class="gallery-card-badge video-badge" title="Video"><i class="fa-solid fa-play"></i></span>' if item_type == 'video' else ''

        card_markup = f'''          <div class="portfolio-media-card" 
                   id="{escape_html(item_id)}" 
                   itemscope itemtype="https://schema.org/ImageObject"
                   data-index="{idx}"
                   data-code="{escape_html(code)}" 
                   data-category="{escape_html(cat)}" 
                   data-group="{escape_html(group)}" 
                   data-subcat="" 
                   data-type="{escape_html(item_type)}" 
                   data-year="{escape_html(date_str)}" 
                   data-src="{escape_html(src)}" 
                   data-thumb="{escape_html(thumb)}" 
                   data-title="{escape_html(title)}" 
                   data-desc="{escape_html(desc)}" 
                   data-folder="{escape_html(folder_label)}"
                   data-tags="{escape_html(tags_str)}" 
                   data-location="{escape_html(loc)}" 
                   onclick="openGalleryMedia({idx})">
            <meta itemprop="name" content="{escape_html(title)}">
            <meta itemprop="description" content="{escape_html(desc)}">
            <meta itemprop="contentUrl" content="{escape_html(src)}">
            <meta itemprop="thumbnailUrl" content="{escape_html(thumb)}">
            
            <div class="gallery-card-inner">
              <img src="{escape_html(thumb)}" 
                   alt="{escape_html(alt_text)}" 
                   class="gallery-card-img" 
                   loading="lazy"
                   decoding="async">
              {media_badge}
              <div class="gallery-card-overlay">
                <span class="icon-focus"><i class="fa-solid fa-expand"></i></span>
              </div>
            </div>

            <!-- Pre-Rendered Hidden Metadata for SEO & Accessibility -->
            <div class="gallery-card-hidden-meta" style="display: none;" aria-hidden="true">
              <span class="hidden-title">{escape_html(title)}</span>
              <span class="hidden-desc">{escape_html(desc)}</span>
              <span class="hidden-date">{escape_html(date_str)}</span>
              <span class="hidden-location">{escape_html(loc)}</span>
              <span class="hidden-tags">{escape_html(tags_str)}</span>
            </div>
          </div>'''
        cards_html.append(card_markup)

    all_cards_str = '\n'.join(cards_html)

    # 4. Filter Pills HTML: Me (default active), Moments, Tech, Reels (Strictly NO "All" filter)
    filter_pills_html = '''        <!-- Category Filter Pills (Folder-Wise: Me by default, Moments, Tech, Reels) -->
        <div class="gallery-filters-bar" role="tablist" aria-label="Gallery Categories">
          <button type="button" class="gallery-filter-pill active" data-folder-filter="me" role="tab" aria-selected="true">
            <i class="fa-solid fa-user"></i>
            <span>Me</span>
          </button>
          <button type="button" class="gallery-filter-pill" data-folder-filter="moments" role="tab" aria-selected="false">
            <i class="fa-solid fa-award"></i>
            <span>Moments</span>
          </button>
          <button type="button" class="gallery-filter-pill" data-folder-filter="tech" role="tab" aria-selected="false">
            <i class="fa-solid fa-microchip"></i>
            <span>Tech</span>
          </button>
          <button type="button" class="gallery-filter-pill" data-folder-filter="reel" role="tab" aria-selected="false">
            <i class="fa-solid fa-clapperboard"></i>
            <span>Reels</span>
          </button>
        </div>'''

    gallery_section_html = f'''      <!-- ==========================================================================
           PORTFOLIO GALLERY
           Clean Mobirise-Inspired Photo-First Grid with Dedicated Video Player & Lightbox
           Strict Zero Em-Dash / En-Dash Contract Verified
           ========================================================================== -->
      <article class="gallery" data-page="gallery" id="gallery">
        <header>
          <h2 class="h2 article-title">Gallery</h2>
        </header>

{filter_pills_html}

        <!-- Mobirise-Style Photo Grid -->
        <div class="gallery-media-grid" id="portfolioMediaGrid">
{all_cards_str}
        </div>

        <!-- Empty Filter State -->
        <div id="galleryEmptyState" class="gallery-empty-state" style="display: none;">
          <div class="empty-state-icon"><i class="fa-solid fa-shapes"></i></div>
          <h4>No moments found in this group</h4>
          <p>Pick a different category to view moments.</p>
          <button type="button" class="gallery-reset-filter-btn" id="galleryResetFilterBtn">
            <i class="fa-solid fa-rotate-left"></i>
            <span>Reset to Me</span>
          </button>
        </div>

        <!-- Next / Previous Page Navigation Controls (Arrow Icons & Dynamic Capsule Indicator) -->
        <div class="gallery-pagination-bar" id="galleryPaginationBar">
          <button type="button" class="gallery-page-arrow-btn" id="galleryPrevPageBtn" aria-label="Previous Page">
            <i class="fa-solid fa-chevron-left"></i>
          </button>
          <div class="gallery-page-indicator" id="galleryPageIndicator"></div>
          <div class="gallery-page-capsule" id="galleryPageCapsule">Me • Page 1 of 7</div>
          <button type="button" class="gallery-page-arrow-btn" id="galleryNextPageBtn" aria-label="Next Page">
            <i class="fa-solid fa-chevron-right"></i>
          </button>
        </div>

        <!-- Section Bottom Pagination Navigation -->
        <div class="section-bottom-pagination two-way">
          <button type="button" class="pagination-nav-btn prev-btn" onclick="navigateToPage('testimonials')">
            <span class="btn-sub"><i class="fa-solid fa-arrow-left"></i> Previous</span>
            <span class="btn-main">What People Are Saying</span>
          </button>
          <button type="button" class="pagination-nav-btn next-btn" onclick="navigateToPage('contact')">
            <span class="btn-sub">Next Section</span>
            <span class="btn-main">Get in Touch / Contact <i class="fa-solid fa-arrow-right"></i></span>
          </button>
        </div>
      </article>'''

    # Update index.html
    index_file = os.path.join(ROOT_DIR, 'index.html')
    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()

    gal_start = html.find('<article class="gallery"')
    next_art = html.find('<article class="moment-detail"')
    if gal_start != -1 and next_art != -1:
        c_pos = html.rfind('<!-- ==========================================================================\n           PORTFOLIO', 0, gal_start)
        replace_start = c_pos if c_pos != -1 else gal_start
        html = html[:replace_start] + gallery_section_html + '\n\n      ' + html[next_art:]
        print(f"Cleanly replaced <article class=\"gallery\"> with {len(cards_html)} cards.")
    else:
        print("Error: Could not locate gallery section in index.html!")
        return

    # Update mobile lightbox arrows and swipe hint text
    html = html.replace('fa-chevron-up', 'fa-chevron-left')
    html = html.replace('fa-chevron-down', 'fa-chevron-right')
    html = html.replace('Swipe Up for Next | Swipe Down for Previous', 'Swipe Left for Next | Swipe Right for Previous')

    # Strict Zero Em-Dash & En-Dash check
    assert '\u2014' not in html, 'Found em-dash in updated index.html'
    assert '\u2013' not in html, 'Found en-dash in updated index.html'

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Wrote updated index.html successfully!")

    # Mirror to out/index.html
    out_index_file = os.path.join(ROOT_DIR, 'out', 'index.html')
    if os.path.exists(out_index_file):
        with open(out_index_file, 'r', encoding='utf-8') as f:
            out_html = f.read()
        o_gal_start = out_html.find('<article class="gallery"')
        o_next_art = out_html.find('<article class="moment-detail"')
        if o_gal_start != -1 and o_next_art != -1:
            o_c_pos = out_html.rfind('<!-- ==========================================================================\n           PORTFOLIO', 0, o_gal_start)
            o_replace_start = o_c_pos if o_c_pos != -1 else o_gal_start
            out_html = out_html[:o_replace_start] + gallery_section_html + '\n\n      ' + out_html[o_next_art:]
            out_html = out_html.replace('fa-chevron-up', 'fa-chevron-left')
            out_html = out_html.replace('fa-chevron-down', 'fa-chevron-right')
            out_html = out_html.replace('Swipe Up for Next | Swipe Down for Previous', 'Swipe Left for Next | Swipe Right for Previous')
            with open(out_index_file, 'w', encoding='utf-8') as f:
                f.write(out_html)
            print("Wrote updated out/index.html successfully!")

    # Mirror gallery files to out/assets/img/gallery
    out_gallery_dir = os.path.join(ROOT_DIR, 'out', 'assets', 'img', 'gallery')
    if os.path.exists(out_gallery_dir):
        for fdr in FOLDERS:
            src_fdr = os.path.join(GALLERY_DIR, fdr)
            dst_fdr = os.path.join(out_gallery_dir, fdr)
            if os.path.exists(src_fdr):
                if os.path.exists(dst_fdr):
                    shutil.rmtree(dst_fdr)
                shutil.copytree(src_fdr, dst_fdr)
        # Remove old directories if they exist in out/assets/img/gallery
        for old_dir in ['portraits', 'tech-lab', 'hardware-iot', 'honors', 'videos']:
            old_p = os.path.join(out_gallery_dir, old_dir)
            if os.path.exists(old_p):
                shutil.rmtree(old_p)
        print("Synchronized out/assets/img/gallery successfully!")

    # Mirror js and data files
    out_data = os.path.join(ROOT_DIR, 'out', 'data', 'gallery-items.json')
    if os.path.exists(os.path.dirname(out_data)):
        shutil.copyfile(old_items_file, out_data)
    out_js = os.path.join(ROOT_DIR, 'out', 'js', 'gallery-data.js')
    if os.path.exists(os.path.dirname(out_js)):
        shutil.copyfile(os.path.join(ROOT_DIR, 'js', 'gallery-data.js'), out_js)
    print("Synchronized out/data and out/js successfully!")

if __name__ == '__main__':
    main()
