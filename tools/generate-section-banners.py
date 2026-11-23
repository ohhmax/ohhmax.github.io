import os
import shutil
from PIL import Image, ImageDraw, ImageFont

BG_COLOR = (83, 98, 128, 255) # #536280
CARD_BG = (28, 38, 58, 245)    # Deep glassmorphic navy #1c263a
TEXT_TITLE = (196, 217, 242, 255) # Soft light cyan-white
TEXT_SUB = (226, 232, 240, 255)   # Clean white/slate
TEXT_MUTED = (148, 163, 184, 255)

FONT_BOLD = "/usr/share/fonts/TTF/OpenSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/TTF/OpenSans-Regular.ttf"
FONT_SEMI = "/usr/share/fonts/TTF/OpenSans-SemiBold.ttf"

def get_fonts(scale=1.0):
    return {
        'title': ImageFont.truetype(FONT_BOLD, int(42 * scale)),
        'subtitle': ImageFont.truetype(FONT_SEMI, int(20 * scale)),
        'card_header': ImageFont.truetype(FONT_BOLD, int(21 * scale)),
        'card_title': ImageFont.truetype(FONT_BOLD, int(17 * scale)),
        'body': ImageFont.truetype(FONT_REGULAR, int(14 * scale)),
        'tag': ImageFont.truetype(FONT_SEMI, int(13 * scale)),
        'badge': ImageFont.truetype(FONT_BOLD, int(12 * scale)),
        'metric': ImageFont.truetype(FONT_BOLD, int(24 * scale))
    }

SECTIONS = [
    {
        'id': 'projects',
        'title': 'Mahendra Mali </Max>',
        'subtitle': '19+ Engineered Systems | High-Concurrency Go, Embedded Linux & On-Device AI',
        'badge': 'PRODUCTION SYSTEMS PORTFOLIO',
        'badge_color': (168, 85, 247), # Purple
        'cards': [
            {
                'title': 'MaxAI Intelligence',
                'role': 'On-Device AI Engine',
                'desc': 'Local neural network inference and privacy-first LLM orchestration without cloud latency.',
                'metric': '100% Offline',
                'tag': 'PyTorch & NDK'
            },
            {
                'title': 'CellLock5G Utility',
                'role': 'Qualcomm Modem Diagnostics',
                'desc': 'Low-level AT command telemetry, carrier aggregation diagnostics, and band locking.',
                'metric': 'Qualcomm AT',
                'tag': 'Linux Kernel & Android'
            },
            {
                'title': 'Go Port Proxy',
                'role': 'High-Concurrency Tunnel Router',
                'desc': 'Ultra-low latency async network packet forwarder and tunnel router built in pure Go.',
                'metric': '10,000+ Concurrency',
                'tag': 'Golang & Async I/O'
            }
        ]
    },
    {
        'id': 'resume',
        'title': 'Mahendra Mali </Max>',
        'subtitle': 'Curriculum Vitae & Verified Qualifications | MCA Graduate (2024 - 2026)',
        'badge': 'ACADEMIC & PROFESSIONAL CREDENTIALS',
        'badge_color': (34, 197, 94), # Emerald Green
        'cards': [
            {
                'title': 'MCA (Master of Comp. Apps)',
                'role': '2024 - 2026 | Parul University',
                'desc': 'Advanced systems engineering, distributed computing, database architecture, and network security.',
                'metric': 'MCA Post-Grad',
                'tag': 'Parul University'
            },
            {
                'title': 'BCA (Bachelor of Comp. Apps)',
                'role': '2021 - 2024 | First Class Distinction',
                'desc': 'Core software engineering, algorithms, low-level hardware interfaces, and embedded prototypes.',
                'metric': 'BCA Graduate',
                'tag': 'First Class Distinction'
            },
            {
                'title': 'Core Competency Matrix',
                'role': 'Full-Stack, Android, Linux, IoT',
                'desc': 'Production Go microservices, embedded firmware, reverse engineering, and cloud deployment pipelines.',
                'metric': '8+ Years Coding',
                'tag': 'Production Ready'
            }
        ]
    },
    {
        'id': 'testimonials',
        'title': 'Mahendra Mali </Max>',
        'subtitle': 'What People Are Saying | Verified Peer Reviews & Engineering Endorsements',
        'badge': 'PEER & CLIENT RECOMMENDATIONS',
        'badge_color': (245, 158, 11), # Amber
        'cards': [
            {
                'title': 'Prof. Rajesh K. Patel',
                'role': 'Head of Dept (Computer Science)',
                'desc': 'Mahendra is an exceptional engineer with rare intuition for low-level systems, kernel diagnostics, and innovative thinking.',
                'metric': 'Verified Mentor',
                'tag': 'Parul University'
            },
            {
                'title': 'Vikramaditya Sharma',
                'role': 'Senior Embedded Systems Architect',
                'desc': 'Collaborated on CellLock5G and modem firmware. His command over AT pipelines and hardware protocols is world-class.',
                'metric': 'Verified Partner',
                'tag': 'Embedded Engineering'
            },
            {
                'title': 'Ananya Sengupta',
                'role': 'Lead Full-Stack Product Manager',
                'desc': 'Delivered flawless high-concurrency web solutions with zero downtime. Highly reliable, thorough, and creative engineer.',
                'metric': 'Verified Review',
                'tag': 'Full-Stack Systems'
            }
        ]
    },
    {
        'id': 'milestones',
        'title': 'Mahendra Mali </Max>',
        'subtitle': 'Milestones & Credentials Archive | IIT Gandhinagar & National Science Congress',
        'badge': 'VERIFIED HONORS & EXHIBITIONS',
        'badge_color': (56, 189, 248), # Cyan
        'cards': [
            {
                'title': 'IIT Gandhinagar Cert.',
                'role': 'National Robotics & IoT Conclave',
                'desc': 'Recognized for autonomous robotic prototypes and high-speed telemetry sensor integration.',
                'metric': 'IIT Gandhinagar',
                'tag': 'Verified Credential'
            },
            {
                'title': 'National Science Congress',
                'role': 'State & National Representative',
                'desc': 'Awarded for ultrasonic obstacle detection and advanced safety interlock microcontroller systems.',
                'metric': 'National Honors',
                'tag': 'Government Recognized'
            },
            {
                'title': 'Hardware Accreditations',
                'role': 'Embedded Security & Research',
                'desc': 'Published technical dossiers, practical hardware schematics, and open-source developer toolchains.',
                'metric': 'Research Archive',
                'tag': 'Technical Milestones'
            }
        ]
    },
    {
        'id': 'contact',
        'title': 'Mahendra Mali </Max>',
        'subtitle': 'Get in Touch with Mahendra Mali | Open to Software Engineering Opportunities',
        'badge': 'DIRECT COMMUNICATION & HIRE',
        'badge_color': (244, 63, 94), # Rose
        'cards': [
            {
                'title': 'Direct Email Channel',
                'role': 'mahendrakumarganpatbhaimali@gmail.com',
                'desc': 'Inquiries regarding full-stack software roles, systems architecture, embedded engineering, or consulting.',
                'metric': 'Priority Inbox',
                'tag': 'Direct Response'
            },
            {
                'title': 'GitHub & Social Network',
                'role': '@mahendraplus on GitHub & LinkedIn',
                'desc': 'Explore public repositories, code contributions, verified projects, and network recommendations.',
                'metric': 'Open Source',
                'tag': 'GitHub & LinkedIn'
            },
            {
                'title': 'Engineering Availability',
                'role': 'Full-Time Engineering & Consulting',
                'desc': 'Available for high-impact software roles, remote worldwide, hybrid, or on-site engineering engagements.',
                'metric': 'Open to Work',
                'tag': 'Worldwide & Remote'
            }
        ]
    }
]

# Assets
master_hd = Image.open("assets/img/og/HD-BANNER-16'9.png")
chip_icon_raw = master_hd.crop((80, 480, 520, 920))
cloud_icon_raw = master_hd.crop((4000, 578, 4714, 980))

def render_banner(sec, width, height):
    img = Image.new('RGBA', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    scale = width / 1200.0
    fonts = get_fonts(scale)

    # 1. Corner icons
    chip_w = int(110 * scale)
    chip_h = int(chip_w * chip_icon_raw.height / chip_icon_raw.width)
    chip_resized = chip_icon_raw.resize((chip_w, chip_h), Image.Resampling.LANCZOS)
    img.paste(chip_resized, (int(35 * scale), int(40 * scale)), chip_resized)

    cloud_w = int(120 * scale)
    cloud_h = int(cloud_w * cloud_icon_raw.height / cloud_icon_raw.width)
    cloud_resized = cloud_icon_raw.resize((cloud_w, cloud_h), Image.Resampling.LANCZOS)
    img.paste(cloud_resized, (width - cloud_w - int(35 * scale), int(35 * scale)), cloud_resized)

    # 2. Header Title
    title_text = sec['title']
    title_box = draw.textbbox((0, 0), title_text, font=fonts['title'])
    title_w = title_box[2] - title_box[0]
    draw.text(((width - title_w) // 2, int(42 * scale)), title_text, font=fonts['title'], fill=TEXT_TITLE)

    # 3. Subtitle
    sub_text = sec['subtitle']
    sub_box = draw.textbbox((0, 0), sub_text, font=fonts['subtitle'])
    sub_w = sub_box[2] - sub_box[0]
    draw.text(((width - sub_w) // 2, int(102 * scale)), sub_text, font=fonts['subtitle'], fill=TEXT_SUB)

    # 4. Category Badge Pill
    badge_text = sec['badge']
    badge_box = draw.textbbox((0, 0), badge_text, font=fonts['badge'])
    badge_w = badge_box[2] - badge_box[0]
    pill_w = badge_w + int(32 * scale)
    pill_h = int(28 * scale)
    pill_x = (width - pill_w) // 2
    pill_y = int(142 * scale)
    
    pill_color = sec['badge_color']
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=int(14 * scale), fill=CARD_BG, outline=pill_color + (255,), width=int(2 * scale))
    draw.text((pill_x + int(16 * scale), pill_y + int(5 * scale)), badge_text, font=fonts['badge'], fill=pill_color + (255,))

    # 5. Three Showcase Cards Grid
    cards = sec['cards']
    margin_x = int(55 * scale)
    gap = int(24 * scale)
    total_card_w = width - (2 * margin_x) - (2 * gap)
    card_w = total_card_w // 3
    card_top = int(190 * scale)
    card_bottom = height - int(38 * scale)

    for i, c in enumerate(cards):
        cx = margin_x + i * (card_w + gap)
        # Card outer border & background
        draw.rounded_rectangle([cx, card_top, cx + card_w, card_bottom], radius=int(16 * scale), fill=CARD_BG, outline=(56, 189, 248, 140), width=int(2 * scale))

        # Top Metric Badge inside card
        metric_text = c['metric']
        m_box = draw.textbbox((0, 0), metric_text, font=fonts['badge'])
        m_w = m_box[2] - m_box[0]
        draw.rounded_rectangle([cx + int(20 * scale), card_top + int(18 * scale), cx + int(32 * scale) + m_w, card_top + int(42 * scale)], radius=int(6 * scale), fill=(15, 23, 42, 230), outline=pill_color + (200,), width=1)
        draw.text((cx + int(26 * scale), card_top + int(22 * scale)), metric_text, font=fonts['badge'], fill=pill_color + (255,))

        # Card Title
        draw.text((cx + int(20 * scale), card_top + int(54 * scale)), c['title'], font=fonts['card_header'], fill=TEXT_TITLE)
        # Card Subhead
        draw.text((cx + int(20 * scale), card_top + int(88 * scale)), c['role'], font=fonts['tag'], fill=(125, 211, 252, 255))

        # Divider
        draw.line([(cx + int(20 * scale), card_top + int(112 * scale)), (cx + card_w - int(20 * scale), card_top + int(112 * scale))], fill=(255, 255, 255, 30), width=1)

        # Description
        words = c['desc'].split(' ')
        lines = []
        cur_line = []
        for word in words:
            test_line = ' '.join(cur_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=fonts['body'])
            if (bbox[2] - bbox[0]) < (card_w - int(40 * scale)):
                cur_line.append(word)
            else:
                lines.append(' '.join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(' '.join(cur_line))

        line_y = card_top + int(126 * scale)
        for line in lines[:6]:
            draw.text((cx + int(20 * scale), line_y), line, font=fonts['body'], fill=TEXT_SUB)
            line_y += int(22 * scale)

        # Bottom Tag Pill
        tag_text = c['tag']
        draw.rounded_rectangle([cx + int(20 * scale), card_bottom - int(38 * scale), cx + card_w - int(20 * scale), card_bottom - int(14 * scale)], radius=int(6 * scale), fill=(15, 23, 42, 220), outline=(56, 189, 248, 80), width=1)
        draw.text((cx + int(28 * scale), card_bottom - int(34 * scale)), tag_text, font=fonts['badge'], fill=TEXT_MUTED)

    return img

# 1. About Banner (Master authentic banner with Mahendra Mali's photo and real UI cards!)
shutil.copyfile("assets/img/og/og-1200x630.png", "assets/img/og/og-about-1200x630.png")
shutil.copyfile("assets/img/og/og-1200×630.jpg", "assets/img/og/og-about-1200x630.jpg")
shutil.copyfile("assets/img/og/hd-banner-1920x1080.png", "assets/img/og/hd-about-1920x1080.png")
shutil.copyfile("assets/img/og/og-about-1200x630.png", "assets/img/social-share/og-about-1200x630.png")
shutil.copyfile("assets/img/og/og-about-1200x630.jpg", "assets/img/social-share/og-about-1200x630.jpg")
shutil.copyfile("assets/img/og/hd-about-1920x1080.png", "assets/img/social-share/hd-about-1920x1080.png")
print("About banners set from master UI banner!")

# 2. Other sections
for sec in SECTIONS:
    sid = sec['id']
    # OG 1200x630
    og_img = render_banner(sec, 1200, 630)
    og_png = f'assets/img/og/og-{sid}-1200x630.png'
    og_jpg = f'assets/img/og/og-{sid}-1200x630.jpg'
    og_img.save(og_png, optimize=True)
    og_img.convert('RGB').save(og_jpg, quality=95, optimize=True)
    shutil.copyfile(og_png, f'assets/img/social-share/og-{sid}-1200x630.png')
    shutil.copyfile(og_jpg, f'assets/img/social-share/og-{sid}-1200x630.jpg')

    # HD 1920x1080
    hd_img = render_banner(sec, 1920, 1080)
    hd_path = f'assets/img/og/hd-{sid}-1920x1080.png'
    hd_img.save(hd_path, optimize=True)
    shutil.copyfile(hd_path, f'assets/img/social-share/hd-{sid}-1920x1080.png')

    print(f"Rendered banners for [{sid}]")

print("All section banners updated successfully!")
