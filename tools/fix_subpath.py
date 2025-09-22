#!/usr/bin/env python3
"""
Prefix root-leading asset/media URLs with /mil.gxe/ for GitHub Pages subpath hosting.
- Scans all .html files (excluding tools/backups and files starting with _smoke)
- Replaces occurrences like src="/assets/...", href="/media/...", href="/sitemap.html" (root) with /mil.gxe/...
- Backs up modified files under tools/backups/<timestamp>/...

Run: python tools/fix_subpath.py
"""
from pathlib import Path
import re
import shutil
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / 'tools' / 'backups' / datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Patterns to replace when they start with a single leading slash (not //)
PATTERNS = [
    (re.compile(r'(src|href|poster)=["\']/(assets/[^"\']*)["\']', re.IGNORECASE), r"\1=\"/mil.gxe/\2\""),
    (re.compile(r'(src|href|poster)=["\']/(media/[^"\']*)["\']', re.IGNORECASE), r"\1=\"/mil.gxe/\2\""),
    (re.compile(r'(href)=["\']/site\.webmanifest["\']', re.IGNORECASE), r'href="/mil.gxe/site.webmanifest"'),
    (re.compile(r'(href)=["\']/(index\.html)["\']', re.IGNORECASE), r'href="/mil.gxe/index.html"'),
    (re.compile(r'(href)=["\']/(privacy\.html|accessibility\.html|sitemap\.html|apply\.html)["\']', re.IGNORECASE), r'href="/mil.gxe/\2"'),
]

changed = []
scanned = 0
for p in ROOT.rglob('*.html'):
    if 'tools' in p.parts:
        continue
    if p.name.startswith('_smoke'):
        continue
    scanned += 1
    s = p.read_text(encoding='utf-8', errors='replace')
    new = s
    for pat, repl in PATTERNS:
        new = pat.sub(repl, new)
    if new != s:
        rel = p.relative_to(ROOT)
        bak = BACKUP_DIR / rel
        bak.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, bak)
        p.write_text(new, encoding='utf-8')
        changed.append(rel)

print(f"Scanned {scanned} HTML files.")
if changed:
    print(f"Updated {len(changed)} files:")
    for c in changed:
        print(' -', c)
    print('Backups written to', BACKUP_DIR)
else:
    print('No root-leading asset/media links found to prefix.')
