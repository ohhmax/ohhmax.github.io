"""
tools/reorganize_gallery_media.py
Removes the 12 deleted gallery photos from metadata.
Renames all 130 remaining photos and videos with self-describing metadata:
  <year>_<title-slug>.<ext>
Ensures easy addition/removal of media in the future.
Updates data/gallery-items.json and assets/js/gallery-data.js.
Strict Zero Em-Dash / En-Dash Contract Verified.
"""

import os
import json
import re
import shutil

def slugify(text):
    text = text.lower()
    text = re.sub(r'[\'\"]', '', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def extract_year(date_str):
    m = re.search(r'20\d\d', str(date_str or ''))
    return m.group(0) if m else '2024'

LABEL_MAP = {
    'videos': 'Reels & Demos',
    'honors': 'Honors & Fairs',
    'hardware-iot': 'Hardware & IoT',
    'tech-lab': 'Tech Lab',
    'fitness': 'Fitness',
    'portraits': 'Portraits & Life'
}

def main():
    with open('data/gallery-items.json', 'r', encoding='utf-8') as f:
        items = json.load(f)

    print('Initial items in json:', len(items))

    # Identify existing and deleted items
    existing_items = []
    deleted_items = []

    for it in items:
        if os.path.exists(it['src']):
            existing_items.append(it)
        else:
            deleted_items.append(it)

    print(f'Existing items on disk: {len(existing_items)}, Deleted items: {len(deleted_items)}')

    # Clean up orphan thumbnails of deleted items
    for it in deleted_items:
        th = it.get('thumb')
        if th and os.path.exists(th):
            os.remove(th)
            print('Removed orphan thumb for deleted item:', th)

    # Process and rename remaining 130 items with year prefix
    seen_paths = set()
    updated_items = []

    for idx, it in enumerate(existing_items):
        group = it.get('group', 'portraits')
        folder_label = LABEL_MAP.get(group, 'Media Vault')
        is_video = (it.get('type') == 'video')
        ext = '.mp4' if is_video else '.jpg'

        year = extract_year(it.get('date', ''))
        title_slug = slugify(it['title'])

        new_filename = f'{year}_{title_slug}{ext}'
        
        # Ensure uniqueness
        base_slug = f'{year}_{title_slug}'
        counter = 2
        while f'{group}/{new_filename}' in seen_paths:
            new_filename = f'{base_slug}-{counter}{ext}'
            counter += 1
        seen_paths.add(f'{group}/{new_filename}')

        new_src = f'assets/img/gallery/{group}/{new_filename}'
        new_thumb_fn = f'thumb_{new_filename.replace(ext, ".webp")}'
        new_thumb = f'assets/img/gallery/{group}/thumbs/{new_thumb_fn}'

        old_src = it['src']
        old_thumb = it.get('thumb', '')

        # Rename source file if different
        if old_src != new_src and os.path.exists(old_src):
            os.rename(old_src, new_src)

        # Rename thumbnail if different
        if old_thumb and old_thumb != new_thumb and os.path.exists(old_thumb):
            os.rename(old_thumb, new_thumb)

        alt_text = f"{it['title']} ({year}) | {folder_label} - Mahendra Mali (Max) Portfolio"

        new_item = dict(it)
        new_item['src'] = new_src
        new_item['thumb'] = new_thumb
        new_item['filename'] = new_filename
        new_item['year'] = year
        new_item['alt'] = alt_text
        updated_items.append(new_item)

    print(f'Processed and renamed {len(updated_items)} items successfully!')

    # Save updated data/gallery-items.json
    with open('data/gallery-items.json', 'w', encoding='utf-8') as f:
        json.dump(updated_items, f, indent=2, ensure_ascii=False)
    print('Saved updated data/gallery-items.json')

    # Save assets/js/gallery-data.js
    gallery_data_js = f'''/**
 * assets/js/gallery-data.js
 * MaxPortfolio - Dedicated Gallery and Visual Archive Data
 * Self-describing naming convention: <year>_<title-slug>.<ext>
 * Groupwise Organized Media Vault (videos, honors, hardware-iot, tech-lab, fitness, portraits)
 * Strict Zero Em-Dash / En-Dash Contract Verified.
 */

window.MAX_GALLERY_DATA = {json.dumps(updated_items, indent=2, ensure_ascii=False)};
'''
    assert '\u2014' not in gallery_data_js, 'Found em-dash'
    assert '\u2013' not in gallery_data_js, 'Found en-dash'

    with open('assets/js/gallery-data.js', 'w', encoding='utf-8') as f:
        f.write(gallery_data_js)
    print('Saved updated assets/js/gallery-data.js')

if __name__ == '__main__':
    main()
