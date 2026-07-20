// Cyber Threat Intelligence Portfolio - Lógica Principal
// NOVO FLUXO: País → Categoria → Cards

// Estado Global da Aplicação
const appState = {
    currentScreen: 'screen-geopolitics', // Começa na tela de países
    currentLanguage: 'pt',
    selectedCountry: null,
    selectedCategory: null,
    selectedSubcategory: null,
    filteredData: []
};

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    initializeLanguage();
    initializeNavigation();
    initializeFilters();
    initializeModal();
    updateLanguage();
    
    // Garantir que apenas a primeira tela (países) esteja visível
    goToScreen('screen-geopolitics');
    renderCountries();
});

// SISTEMA DE IDIOMAS
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
    
    // Re-renderizar cards se estiver na tela de cards
    if (appState.currentScreen === 'screen-cards') {
        renderCards();
    }
    
    // Re-renderizar países se estiver na tela de geopolítica
    if (appState.currentScreen === 'screen-geopolitics') {
        renderCountries();
    }
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

// SISTEMA DE NAVEGAÇÃO ENTRE TELAS - NOVO FLUXO
function initializeNavigation() {
    // Voltar de Categoria para Países
    document.getElementById('btn-back-countries').addEventListener('click', () => {
        goToScreen('screen-geopolitics');
        appState.selectedCountry = null;
    });
    
    // Voltar de Cards para Categoria
    document.getElementById('btn-back-category').addEventListener('click', () => {
        goToScreen('screen-category');
        appState.selectedCategory = null;
        appState.selectedSubcategory = null;
    });
}

function goToScreen(screenId) {
    // Esconder todas as telas
    const allScreens = document.querySelectorAll('.screen');
    allScreens.forEach(screen => {
        screen.classList.add('hidden');
    });
    
    // Mostrar apenas a tela selecionada
    const targetScreen = document.getElementById(screenId);
    targetScreen.classList.remove('hidden');
    
    appState.currentScreen = screenId;
    
    // Log para debug
    console.log(`[CTI] Navegando para: ${screenId}`);
}

function resetFilters() {
    appState.selectedCountry = null;
    appState.selectedCategory = null;
    appState.selectedSubcategory = null;
    appState.filteredData = [];
}

// RENDERIZAÇÃO DE PAÍSES (TELA 1 - AGORA É A PRIMEIRA)
function renderCountries() {
    const container = document.getElementById('countries-container');
    container.innerHTML = '';
    
    const lang = appState.currentLanguage;
    
    console.log(`[CTI] Renderizando ${countries.length} países`);
    
    countries.forEach(country => {
        const btn = document.createElement('button');
        btn.className = 'country-btn';
        btn.onclick = () => selectCountry(country.code);
        
        // Usar emoji de bandeira como placeholder
        const flagDiv = document.createElement('div');
        flagDiv.className = 'text-5xl';
        flagDiv.textContent = country.flag;
        
        const nameDiv = document.createElement('div');
        nameDiv.className = 'country-name';
        nameDiv.textContent = country.name[lang];
        
        btn.appendChild(flagDiv);
        btn.appendChild(nameDiv);
        container.appendChild(btn);
    });
}

function selectCountry(countryCode) {
    appState.selectedCountry = countryCode;
    
    console.log(`[CTI] País selecionado: ${countryCode}`);
    
    // Ir para a tela de categorias
    goToScreen('screen-category');
}

// SISTEMA DE FILTROS (TELA 2)
function initializeFilters() {
    // Listeners para botões de subcategoria
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
    
    console.log(`[CTI] Categoria selecionada: ${category} - ${subcategory}`);
    
    // Ir para a tela de cards
    filterAndDisplayCards();
    goToScreen('screen-cards');
}

// FILTRAGEM E RENDERIZAÇÃO DE CARDS (Tela 3)
function filterAndDisplayCards() {
    const { selectedCountry, selectedCategory, selectedSubcategory } = appState;
    
    // Obter dados da categoria/subcategoria selecionada
    const data = cyberDatabase[selectedCategory][selectedSubcategory] || [];
    
    console.log(`[CTI] Dados disponíveis antes do filtro: ${data.length}`);
    
    // Filtrar por país
    if (selectedCountry === 'UN' || selectedCountry === 'EU') {
        // Mostrar todos para países globais
        appState.filteredData = data;
    } else {
        appState.filteredData = data.filter(item => item.paisCode === selectedCountry);
    }
    
    console.log(`[CTI] Cards após filtro: ${appState.filteredData.length}`);
    
    renderCards();
}

function renderCards() {
    const container = document.getElementById('cards-container');
    container.innerHTML = '';
    
    const lang = appState.currentLanguage;
    
    // MENSAGEM ESTILIZADA QUANDO NÃO HÁ CARDS
    if (appState.filteredData.length === 0) {
        const emptyMessage = document.createElement('div');
        emptyMessage.className = 'col-span-full flex flex-col items-center justify-center py-20 gap-8';
        
        // Ícone de Alerta
        const icon = document.createElement('div');
        icon.className = 'text-8xl';
        icon.textContent = '⚠️';
        
        // Mensagem Principal
        const message = document.createElement('h2');
        message.className = 'text-4xl font-bold text-center';
        message.style.color = '#00f0ff';
        message.style.textShadow = '0 0 20px #00f0ff';
        message.style.letterSpacing = '0.1em';
        message.textContent = lang === 'pt' 
            ? 'NENHUMA AMEAÇA ATIVA DETECTADA NESTE SETOR'
            : 'NO ACTIVE THREATS DETECTED IN THIS SECTOR';
        
        // Submensagem
        const subMessage = document.createElement('p');
        subMessage.className = 'text-xl text-center';
        subMessage.style.color = '#a1a1aa';
        subMessage.textContent = lang === 'pt'
            ? 'Este filtro não possui dados cadastrados no momento.'
            : 'This filter has no registered data at the moment.';
        
        // Botão de Voltar Estilizado
        const backButton = document.createElement('button');
        backButton.className = 'px-8 py-4 bg-black border-2 rounded-lg font-bold text-lg transition-all';
        backButton.style.borderColor = '#00f0ff';
        backButton.style.color = '#00f0ff';
        backButton.textContent = lang === 'pt' ? '← VOLTAR À SELEÇÃO' : '← BACK TO SELECTION';
        
        backButton.addEventListener('mouseenter', () => {
            backButton.style.background = '#00f0ff';
            backButton.style.color = '#000000';
            backButton.style.boxShadow = '0 0 30px rgba(0, 240, 255, 0.5)';
        });
        
        backButton.addEventListener('mouseleave', () => {
            backButton.style.background = '#000000';
            backButton.style.color = '#00f0ff';
            backButton.style.boxShadow = 'none';
        });
        
        backButton.addEventListener('click', () => {
            goToScreen('screen-category');
        });
        
        emptyMessage.appendChild(icon);
        emptyMessage.appendChild(message);
        emptyMessage.appendChild(subMessage);
        emptyMessage.appendChild(backButton);
        
        container.appendChild(emptyMessage);
        return;
    }
    
    // Renderizar cards normalmente
    appState.filteredData.forEach(threat => {
        const card = createCard(threat, lang);
        container.appendChild(card);
    });
}

function createCard(threat, lang) {
    const card = document.createElement('div');
    card.className = `rpg-card ${getCardBackgroundClass(appState.selectedSubcategory)} cursor-pointer`;
    
    // Evento de clique para abrir modal
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
    flag.className = 'text-3xl';
    const countryData = countries.find(c => c.code === threat.paisCode);
    flag.textContent = countryData ? countryData.flag : '🌐';
    
    header.appendChild(title);
    header.appendChild(flag);
    
    // Container de imagem (placeholder por enquanto)
    const imageContainer = document.createElement('div');
    imageContainer.className = 'card-image-container';
    
    const imagePlaceholder = document.createElement('div');
    imagePlaceholder.className = 'card-placeholder';
    imagePlaceholder.textContent = threat.imagePlaceholder || '🎯';
    
    imageContainer.appendChild(imagePlaceholder);
    
    // Body do card - APENAS ESPECIALIDADE
    const body = document.createElement('div');
    body.className = 'card-body';
    
    const specialty = document.createElement('p');
    specialty.className = 'card-specialty';
    specialty.textContent = threat.especialidade[lang] || threat.especialidade.pt;
    
    body.appendChild(specialty);
    
    // Footer do card - APENAS RARIDADE
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
    
    // Animação de hover
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
    });
    
    return card;
}

// Retorna a classe CSS apropriada baseada na subcategoria
function getCardBackgroundClass(subcategory) {
    const classMap = {
        // Grupos
        'lucro': 'bg-lucro',
        'fama': 'bg-fama',
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

// SISTEMA DE MODAL - Dossiê de Inteligência

// Calcula níveis táticos e estratégicos baseado na raridade
function calculateLevels(raridade) {
    const stars = (raridade.match(/⭐/g) || []).length;
    
    // Base: 20 por estrela
    const baseLevel = stars * 20;
    
    // Adiciona variação aleatória mas consistente
    const tactical = Math.min(100, baseLevel + Math.floor(Math.random() * 10));
    const strategic = Math.min(100, baseLevel + Math.floor(Math.random() * 10));
    
    return { tactical, strategic };
}

// Abre o modal com informações completas
function openThreatModal(threat, lang) {
    const modal = document.getElementById('threat-modal');
    const modalBody = document.getElementById('modal-body');
    
    // Calcular níveis
    const levels = calculateLevels(threat.raridade);
    
    // Obter dados do país
    const countryData = countries.find(c => c.code === threat.paisCode);
    const countryName = countryData ? countryData.name[lang] : 'Unknown';
    const countryFlag = countryData ? countryData.flag : '🌐';
    
    // Montar conteúdo do modal
    modalBody.innerHTML = `
        <!-- Cabeçalho -->
        <div class="modal-header">
            <div class="modal-title">
                ${threat.nome}
            </div>
            <div class="modal-subtitle">
                <span class="text-4xl">${countryFlag}</span>
                <span>${countryName}</span>
                <span class="text-yellow-400 text-2xl ml-auto">${threat.raridade}</span>
            </div>
        </div>
        
        <!-- Imagem -->
        <div class="modal-image-container">
            <div class="modal-image-placeholder">${threat.imagePlaceholder || '🎯'}</div>
        </div>
        
        <!-- Tipo/Categoria -->
        <div class="modal-section">
            <div class="modal-section-title">${lang === 'pt' ? 'Classificação' : 'Classification'}</div>
            <div class="card-type" style="display: inline-block; font-size: 1rem; padding: 0.5rem 1rem;">
                ${threat.tipo[lang] || threat.tipo.pt}
            </div>
        </div>
        
        <!-- Descrição -->
        <div class="modal-section">
            <div class="modal-section-title">${lang === 'pt' ? 'Dossiê de Inteligência' : 'Intelligence Dossier'}</div>
            <div class="modal-description">
                ${threat.descricao[lang] || threat.descricao.pt}
            </div>
        </div>
        
        <!-- Especialidade -->
        <div class="modal-section">
            <div class="modal-section-title">${lang === 'pt' ? 'Especialidade' : 'Specialty'}</div>
            <div class="modal-specialty">
                ${threat.especialidade[lang] || threat.especialidade.pt}
            </div>
        </div>
        
        <!-- Níveis Táticos e Estratégicos -->
        <div class="modal-section">
            <div class="modal-section-title">${lang === 'pt' ? 'Análise de Capacidade Operacional' : 'Operational Capability Analysis'}</div>
            
            <div class="stats-container">
                <!-- Nível Tático -->
                <div class="stat-item">
                    <div class="stat-label">
                        <span class="stat-name">${lang === 'pt' ? 'Nível Tático' : 'Tactical Level'}</span>
                        <span class="stat-value">${levels.tactical}/100</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${levels.tactical}%;"></div>
                    </div>
                </div>
                
                <!-- Nível Estratégico -->
                <div class="stat-item">
                    <div class="stat-label">
                        <span class="stat-name">${lang === 'pt' ? 'Nível Estratégico' : 'Strategic Level'}</span>
                        <span class="stat-value">${levels.strategic}/100</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${levels.strategic}%;"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Aplicar classe de fundo dinâmico ao modal
    const modalContent = modal.querySelector('.modal-content');
    modalContent.className = `modal-content bg-zinc-950 border-2 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto relative ${getCardBackgroundClass(appState.selectedSubcategory)}`;
    
    // Mostrar modal
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    
    // Prevenir scroll do body
    document.body.style.overflow = 'hidden';
}

// Fecha o modal
function closeThreatModal() {
    const modal = document.getElementById('threat-modal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    
    // Restaurar scroll do body
    document.body.style.overflow = 'auto';
}

// Inicializar eventos do modal
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

// Utilitários
function log(message, data = null) {
    if (data) {
        console.log(`[CTI Portfolio] ${message}`, data);
    } else {
        console.log(`[CTI Portfolio] ${message}`);
    }
}

// Debug: Expor estado global no console (apenas para desenvolvimento)
window.cyberPortfolio = {
    state: appState,
    database: cyberDatabase,
    countries: countries,
    changeLanguage: changeLanguage,
    goToScreen: goToScreen
};