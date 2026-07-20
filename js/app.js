// Cyber Threat Intelligence Portfolio - Lógica Principal
// Sistema de navegação, filtros, idiomas e renderização de cards

// Estado Global da Aplicação
const appState = {
    currentScreen: 'screen-category',
    currentLanguage: 'pt',
    selectedCategory: null,
    selectedSubcategory: null,
    selectedCountry: null,
    filteredData: []
};

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    initializeLanguage();
    initializeNavigation();
    initializeFilters();
    updateLanguage();
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

// SISTEMA DE NAVEGAÇÃO ENTRE TELAS
function initializeNavigation() {
    document.getElementById('btn-back-category').addEventListener('click', () => {
        goToScreen('screen-category');
        resetFilters();
    });
    
    document.getElementById('btn-back-geopolitics').addEventListener('click', () => {
        goToScreen('screen-geopolitics');
        appState.selectedCountry = null;
    });
}

function goToScreen(screenId) {
    // Remover classe 'active' de todas as telas
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Ativar a tela selecionada
    document.getElementById(screenId).classList.add('active');
    appState.currentScreen = screenId;
}

function resetFilters() {
    appState.selectedCategory = null;
    appState.selectedSubcategory = null;
    appState.selectedCountry = null;
    appState.filteredData = [];
}

// SISTEMA DE FILTROS
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
    
    // Ir para a tela de seleção geopolítica
    goToScreen('screen-geopolitics');
    renderCountries();
}

// RENDERIZAÇÃO DE PAÍSES (Tela 2)
function renderCountries() {
    const container = document.getElementById('countries-container');
    container.innerHTML = '';
    
    const lang = appState.currentLanguage;
    
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
    filterAndDisplayCards();
    goToScreen('screen-cards');
}

// FILTRAGEM E RENDERIZAÇÃO DE CARDS (Tela 3)
function filterAndDisplayCards() {
    const { selectedCategory, selectedSubcategory, selectedCountry } = appState;
    
    // Obter dados da categoria/subcategoria selecionada
    const data = cyberDatabase[selectedCategory][selectedSubcategory] || [];
    
    // Filtrar por país
    if (selectedCountry === 'UN' || selectedCountry === 'EU') {
        // Mostrar todos para países globais
        appState.filteredData = data;
    } else {
        appState.filteredData = data.filter(item => item.paisCode === selectedCountry);
    }
    
    renderCards();
}

function renderCards() {
    const container = document.getElementById('cards-container');
    container.innerHTML = '';
    
    const lang = appState.currentLanguage;
    
    if (appState.filteredData.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center text-2xl text-gray-500 py-20">
                ${lang === 'pt' ? 'Nenhuma ameaça encontrada para este filtro.' : 'No threats found for this filter.'}
            </div>
        `;
        return;
    }
    
    appState.filteredData.forEach(threat => {
        const card = createCard(threat, lang);
        container.appendChild(card);
    });
}

function createCard(threat, lang) {
    const card = document.createElement('div');
    card.className = `rpg-card ${getCardBackgroundClass(appState.selectedSubcategory)}`;
    
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
    
    // Body do card
    const body = document.createElement('div');
    body.className = 'card-body';
    
    const description = document.createElement('p');
    description.className = 'card-description';
    description.textContent = threat.descricao[lang] || threat.descricao.pt;
    
    const specialty = document.createElement('p');
    specialty.className = 'card-specialty';
    specialty.textContent = `${lang === 'pt' ? 'Especialidade' : 'Specialty'}: ${threat.especialidade[lang] || threat.especialidade.pt}`;
    
    body.appendChild(description);
    body.appendChild(specialty);
    
    // Footer do card
    const footer = document.createElement('div');
    footer.className = 'card-footer';
    
    const type = document.createElement('div');
    type.className = 'card-type';
    type.textContent = threat.tipo[lang] || threat.tipo.pt;
    
    const rarity = document.createElement('div');
    rarity.className = 'card-rarity';
    rarity.textContent = threat.raridade;
    
    footer.appendChild(type);
    footer.appendChild(rarity);
    
    // Montar card completo
    card.appendChild(header);
    card.appendChild(imageContainer);
    card.appendChild(body);
    card.appendChild(footer);
    
    // Animação de hover
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-10px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
    });
    
    return card;
}

// Retorna a classe CSS apropriada baseada na subcategoria
function getCardBackgroundClass(subcategory) {
    const classMap = {
        'lucro': 'bg-profit',
        'fama': 'bg-fame',
        'adolescentes': 'bg-teens',
        'ransomware': 'bg-ransomware',
        'hacktivismo': 'bg-hacktivism',
        'espionagem': 'bg-espionage',
        'inteligencia': 'bg-intelligence',
        'militar': 'bg-military',
        'policia': 'bg-police'
    };
    
    return classMap[subcategory] || 'bg-government';
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