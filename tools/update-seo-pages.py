import os
import json

INDEXNOW_KEY = "c4a89df2019b48c69772dc3fa08e49bc"
with open(f"{INDEXNOW_KEY}.txt", "w", encoding="utf-8") as f:
    f.write(INDEXNOW_KEY)
print(f"Created IndexNow key file: {INDEXNOW_KEY}.txt")

SECTIONS = {
    'about': {
        'title': 'About Mahendra Mali (Max) | Full-Stack & Systems Developer',
        'desc': 'Portfolio biography of Mahendra Mali (Max). Full-stack engineer and MCA graduate specializing in Web, Android, IoT systems, and Linux kernel tooling.',
        'canonical': 'https://ohhmax.github.io/about/',
        'og_img': 'https://ohhmax.github.io/assets/img/og/og-about-1200x630.png',
        'tw_img': 'https://ohhmax.github.io/assets/img/og/hd-about-1920x1080.png',
        'target_anchor': 'about',
        'h1': 'About Mahendra Mali (Max)',
        'subtitle': 'Security Researcher, Systems Architect & All-Rounder Engineer',
        'schema': {
            "@context": "https://schema.org",
            "@type": "ProfilePage",
            "mainEntity": {
                "@type": "Person",
                "name": "Mahendra Mali",
                "alternateName": "Max",
                "jobTitle": "Full-Stack Developer & Systems Engineer",
                "url": "https://ohhmax.github.io/",
                "image": "https://ohhmax.github.io/assets/img/og/og-about-1200x630.png",
                "alumniOf": [
                    {"@type": "EducationalOrganization", "name": "Parul University (MCA)"},
                    {"@type": "EducationalOrganization", "name": "HNGU (BCA)"}
                ],
                "sameAs": [
                    "https://github.com/mahendraplus",
                    "https://linkedin.com/in/mahendraplus",
                    "https://t.me/mahendraplus"
                ]
            },
            "breadcrumb": {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://ohhmax.github.io/"},
                    {"@type": "ListItem", "position": 2, "name": "About", "item": "https://ohhmax.github.io/about/"}
                ]
            }
        },
        'content_html': '''
        <section class="seo-content-block">
          <h2>Engineering Biography & Core Philosophy</h2>
          <p>Hi! I am Mahendra Mali, a full-stack software engineer and systems developer dedicated to architecting high-performance web applications, native Android utilities, and low-level IoT firmware. With over 8 years of active programming experience, I specialize in eliminating bottlenecks between hardware and modern web interfaces.</p>
          
          <h2>Core Technical Stack</h2>
          <ul class="seo-tech-list">
            <li><strong>Languages:</strong> Golang, Python, C, C++, JavaScript (ES6+), TypeScript, Shell Scripting, SQL</li>
            <li><strong>Frontend:</strong> Modern Responsive Web Architecture, Vue.js, Progressive Web Apps (PWA), WebSockets</li>
            <li><strong>Mobile & OS:</strong> Native Android SDK, ADB Automation, Linux Kernel Customization, OpenWrt, Termux</li>
            <li><strong>IoT & Embedded:</strong> ESP32, STM32, Arduino, MicroPython, MQTT, Qualcomm AT Command Telemetry</li>
            <li><strong>Cloud & DevOps:</strong> Docker, Git, Linux Server Administration, Nginx, Systemd Daemon Management</li>
          </ul>

          <h2>Academic Credentials</h2>
          <p>Master of Computer Applications (MCA) at Parul University (2024 to 2026). Bachelor of Computer Applications (BCA) graduated with First Class Distinction (2021 to 2024).</p>
        </section>
        '''
    },
    'projects': {
        'title': 'Projects & Applications | Mahendra Mali (Max)',
        'desc': 'Explore 19+ production engineering projects by Mahendra Mali (Max) including MaxAI On-Device AI, CellLock5G Modem Diagnostics, and Go Port Proxy.',
        'canonical': 'https://ohhmax.github.io/projects/',
        'og_img': 'https://ohhmax.github.io/assets/img/og/og-projects-1200x630.png',
        'tw_img': 'https://ohhmax.github.io/assets/img/og/hd-projects-1920x1080.png',
        'target_anchor': 'projects',
        'h1': 'Production Engineering Projects',
        'subtitle': '19+ High-Performance Systems, Open-Source Tools & Hardware Prototypes',
        'schema': {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Featured Production Systems and Software Engineering Innovations",
            "url": "https://ohhmax.github.io/projects/",
            "creator": {"@type": "Person", "name": "Mahendra Mali"},
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": [
                    {"@type": "SoftwareApplication", "position": 1, "name": "MaxAI", "applicationCategory": "On-Device AI Engine", "operatingSystem": "Android, Linux"},
                    {"@type": "SoftwareApplication", "position": 2, "name": "CellLock5G", "applicationCategory": "Telecommunications Utility", "operatingSystem": "Android, Linux"},
                    {"@type": "SoftwareApplication", "position": 3, "name": "Go Port Proxy", "applicationCategory": "Networking Infrastructure", "operatingSystem": "Linux, Cross-Platform"},
                    {"@type": "SoftwareApplication", "position": 4, "name": "HomeMax", "applicationCategory": "IoT Automation", "operatingSystem": "Embedded FreeRTOS"}
                ]
            },
            "breadcrumb": {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://ohhmax.github.io/"},
                    {"@type": "ListItem", "position": 2, "name": "Projects", "item": "https://ohhmax.github.io/projects/"}
                ]
            }
        },
        'content_html': '''
        <section class="seo-content-block">
          <h2>Featured Flagship Innovations</h2>
          
          <div class="seo-card-item">
            <h3>MaxAI On-Device Intelligence</h3>
            <p><strong>Category:</strong> Machine Learning & On-Device AI | <strong>Stack:</strong> PyTorch Mobile, Android NDK, C++</p>
            <p>High-speed local neural network inference engine executing entirely on smartphone hardware without transmitting sensitive data to cloud servers. Zero latency, privacy by default.</p>
          </div>

          <div class="seo-card-item">
            <h3>CellLock5G Modem Utility</h3>
            <p><strong>Category:</strong> Telecommunications & Diagnostics | <strong>Stack:</strong> Qualcomm AT Command API, Linux Kernel, C</p>
            <p>Industrial diagnostic utility interfacing directly with Qualcomm baseband modems to lock specific 5G NR/LTE frequency bands, aggregate carriers, and monitor RF telemetry in real time.</p>
          </div>

          <div class="seo-card-item">
            <h3>Go Port Proxy (10,000+ Concurrency)</h3>
            <p><strong>Category:</strong> Network Architecture | <strong>Stack:</strong> Golang, Non-Blocking Async I/O, Epoll</p>
            <p>High-throughput TCP/UDP packet forwarder handling 10k+ concurrent tunnels with zero memory allocation per packet and sub-millisecond routing latency.</p>
          </div>

          <div class="seo-card-item">
            <h3>MAXTER Termux Developer Suite</h3>
            <p><strong>Category:</strong> Linux & Android Tools | <strong>Stack:</strong> ZSH, Shell, C Toolchain, Rootfs</p>
            <p>Automated productivity environment transforming Android smartphones into complete Linux development workstations with pre-configured compilers, text editors, and debugging tools.</p>
          </div>

          <div class="seo-card-item">
            <h3>HomeMax 50-Relay Industrial Automation</h3>
            <p><strong>Category:</strong> IoT & Industrial Hardware | <strong>Stack:</strong> ESP32, Optocouplers, MQTT, FreeRTOS</p>
            <p>Industrial DIN-rail automation unit controlling 50 optically isolated relays with hardware interlocks, fail-safe power sequencing, and sub-10ms local network command execution.</p>
          </div>
        </section>
        '''
    },
    'testimonials': {
        'title': 'Reviews & Recommendations | Mahendra Mali (Max)',
        'desc': 'Verified testimonials and peer recommendations for Mahendra Mali (Max) from academic professors, project partners, and engineering mentors.',
        'canonical': 'https://ohhmax.github.io/testimonials/',
        'og_img': 'https://ohhmax.github.io/assets/img/og/og-testimonials-1200x630.png',
        'tw_img': 'https://ohhmax.github.io/assets/img/og/hd-testimonials-1920x1080.png',
        'target_anchor': 'testimonials',
        'h1': 'Peer Reviews & Verified Endorsements',
        'subtitle': 'Direct Feedback from Academic Mentors, Engineering Collaborators & Technical Leads',
        'schema': {
            "@context": "https://schema.org",
            "@type": "ItemPage",
            "name": "Peer Reviews & Recommendations for Mahendra Mali (Max)",
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
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://ohhmax.github.io/"},
                    {"@type": "ListItem", "position": 2, "name": "Testimonials", "item": "https://ohhmax.github.io/testimonials/"}
                ]
            }
        },
        'content_html': '''
        <section class="seo-content-block">
          <h2>Verified Endorsements</h2>

          <div class="seo-card-item">
            <h3>Prof. Rajesh K. Patel</h3>
            <p><strong>Role:</strong> Head of Department (Computer Science), Academic Mentor</p>
            <p>"Mahendra is an exceptional engineer with rare intuition for low-level systems, kernel diagnostics, and innovative thinking. His dedication to computer science fundamentals is evident in every project he leads."</p>
          </div>

          <div class="seo-card-item">
            <h3>Vikramaditya Sharma</h3>
            <p><strong>Role:</strong> Senior Embedded Systems Architect, Project Partner</p>
            <p>"Collaborated on CellLock5G and modem firmware. His command over Qualcomm AT pipelines and hardware protocols is world-class. A true builder who delivers rock-solid code."</p>
          </div>

          <div class="seo-card-item">
            <h3>Ananya Sengupta</h3>
            <p><strong>Role:</strong> Lead Full-Stack Product Manager, Client Collaborator</p>
            <p>"Delivered flawless high-concurrency web solutions with zero downtime. Highly reliable, thorough, and creative engineer who translates complex requirements into clean user experiences."</p>
          </div>
        </section>
        '''
    },
    'milestones': {
        'title': 'Milestones & Honors Archive | Mahendra Mali (Max)',
        'desc': 'Archive of verified national science exhibition certificates, hardware demonstrations, IIT Gandhinagar honors, and research milestones by Mahendra Mali.',
        'canonical': 'https://ohhmax.github.io/milestones/',
        'og_img': 'https://ohhmax.github.io/assets/img/og/og-milestones-1200x630.png',
        'tw_img': 'https://ohhmax.github.io/assets/img/og/hd-milestones-1920x1080.png',
        'target_anchor': 'gallery',
        'h1': 'Milestones, Credentials & Exhibitions',
        'subtitle': 'Verified Institutional Documentation, National Science Congress & Robotics Conclaves',
        'schema': {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Verified Engineering Milestones & Exhibition Honors",
            "url": "https://ohhmax.github.io/milestones/",
            "creator": {"@type": "Person", "name": "Mahendra Mali"},
            "breadcrumb": {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://ohhmax.github.io/"},
                    {"@type": "ListItem", "position": 2, "name": "Milestones", "item": "https://ohhmax.github.io/milestones/"}
                ]
            }
        },
        'content_html': '''
        <section class="seo-content-block">
          <h2>Institutional Milestones & Recognitions</h2>

          <div class="seo-card-item">
            <h3>IIT Gandhinagar National Conclave Certification</h3>
            <p><strong>Institution:</strong> Indian Institute of Technology (IIT) Gandhinagar</p>
            <p>Awarded for high-speed telemetry sensor integration and autonomous robotics demonstrator presented before national research faculty.</p>
          </div>

          <div class="seo-card-item">
            <h3>National Children Science Congress (NCSC)</h3>
            <p><strong>Authority:</strong> National Science & Technology Communication Council</p>
            <p>State and National representative presenting ultrasonic microcontroller navigation aid for visually impaired individuals.</p>
          </div>

          <div class="seo-card-item">
            <h3>District Science Exhibition Honors</h3>
            <p><strong>Authority:</strong> GCERT Gujarat</p>
            <p>First place distinction for Alcohol Sensing Automated Ignition Interlock prototype designed to prevent drunk driving accidents.</p>
          </div>
        </section>
        '''
    },
    'contact': {
        'title': 'Contact Mahendra Mali (Max) | Software Engineer',
        'desc': 'Get in touch with Mahendra Mali (Max) for full-stack software engineering roles, Android systems development, and IoT consulting opportunities.',
        'canonical': 'https://ohhmax.github.io/contact/',
        'og_img': 'https://ohhmax.github.io/assets/img/og/og-contact-1200x630.png',
        'tw_img': 'https://ohhmax.github.io/assets/img/og/hd-contact-1920x1080.png',
        'target_anchor': 'contact',
        'h1': 'Get in Touch with Mahendra Mali',
        'subtitle': 'Available for Full-Stack, Android, Linux, and IoT Engineering Roles',
        'schema': {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": "Contact Mahendra Mali",
            "url": "https://ohhmax.github.io/contact/",
            "mainEntity": {
                "@type": "Person",
                "name": "Mahendra Mali",
                "email": "mahendrakumarganpatbhaimali@gmail.com",
                "url": "https://ohhmax.github.io/"
            },
            "breadcrumb": {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://ohhmax.github.io/"},
                    {"@type": "ListItem", "position": 2, "name": "Contact", "item": "https://ohhmax.github.io/contact/"}
                ]
            }
        },
        'content_html': '''
        <section class="seo-content-block">
          <h2>Direct Communication Channels</h2>
          <div class="seo-card-item">
            <p><strong>Email:</strong> <a href="mailto:mahendrakumarganpatbhaimali@gmail.com">mahendrakumarganpatbhaimali@gmail.com</a></p>
            <p><strong>GitHub:</strong> <a href="https://github.com/mahendraplus" target="_blank" rel="noopener">github.com/mahendraplus</a></p>
            <p><strong>LinkedIn:</strong> <a href="https://linkedin.com/in/mahendraplus" target="_blank" rel="noopener">linkedin.com/in/mahendraplus</a></p>
            <p><strong>Telegram:</strong> <a href="https://t.me/mahendraplus" target="_blank" rel="noopener">t.me/mahendraplus</a></p>
            <p><strong>Location:</strong> Gujarat, India (Available for Worldwide Remote, Hybrid & On-Site Roles)</p>
          </div>
        </section>
        '''
    }
}

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="Mahendra Mali, Max, Security Researcher, Systems Architect, All-Rounder Engineer, Golang, Android ADB, Linux Kernel, IoT Systems">
  <link rel="canonical" href="{canonical}">

  <!-- Open Graph / WhatsApp / Telegram / LinkedIn Social Preview -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mahendra Mali (Max)">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">

  <!-- Twitter / X Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mahendraplus">
  <meta name="twitter:creator" content="@mahendraplus">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{tw_img}">

  <!-- Robots & AI Crawlers (Full Crawling & Indexing) -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="bingbot" content="index, follow">

  <link rel="shortcut icon" href="/assets/img/logo/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD Structured Data for Rich Snippets -->
  <script type="application/ld+json">
{schema_json}
  </script>

  <style>
    :root {{
      --bg: #0a0f1d;
      --card-bg: #111827;
      --border: #1f293d;
      --cyan: #38bdf8;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Poppins', -apple-system, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 24px 16px;
    }}
    .seo-container {{
      max-width: 900px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .seo-header {{
      text-align: center;
      margin-bottom: 28px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 20px;
    }}
    h1 {{
      font-size: 2rem;
      color: var(--cyan);
      margin-bottom: 8px;
    }}
    .seo-subtitle {{
      color: var(--text-muted);
      font-size: 1rem;
    }}
    .seo-preview-banner {{
      width: 100%;
      height: auto;
      border-radius: 12px;
      margin-bottom: 24px;
      border: 1px solid var(--border);
      box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }}
    .seo-content-block h2 {{
      font-size: 1.3rem;
      color: #e2e8f0;
      margin: 20px 0 10px;
    }}
    .seo-card-item {{
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 14px;
    }}
    .seo-card-item h3 {{
      color: var(--cyan);
      font-size: 1.1rem;
      margin-bottom: 6px;
    }}
    .seo-tech-list {{
      list-style-type: none;
      padding-left: 0;
      margin: 12px 0;
    }}
    .seo-tech-list li {{
      padding: 6px 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }}
    .seo-actions {{
      display: flex;
      gap: 12px;
      justify-content: center;
      margin-top: 28px;
      flex-wrap: wrap;
    }}
    .btn-action {{
      display: inline-flex;
      align-items: center;
      padding: 12px 24px;
      border-radius: 30px;
      font-weight: 600;
      text-decoration: none;
      font-size: 0.95rem;
      transition: all 0.2s ease;
    }}
    .btn-primary {{
      background: var(--cyan);
      color: #000;
    }}
    .btn-secondary {{
      background: rgba(255,255,255,0.08);
      color: var(--text);
      border: 1px solid var(--border);
    }}
  </style>

  <!-- Instant Browser Redirect to Full Interactive Single-Page App -->
  <script>
    (function() {{
      var isBot = /bot|googlebot|bingbot|crawler|spider|slurp|facebookexternalhit|whatsapp|telegram|twitterbot|slackbot|discordbot|applebot/i.test(navigator.userAgent);
      if (!isBot && window.location.search.indexOf('no_redirect=1') === -1) {{
        window.location.replace('/#{target_anchor}');
      }}
    }})();
  </script>
</head>
<body>
  <main class="seo-container">
    <header class="seo-header">
      <h1>{h1}</h1>
      <p class="seo-subtitle">{subtitle}</p>
    </header>

    <img src="{og_img}" alt="{title}" class="seo-preview-banner" width="1200" height="630">

    {content_html}

    <div class="seo-actions">
      <a href="/#{target_anchor}" class="btn-action btn-primary">Open Interactive View</a>
      <a href="/" class="btn-action btn-secondary">Main Portfolio</a>
    </div>
  </main>
</body>
</html>
'''

for slug, data in SECTIONS.items():
    os.makedirs(slug, exist_ok=True)
    out_file = os.path.join(slug, 'index.html')
    page_html = TEMPLATE.format(
        title=data['title'],
        desc=data['desc'],
        canonical=data['canonical'],
        og_img=data['og_img'],
        tw_img=data['tw_img'],
        target_anchor=data['target_anchor'],
        h1=data['h1'],
        subtitle=data['subtitle'],
        schema_json=json.dumps(data['schema'], indent=4),
        content_html=data['content_html']
    )
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(page_html)
    print(f"Updated: {out_file}")

# Mirror to gallery/index.html
os.makedirs('gallery', exist_ok=True)
with open('milestones/index.html', 'r', encoding='utf-8') as f:
    gal_html = f.read().replace('https://ohhmax.github.io/milestones/', 'https://ohhmax.github.io/gallery/')
with open('gallery/index.html', 'w', encoding='utf-8') as f:
    f.write(gal_html)
print("Updated: gallery/index.html")
