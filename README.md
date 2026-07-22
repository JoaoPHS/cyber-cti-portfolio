# 🎯 Cyber Threat Intelligence Portfolio - Tactical RPG

Portfólio interativo de Cyber Threat Intelligence gamificado como um RPG de Cartas Tático. Combina dados reais de ameaças cibernéticas com uma interface moderna inspirada em SOC/SIEM operacional.

## 🚀 Características Principais

### 🎮 Experiência Gamificada
- **Cards RPG Táticos**: Cada ator de ameaça é um card com raridade (1-5 ⭐), atributos TAC/EST e especialidades
- **Funil Geopolítico**: Navegação estratégica através de País → Categoria → Cards
- **Modal Holográfico**: Dossiê de inteligência completo com backdrop blur ao clicar nos cards
- **Sistema de Alerta Tático**: Mensagem animada para combinações sem atores cadastrados

### 🎨 Design SOC/SIEM Moderno
- **Paleta**: Preto absoluto (#000000), Cinza grafite (#16161a), Ciano Neon (#00f0ff)
- **Tipografia**: Monoespaçada (JetBrains Mono, Fira Code, Courier New)
- **Texturas Dinâmicas**: Padrões CSS animados baseados na subcategoria:
  - 💰 **Lucro**: Padrão de cifrões verde-menta
  - 📡 **OSINT/SIGINT**: Radar holográfico ciano com varredura
  - 🎖️ **Governo/Militares**: Camuflagem digital urbana
  - ⭐ **Lendas/Especialistas**: Glitch cyberpunk magenta
  - 🚨 **Polícia**: Sirene azul cobalto pulsante

### 🌍 Sistema Bilíngue (PT/EN)
- Seletor de idioma global persistente
- Tradução instantânea de toda interface e conteúdo dos cards
- Suporte completo para português e inglês

### 🤖 Automação com Python
- **builder.py**: Script que gera automaticamente o banco de dados
- Extração de dados do **MITRE ATT&CK** via STIX
- Mapeamento inteligente de países por palavras-chave
- Cálculo automático de atributos de RPG (raridade, TAC, EST)
- Síntese de dossiês de inteligência

## 📂 Estrutura do Projeto

```
cyber-cti-portfolio/
├── index.html              # Interface principal (3 telas)
├── css/
│   └── styles.css          # Estilos táticos e texturas dinâmicas
├── js/
│   ├── data.js             # Banco de dados (gerado por builder.py)
│   └── app.js              # Lógica de navegação, filtros e modal
├── assets/
│   └── images/             # Imagens dos cards (opcional)
├── builder.py              # Script Python automatizador
├── README.md               # Este arquivo
└── start.bat               # Atalho para abrir o projeto
```

## 🔧 Como Usar

### 📖 Visualização do Portfólio

1. **Abrir no navegador**:
   ```bash
   # Opção 1: Duplo clique no arquivo
   start.bat
   
   # Opção 2: Abrir diretamente
   index.html
   ```

2. **Navegação**:
   - **Tela 1**: Selecione um país (Rússia, EUA, China, Irã, Israel, Coreia do Norte, União Europeia)
   - **Tela 2**: Escolha uma categoria e subcategoria
   - **Tela 3**: Visualize os cards e clique para detalhes

### 🐍 Executar o Builder (Atualizar Dados)

```bash
# Instalar dependências
pip install requests

# Executar o script
python builder.py
```

**O que o builder.py faz**:
1. 🌐 Baixa dados do MITRE ATT&CK
2. 🔍 Filtra intrusion-sets (grupos de ameaça)
3. 🗺️ Mapeia países por palavras-chave
4. ⭐ Calcula raridade e atributos de RPG
5. 📝 Sintetiza dossiês de inteligência
6. 🏆 Mescla atores lendários hardcoded
7. 💾 Gera o arquivo `js/data.js`

## 🎯 Taxonomia de Atores

### 📊 Categorias e Subcategorias

#### 👥 **Grupos**
- **Lucro**: Ransomware, extorsão, crimes financeiros
- **OSINT/SIGINT**: Hacktivismo, coleta de dados, surveillance
- **Associado a Gov**: APTs estatais, espionagem cibernética

#### 👤 **Indivíduos**
- **Lendas**: Hackers históricos famosos (Kevin Mitnick, Adrian Lamo)
- **Especialistas**: Alto nível técnico, pesquisadores, vigilantes
- **Lucro**: Cibercriminosos, fraudadores financeiros

#### 🏛️ **Organizações Governamentais**
- **Militares**: Guerra cibernética, forças armadas (CNMF, SSF, Bureau 121)
- **Inteligência**: Espionagem, SIGINT (NSA TAO, Unit 8200, Mossad)
- **Polícia Especializada**: Law enforcement (FBI Cyber, Europol EC3)

## 🌟 Atores Lendários Destacados

- 💥 **Sandworm Team (GRU Unit 74455)**: APT mais destrutivo do mundo
- 🇰🇵 **Lazarus Group / APT38**: Heists financeiros bilionários
- 🕵️ **APT29 (Cozy Bear)**: SolarWinds e supply chain attacks
- 🐻 **APT28 (Fancy Bear)**: Interferência eleitoral e operações GRU
- 🦅 **NSA TAO**: Unidade de elite ofensiva americana
- 🇮🇱 **Unit 8200**: SIGINT israelense (Stuxnet, vigilância regional)
- 👑 **Kevin Mitnick**: Pioneiro da engenharia social moderna

## 🎨 Personalização

### Adicionar Imagens aos Cards

1. Salve imagens em `assets/images/`
2. No `data.js`, configure:
   ```javascript
   imagePlaceholder: "assets/images/sandworm.png"
   ```

### Adicionar Novos Atores Manualmente

Edite `js/data.js` e adicione na estrutura:

```javascript
cyberDatabase.grupos.lucro.push({
    nome: "Nome do Grupo",
    paisCode: "RU",
    subcategoria: "lucro",
    raridade: "⭐⭐⭐⭐⭐",
    descricao: {
        pt: "Descrição em português...",
        en: "Description in english..."
    },
    especialidade: {
        pt: "Ransomware, Extorsão",
        en: "Ransomware, Extortion"
    },
    tipo: {
        pt: "Ransomware / Lucro",
        en: "Ransomware / Profit"
    },
    imagePlaceholder: "🔒"
});
```

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estrutura semântica
- **Tailwind CSS**: Framework utility-first via CDN
- **CSS3**: Texturas dinâmicas, animações, backdrop-filter
- **JavaScript (ES6+)**: Lógica de navegação e renderização
- **Python 3**: Script de automação do banco de dados
- **MITRE ATT&CK**: Fonte de dados de threat intelligence

## 🧪 Funcionalidades Avançadas

### API de Debug (Console)

```javascript
// Acessar no console do navegador
window.cyberTacticalRPG

// Trocar idioma programaticamente
window.cyberTacticalRPG.actions.changeLanguage('en')

// Navegar para tela específica
window.cyberTacticalRPG.actions.goToScreen('screen-cards')

// Ver estado atual
console.log(window.cyberTacticalRPG.state)
```

### Atributos de RPG

- **Raridade (1-5 ⭐)**: Baseada em impacto histórico e capacidade técnica
- **TAC (Tático)**: Habilidade operacional e técnicas avançadas
- **EST (Estratégico)**: Alcance geopolítico e impacto de longo prazo

## 📜 Licença

Este é um projeto educacional para demonstração de habilidades em Cyber Threat Intelligence e desenvolvimento front-end.

## 🔗 Recursos Úteis

- [MITRE ATT&CK](https://attack.mitre.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [STIX Data Format](https://oasis-open.github.io/cti-documentation/)

---

**Desenvolvido com 🛡️ por um Analista de CTI**  
*"Conhecimento é a melhor defesa contra ameaças cibernéticas"*
