#!/usr/bin/env python3
"""
Check local HTML files for missing internal asset/page links.

This script scans all .html files (excluding tools/backups and files starting with _smoke)
and reports attributes that point to local files (href/src/poster) and whether the target
exists within the repository. It does not modify files; it prints a concise report.

Run: python tools/check_links.py
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

HTML_GLOB = '**/*.html'
SKIP_DIRS = {'tools', '.git'}

# Match src/href/poster attributes and capture the value
ATTR_RE = re.compile(r'''(?:src|href|poster)=\s*['\"]([^'\"]+)['\"]''', re.IGNORECASE)

def is_local_path(val: str) -> bool:
    # treat as local if it starts with / or doesn't have scheme like http:// or https://
    return not (val.startswith('http://') or val.startswith('https://') or val.startswith('//'))

def normalize_target(path_str: str, page_path: Path) -> Path:
    # If path is absolute-root-like (/something), make it relative to project root
    if path_str.startswith('/'):
        return ROOT / path_str.lstrip('/')
    # If a hash or mailto or javascript pseudo, return None
    if path_str.startswith('#') or path_str.startswith('mailto:') or path_str.startswith('javascript:'):
        return None
    # Otherwise, resolve relative to page
    return (page_path.parent / path_str).resolve()

def scan() -> int:
    scanned = 0
    issues = []  # tuples (page, attr_value, resolved_target, exists)
    for p in ROOT.rglob('*.html'):
        if 'tools' in p.parts:
            continue
        if p.name.startswith('_smoke'):
            continue
        scanned += 1
        s = p.read_text(encoding='utf-8', errors='replace')
        for m in ATTR_RE.finditer(s):
            val = m.group(1).strip()
            if not val:
                continue
            if not is_local_path(val):
                # skip remote or protocol-relative
                continue
            target = normalize_target(val, p)
            if target is None:
                continue
            exists = target.exists()
            # keep the string form of resolved target relative to ROOT when possible
            try:
                rel = target.relative_to(ROOT)
            except Exception:
                rel = target
            if not exists:
                issues.append((p.relative_to(ROOT), val, rel, exists))

    # Print report
    print(f"Scanned {scanned} HTML files. Found {len(issues)} missing local targets.")
    if issues:
        print('\nMissing targets:')
        for page, val, rel, exists in issues:
            print(f' - {page}: "{val}" -> {rel} (MISSING)')
        return 2
    else:
        print('No missing local targets found.')
        return 0

if __name__ == '__main__':
    sys.exit(scan())
