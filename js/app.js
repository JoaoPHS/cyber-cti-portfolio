// ═══════════════════════════════════════════════════════════════
// CYBER THREAT INTELLIGENCE PORTFOLIO - TACTICAL RPG ENGINE
// Flow: Country → Category → RPG Cards
// ═══════════════════════════════════════════════════════════════

const LANG_STORAGE_KEY = 'cti-portfolio-lang';

/**
 * InfoSec — Immutable XSS sanitizer for untrusted external strings
 * (MITRE ATT&CK / data.js payloads). Dictionary mapping neutralizes
 * markup metacharacters and quote forms that enable tag injection or
 * attribute/event-handler payloads (e.g. onerror=, onload=) when values
 * are concatenated into HTML templates.
 *
 * Mapping (OWASP-aligned entity encoding):
 *   & → &amp;   < → &lt;   > → &gt;
 *   " → &quot;  ' → &#x27;  / → &#x2F;
 */
function sanitizeXSS(content) {
    if (content == null) return '';
    const entityMap = Object.freeze({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;'
    });
    return String(content).replace(/[&<>"'/]/g, (ch) => entityMap[ch]);
}

/** @deprecated Prefer sanitizeXSS — kept as a thin alias for call-site compatibility. */
function escapeHTML(str) {
    try {
        return sanitizeXSS(str);
    } catch (err) {
        console.warn('[CTI][InfoSec] sanitizeXSS failed — returning empty string:', err);
        return '';
    }
}

/**
 * InfoSec — Allow only http(s) or relative asset paths for image src.
 * Rejects javascript:/data:/vbscript: URI schemes used in XSS vectors.
 */
function sanitizeImageURL(url) {
    try {
        if (url == null) return '';
        const value = String(url).trim();
        if (!value) return '';
        if (/[\x00-\x1f\x7f]/.test(value)) return '';
        if (/^(javascript|data|vbscript|file):/i.test(value)) return '';
        if (/^https?:\/\//i.test(value) || value.startsWith('assets/') || value.startsWith('./assets/')) {
            return sanitizeXSS(value);
        }
        return '';
    } catch (err) {
        console.warn('[CTI][InfoSec] sanitizeImageURL failed:', err);
        return '';
    }
}

function getSavedLanguage() {
    try {
        const saved = localStorage.getItem(LANG_STORAGE_KEY);
        if (saved === 'pt' || saved === 'en') {
            return saved;
        }
    } catch (e) {
        console.warn('[CTI] LocalStorage unavailable while reading language:', e);
    }
    return 'pt';
}

let globalLanguage = getSavedLanguage();

const appState = {
    currentScreen: 'screen-geopolitics',
    currentLanguage: globalLanguage,
    selectedCountry: null,
    selectedCategory: null,
    selectedSubcategory: null,
    filteredData: []
};

document.addEventListener('DOMContentLoaded', () => {
    console.log('[CTI TACTICAL RPG] Bootstrapping engine...');

    initializeLanguage();
    initializeNavigation();
    initializeFilters();
    initializeModal();
    initializeDonatePanel();
    updateLanguage();

    goToScreen('screen-geopolitics');
    renderCountries();

    console.log('[CTI TACTICAL RPG] System online.');
});

// ═══════════════════════════════════════════════════════════════
// LANGUAGE SYSTEM (PT/EN)
// ═══════════════════════════════════════════════════════════════

function initializeLanguage() {
    document.getElementById('lang-pt').addEventListener('click', () => changeLanguage('pt'));
    document.getElementById('lang-en').addEventListener('click', () => changeLanguage('en'));
    updateLanguageButtons();
}

function changeLanguage(lang) {
    if (lang !== 'pt' && lang !== 'en') {
        lang = 'pt';
    }

    globalLanguage = lang;
    appState.currentLanguage = lang;

    try {
        localStorage.setItem(LANG_STORAGE_KEY, lang);
    } catch (e) {
        console.warn('[CTI] LocalStorage unavailable while saving language:', e);
    }

    updateLanguageButtons();
    updateLanguage();

    if (appState.currentScreen === 'screen-geopolitics') {
        renderCountries();
    } else if (appState.currentScreen === 'screen-cards') {
        renderGridCards();
    }

    console.log(`[CTI] Language set to: ${lang.toUpperCase()} (persisted)`);
}

function updateLanguageButtons() {
    document.getElementById('lang-pt').classList.toggle('active', appState.currentLanguage === 'pt');
    document.getElementById('lang-en').classList.toggle('active', appState.currentLanguage === 'en');
}

function updateLanguage() {
    const lang = appState.currentLanguage;
    document.querySelectorAll('[data-lang]').forEach(element => {
        const key = element.getAttribute('data-lang');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });

    if (appState.selectedCountry) {
        displayGeopoliticalDossier(appState.selectedCountry);
    }
}

// ═══════════════════════════════════════════════════════════════
// SCREEN NAVIGATION
// ═══════════════════════════════════════════════════════════════

const LIVE_MAP_URL = 'https://threatmap.checkpoint.com/';

function initializeNavigation() {
    document.getElementById('btn-back-countries').addEventListener('click', () => {
        goToScreen('screen-geopolitics');
        appState.selectedCountry = null;
        console.log('[CTI] Navigation: back to country selection');
    });

    document.getElementById('btn-back-category').addEventListener('click', () => {
        goToScreen('screen-category');
        appState.selectedCategory = null;
        appState.selectedSubcategory = null;
        console.log('[CTI] Navigation: back to category selection');
    });

    const btnLiveMap = document.getElementById('btn-live-threat-map');
    if (btnLiveMap) {
        btnLiveMap.addEventListener('click', openLiveMap);
    }

    const btnBackLiveMap = document.getElementById('btn-back-livemap');
    if (btnBackLiveMap) {
        btnBackLiveMap.addEventListener('click', closeLiveMap);
    }
}

function goToScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));

    const targetScreen = document.getElementById(screenId);
    if (!targetScreen) {
        console.error(`[CTI] Screen not found: ${screenId}`);
        return;
    }

    targetScreen.classList.remove('hidden');
    targetScreen.classList.add('fade-in');
    appState.currentScreen = screenId;
    console.log(`[CTI] Active screen: ${screenId}`);
}

function openLiveMap() {
    const iframe = document.getElementById('live-threat-iframe');
    if (iframe && (!iframe.src || iframe.src === 'about:blank' || iframe.src.endsWith('about:blank'))) {
        iframe.src = LIVE_MAP_URL;
    }
    goToScreen('livemap-screen');
    console.log('[CTI] Live Threat Map opened (Check Point ThreatCloud)');
}

function closeLiveMap() {
    const iframe = document.getElementById('live-threat-iframe');
    if (iframe) {
        iframe.src = 'about:blank';
    }
    goToScreen('screen-geopolitics');
    console.log('[CTI] Returning from Live Threat Map');
}

// ═══════════════════════════════════════════════════════════════
// SCREEN 1: COUNTRY GRID
// ═══════════════════════════════════════════════════════════════

function renderCountries() {
    const container = document.getElementById('countries-container');
    container.innerHTML = '';
    const lang = appState.currentLanguage;

    countries.forEach(country => {
        const btn = document.createElement('button');
        btn.className = 'country-btn fade-in cursor-pointer';
        btn.type = 'button';
        btn.style.touchAction = 'manipulation';

        const flagClass = getFlagIconClass(country.code);
        const safeFlagClass = sanitizeXSS(flagClass);
        const flagHTML = flagClass === 'global-icon'
            ? `<span class="country-flag-emoji">${sanitizeXSS(country.flag)}</span>`
            : `<span class="fi ${safeFlagClass} country-flag-svg w-12 h-8 md:w-16 md:h-12"></span>`;

        const availableLabel = translations[lang]?.['indicator-available'] || 'Available';
        const safeName = sanitizeXSS(country.name?.[lang] || country.name?.en || country.code || '');
        const safeAvailable = sanitizeXSS(availableLabel);
        btn.innerHTML = `
            <span class="country-flag-wrap flex items-center justify-center">${flagHTML}</span>
            <span class="country-name text-xs md:text-sm">${safeName}</span>
            <span class="country-indicator available blink-indicator">${safeAvailable}</span>
        `;
        btn.addEventListener('click', () => selectCountry(country.code), { passive: true });
        container.appendChild(btn);
    });
}

function getFlagIconClass(countryCode) {
    const flagMap = {
        RU: 'fi-ru',
        US: 'fi-us',
        CN: 'fi-cn',
        KP: 'fi-kp',
        IR: 'fi-ir',
        IL: 'fi-il',
        IN: 'fi-in',
        BR: 'fi-br',
        EU: 'fi-eu',
        global: 'fi-un',
        UN: 'fi-un'
    };
    return flagMap[countryCode] || 'global-icon';
}

function checkCountryHasCards(countryCode) {
    const allActors = [
        ...(cyberDatabase.groups?.profit || []),
        ...(cyberDatabase.groups?.osint_sigint || []),
        ...(cyberDatabase.groups?.government || []),
        ...(cyberDatabase.individuals?.famous || []),
        ...(cyberDatabase.organizations?.defense_law || []),
        ...(cyberDatabase.organizations?.military_espionage || [])
    ];
    return allActors.some(actor => actorCountryCode(actor) === normalizeCountryCode(countryCode));
}

function selectCountry(countryCode) {
    appState.selectedCountry = countryCode;
    displayGeopoliticalDossier(countryCode);
    goToScreen('screen-category');
    console.log(`[CTI] Country selected: ${countryCode}`);
}

function displayGeopoliticalDossier(countryCode) {
    const profile = (typeof countryProfiles !== 'undefined' ? countryProfiles : {})[countryCode];
    const titleElement = document.getElementById('dossier-title');
    const modusElement = document.getElementById('dossier-modus');
    if (!titleElement || !modusElement) return;

    if (!profile) {
        titleElement.textContent = '';
        modusElement.textContent = '';
        return;
    }

    const lang = appState.currentLanguage;
    titleElement.textContent = profile.title?.[lang] || profile.titulo?.[lang] || '';
    modusElement.textContent = profile.modus?.[lang] || '';
}

// ═══════════════════════════════════════════════════════════════
// SCREEN 2: CATEGORY FILTERS
// ═══════════════════════════════════════════════════════════════

function initializeFilters() {
    document.querySelectorAll('.subcategory-btn').forEach(button => {
        button.addEventListener('click', () => {
            const category = button.getAttribute('data-category');
            const subcategory = button.getAttribute('data-subcategory');
            selectSubcategory(category, subcategory);
        });
    });
}

function selectSubcategory(category, subcategory) {
    appState.selectedCategory = category;
    appState.selectedSubcategory = subcategory;
    filterAndDisplayCards();
    goToScreen('screen-cards');
    console.log(`[CTI] Filter: ${category}/${subcategory}`);
}

function normalizeCountryCode(code) {
    if (code == null) return '';
    const value = String(code).trim();
    const aliases = {
        russia: 'RU', ru: 'RU', RU: 'RU',
        eua: 'US', usa: 'US', us: 'US', US: 'US',
        china: 'CN', cn: 'CN', CN: 'CN',
        coreia_norte: 'KP', kp: 'KP', KP: 'KP',
        ira: 'IR', iran: 'IR', ir: 'IR', IR: 'IR',
        israel: 'IL', il: 'IL', IL: 'IL',
        india: 'IN', in: 'IN', IN: 'IN',
        brasil: 'BR', brazil: 'BR', br: 'BR', BR: 'BR',
        eu: 'EU', ue: 'EU', EU: 'EU',
        global: 'global', un: 'global', UN: 'global'
    };
    if (aliases[value] != null) return aliases[value];
    const lower = value.toLowerCase();
    if (aliases[lower] != null) return aliases[lower];
    return value;
}

function actorCountryCode(item) {
    return normalizeCountryCode(item.countryCode || item.countryId || item.paisCode || item.paisId || '');
}

function filterAndDisplayCards() {
    const { selectedCountry, selectedCategory, selectedSubcategory } = appState;
    const data = cyberDatabase[selectedCategory]?.[selectedSubcategory] || [];
    console.log(`[CTI] Subcategory pool size: ${data.length}`);

    const target = normalizeCountryCode(selectedCountry);
    appState.filteredData = data.filter(item => actorCountryCode(item) === target);
    console.log(`[CTI] Cards after country filter: ${appState.filteredData.length} (country=${target})`);

    renderGridCards();
}

function renderGridCards() {
    const container = document.getElementById('cards-container');
    container.innerHTML = '';
    const lang = appState.currentLanguage;

    if (appState.filteredData.length === 0) {
        const alert = document.createElement('div');
        alert.className = 'tactical-alert col-span-full';

        const icon = document.createElement('div');
        icon.className = 'tactical-alert-icon';
        icon.textContent = '⚠️';

        const message = document.createElement('div');
        message.className = 'tactical-alert-message';
        message.textContent = lang === 'pt'
            ? 'NENHUMA AMEAÇA ATIVA DETECTADA NESTE SETOR'
            : 'NO ACTIVE THREATS DETECTED IN THIS SECTOR';

        const subMessage = document.createElement('div');
        subMessage.className = 'tactical-alert-submessage';
        subMessage.textContent = lang === 'pt'
            ? 'Esta combinação de filtros não possui atores cadastrados.'
            : 'This filter combination has no registered threat actors.';

        const backButton = document.createElement('button');
        backButton.className = 'tactical-alert-btn';
        backButton.textContent = lang === 'pt' ? '← VOLTAR' : '← BACK';
        backButton.addEventListener('click', () => goToScreen('screen-category'));

        alert.appendChild(icon);
        alert.appendChild(message);
        alert.appendChild(subMessage);
        alert.appendChild(backButton);
        container.appendChild(alert);
        return;
    }

    appState.filteredData.forEach(threat => {
        container.appendChild(createCard(threat, lang));
    });
    console.log(`[CTI] Rendered ${appState.filteredData.length} cards`);
}

// Alias requested in architecture docs
function renderCards() {
    return renderGridCards();
}

function createCard(threat, lang) {
    const card = document.createElement('article');
    card.className = 'rpg-card cursor-pointer';
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.setAttribute('aria-label', String(threat.name || threat.nome || 'Threat actor'));
    card.style.touchAction = 'manipulation';
    applyCardStyle(card, threat);

    let opening = false;
    const openDossier = (e) => {
        if (opening) return;
        opening = true;
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        openDetailModal(threat, lang);
        // Allow re-open after modal close cycle
        setTimeout(() => { opening = false; }, 400);
    };

    // Immediate single-tap on mobile (no 300ms hover delay / no double-tap)
    card.addEventListener('pointerup', (e) => {
        if (e.pointerType === 'touch' || e.pointerType === 'pen') {
            openDossier(e);
        }
    }, { passive: false });

    card.addEventListener('click', (e) => {
        // Desktop / keyboard-emulated click only (touch already handled via pointerup)
        if (e.pointerType === 'touch' || e.pointerType === 'pen') return;
        openDossier(e);
    });

    card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            openDossier(e);
        }
    });

    const header = document.createElement('div');
    header.className = 'card-header';

    const title = document.createElement('div');
    title.className = 'card-title';
    // DOM textContent assignment — no HTML parse; XSS-safe without entity encoding
    title.textContent = threat.name || threat.nome || '';

    const flag = document.createElement('span');
    const code = actorCountryCode(threat);
    const flagClass = getFlagIconClass(code);
    if (flagClass === 'global-icon') {
        flag.className = 'card-flag-emoji';
        const countryData = countries.find(c => c.code === code);
        flag.textContent = countryData ? countryData.flag : '🌐';
    } else {
        flag.className = `fi ${flagClass} card-flag-svg`;
    }

    header.appendChild(title);
    header.appendChild(flag);

    const imageContainer = document.createElement('div');
    imageContainer.className = 'card-image-container pixelated-screen';

    const imagePlaceholder = document.createElement('div');
    imagePlaceholder.className = 'card-placeholder';

    const img = document.createElement('img');
    img.src = getClassImagePath(threat);
    img.alt = threat.name || threat.nome || 'Threat actor';
    img.className = 'card-class-image';
    img.loading = 'lazy';
    img.draggable = false;
    img.onerror = function() {
        handleCardImageError(this, threat);
    };
    imagePlaceholder.appendChild(img);
    imageContainer.appendChild(imagePlaceholder);

    const body = document.createElement('div');
    body.className = 'card-body';

    const specialty = document.createElement('div');
    specialty.className = 'card-specialty';
    const specialtyObj = threat.specialty || threat.especialidade || {};
    specialty.textContent = specialtyObj[lang] || specialtyObj.pt || '';
    body.appendChild(specialty);

    const footer = document.createElement('div');
    footer.className = 'card-footer';
    const stars = resolveStars(threat);
    const rarity = renderThreatScale(stars);
    rarity.classList.add('card-rarity', 'flex', 'items-center', 'justify-center', 'space-x-0.5');
    footer.appendChild(rarity);

    card.appendChild(header);
    card.appendChild(imageContainer);
    card.appendChild(body);
    card.appendChild(footer);
    return card;
}

/**
 * Resolve threat rank (0–5).
 * Priority: card.stars → rarity string → tactical score.
 */
function resolveStars(card) {
    if (card == null) return 0;

    if (typeof card === 'number') {
        return Math.min(5, Math.max(0, Math.round(card)));
    }

    if (typeof card === 'string') {
        const matches = card.match(/\u2B50|\u2605/g);
        if (matches) return Math.min(5, matches.length);
        const n = parseInt(card, 10);
        return Number.isFinite(n) ? Math.min(5, Math.max(0, n)) : 0;
    }

    if (typeof card === 'object') {
        if (Number.isFinite(card.stars)) {
            return Math.min(5, Math.max(0, Math.round(card.stars)));
        }
        if (Number.isFinite(card.estrelas)) {
            return Math.min(5, Math.max(0, Math.round(card.estrelas)));
        }
        if (card.rarity != null) {
            return resolveStars(card.rarity);
        }
        if (card.raridade != null) {
            return resolveStars(card.raridade);
        }
        const tac = card.tactical ?? card.tac;
        if (Number.isFinite(tac)) {
            if (tac >= 95) return 5;
            if (tac >= 85) return 4;
            if (tac >= 70) return 3;
            if (tac >= 50) return 2;
            return 1;
        }
    }
    return 0;
}

/** GTA Wanted-style threat scale (dynamic star count). */
function renderThreatScale(stars) {
    const count = Math.min(5, Math.max(0, Math.round(Number(stars) || 0)));
    const wrap = document.createElement('div');
    wrap.className = 'tactical-stars flex items-center space-x-0.5';
    wrap.setAttribute('aria-label', `Threat Level ${count}`);
    wrap.dataset.stars = String(count);

    for (let i = 0; i < count; i++) {
        wrap.appendChild(createMilitaryStarSVG(16));
    }
    return wrap;
}

function renderThreatScaleHTML(stars, size = 18) {
    const count = Math.min(5, Math.max(0, Math.round(Number(stars) || 0)));
    let icons = '';
    for (let i = 0; i < count; i++) {
        icons += `
            <svg class="tactical-star-icon inline-block filter drop-shadow-[0_0_3px_#FFD700]"
                 viewBox="0 0 24 24" width="${size}" height="${size}" aria-hidden="true">
                <polygon points="12,2 15,9 22,9 17,14 19,21 12,17 5,21 7,14 2,9 9,9"
                         fill="#FFD700" stroke="#000000" stroke-width="2"
                         stroke-linejoin="round" paint-order="stroke fill"/>
            </svg>`;
    }
    return `<div class="tactical-stars flex items-center space-x-0.5" data-stars="${count}" aria-label="Threat Level ${count}">${icons}</div>`;
}

function getRarityCount(source) {
    return resolveStars(source);
}

function createMilitaryStarSVG(size = 14) {
    const svgNS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('width', String(size));
    svg.setAttribute('height', String(size));
    svg.setAttribute('aria-hidden', 'true');
    svg.classList.add('tactical-star-icon', 'inline-block', 'filter', 'drop-shadow-[0_0_3px_#FFD700]');

    const polygon = document.createElementNS(svgNS, 'polygon');
    polygon.setAttribute('points', '12,2 15,9 22,9 17,14 19,21 12,17 5,21 7,14 2,9 9,9');
    polygon.setAttribute('fill', '#FFD700');
    polygon.setAttribute('stroke', '#000000');
    polygon.setAttribute('stroke-width', '2');
    polygon.setAttribute('stroke-linejoin', 'round');
    polygon.setAttribute('paint-order', 'stroke fill');
    svg.appendChild(polygon);
    return svg;
}

const GENERIC_CARD_IMAGE_PATHS = new Set([
    'assets/images/class_groups.jpg',
    'assets/images/class_individuals.jpg',
    'assets/images/class_organizations.jpg',
    'assets/images/class_espionage.jpg',
    'assets/images/profit.jpg',
    'assets/images/osint.jpg',
    'assets/images/associated.jpg',
    'assets/images/associate.jpg',
    'assets/images/famous.jpg',
    'assets/images/enforcement.jpg',
    'assets/images/enforce.jpg',
    'assets/images/military.jpg',
    'assets/images/group.jpg',
    'assets/images/groups.jpg',
    'assets/images/persons.jpg',
    'assets/images/person.jpg',
    'assets/images/gov.jpg',
    'assets/images/govs.jpg',
    'assets/images/gru.jpg'
]);

function isRealCardImage(src) {
    if (!src || typeof src !== 'string') return false;
    const value = src.trim();
    if (!value) return false;
    if (/^https?:\/\//i.test(value)) return true;
    if (!value.includes('/') && !value.includes('\\')) return false;
    const normalized = value.replace(/\\/g, '/').toLowerCase();
    if (GENERIC_CARD_IMAGE_PATHS.has(normalized)) return false;
    return /\.(jpe?g|png|webp|gif|svg)(\?.*)?$/i.test(value);
}

function getCategoryClassArt(card) {
    const cat = card.category || card.categoria;
    const sub = card.subcategory || card.subcategoria || appState.selectedSubcategory;

    if (cat === 'groups' || cat === 'grupos') {
        if (sub === 'profit' || sub === 'lucro') return 'assets/images/profit.jpg';
        if (sub === 'osint_sigint') return 'assets/images/osint.jpg';
        if (sub === 'government' || sub === 'governo') return 'assets/images/associated.jpg';
        return 'assets/images/class_groups.jpg';
    }
    if (cat === 'organizations' || cat === 'organizacoes') {
        if (sub === 'military_espionage' || sub === 'espionagem_militar') {
            return 'assets/images/class_espionage.jpg';
        }
        return 'assets/images/enforce.jpg';
    }
    if (cat === 'individuals' || cat === 'individuos') {
        return 'assets/images/famous.jpg';
    }
    return 'assets/images/class_groups.jpg';
}

function getClassImagePath(threat) {
    const own =
        (typeof threat.image === 'string' && threat.image.trim()) ||
        (typeof threat.imagem === 'string' && threat.imagem.trim()) ||
        (typeof threat.imagePlaceholder === 'string' && threat.imagePlaceholder.trim()) ||
        '';

    if (isRealCardImage(own)) {
        const src = own.trim();
        if (/^https?:\/\/([^/]*\.)?fbi\.gov\//i.test(src)) {
            return getCategoryClassArt(threat);
        }
        return src;
    }
    return getCategoryClassArt(threat);
}

function handleCardImageError(img, threat) {
    if (!img) return;
    const tried = img.dataset.fallbackStep || '0';
    const chain = [
        getCategoryClassArt(threat),
        'assets/images/famous.jpg',
        'assets/images/person.jpg',
        'assets/images/class_groups.jpg',
        'assets/images/gru.jpg'
    ];
    const next = parseInt(tried, 10) || 0;
    if (next < chain.length) {
        img.dataset.fallbackStep = String(next + 1);
        img.src = chain[next];
    } else {
        img.onerror = null;
        img.style.display = 'none';
    }
}

function applyCardStyle(card, threat) {
    const cat = threat.category || threat.categoria;
    const subcategory = (cat === 'individuals' || cat === 'individuos')
        ? (threat.subcategory || threat.subcategoria || 'famous')
        : (threat.subcategory || threat.subcategoria || appState.selectedSubcategory);
    card.classList.add(getCardBackgroundClass(subcategory));
}

function getCardBackgroundClass(subcategory) {
    const classMap = {
        profit: 'bg-profit',
        lucro: 'bg-profit',
        government: 'bg-government',
        governo: 'bg-government',
        osint_sigint: 'bg-osint-sigint',
        famous: 'bg-famous',
        famosos: 'bg-famous',
        defense_law: 'bg-defense-law',
        defesa_lei: 'bg-defense-law',
        military_espionage: 'bg-military-espionage',
        espionagem_militar: 'bg-military-espionage'
    };
    return classMap[subcategory] || 'bg-default';
}

// ═══════════════════════════════════════════════════════════════
// INTELLIGENCE DOSSIER MODAL
// ═══════════════════════════════════════════════════════════════

function calculateLevels(rarity) {
    const stars = getRarityCount(rarity);
    const baseLevel = stars * 20;
    const tactical = Math.min(100, baseLevel + Math.floor(Math.random() * 10));
    const strategic = Math.min(100, baseLevel + Math.floor(Math.random() * 10));
    return { tactical, strategic };
}

function openThreatModal(threat, lang) {
    const modal = document.getElementById('threat-modal');
    const modalBody = document.getElementById('modal-body');
    const modalWrapper = modal.querySelector('.modal-content-wrapper');

    const fallbackLevels = calculateLevels(threat.rarity || threat.raridade);
    const tacTarget = Number.isFinite(threat.tactical)
        ? threat.tactical
        : (Number.isFinite(threat.tac) ? threat.tac : fallbackLevels.tactical);
    const estTarget = Number.isFinite(threat.strategic)
        ? threat.strategic
        : (Number.isFinite(threat.est) ? threat.est : fallbackLevels.strategic);

    const code = actorCountryCode(threat);
    const countryData = countries.find(c => c.code === code);
    const flagClass = getFlagIconClass(code);

    let countryFlagHTML = '';
    if (flagClass === 'global-icon') {
        countryFlagHTML = `<span class="modal-flag-emoji">${sanitizeXSS(countryData ? countryData.flag : '🌐')}</span>`;
    } else {
        countryFlagHTML = `<span class="fi ${sanitizeXSS(flagClass)} modal-flag-svg"></span>`;
    }

    const modalLayoutClasses = [
        'modal-content-wrapper',
        'flex', 'flex-col',
        'max-w-lg', 'md:max-w-2xl', 'lg:max-w-3xl',
        'w-[92vw]',
        'max-h-[85vh]', 'lg:max-h-[90vh]',
        'overflow-y-auto',
        'min-h-0',
        'rounded-md',
        'border', 'border-zinc-800',
        'bg-black',
        getCardBackgroundClass(appState.selectedSubcategory)
    ].join(' ');

    modalWrapper.className = modalLayoutClasses;

    const actorName = threat.name || threat.nome || 'Unknown';
    const descObj = threat.description || threat.descricao || {};
    const specObj = threat.specialty || threat.especialidade || {};

    // InfoSec: sanitize all untrusted MITRE/data.js fields before HTML concatenation
    const safeName = sanitizeXSS(actorName);
    const safeType = sanitizeXSS(resolveOperationalTypeLabel(threat, lang || globalLanguage));
    const safeDescription = sanitizeXSS(descObj[lang] || descObj.pt || '');
    const safeSpecialty = sanitizeXSS(specObj[lang] || specObj.pt || '');
    const safeImageSrc = sanitizeImageURL(getClassImagePath(threat)) || sanitizeImageURL(getCategoryClassArt(threat));

    modalBody.innerHTML = `
        <div class="modal-dossier-layout">
            <div class="modal-visual">
                <div class="modal-image-container pixelated-screen">
                    <div class="modal-image-placeholder">
                        <img src="${safeImageSrc}" alt="${safeName}" class="modal-class-image relative block w-full h-44 md:h-64 lg:h-72 object-cover object-center" onerror="handleImageError(this);">
                    </div>
                </div>
            </div>

            <div class="modal-intel p-4 md:p-6 lg:p-8">
                <div class="modal-header">
                    <div class="modal-title">
                        ${lang === 'pt' ? 'DOSSIÊ DE INTELIGÊNCIA' : 'INTELLIGENCE BRIEF'}
                    </div>
                    <div class="modal-subtitle">
                        ${countryFlagHTML}
                        <span style="flex: 1; min-width: 0; word-break: break-word;">${safeName}</span>
                        ${renderThreatScaleHTML(resolveStars(threat), 18)}
                    </div>
                </div>

                <div class="modal-section">
                    <div class="modal-section-title">${lang === 'pt' ? 'Classificação Operacional' : 'Operational Classification'}</div>
                    <div class="modal-type-badge">
                        ${safeType}
                    </div>
                </div>

                <div class="modal-section">
                    <div class="modal-section-title">${lang === 'pt' ? 'Análise Táctica' : 'Tactical Analysis'}</div>
                    <div class="modal-description">
                        ${safeDescription}
                    </div>
                </div>

                <div class="modal-section">
                    <div class="modal-section-title">${lang === 'pt' ? 'Especialidade Técnica' : 'Technical Specialty'}</div>
                    <div class="modal-specialty">
                        ${safeSpecialty}
                    </div>
                </div>

                <div class="modal-section">
                    <div class="modal-section-title">${lang === 'pt' ? 'Capacidade Operacional' : 'Operational Capability'}</div>
                    <div class="stats-container">
                        <div class="stat-item">
                            <div class="stat-label">
                                <span class="stat-name">${lang === 'pt' ? 'Nível Tático (TAC)' : 'Tactical Level (TAC)'}</span>
                                <span class="stat-value" data-counter="${tacTarget}">0/100</span>
                            </div>
                            <div class="progress-bar-container">
                                <div class="progress-bar transition-all duration-500" data-target="${tacTarget}" style="width: 0%;"></div>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">
                                <span class="stat-name">${lang === 'pt' ? 'Nível Estratégico (EST)' : 'Strategic Level (EST)'}</span>
                                <span class="stat-value" data-counter="${estTarget}">0/100</span>
                            </div>
                            <div class="progress-bar-container">
                                <div class="progress-bar transition-all duration-500" data-target="${estTarget}" style="width: 0%;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    setTimeout(() => {
        animateOperationalStats(modalBody);
    }, 80);

    console.log(`[CTI] Modal open: ${actorName} | TAC ${tacTarget} | EST ${estTarget}`);
}

/**
 * Operational classification badge for cards/modal.
 * Maps subcategory → clean bilingual UI labels (never raw polluted type strings).
 */
function resolveOperationalTypeLabel(threat, lang = globalLanguage) {
    const language = (lang === 'en' || lang === 'pt') ? lang : globalLanguage;
    const sub = String(threat?.subcategory || threat?.subcategoria || '').trim().toLowerCase();

    const keyBySubcategory = {
        military_espionage: 'subcat-espionage-military',
        espionagem_militar: 'subcat-espionage-military',
        defense_law: 'subcat-defense-law',
        defesa_lei: 'subcat-defense-law',
        profit: 'subcat-profit',
        lucro: 'subcat-profit',
        government: 'subcat-government',
        governo: 'subcat-government',
        osint_sigint: 'subcat-osint-sigint',
        famous: 'subcat-famous',
        famosos: 'subcat-famous'
    };

    const dictKey = keyBySubcategory[sub];
    const fromDict = dictKey && translations?.[language]?.[dictKey];
    if (fromDict) return fromDict;

    // Last resort: type field, but strip known PT/EN hybrids from the builder
    const typeObj = threat?.type || threat?.tipo || {};
    const raw = String(typeObj[language] || typeObj.pt || typeObj.en || '').trim();
    if (/ag[eê]ncia\s+(intelligence|military|national\s*cert)/i.test(raw) ||
        /^(intelligence|military)\s+agency$/i.test(raw)) {
        const fallbackKey = (sub === 'military_espionage' || /intel|militar|espion/i.test(raw))
            ? 'subcat-espionage-military'
            : 'subcat-defense-law';
        return translations?.[language]?.[fallbackKey] || raw;
    }
    return raw;
}

function openDetailModal(threat, lang) {
    return openThreatModal(threat, lang);
}

function animateOperationalStats(modalBody, durationMs = 500) {
    const progressBars = modalBody.querySelectorAll('.progress-bar[data-target]');
    const counters = modalBody.querySelectorAll('.stat-value[data-counter]');
    const startTime = performance.now();

    progressBars.forEach(bar => {
        bar.style.transition = `width ${durationMs}ms ease-out`;
        // Force reflow so width:0% → target animates fluidly on mobile
        void bar.offsetWidth;
        bar.style.width = `${bar.getAttribute('data-target')}%`;
    });

    function tick(now) {
        const elapsed = now - startTime;
        const progress = Math.min(1, elapsed / durationMs);
        const eased = 1 - Math.pow(1 - progress, 2);

        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-counter'), 10) || 0;
            counter.textContent = `${Math.round(target * eased)}/100`;
        });

        if (progress < 1) {
            requestAnimationFrame(tick);
        } else {
            counters.forEach(counter => {
                const target = parseInt(counter.getAttribute('data-counter'), 10) || 0;
                counter.textContent = `${target}/100`;
            });
        }
    }

    requestAnimationFrame(tick);
}

function handleImageError(img) {
    console.log('[CTI] Broken image detected — applying local fallback');
    img.onerror = function() {
        this.onerror = null;
        this.src = 'assets/images/famous.jpg';
    };
    img.src = 'assets/images/class_individuals.jpg';
}

function closeThreatModal() {
    document.getElementById('threat-modal').classList.remove('active');
    document.body.style.overflow = 'auto';
    console.log('[CTI] Modal closed');
}

function initializeModal() {
    document.getElementById('modal-close').addEventListener('click', closeThreatModal);

    document.getElementById('threat-modal').addEventListener('click', (e) => {
        if (e.target.id === 'threat-modal') {
            closeThreatModal();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && document.getElementById('threat-modal').classList.contains('active')) {
            closeThreatModal();
        }
        if (e.key === 'Escape' && !document.getElementById('donate-modal').classList.contains('hidden')) {
            closeDonateModal();
        }
    });
}

// ═══════════════════════════════════════════════════════════════
// DONATION PANEL — BITCOIN
// ═══════════════════════════════════════════════════════════════

const BTC_WALLET_ADDRESS = 'bc1qplt644jvesg0aewdutwz5wxhrzr9mdlma5pz6n';

function getBitcoinQrUrl(address) {
    const data = encodeURIComponent(address);
    return `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${data}&bgcolor=000000&color=00f0ff&qzone=2`;
}

function initializeDonatePanel() {
    const btn = document.getElementById('btn-donate');
    const modal = document.getElementById('donate-modal');
    const closeBtn = document.getElementById('donate-modal-close');
    const copyBtn = document.getElementById('btn-copy-btc');
    const codeEl = document.getElementById('btc-wallet-address');
    const qrImg = document.getElementById('donate-qr');

    if (!btn || !modal || !codeEl || !qrImg) return;

    codeEl.textContent = BTC_WALLET_ADDRESS;
    qrImg.src = getBitcoinQrUrl(BTC_WALLET_ADDRESS);
    qrImg.alt = `Bitcoin QR Code ${BTC_WALLET_ADDRESS}`;

    btn.addEventListener('click', openDonateModal);
    closeBtn?.addEventListener('click', closeDonateModal);
    modal.addEventListener('click', (e) => {
        if (e.target.id === 'donate-modal') closeDonateModal();
    });
    copyBtn?.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(BTC_WALLET_ADDRESS);
            const lang = appState.currentLanguage;
            copyBtn.textContent = lang === 'pt' ? 'COPIADO' : 'COPIED';
            setTimeout(() => {
                copyBtn.textContent = translations[lang]?.['donate-copy'] || 'COPY ADDRESS';
            }, 1400);
        } catch (err) {
            console.warn('[CTI] Failed to copy BTC address:', err);
        }
    });
}

function openDonateModal() {
    const modal = document.getElementById('donate-modal');
    if (!modal) return;
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeDonateModal() {
    const modal = document.getElementById('donate-modal');
    if (!modal) return;
    modal.classList.add('hidden');
    if (!document.getElementById('threat-modal')?.classList.contains('active')) {
        document.body.style.overflow = 'auto';
    }
}

// ═══════════════════════════════════════════════════════════════
// DEBUG API
// ═══════════════════════════════════════════════════════════════

window.cyberTacticalRPG = {
    state: appState,
    database: cyberDatabase,
    countries,
    translations,
    countryProfiles: typeof countryProfiles !== 'undefined' ? countryProfiles : {},
    security: {
        sanitizeXSS,
        escapeHTML,
        sanitizeImageURL
    },
    actions: {
        changeLanguage,
        goToScreen,
        selectCountry,
        selectSubcategory,
        openLiveMap,
        closeLiveMap,
        openDetailModal,
        renderGridCards,
        openDonateModal,
        closeDonateModal
    }
};

console.log('[CTI TACTICAL RPG] Debug API exposed at window.cyberTacticalRPG');
