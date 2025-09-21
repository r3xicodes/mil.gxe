#!/usr/bin/env python3
"""
Standardize navbar (header) and footer across all HTML files in the repo.
- Replaces any <header class="site-header">...</header> and <footer class="site-footer">...</footer>
  with canonical, root-relative header/footer HTML.
- Backs up originals to tools/backups/<timestamp> before writing.

Run: python tools/sync_nav_footer.py
"""
from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "tools" / "backups" / datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

HEADER_CANON = '''<header class="site-header">
  <div class="topbar"><div class="container">Connect • Apply Now • Chat • Contact Recruiter</div></div>
  <div class="nav container">
  <div class="brand"><a href="/mil.gxe/index.html" aria-label="GXE home"><img src="/mil.gxe/assets/images/emblem.png" alt="GXE emblem" width="54" height="54" style="border-radius:8px;object-fit:cover"></a><div style="line-height:1"><strong>mil.gxe</strong><div class="muted">Great Holy Xanarcica Empire</div></div></div>
    <nav class="primary">
  <a href="/mil.gxe/about.html">About</a>
  <a href="/mil.gxe/ways-to-serve/index.html">Ways to Serve</a>
  <a href="/mil.gxe/branches/index.html">Branches</a>
  <a href="/mil.gxe/careers/index.html">Careers</a>
  <a href="/mil.gxe/training/index.html">Training</a>
  <a href="/mil.gxe/bases/index.html">Bases</a>
  <a href="/mil.gxe/contact/index.html">Contact</a>
  <a class="cta-apply" href="/mil.gxe/apply.html">Apply Now</a>
    </nav>
  </div>
</header>'''

FOOTER_CANON = '''<footer class="site-footer">
  <div class="container footer-inner">
    <div>
      <strong>Contact</strong>
  <div class="muted"><a href="/mil.gxe/contact/index.html">Contact</a> • <a href="/mil.gxe/contact/recruiter-finder.html">Recruiter Finder</a></div>
    </div>
    <div>
      <strong>Legal</strong>
  <div class="muted"><a href="/mil.gxe/privacy.html">Privacy</a> • <a href="/mil.gxe/accessibility.html">Accessibility</a> • <a href="/mil.gxe/sitemap.html">Sitemap</a></div>
    </div>
    <div>
  <a href="/mil.gxe/index.html"> <img src="/mil.gxe/assets/images/emblem.png" alt="emblem" width="48" height="48"> </a>
      <div class="muted">© 2025 Great Holy Xanarcica Empire</div>
    </div>
  </div>
</footer>'''

HEADER_RE = re.compile(r"<header[^>]*class=[\"']site-header[\"'][\s\S]*?</header>", re.IGNORECASE)
FOOTER_RE = re.compile(r"<footer[^>]*class=[\"']site-footer[\"'][\s\S]*?</footer>", re.IGNORECASE)

changed = []
scanned = 0
for path in ROOT.rglob('*.html'):
    # skip tools backups and smoke files
    if any(part == 'tools' for part in path.parts):
        continue
    if path.name.startswith('_smoke'):
        continue
    scanned += 1
    text = path.read_text(encoding='utf-8', errors='replace')
    newtext = text
    h_match = HEADER_RE.search(newtext)
    f_match = FOOTER_RE.search(newtext)
    did = False
    if h_match:
        newtext = newtext[:h_match.start()] + HEADER_CANON + newtext[h_match.end():]
        did = True
    if f_match:
        # recalc f_match if header changed (re-search)
        f_match2 = FOOTER_RE.search(newtext)
        if f_match2:
            newtext = newtext[:f_match2.start()] + FOOTER_CANON + newtext[f_match2.end():]
            did = True
    if did and newtext != text:
        # backup
        rel = path.relative_to(ROOT)
        bak_path = BACKUP_DIR / rel
        bak_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, bak_path)
        path.write_text(newtext, encoding='utf-8')
        changed.append(path.relative_to(ROOT))

print(f"Scanned {scanned} HTML files.")
if changed:
    print(f"Updated {len(changed)} files:")
    for p in changed:
        print(' -', p)
    print('Backups written to', BACKUP_DIR)
else:
    print('No files needed header/footer replacement.')
