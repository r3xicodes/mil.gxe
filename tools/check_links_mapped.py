#!/usr/bin/env python3
"""
One-off checker: same as check_links.py but maps '/mil.gxe/' prefix to repo root before checking file existence.
"""
from pathlib import Path
import re, sys


def find_repo_root(start: Path) -> Path:
    """Walk up from start until we find a directory that looks like project root.
    Heuristics: contains index.html, or 'assets' directory, or a .git folder.
    """
    cur = start
    for _ in range(10):
        if (cur / 'index.html').exists() or (cur / 'assets').exists() or (cur / '.git').exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    # fallback to two levels up (tools/.. -> repo)
    return start.parents[1]


ROOT = Path(__file__).resolve().parents[1].resolve()
ATTR_RE = re.compile(r'''(?:src|href|poster)=\s*['\"]([^'\"]+)['\"]''', re.IGNORECASE)
BASE_RE = re.compile(r"<base[^>]+href=[\'\"]([^\'\"]+)[\'\"]", re.IGNORECASE)

def is_local(val):
    return not (val.startswith('http://') or val.startswith('https://') or val.startswith('//'))

def normalize_rootish(val: str, page: Path) -> Path:
    """Normalize a value potentially starting with / or /mil.gxe/ to an absolute filesystem Path."""
    # map /mil.gxe/... -> /... (repo root)
    if val.startswith('/mil.gxe/'):
        val = '/' + val.split('/', 2)[2]
    if val.startswith('/'):
        return (ROOT / val.lstrip('/')).resolve()
    # otherwise resolve relative to page
    return (page.parent / val).resolve()

def resolve_with_base(val: str, page: Path, base_href: str) -> Path:
    """Resolve val against base_href if provided, else normal resolution.
    base_href may be absolute (/...), a full URL, or relative.
    """
    # ignore non-file protocols and anchors
    if val.startswith('#') or val.startswith('mailto:') or val.startswith('javascript:'):
        return None
    # if absolute root-ish, normalize directly
    if val.startswith('/'):
        return normalize_rootish(val, page)

    # if no base, resolve relative to page
    if not base_href:
        return normalize_rootish(val, page)

    # If base is a full http(s) URL or protocol-relative, we can't map to filesystem reliably
    if base_href.startswith('http://') or base_href.startswith('https://') or base_href.startswith('//'):
        # if base points to the same site root with a path, try to map path component to repo
        # extract path part
        try:
            from urllib.parse import urlparse
            u = urlparse(base_href)
            base_path = u.path or '/'
        except Exception:
            base_path = base_href
    else:
        base_path = base_href

    # if base_path is absolute root-like or came from a URL, use URL-joining semantics
    if base_path.startswith('/') or base_href.startswith('http://') or base_href.startswith('https://') or base_href.startswith('//'):
        from urllib.parse import urljoin, urlparse
        # determine a path portion to use for joining
        base_for_join = base_path if base_path.startswith('/') else (urlparse(base_href).path or '/')

        # special-case mapping for GitHub Pages subpath: if base_for_join begins with
        # the repo directory name (e.g. '/mil.gxe/'), treat that as the repo root and
        # use URL-join semantics so '../' is resolved correctly against the base path.
        repo_root_segment = f'/{ROOT.name}'
        if base_for_join == repo_root_segment or base_for_join == repo_root_segment + '/':
            from urllib.parse import urljoin
            combined = urljoin(base_for_join if base_for_join.endswith('/') else base_for_join + '/', val)
            # If combined begins with the repo-name segment (e.g. '/mil.gxe/...'), strip that
            repo_prefix = repo_root_segment
            if combined.startswith(repo_prefix + '/'):
                # remove the leading '/<repo>' so '/mil.gxe/assets/x' -> '/assets/x'
                combined = combined[len(repo_prefix):]
                if not combined.startswith('/'):
                    combined = '/' + combined
            if combined.startswith('/'):
                return (ROOT / combined.lstrip('/')).resolve()
            return (ROOT / combined).resolve()
        if base_for_join.startswith(repo_root_segment + '/'):
            # compute combined using urljoin against the full base_for_join
            from urllib.parse import urljoin
            combined = urljoin(base_for_join if base_for_join.endswith('/') else base_for_join + '/', val)
            # If combined starts with '/<repo>/', strip repo prefix so it maps to repo root
            repo_prefix = repo_root_segment + '/'
            if combined.startswith(repo_prefix):
                combined = combined[len(repo_root_segment):]
                if not combined.startswith('/'):
                    combined = '/' + combined
                return (ROOT / combined.lstrip('/')).resolve()
            if combined.startswith('/'):
                return (ROOT / combined.lstrip('/')).resolve()
            # otherwise treat as relative under the tail directory
            tail = base_for_join.split('/', 2)[2] if '/' in base_for_join[1:] else ''
            base_dir = (ROOT / tail).resolve() if tail else ROOT.resolve()
            return (base_dir / combined).resolve()

        # fallback: use urljoin to combine base path and val, then map to filesystem
        combined = urljoin(base_for_join if base_for_join.endswith('/') else base_for_join + '/', val)
        # If combined is root-absolute -> map under ROOT
        if combined.startswith('/'):
            return (ROOT / combined.lstrip('/')).resolve()
        # If combined is relative (may contain ../), resolve relative to the page's dir
        return (page.parent / combined).resolve()

    # relative base -> resolve relative to page (filesystem semantics ok)
    base_fs = (page.parent / base_path).resolve()
    # If base points to a file, use its parent dir
    if base_fs.exists() and base_fs.is_file():
        base_dir = base_fs.parent
    else:
        base_dir = base_fs

    return (base_dir / val).resolve()

def run():
    scanned = 0
    issues = []
    for p in ROOT.rglob('*.html'):
        if 'tools' in p.parts or p.name.startswith('_smoke'):
            continue
        scanned += 1
        s = p.read_text(encoding='utf-8', errors='replace')
        # find base href if any
        base_m = BASE_RE.search(s)
        base_href = base_m.group(1).strip() if base_m else ''

        for m in ATTR_RE.finditer(s):
            v = m.group(1).strip()
            if not v or not is_local(v):
                continue
            # try direct absolute mapping first
            try:
                t = resolve_with_base(v, p, base_href)
            except Exception:
                t = None
            if t is None:
                continue
            # now if resolved target exists, good
            if not t.exists():
                try:
                    rel = t.relative_to(ROOT)
                except Exception:
                    rel = t
                issues.append((p.relative_to(ROOT), v, rel))

    print(f"Scanned {scanned} HTML files. Found {len(issues)} missing local targets (mapped+base-aware).")
    for page, val, rel in issues:
        print(f' - {page}: "{val}" -> {rel} (MISSING)')
    return 2 if issues else 0


if __name__ == '__main__':
    sys.exit(run())
