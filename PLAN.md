# mil.gxe — Full In-Depth Site Plan

This document is a comprehensive, actionable plan for building *mil.gxe* — a professional, futuristic military portal for the Great Holy Xanarcica Empire (GXE) using GitHub Pages + VS Code.

## 1. Executive Summary

Goal: Create a static, authoritative, and visually striking military website that balances realism and sci-fi lore. The site will be fully static so it's compatible with GitHub Pages (free), easy to maintain via VS Code, and extensible for future additions.

Audience: Enthusiasts, role-players, lore readers, recruits, and visitors who expect polished UX and believable government/military presentation.

Success Criteria:
- Clean, responsive UI reflecting GXE brand.
- Deployable on GitHub Pages with zero server-side code.
- Maintainable content structure (Markdown/Jekyll or JSON + static templates).
- Basic interactivity (modals, search, SVG map) implemented client-side.

---

## 2. Core Goals (Detailed)

- Authoritative visual design like real military orgs.
- Futuristic and slightly militaristic branding.
- Accessible and mobile-first.
- Content-first: easy to add branches, equipment, and operations.
- Lightweight for fast loading; images optimized and lazy-loaded.

---

## 3. Design System

Colors (primary):
- GXE Blood Red: #A10000
- Jet Black: #0A0A0A
- Titanium White: #F3F4F6
- Light Gray: #9AA3A8
- Neon Turquoise (accent): #00E5D4

Typography:
- Headings: Oswald / Orbitron / Rajdhani (bold, tracker tightened)
- Body: Inter / Roboto (regular 400, 500)
- UI: Monospace for technical spec areas (optional)

Components:
- Global Navbar (fixed) with dropdowns
- Hero (video/image) with overlay and CTA
- Card grid for branches/equipment
- Timeline (horizontal/vertical) component
- Modal for spec sheets
- Toast/alert for announcements

Motion:
- Micro-interactions (hover glow, scanlines)
- Scroll reveal with AOS or IntersectionObserver
- Subtle parallax in hero

Accessibility:
- Color contrast > 4.5:1 for body text
- Keyboard navigable modals and dropdowns
- ARIA roles for nav, main, and dialogs

---

## 4. Sitemap & Content Model

Top-level pages:
- / (Home)
- /about/
- /branches/
  - /branches/air-force/
  - /branches/navy/
  - /branches/ground/
  - ...
- /technology/
  - /technology/<slug>/
- /operations/
  - /operations/<campaign-slug>/
- /media/
- /contact/

Content formats:
- Core content in Markdown (Jekyll site) or JSON data files used by templates.
- Equipment and operations modeled as data objects with fields:
  - id, name, slug, image, thumbnail, summary, specs (key/value), long_description, tags, related_links

Example equipment spec (JSON):
{
  "id": "xf-1",
  "name": "Xanarcica Falcon XF-1",
  "type": "fighter",
  "year": 2041,
  "specs": { "length": "19.4 m", "max_speed": "Mach 2.4" }
}

---

## 5. Technical Stack Options & Recommendation

Option A — Static + Jekyll (Recommended for speed & simplicity):
- Jekyll with GitHub Pages (built-in)
- TailwindCSS or Bootstrap for rapid UI
- Small JS helpers (Alpine.js, AOS, or vanilla)
- Data stored in _data/*.yml or _posts for operations

Pros: simple GitHub Pages deployment, Markdown content, low maintenance.
Cons: less SPA-like interactivity (but fine for our needs).

Option B — Vite + React + Tailwind (Advanced):
- Vite + React, Tailwind, deploy to gh-pages branch
- Use react-router for routing
- Good for heavy interactivity (SVG map with d3/React)

Pros: modern stack, interactive components
Cons: more complex GitHub Pages setup and CI; build step required.

Recommendation: Start with Jekyll + Tailwind (fast, easy, GitHub-native). If you later need dynamic features, migrate a sub-section to React or ship a small SPA.

---

## 6. Project Structure (Jekyll + Tailwind example)

- index.html (or /_layouts/)
- _config.yml
- _layouts/
  - default.html
  - page.html
  - post.html
- _includes/
  - header.html
  - footer.html
  - hero.html
- _data/
  - branches.yml
  - equipment.yml
  - operations.yml
- assets/
  - css/
    - main.css (Tailwind compiled)
  - js/
    - main.js
  - images/
- PLAN.md
- README.md

---

## 7. UI/UX Specs (per page)

Home:
- Hero with emblem, motto, and CTAs
- Featured operations carousel
- Branch cards
- Latest news section (optional)

About:
- Intro with timeline (interactive)
- Leadership cards with bios and images

Branches:
- Landing grid of branches
- Each branch page: insignia, mission, units, gallery, key equipment

Technology:
- Filterable grid (type, era)
- Each card opens modal or detail page with spec sheet and images

Operations:
- Map + dossier cards
- Filter by era/conflict

Media:
- Responsive gallery, download buttons

Contact/Join:
- CTA, external form link, recruitment FAQs

---

## 8. Features & Implementation Notes

Animations:
- Use AOS.js for reveal animations or IntersectionObserver for custom control.
- Parallax via CSS transform on scroll with requestAnimationFrame throttle.

Search:
- Fuse.js client-side search over a pre-built JSON index (_site/search.json).

Map:
- Create an SVG map in /assets/images/gxe-map.svg. Use simple IDs for regions and a JS handler to show tooltips/modals.

Spec Modals:
- Accessible modal dialog using CSS + JS. Prefetch data attributes for quick open.

Images/Videos:
- Use WebP where possible and provide fallback.
- Lazy-load with loading=lazy and IntersectionObserver.

---

## 9. Deployment & CI

GitHub Pages (no CI required):
- If using Jekyll: push to main; enable GitHub Pages in repo settings (root or /docs/).
- If using a build step (Tailwind CLI or Vite), either commit build output to gh-pages branch or configure GitHub Actions to build and deploy.

Optional GitHub Actions (example):
- Build Tailwind + Jekyll and push _site/ to gh-pages branch.

---

## 10. Roadmap & Milestones

Phase 0 — Planning (this doc)
Phase 1 — Minimal Viable Site (2 weeks)
- Setup Jekyll + Tailwind
- Implement header/footer, Home, About, Branches (landing)
- Add 10 equipment cards and 5 operation dossiers

Phase 2 — Interactivity & polish (2–3 weeks)
- Add search, SVG map, modals, and animations
- Optimize assets, add light/dark toggle

Phase 3 — Media + Launch (1 week)
- Add galleries, downloads, recruitment CTA
- SEO, meta tags, final QA

Phase 4 — Expansion (ongoing)
- Add API-backed features later (if desired)
- Add multi-language support, export to other domains

---

## 11. Content Guidelines & Tone

- Use authoritative, formal tone in official pages, but allow lore voice in dossiers.
- Keep bios and operation writeups concise (100–300 words).
- Use consistent naming (branch slugs, equipment IDs).

---

## 12. Risk & Mitigation

- Risk: GH Pages size limits for media. Mitigation: Use external CDN or GitHub Releases for large files.
- Risk: Overly heavy front-end. Mitigation: Lazy-load assets, minimize JS.

---

## 13. Next Steps (Actionable)

1. Approve the design system and sitemap.
2. Choose technical option (Jekyll recommended).
3. I can scaffold a minimal starter (index.html, header/footer, Tailwind setup) — say the word and I'll create it.

---

## Appendix A — Example JSON Schemas

Equipment (equipment.yml or equipment.json):
- id: xf-1
  name: Xanarcica Falcon XF-1
  slug: xf-1
  type: fighter
  era: 2040s
  summary: "A multi-role air superiority fighter..."
  specs:
    length: "19.4 m"
    wingspan: "11.2 m"
    max_speed: "Mach 2.4"

Operation (operations.yml):
- id: op-sable
  title: Operation Sable Dawn
  year: 2043
  summary: "A swift amphibious operation securing the southern archipelago."
  region_ids: [southern-archipelago]

---

End of PLAN.md
