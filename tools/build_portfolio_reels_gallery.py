"""
tools/build_portfolio_reels_gallery.py
Builds the clean, photo-first Mobirise-inspired Gallery for index.html.
Features:
- Pure photo/video grid with 1:1 square aspect ratio (no text clutter on cards)
- 4 Primary Domain Groups (+ All): Hardware & IoT, Tech Lab, Honors & Awards, Life & Portraits
- Clean unnumbered search toolbar (photo numbers removed)
- Next / Previous Arrow Pagination with smooth enter/exit animations
- Center focus icon on hover & subtle bottom title overlay
- All descriptions, tags, year, Schema.org microdata embedded but hidden for SEO
- Separate Photo Lightbox with swipe, keyboard, and edge arrows
- Separate Video Player with instant thumbnail poster, loading spinner, and sound on
- Standalone top-level section header: 'Gallery'
Strict Zero Em-Dash & En-Dash Contract Verified.
"""

import json
import re
import xml.sax.saxutils as saxutils

def escape_html(s):
    return saxutils.escape(str(s or ''))

def main():
    with open('data/gallery-items.json', 'r', encoding='utf-8') as f:
        items = json.load(f)

    # Sort items chronologically descending (Latest to Oldest)
    def sort_key(item):
        m = re.search(r'20\d\d', item.get('date', ''))
        yr = int(m.group(0)) if m else 2021
        return (yr, item.get('category', ''), item.get('title', ''))

    items_sorted = sorted(items, key=sort_key, reverse=True)

    cards_html = []
    for idx, it in enumerate(items_sorted):
        item_id = it.get('id', f'gallery-item-{idx}')
        code = it.get('code', f'MAX-{idx+1:03d}')
        title = it.get('title', 'Engineering Moment')
        desc = it.get('desc', '')
        cat = it.get('category', 'portraits')
        subcat = it.get('subcat', '')
        item_type = it.get('type', 'image')
        src = it.get('src', '')
        thumb = it.get('thumb', src)
        date_str = it.get('date', '2024')
        loc = it.get('location', 'Gujarat, India')
        tags = it.get('tags', [])
        tags_str = ' '.join(f'#{t}' for t in tags[:5])
        orig_group = it.get('group', '')

        # Map into exactly 4 primary domain groups
        if cat == 'innovations' or orig_group == 'hardware-iot' or 'hardware' in orig_group:
            unified_group = 'hardware'
            folder_label = 'Hardware & IoT'
        elif cat in ('workspace', 'milestones') or orig_group == 'tech-lab' or 'lab' in orig_group:
            unified_group = 'tech-lab'
            folder_label = 'Tech Lab'
        elif cat == 'honors' or orig_group == 'honors':
            unified_group = 'honors'
            folder_label = 'Honors & Awards'
        else:
            unified_group = 'life'
            folder_label = 'Life & Portraits'

        alt_text = it.get('alt', f"{title} | {folder_label} - Mahendra Mali (Max) Portfolio")

        # Distinct click action: photos and videos both open unified full-screen lightbox
        click_action = f"openGalleryMedia({idx})"
        if item_type == 'video':
            media_badge = '<span class="gallery-card-badge video-badge" title="Video"><i class="fa-solid fa-play"></i></span>'
        else:
            media_badge = ''

        card_markup = f'''          <div class="portfolio-media-card" 
                   id="{escape_html(item_id)}" 
                   itemscope itemtype="https://schema.org/ImageObject"
                   data-index="{idx}"
                   data-code="{escape_html(code)}" 
                   data-category="{escape_html(cat)}" 
                   data-group="{escape_html(unified_group)}" 
                   data-subcat="{escape_html(subcat)}" 
                   data-type="{escape_html(item_type)}" 
                   data-year="{escape_html(date_str)}" 
                   data-src="{escape_html(src)}" 
                   data-thumb="{escape_html(thumb)}" 
                   data-title="{escape_html(title)}" 
                   data-desc="{escape_html(desc)}" 
                   data-folder="{escape_html(folder_label)}"
                   data-tags="{escape_html(tags_str)}" 
                   data-location="{escape_html(loc)}" 
                   onclick="{click_action}">
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

    # Clean Mobirise-Style Gallery Section Markup (Portfolio Theme)
    gallery_section_html = f'''      <!-- ==========================================================================
           PORTFOLIO GALLERY
           Clean Mobirise-Inspired Photo-First Grid with Dedicated Video Player & Lightbox
           Strict Zero Em-Dash / En-Dash Contract Verified
           ========================================================================== -->
      <article class="gallery" data-page="gallery" id="gallery">
        <header>
          <h2 class="h2 article-title">Gallery</h2>
        </header>

        <!-- Category Filter Pills (Mobirise-Inspired, 4 Engineering & Life Groups + All) -->
        <div class="gallery-filters-bar" role="tablist" aria-label="Gallery Categories">
          <button type="button" class="gallery-filter-pill active" data-folder-filter="all" role="tab">
            <i class="fa-solid fa-shapes"></i>
            <span>All</span>
          </button>
          <button type="button" class="gallery-filter-pill" data-folder-filter="hardware" role="tab">
            <i class="fa-solid fa-microchip"></i>
            <span>Hardware &amp; IoT</span>
          </button>
          <button type="button" class="gallery-filter-pill" data-folder-filter="tech-lab" role="tab">
            <i class="fa-solid fa-terminal"></i>
            <span>Tech Lab</span>
          </button>
          <button type="button" class="gallery-filter-pill" data-folder-filter="honors" role="tab">
            <i class="fa-solid fa-trophy"></i>
            <span>Honors &amp; Awards</span>
          </button>
          <button type="button" class="gallery-filter-pill" data-folder-filter="life" role="tab">
            <i class="fa-solid fa-camera"></i>
            <span>Life &amp; Portraits</span>
          </button>
        </div>

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
            <span>View All</span>
          </button>
        </div>

        <!-- Next / Previous Page Navigation Controls (Arrow Icons & Dynamic Capsule Indicator) -->
        <div class="gallery-pagination-bar" id="galleryPaginationBar">
          <button type="button" class="gallery-page-arrow-btn" id="galleryPrevPageBtn" aria-label="Previous Page">
            <i class="fa-solid fa-chevron-left"></i>
          </button>
          <div class="gallery-page-indicator" id="galleryPageIndicator"></div>
          <div class="gallery-page-capsule" id="galleryPageCapsule">Page 1 of 16</div>
          <button type="button" class="gallery-page-arrow-btn" id="galleryNextPageBtn" aria-label="Next Page">
            <i class="fa-solid fa-chevron-right"></i>
          </button>
        </div>
      </article>'''

    # Full-Screen Immersive Media Lightbox (Photos & Videos with Direct Overlay Controls, Zero Captions)
    photo_lightbox_html = '''  <!-- Full-Screen Immersive Media Lightbox (Photos & Videos, Zero Captions) -->
  <div id="photoFullscreenLightbox" class="fullscreen-photo-lightbox" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Full-Screen Media View">
    <div class="lightbox-backdrop" id="photoLightboxBackdrop" onclick="closeGalleryModals(true)"></div>
    <div class="lightbox-dialog">
      <!-- Direct Overlaid Floating Controls -->
      <button type="button" class="lightbox-overlay-btn btn-close" id="photoLightboxCloseBtn" onclick="closeGalleryModals(true)" aria-label="Close">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <!-- Desktop Capsule Navigation: Top-Left Previous, Bottom-Right Next -->
      <button type="button" class="lightbox-capsule-btn desktop-capsule-prev capsule-prev desktop-only-btn" id="photoLightboxPrevBtn" onclick="navigateGalleryMedia(-1)" aria-label="Previous Media">
        <i class="fa-solid fa-chevron-left"></i>
        <span>Previous</span>
      </button>
      <button type="button" class="lightbox-capsule-btn desktop-capsule-next capsule-next desktop-only-btn" id="photoLightboxNextBtn" onclick="navigateGalleryMedia(1)" aria-label="Next Media">
        <span>Next</span>
        <i class="fa-solid fa-chevron-right"></i>
      </button>

      <!-- Mobile Capsule Controls: Top-Left Previous, Bottom-Right Next (Animated Borders) -->
      <button type="button" class="lightbox-capsule-btn mobile-capsule-prev capsule-prev" id="photoLightboxMobilePrevBtn" onclick="navigateGalleryMedia(-1)" aria-label="Previous Media">
        <i class="fa-solid fa-chevron-up"></i>
        <span>Previous</span>
      </button>
      <button type="button" class="lightbox-capsule-btn mobile-capsule-next capsule-next" id="photoLightboxMobileNextBtn" onclick="navigateGalleryMedia(1)" aria-label="Next Media">
        <span>Next</span>
        <i class="fa-solid fa-chevron-down"></i>
      </button>

      <!-- First-Time Swipe Gesture Animated Hint (Auto-fades on swipe or timeout) -->
      <div class="lightbox-swipe-hint" id="lightboxSwipeHint" aria-hidden="true" style="display: none;">
        <div class="swipe-hint-icon-box">
          <i class="fa-solid fa-arrows-up-down"></i>
        </div>
        <div class="swipe-hint-text-wrap">
          <span class="swipe-hint-title">Swipe to Navigate</span>
          <span class="swipe-hint-sub">Swipe Up for Next | Swipe Down for Previous</span>
        </div>
      </div>

      <!-- Full-Screen Media Stage (Zero Captions, Zero Descriptions) -->
      <div class="lightbox-media-wrap" id="photoLightboxImageWrap">
        <img id="photoLightboxImg" src="" alt="Full-Screen Image" class="lightbox-fullscreen-media">
        
        <!-- Video Stage with Top-Right Monospace Countdown Timer -->
        <div class="lightbox-video-stage" id="galleryVideoStage" style="display: none;">
          <video id="galleryVideoPlayer" 
                 class="lightbox-fullscreen-media" 
                 playsinline 
                 preload="auto" 
                 loop></video>
          <div class="video-countdown-scrim" id="galleryVideoCountdown" aria-label="Remaining Video Time">00:00</div>
        </div>
      </div>

      <!-- Cyber Loading Spinner -->
      <div class="lightbox-loading-spinner" id="galleryMediaSpinner" style="display: none;">
        <div class="spinner-ring"></div>
      </div>
    </div>
  </div>'''

    video_modal_html = '''  <!-- Secondary Video Modal Hook (Preserves DOM ID Compatibility) -->
  <div id="galleryVideoModal" class="gallery-video-modal" aria-hidden="true" style="display: none;"></div>'''

    # Read index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Exact boundary replacement for <article class="gallery">
    gal_start = html.find('<article class="gallery"')
    next_art = html.find('<article class="moment-detail"')
    if gal_start != -1 and next_art != -1:
        comment_header = '<!-- ==========================================================================\n           PORTFOLIO'
        c_pos = html.rfind(comment_header, 0, gal_start)
        replace_start = c_pos if c_pos != -1 else gal_start
        html = html[:replace_start] + gallery_section_html + '\n\n      ' + html[next_art:]
        print(f'Cleanly replaced <article class="gallery"> with exactly {len(cards_html)} cards.')
    else:
        print('Error: Could not locate gallery section boundaries!')

    # Exact boundary replacement for #photoFullscreenLightbox and modals
    lb_start = html.find('<div id="photoFullscreenLightbox"')
    if lb_start == -1:
        lb_start = html.find('<!-- High-Resolution Full-Screen Photo Lightbox')
    
    dock_boundary = html.find('UNIFIED MAXHIVE BOTTOM NAVIGATION DOCK')
    if lb_start != -1 and dock_boundary != -1:
        c_dock = html.rfind('<!-- ===', lb_start, dock_boundary)
        replace_modals_end = c_dock if c_dock != -1 else dock_boundary
        combined_modals = photo_lightbox_html + '\n\n' + video_modal_html
        html = html[:lb_start] + combined_modals + '\n\n  ' + html[replace_modals_end:]
        print('Cleanly replaced gallery modals with Lightbox & Video Player.')
    else:
        print('Error: Could not locate modals boundaries!')

    # Update drawer link text
    html = re.sub(
        r'<button type="button" class="maxhive-grid-menu-card item-purple" data-drawer-navigate="gallery">[\s\S]*?<\/button>',
        '''<button type="button" class="maxhive-grid-menu-card item-purple" data-drawer-navigate="gallery">
          <div class="grid-card-icon"><i class="fa-solid fa-photo-film"></i></div>
          <div class="grid-card-text">
            <strong>Gallery</strong>
            <small>Photos &amp; Videos</small>
          </div>
        </button>''',
        html
    )

    # Strict Zero Em-Dash & En-Dash check
    assert '\u2014' not in html, 'Found em-dash in updated index.html'
    assert '\u2013' not in html, 'Found en-dash in updated index.html'

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('index.html updated successfully with clean 4-group gallery and arrow pagination!')

if __name__ == '__main__':
    main()
