#!/usr/bin/env python3
"""
Scan .html files in the workspace and remove duplicate HTML documents inside a single file.
Behavior:
 - For any .html file containing more than one '<!doctype' (case-insensitive), split on that token.
 - Keep the last document (assumed canonical), back up the original to tools/backups/<timestamp>/path
 - Rewrite the file with the last document and print a summary report.

Run: python tools/clean_html_duplicates.py
"""
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "tools" / "backups" / datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

def find_html_files(root: Path):
    for p in root.rglob('*.html'):
        yield p


def process_file(path: Path):
    text = path.read_text(encoding='utf-8', errors='replace')
    lowered = text.lower()
    token = '<!doctype'
    count = lowered.count(token)
    if count <= 1:
        return False, 0
    # find split points preserving original cases: we'll locate positions of token in original text case-insensitively
    parts = []
    i = 0
    L = len(text)
    lt = lowered
    while True:
        idx = lt.find(token, i)
        if idx == -1:
            # append trailing if any
            if i < L:
                parts.append(text[i:])
            break
        # if found at idx, and idx > i, append leading
        if idx > i:
            parts.append(text[i:idx])
        # from idx onwards, find next token to extract full document later
        i = idx
        # move forward to find next occurrence to determine fragment boundary
        nxt = lt.find(token, i+1)
        if nxt == -1:
            parts.append(text[i:])
            i = L
            break
        else:
            parts.append(text[i:nxt])
            i = nxt
    # Normalize parts: some leading fragment before first doctype may exist; we want documents that start with doctype
    docs = [p for p in parts if p.strip().lower().startswith(token)]
    if len(docs) <= 1:
        return False, len(docs)
    # Keep last doc
    last = docs[-1].lstrip('\n\r\t ')
    # Backup original
    bak_path = BACKUP_DIR / path.relative_to(ROOT)
    bak_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, bak_path)
    # Write new content
    path.write_text(last, encoding='utf-8')
    return True, len(docs)


def main():
    modified = []
    scanned = 0
    for f in find_html_files(ROOT):
        scanned += 1
        changed, docs = process_file(f)
        if changed:
            modified.append((f, docs))
    print(f"Scanned {scanned} .html files.")
    if modified:
        print(f"Modified {len(modified)} files (removed duplicated docs):")
        for p, docs in modified:
            print(f" - {p.relative_to(ROOT)}  (found {docs} docs)")
        print(f"Backups were written to: {BACKUP_DIR}")
        sys.exit(0)
    else:
        print("No files needed modification.")
        sys.exit(0)

if __name__ == '__main__':
    main()
