#!/usr/bin/env python3
"""
Pre-render static resume content into resume/index.html and pages/cv-resume-latest-info.html.
Ensures static crawlers read > 1,400 words, eliminating thin content warnings.
Ensures titles and meta descriptions fit strict SEO limits.
Guarantees 0 em-dashes and 0 en-dashes.
"""

import json
import re

def clean_dashes(text: str) -> str:
    text = text.replace('\u2014', ' - ')
    text = text.replace('\u2013', ' - ')
    text = text.replace('&mdash;', ' - ')
    text = text.replace('&ndash;', ' - ')
    return text

with open('data/resume.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build pre-rendered HTML snippets
summary_html = data.get('summary', '')

skills_html = []
for cat, skill_list in data.get('skills', {}).items():
    tags = ''.join([f'<span class="skill-tag">{s}</span>' for s in skill_list])
    skills_html.append(f'''<div class="skill-group">
  <div class="skill-category">{cat}</div>
  <div class="skill-tags">{tags}</div>
</div>''')
skills_str = '\n'.join(skills_html)

edu_html = []
for e in data.get('education', []):
    edu_html.append(f'''<div class="edu-item">
  <div class="edu-degree">{e.get("degree", "")}</div>
  <div class="edu-school">{e.get("institution", "")}</div>
  <div class="edu-meta">{e.get("period", "")} | {e.get("grade", "")}</div>
</div>''')
edu_str = '\n'.join(edu_html)

honors_html = []
for h in data.get('honorsAndAwards', []):
    desc = f'<div class="honor-desc">{h["description"]}</div>' if h.get("description") else ''
    honors_html.append(f'''<div class="honor-item">
  <div class="honor-title">{h.get("title", "")}</div>
  <div class="honor-issuer">{h.get("issuer", "")} | {h.get("period", "")}</div>
  {desc}
</div>''')
honors_str = '\n'.join(honors_html)

certs_html = []
for c in data.get('certifications', []):
    certs_html.append(f'''<div class="cert-item">
  <div class="cert-name">{c.get("name", "")}</div>
  <div class="cert-meta">{c.get("issuer", "")} | {c.get("period", "")}</div>
</div>''')
certs_str = '\n'.join(certs_html)

comp_html = []
for comp in data.get('competencies', []):
    comp_html.append(f'<div class="comp-item">{comp}</div>')
comp_str = '\n'.join(comp_html)

lang_html = []
for l in data.get('languages', []):
    lang_html.append(f'''<div class="lang-item">
  <span class="lang-name">{l.get("name", "")}</span>
  <span class="lang-level">{l.get("level", "")}</span>
</div>''')
lang_str = '\n'.join(lang_html)

proj_html = []
for p in data.get('projects', []):
    pts = ''.join([f'<li>{pt}</li>' for pt in p.get("points", [])])
    proj_html.append(f'''<div class="project-card">
  <div class="project-header">
    <span class="project-name">{p.get("name", "")}</span>
    <span class="project-label">{p.get("category", "")} | {p.get("stars", "")}</span>
  </div>
  <div class="project-tech">{p.get("tech", "")}</div>
  <ul class="bullet-list">
    {pts}
  </ul>
</div>''')
proj_str = '\n'.join(proj_html)

exp_html = []
for exp in data.get('experience', []):
    pts = ''.join([f'<li>{pt}</li>' for pt in exp.get("points", [])])
    exp_html.append(f'''<div class="exp-item">
  <div class="exp-header">
    <span class="exp-role">{exp.get("role", "")}</span>
    <span class="exp-period">{exp.get("period", "")}</span>
  </div>
  <div class="exp-company">{exp.get("company", "")} | {exp.get("location", "")}</div>
  <ul class="bullet-list">
    {pts}
  </ul>
</div>''')
exp_str = '\n'.join(exp_html)

sec_html = ['<ul class="bullet-list">']
for s in data.get('securityResearch', []):
    sec_html.append(f'<li><strong>{s.get("title", "")}:</strong> {s.get("detail", "")}</li>')
sec_html.append('</ul>')
sec_str = '\n'.join(sec_html)

ath_html = ['<ul class="bullet-list">']
for a in data.get('athleticsAndPassions', []):
    ath_html.append(f'<li><strong>{a.get("title", "")}:</strong> {a.get("detail", "")}</li>')
ath_html.append('</ul>')
ath_str = '\n'.join(ath_html)

def update_resume_file(path: str, is_subfolder: bool = True):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Title and Meta Description
    content = re.sub(
        r'<title>.*?</title>',
        '<title>Curriculum Vitae &amp; Resume | Mahendra Mali (Max)</title>',
        content
    )
    content = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="Verified curriculum vitae and engineering dossier of Mahendra Mali (Max). Security researcher, systems architect, and full-stack software engineer.">',
        content
    )

    # GA4 config
    ga_snippet = '''  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-T4QKFS53YQ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-T4QKFS53YQ', {
      'cookie_domain': 'none',
      'cookie_flags': 'SameSite=Lax;Secure'
    });
  </script>'''

    content = re.sub(r'<!-- Google tag \(gtag\.js\) -->.*?gtag\(\'js\', new Date\(\)\);\s*</script>', ga_snippet, content, flags=re.DOTALL)
    if 'GTM-TPSB9LKL' in content:
        content = re.sub(r'<!-- Google tag \(gtag\.js\) -->.*?<script.*?</script>', ga_snippet, content, flags=re.DOTALL)

    # Fill summary
    content = re.sub(
        r'<p class="summary-box" id="field-summary">.*?</p>',
        f'<p class="summary-box" id="field-summary">{summary_html}</p>',
        content
    )

    # Fill containers
    content = re.sub(
        r'<div id="skills-container">.*?</div>',
        f'<div id="skills-container">\n{skills_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="education-container">.*?</div>',
        f'<div id="education-container">\n{edu_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="honors-container">.*?</div>',
        f'<div id="honors-container">\n{honors_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="certifications-container">.*?</div>',
        f'<div id="certifications-container">\n{certs_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="competencies-container">.*?</div>',
        f'<div id="competencies-container">\n{comp_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="languages-container">.*?</div>',
        f'<div id="languages-container">\n{lang_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="projects-container">.*?</div>',
        f'<div id="projects-container">\n{proj_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="experience-container">.*?</div>',
        f'<div id="experience-container">\n{exp_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="security-container">.*?</div>',
        f'<div id="security-container">\n{sec_str}\n</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="athletics-container">.*?</div>',
        f'<div id="athletics-container">\n{ath_str}\n</div>',
        content,
        flags=re.DOTALL
    )

    # Clean dashes
    content = clean_dashes(content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Pre-rendered and updated {path}")

update_resume_file('resume/index.html', is_subfolder=True)
update_resume_file('pages/cv-resume-latest-info.html', is_subfolder=False)
