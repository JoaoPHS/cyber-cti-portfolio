# Cyber Threat Intelligence Portfolio — Tactical RPG

Interactive Cyber Threat Intelligence portfolio gamified as a tactical RPG card experience. Real threat-actor data meets a SOC/SIEM-inspired UI.

## Highlights

### Gamified experience
- **Tactical RPG cards**: rarity (1–5 ★), TAC/EST attributes, specialties
- **Geopolitical funnel**: Country → Category → Cards
- **Intelligence dossier modal**: stacked hero + scrollable intel brief
- **Empty-state alert**: clear feedback when a filter has no actors

### SOC/SIEM design
- **Palette**: absolute black (`#000000`), graphite, neon cyan (`#00f0ff`)
- **Typography**: monospace (JetBrains Mono, Fira Code, Courier New)
- **Dynamic textures** by subcategory (profit, OSINT/SIGINT, government, famous, defense, military espionage)

### Bilingual (PT/EN)
- Persistent language selector
- Instant UI + card content translation

### Python automation
- `builder.py` builds `js/data.js` from **MITRE ATT&CK**
- Static drawers for legendary individuals / curated groups & orgs
- Taxonomy normalization to English keys before write

## Project structure

```
cyber-cti-portfolio/
├── index.html
├── css/styles.css
├── js/data.js
├── js/app.js
├── assets/images/
├── builder.py
├── Architecture.md
├── README.md
└── start.bat
```

## How to use

### Preview the portfolio

```bash
# Option 1
start.bat

# Option 2 — local server (recommended)
python -m http.server 8765
# open http://127.0.0.1:8765/
```

### Rebuild the database

```bash
pip install requests deep-translator
python builder.py
```

`builder.py` will:
1. Download MITRE ATT&CK STIX data
2. Filter intrusion sets
3. Map country origin heuristics
4. Compute rarity / TAC / EST
5. Merge `STATIC_GROUPS` + `STATIC_INDIVIDUALS` + `STATIC_ORGANIZATIONS`
6. Apply manual taxonomy corrections + `normalize_taxonomies()`
7. Emit `js/data.js`

> Note: the FBI Wanted API was removed (403 Forbidden). Individuals are maintained in `STATIC_INDIVIDUALS`.

## Actor taxonomy

### Groups
- **Profit**: ransomware, extortion, financial crime
- **OSINT/SIGINT**: open-source / signals-oriented collectives
- **Associated with Gov**: non-military state-sponsored APTs / proxies

### Individuals
- **Famous**: high-profile operators and legendary figures

### Government organizations
- **Defense & Law Enforcement**: CERTs, police cyber units, civilian defense agencies
- **Espionage & Military Operations**: military cyber commands / intel units

## Add a static actor

Edit the matching list in `builder.py` (`STATIC_GROUPS`, `STATIC_INDIVIDUALS`, or `STATIC_ORGANIZATIONS`), then rebuild:

```python
{
    'id': 'example_actor',
    'category': 'groups',
    'subcategory': 'profit',
    'countryId': 'brasil',
    'stars': 4,
    'name': 'Example Actor',
    'countryName': {'pt': 'Brasil', 'en': 'Brazil'},
    'tactical': 88,
    'strategic': 80,
    'specialty': {'pt': '...', 'en': '...'},
    'description': {'pt': '...', 'en': '...'},
    'type': {'pt': 'Lucro', 'en': 'Profit'},
    'image': 'assets/images/profit.jpg'
}
```

## Tech stack

- HTML5 · Tailwind CSS (CDN) · custom CSS3
- JavaScript (ES6+)
- Python 3 (`builder.py`)
- MITRE ATT&CK STIX feed

## Debug API (browser console)

```javascript
window.cyberTacticalRPG
window.cyberTacticalRPG.actions.changeLanguage('en')
window.cyberTacticalRPG.actions.goToScreen('screen-cards')
console.log(window.cyberTacticalRPG.state)
```

## Security

- `sanitizeXSS()` on dynamic HTML interpolations
- Sandboxed Check Point iframe + CSP meta policy
- See `Architecture.md` for details

## License

Educational CTI / front-end portfolio demonstration.

## Resources

- [MITRE ATT&CK](https://attack.mitre.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [STIX](https://oasis-open.github.io/cti-documentation/)
- [Check Point ThreatMap](https://threatmap.checkpoint.com/)

---

**Built for Cyber Threat Intelligence practice**
