# Project Architecture — Cyber Threat Intelligence Portfolio

## Overview

Interactive **Cyber Threat Intelligence (CTI)** portfolio presented as a **tactical RPG card game**. Real threat actors (APT groups, individuals, government agencies) are rendered as RPG cards with attributes, rarity, and geopolitical classification.

### Core traits
- **Bilingual UI**: Portuguese (PT) and English (EN)
- **Automated data**: Python builder generates `js/data.js` from MITRE ATT&CK
- **Static drawers**: Legendary individuals and selected organizations live in `STATIC_*` lists
- **Design**: Modern SOC/SIEM aesthetic (black, graphite, neon cyan)
- **Responsive**: Desktop and mobile layouts

---

## File structure

```
cyber-cti-portfolio/
├── index.html              # Main UI (screens + modal + live map)
├── builder.py              # Data automation / MITRE ingest
├── Architecture.md         # This document
├── README.md               # Project overview & usage
├── start.bat               # Local launch helper
├── .gitignore
├── css/
│   └── styles.css          # Theme, animations, modal, CRT effects
├── js/
│   ├── data.js             # Database (generated / curated)
│   └── app.js              # Navigation, filters, modal, i18n, XSS guards
└── assets/
    └── images/
        ├── radar.svg
        ├── class_groups.jpg
        ├── class_individuals.jpg
        ├── class_organizations.jpg
        ├── class_espionage.jpg
        ├── class_famous.jpg
        ├── profit.jpg
        ├── osint.jpg
        ├── associated.jpg
        ├── famous.jpg
        ├── enforce.jpg
        ├── military.jpg
        ├── person.jpg
        ├── govs.jpg
        └── gru.jpg
```

---

## Navigation flow

### Screen 1 — Geopolitics (`screen-geopolitics`)
- **LIVE THREAT MAP** button → Check Point ThreatCloud iframe
- Country grid: RU, US, CN, KP, IR, IL, IN, BR, EU, Global

### Screen 2 — Category (`screen-category`)
- Geopolitical dossier (country modus operandi)
- Categories:
  1. **Groups** → Profit | OSINT/SIGINT | Associated with Gov
  2. **Individuals** → Famous
  3. **Government Organizations** → Defense & Law Enforcement | Espionage & Military Operations

### Screen 3 — Cards (`screen-cards`)
- RPG card grid filtered by country + category + subcategory

### Live map (`livemap-screen`)
- Sandboxed iframe: `https://threatmap.checkpoint.com/`
- `sandbox="allow-scripts allow-same-origin allow-popups"`
- `referrerpolicy="no-referrer"` · `loading="lazy"`

### Modal — Intelligence dossier (`threat-modal`)
- Stacked layout on all viewports (hero image → intel column)
- Single continuous scroll
- Fields: name, classification, tactical analysis, specialty, TAC/EST bars

---

## Data model (`js/data.js`)

### `cyberDatabase`
```text
groups.profit | groups.osint_sigint | groups.government
individuals.famous
organizations.defense_law | organizations.military_espionage
```

### Card schema (English keys)
```json
{
  "id": "optional_static_id",
  "name": "Actor Name",
  "category": "groups | individuals | organizations",
  "subcategory": "profit | osint_sigint | government | famous | defense_law | military_espionage",
  "countryCode": "RU",
  "countryId": "russia",
  "stars": 5,
  "tactical": 90,
  "strategic": 85,
  "specialty": { "pt": "...", "en": "..." },
  "description": { "pt": "...", "en": "..." },
  "type": { "pt": "...", "en": "..." },
  "image": "assets/images/..."
}
```

### Taxonomy design
- **`groups/government`**: non-military state-sponsored APTs / proxies (e.g. Killnet, APT41)
- **`organizations/military_espionage`**: strict military cyber commands (e.g. GRU 74455, IRGC, ComDCiber)

---

## Automation (`builder.py`)

### Pipeline (current)
```text
dynamic MITRE cards
  + STATIC_GROUPS
  + STATIC_INDIVIDUALS
  + STATIC_ORGANIZATIONS
  → apply_manual_corrections()
  → sanitize_actor_keys()
  → normalize_taxonomies()
  → js/data.js
```

### Notes
- FBI Wanted API was removed (HTTP 403); individuals are static only
- CERT / OSINT / elite legacy lists may still exist in the file but are **not** merged in `main()`
- `normalize_taxonomies()` forces English taxonomy keys before write

### Attribute heuristics
- **Stars (1–5)**: impact / sophistication
- **TAC**: operational skill (roughly 50–98)
- **EST**: strategic reach (roughly 45–95)

---

## Front-end engine (`js/app.js`)

### Global state
```js
appState = {
  currentScreen, currentLanguage, selectedCountry,
  selectedCategory, selectedSubcategory, filteredData
}
```

### Security
- `sanitizeXSS(content)` — entity map for `& < > " ' /`
- `sanitizeImageURL(url)` — blocks `javascript:` / `data:` schemes
- CSP meta tag in `index.html` (scripts, styles, imgs, frame-src for Check Point)
- Modal/country HTML interpolations use `sanitizeXSS`

### Key functions
- Navigation: `goToScreen`, `selectCountry`, `selectSubcategory`
- Render: `renderCountries`, `renderGridCards`, `createCard`
- Modal: `openThreatModal` / `openDetailModal`
- i18n: `changeLanguage`, `updateLanguage`
- Art: `getCategoryClassArt`, `getClassImagePath`

---

## Design system

| Token | Value |
|-------|-------|
| Background | `#000000` |
| Panel | `#09090b` / `#16161a` |
| Accent | `#00f0ff` |
| Font | JetBrains Mono / Fira Code / Courier New |

Subcategory scanline/glow themes are driven by CSS variables (`--scan-glow`) tied to the active subcategory.

---

## External integrations

| Resource | Purpose |
|----------|---------|
| Tailwind CDN | Utility layout |
| flag-icons (jsDelivr) | Country flags |
| Check Point ThreatMap | Live attack map iframe |
| api.qrserver.com | Bitcoin donation QR |

---

## Local usage

```bash
# Preview
python -m http.server 8765
# open http://127.0.0.1:8765/

# Rebuild database (MITRE + static drawers)
pip install requests deep-translator
python builder.py
```

### Deploy (GitHub + Vercel)
- Static site: serve repo root
- Do **not** commit `__pycache__/`, `.venv/`, `.env` (see `.gitignore`)
- Prefer regenerating `js/data.js` locally before push if taxonomy changed

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Modal content clipped | Hard refresh CSS; desktop uses stacked scroll on `.modal-content-wrapper` |
| Empty country filter | Actor `countryCode` mismatch vs selector ISO code |
| Stars missing | `stars` / `rarity` / `tactical` resolution in `resolveStars()` |
| Flags missing | flag-icons CDN / CSP `style-src` / `font-src` allowlist |
| CSP blocks assets | Update meta CSP hosts for Tailwind / jsDelivr / QR / Check Point |

---

## References

- [MITRE ATT&CK](https://attack.mitre.org/)
- [STIX](https://oasis-open.github.io/cti-documentation/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Check Point ThreatCloud Map](https://threatmap.checkpoint.com/)

---

## License

Educational CTI / front-end portfolio demonstration.
