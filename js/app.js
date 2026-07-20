// ═══════════════════════════════════════════════════════════════
// CYBER THREAT INTELLIGENCE PORTFOLIO - TACTICAL RPG ENGINE
// Arquitetura: País → Categoria → Cards RPG
// ═══════════════════════════════════════════════════════════════

// Estado Global da Aplicação
const appState = {
    currentScreen: 'screen-geopolitics',
    currentLanguage: 'pt',
    selectedCountry: null,
    selectedCategory: null,
    selectedSubcategory: null,
    filteredData: []
};

// Inicialização Principal
document.addEventListener('DOMContentLoaded', () => {
    console.log('[CTI TACTICAL RPG] Inicializando sistema...');
    
    initializeLanguage();
    initializeNavigation();
    initializeFilters();
    initializeModal();
    updateLanguage();
    
    // Garantir que apenas a Tela 1 (Geopolítica) esteja visível
    goToScreen('screen-geopolitics');
    renderCountries();
    
    console.log('[CTI TACTICAL RPG] Sistema operacional.');
});

// ═══════════════════════════════════════════════════════════════
// SISTEMA DE IDIOMAS (PT/EN)
// ═══════════════════════════════════════════════════════════════

function initializeLanguage() {
    const btnPT = document.getElementById('lang-pt');
    const btnEN = document.getElementById('lang-en');
    
    btnPT.addEventListener('click', () => changeLanguage('pt'));
    btnEN.addEventListener('click', () => changeLanguage('en'));
    
    updateLanguageButtons();
}

function changeLanguage(lang) {
    appState.currentLanguage = lang;
    updateLanguageButtons();
    updateLanguage();
    
    // Re-renderizar conteúdo dinâmico
    if (appState.currentScreen === 'screen-geopolitics') {
        renderCountries();
    } else if (appState.currentScreen === 'screen-cards') {
        renderCards();
    }
    
    console.log(`[CTI] Idioma alterado para: ${lang.toUpperCase()}`);
}

function updateLanguageButtons() {
    const btnPT = document.getElementById('lang-pt');
    const btnEN = document.getElementById('lang-en');
    
    btnPT.classList.toggle('active', appState.currentLanguage === 'pt');
    btnEN.classList.toggle('active', appState.currentLanguage === 'en');
}

function updateLanguage() {
    const lang = appState.currentLanguage;
    const elements = document.querySelectorAll('[data-lang]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-lang');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
}

// ═══════════════════════════════════════════════════════════════
// SISTEMA DE NAVEGAÇÃO ENTRE TELAS (Funil Geopolítico)
// ═══════════════════════════════════════════════════════════════

function initializeNavigation() {
    // Voltar: Tela 2 → Tela 1
    document.getElementById('btn-back-countries').addEventListener('click', () => {
        goToScreen('screen-geopolitics');
        appState.selectedCountry = null;
        console.log('[CTI] Navegação: Retornando para Seleção de Países');
    });
    
    // Voltar: Tela 3 → Tela 2
    document.getElementById('btn-back-category').addEventListener('click', () => {
        goToScreen('screen-category');
        appState.selectedCategory = null;
        appState.selectedSubcategory = null;
        console.log('[CTI] Navegação: Retornando para Seleção de Categoria');
    });
}

function goToScreen(screenId) {
    // Esconder todas as telas
    const allScreens = document.querySelectorAll('.screen');
    allScreens.forEach(screen => screen.classList.add('hidden'));
    
    // Mostrar apenas a tela alvo
    const targetScreen = document.getElementById(screenId);
    targetScreen.classList.remove('hidden');
    
    appState.currentScreen = screenId;
    console.log(`[CTI] Tela ativa: ${screenId}`);
}

// ═══════════════════════════════════════════════════════════════
// TELA 1: RENDERIZAÇÃO DE PAÍSES
// ═══════════════════════════════════════════════════════════════

function renderCountries() {
    const container = document.getElementById('countries-container');
    container.innerHTML = '';
    
    const lang = appState.currentLanguage;
    
    countries.forEach(country => {
        const btn = document.createElement('button');
        btn.className = 'country-btn';
        btn.onclick = () => selectCountry(country.code);
        
        // Emoji da bandeira
        const flagDiv = document.createElement('div');
        flagDiv.className = 'text-6xl';
        flagDiv.textContent = country.flag;
        
        // Nome do país
        const nameDiv = document.createElement('div');
        nameDiv.className = 'country-name';
        nameDiv.textContent = country.name[lang];
        
        btn.appendChild(flagDiv);
        btn.appendChild(nameDiv);
        container.appendChild(btn);
    });
    
    console.log(`[CTI] Renderizados ${countries.length} países`);
}

function selectCountry(countryCode) {
    appState.selectedCountry = countryCode;
    console.log(`[CTI] País selecionado: ${countryCode}`);
    
    // Avançar para Tela 2 (Categorias)
    goToScreen('screen-category');
}

// ═══════════════════════════════════════════════════════════════
// TELA 2: SISTEMA DE FILTROS (Subcategorias)
// ═══════════════════════════════════════════════════════════════

function initializeFilters() {
    const subcategoryButtons = document.querySelectorAll('.subcategory-btn');
    subcategoryButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const category = e.target.getAttribute('data-category');
            const subcategory = e.target.getAttribute('data-subcategory');
            selectSubcategory(category, subcategory);
        });
    });
}

function selectSubcategory(category, subcategory) {
    appState.selectedCategory = category;
    appState.selectedSubcategory = subcategory;
    
    console.log(`[CTI] Filtro selecionado: ${category} > ${subcategory}`);
    
    // Filtrar e exibir cards
    filterAndDisplayCards();
    goToScreen('screen-cards');
}

// ═══════════════════════════════════════════════════════════════
// TELA 3: FILTRAGEM E RENDERIZAÇÃO DE CARDS RPG
// ═══════════════════════════════════════════════════════════════

function filterAndDisplayCards() {
    const { selectedCountry, selectedCategory, selectedSubcategory } = appState;
    
    // Obter dados da subcategoria
    const data = cyberDatabase[selectedCategory]?.[selectedSubcategory] || [];
    
    console.log(`[CTI] Dados disponíveis na subcategoria: ${data.length}`);
    
    // Filtrar por país
    if (selectedCountry === 'UN' || selectedCountry === 'EU') {
        // Países globais: mostrar todos
        appState.filteredData = data;
    } else {
        // Filtrar por código do país
        appState.filteredData = data.filter(item => item.paisCode === selectedCountry);
    }
    
    console.log(`[CTI] Cards filtrados para exibição: ${appState.filteredData.length}`);
    
    renderCards();
}

function renderCards() {
    const container = document.getElementById('cards-container');
    container.innerHTML = '';
    
    const lang = appState.currentLanguage;
    
    // SISTEMA DE ALERTA TÁTICO: Nenhuma Ameaça Detectada
    if (appState.filteredData.length === 0) {
        const alert = document.createElement('div');
        alert.className = 'tactical-alert col-span-full';
        
        // Ícone de Alerta
        const icon = document.createElement('div');
        icon.className = 'tactical-alert-icon';
        icon.textContent = '⚠️';
        
        // Mensagem Principal
        const message = document.createElement('div');
        message.className = 'tactical-alert-message';
        message.textContent = lang === 'pt' 
            ? 'NENHUMA AMEAÇA ATIVA DETECTADA NESTE SETOR'
            : 'NO ACTIVE THREATS DETECTED IN THIS SECTOR';
        
        // Submensagem
        const subMessage = document.createElement('div');
        subMessage.className = 'tactical-alert-submessage';
        subMessage.textContent = lang === 'pt'
            ? 'Esta combinação de filtros não possui atores cadastrados.'
            : 'This filter combination has no registered threat actors.';
        
        // Botão de Voltar
        const backButton = document.createElement('button');
        backButton.className = 'tactical-alert-btn';
        backButton.textContent = lang === 'pt' ? '← VOLTAR' : '← BACK';
        backButton.addEventListener('click', () => {
            goToScreen('screen-category');
        });
        
        alert.appendChild(icon);
        alert.appendChild(message);
        alert.appendChild(subMessage);
        alert.appendChild(backButton);
        
        container.appendChild(alert);
        console.log('[CTI] Alerta tático exibido: Nenhum ator encontrado');
        return;
    }
    
    // Renderizar cards normalmente
    appState.filteredData.forEach(threat => {
        const card = createCard(threat, lang);
        container.appendChild(card);
    });
    
    console.log(`[CTI] ${appState.filteredData.length} cards renderizados`);
}

function createCard(threat, lang) {
    const card = document.createElement('div');
    card.className = `rpg-card ${getCardBackgroundClass(appState.selectedSubcategory)}`;
    
    // Evento de clique: abrir modal
    card.addEventListener('click', () => {
        openThreatModal(threat, lang);
    });
    
    // Header do card
    const header = document.createElement('div');
    header.className = 'card-header';
    
    const title = document.createElement('div');
    title.className = 'card-title';
    title.textContent = threat.nome;
    
    const flag = document.createElement('div');
    flag.className = 'text-4xl';
    const countryData = countries.find(c => c.code === threat.paisCode);
    flag.textContent = countryData ? countryData.flag : '🌐';
    
    header.appendChild(title);
    header.appendChild(flag);
    
    // Container de imagem
    const imageContainer = document.createElement('div');
    imageContainer.className = 'card-image-container';
    
    const imagePlaceholder = document.createElement('div');
    imagePlaceholder.className = 'card-placeholder';
    
    // Renderizar imagem ou emoji
    if (threat.imagePlaceholder && threat.imagePlaceholder.startsWith('assets/')) {
        const img = document.createElement('img');
        img.src = threat.imagePlaceholder;
        img.alt = threat.nome;
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        img.onerror = function() {
            this.style.display = 'none';
            imagePlaceholder.textContent = '🎯';
        };
        imagePlaceholder.appendChild(img);
    } else {
        imagePlaceholder.textContent = threat.imagePlaceholder || '🎯';
    }
    
    imageContainer.appendChild(imagePlaceholder);
    
    // Body do card (Especialidade)
    const body = document.createElement('div');
    body.className = 'card-body';
    
    const specialty = document.createElement('div');
    specialty.className = 'card-specialty';
    specialty.textContent = threat.especialidade[lang] || threat.especialidade.pt;
    
    body.appendChild(specialty);
    
    // Footer do card (Raridade)
    const footer = document.createElement('div');
    footer.className = 'card-footer';
    
    const rarity = document.createElement('div');
    rarity.className = 'card-rarity';
    rarity.textContent = threat.raridade;
    
    footer.appendChild(rarity);
    
    // Montar card completo
    card.appendChild(header);
    card.appendChild(imageContainer);
    card.appendChild(body);
    card.appendChild(footer);
    
    return card;
}

// Retorna a classe CSS de fundo baseada na subcategoria
function getCardBackgroundClass(subcategory) {
    const classMap = {
        // Grupos
        'lucro': 'bg-lucro',
        'governo': 'bg-governo',
        'osint_sigint': 'bg-osint-sigint',
        
        // Indivíduos
        'lendas': 'bg-lendas',
        'especialistas': 'bg-especialistas',
        
        // Organizações
        'militares': 'bg-militares',
        'inteligencia': 'bg-inteligencia',
        'policia_especializada': 'bg-policia'
    };
    
    return classMap[subcategory] || 'bg-default';
}

// ═══════════════════════════════════════════════════════════════
// MODAL: DOSSIÊ DE INTELIGÊNCIA HOLOGRÁFICO (ZOOM)
// ═══════════════════════════════════════════════════════════════

function calculateLevels(raridade) {
    const stars = (raridade.match(/⭐/g) || []).length;
    
    // Base: 20 pontos por estrela
    const baseLevel = stars * 20;
    
    // Adicionar variação aleatória mas consistente
    const tactical = Math.min(100, baseLevel + Math.floor(Math.random() * 10));
    const strategic = Math.min(100, baseLevel + Math.floor(Math.random() * 10));
    
    return { tactical, strategic };
}

function openThreatModal(threat, lang) {
    const modal = document.getElementById('threat-modal');
    const modalBody = document.getElementById('modal-body');
    const modalWrapper = modal.querySelector('.modal-content-wrapper');
    
    // Calcular níveis táticos
    const levels = calculateLevels(threat.raridade);
    
    // Obter dados do país
    const countryData = countries.find(c => c.code === threat.paisCode);
    const countryName = countryData ? countryData.name[lang] : 'Unknown';
    const countryFlag = countryData ? countryData.flag : '🌐';
    
    // Aplicar classe de fundo dinâmico ao wrapper do modal
    modalWrapper.className = `modal-content-wrapper ${getCardBackgroundClass(appState.selectedSubcategory)}`;
    
    // Montar conteúdo do modal
    modalBody.innerHTML = `
        <!-- Cabeçalho -->
        <div class="modal-header">
            <div class="modal-title">
                ${lang === 'pt' ? 'DOSSIÊ DE INTELIGÊNCIA' : 'INTELLIGENCE BRIEF'}
            </div>
            <div class="modal-subtitle">
                <span class="text-5xl">${countryFlag}</span>
                <span style="flex: 1;">${threat.nome}</span>
                <span class="text-yellow-400 text-3xl">${threat.raridade}</span>
            </div>
        </div>
        
        <!-- Imagem Ampliada -->
        <div class="modal-image-container">
            <div class="modal-image-placeholder">
                ${threat.imagePlaceholder && threat.imagePlaceholder.startsWith('assets/') 
                    ? `<img src="${threat.imagePlaceholder}" alt="${threat.nome}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.style.display='none'; this.parentElement.textContent='🎯';">` 
                    : (threat.imagePlaceholder || '🎯')}
            </div>
        </div>
        
        <!-- Tipo/Categoria -->
        <div class="modal-section">
            <div class="modal-section-title">${lang === 'pt' ? 'Classificação Operacional' : 'Operational Classification'}</div>
            <div style="display: inline-block; padding: 0.75rem 1.5rem; background: rgba(0, 240, 255, 0.1); border: 1px solid #00f0ff; border-radius: 0.5rem; color: #00f0ff; font-weight: 600;">
                ${threat.tipo[lang] || threat.tipo.pt}
            </div>
        </div>
        
        <!-- Descrição Detalhada -->
        <div class="modal-section">
            <div class="modal-section-title">${lang === 'pt' ? 'Análise Táctica' : 'Tactical Analysis'}</div>
            <div class="modal-description">
                ${threat.descricao[lang] || threat.descricao.pt}
            </div>
        </div>
        
        <!-- Especialidade -->
        <div class="modal-section">
            <div class="modal-section-title">${lang === 'pt' ? 'Especialidade Técnica' : 'Technical Specialty'}</div>
            <div class="modal-specialty">
                ${threat.especialidade[lang] || threat.especialidade.pt}
            </div>
        </div>
        
        <!-- Atributos Táticos (TAC/EST) -->
        <div class="modal-section">
            <div class="modal-section-title">${lang === 'pt' ? 'Capacidade Operacional' : 'Operational Capability'}</div>
            
            <div class="stats-container">
                <!-- Nível Tático -->
                <div class="stat-item">
                    <div class="stat-label">
                        <span class="stat-name">${lang === 'pt' ? 'Nível Tático (TAC)' : 'Tactical Level (TAC)'}</span>
                        <span class="stat-value">${levels.tactical}/100</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${levels.tactical}%;"></div>
                    </div>
                </div>
                
                <!-- Nível Estratégico -->
                <div class="stat-item">
                    <div class="stat-label">
                        <span class="stat-name">${lang === 'pt' ? 'Nível Estratégico (EST)' : 'Strategic Level (EST)'}</span>
                        <span class="stat-value">${levels.strategic}/100</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${levels.strategic}%;"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Mostrar modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    console.log(`[CTI] Modal aberto: ${threat.nome}`);
}

function closeThreatModal() {
    const modal = document.getElementById('threat-modal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
    
    console.log('[CTI] Modal fechado');
}

function initializeModal() {
    // Botão fechar
    document.getElementById('modal-close').addEventListener('click', closeThreatModal);
    
    // Fechar ao clicar fora do conteúdo
    document.getElementById('threat-modal').addEventListener('click', (e) => {
        if (e.target.id === 'threat-modal') {
            closeThreatModal();
        }
    });
    
    // Fechar com tecla ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeThreatModal();
        }
    });
}

// ═══════════════════════════════════════════════════════════════
// DEBUG: Expor estado global no console (Desenvolvimento)
// ═══════════════════════════════════════════════════════════════

window.cyberTacticalRPG = {
    state: appState,
    database: cyberDatabase,
    countries: countries,
    translations: translations,
    actions: {
        changeLanguage,
        goToScreen,
        selectCountry,
        selectSubcategory
    }
};

console.log('[CTI TACTICAL RPG] API de Debug exposta em: window.cyberTacticalRPG');
