# Arquitetura do Projeto - Cyber Threat Intelligence Portfolio

## 📋 Visão Geral

Este é um portfólio interativo de **Cyber Threat Intelligence (CTI)** no formato de **Card Game RPG tático**, inspirado em jogos como Yu-Gi-Oh e War. O projeto apresenta atores reais de ameaças cibernéticas (APT Groups, indivíduos, agências governamentais) em um sistema de cards RPG com atributos, raridades e classificações geopolíticas.

### Características Principais
- **Bilíngue**: Suporte completo para Português (PT) e Inglês (EN)
- **Automatizado**: Geração automática de dados via script Python (`builder.py`)
- **Fontes Oficiais**: MITRE ATT&CK, FBI Cyber's Most Wanted, bases públicas de CERTs
- **Design**: Estética hacking moderna e minimalista (preto, cinza, cyan neon)
- **Responsivo**: Interface adaptável para desktop e mobile

---

## 🏗️ Estrutura de Arquivos

```
cyber-cti-portfolio/
│
├── index.html              # Interface principal (3 telas + modal + mapa)
├── builder.py              # Script de automação e geração de dados
├── Arquitetura.md          # Este arquivo (documentação técnica)
│
├── css/
│   └── styles.css          # Estilos customizados (tema hacker, animações, CRT)
│
├── js/
│   ├── data.js             # Base de dados (gerada por builder.py)
│   └── app.js              # Lógica principal (navegação, filtros, modal)
│
└── assets/
    └── images/
        ├── radar.svg                      # Ícone do mapa de ameaças
        ├── groups.jpg                     # Categoria: Grupos
        ├── persons.jpg                    # Categoria: Indivíduos
        ├── gov.jpg                        # Categoria: Organizações Gov
        ├── classe_grupos.jpg              # Imagem de classe para grupos
        ├── classe_individuos.jpg          # Imagem de classe para indivíduos
        ├── classe_organizacoes.jpg        # Imagem de classe para orgs gov
        ├── profit.jpg                     # Subcategoria: Lucro
        ├── osint.jpg                      # Subcategoria: OSINT/SIGINT
        ├── assct.jpg                      # Subcategoria: Associado a Gov
        ├── famous.jpg                     # Subcategoria: Famosos
        ├── enforce.jpg                    # Subcategoria: Defesa e Lei
        └── military.jpg                   # Subcategoria: Espionagem Militar
```

---

## 🎯 Fluxo de Navegação

### Tela 1: Seleção Geográfica (`screen-geopolitics`)
- Botão: **MAPA EM TEMPO REAL** (Check Point ThreatCloud)
- Grid de países:
  - **Rússia** (RU)
  - **EUA** (US)
  - **China** (CN)
  - **Coreia do Norte** (KP)
  - **Irã** (IR)
  - **Israel** (IL)
  - **União Europeia** (EU)
  - **Global** (Atores transnacionais)

### Tela 2: Seleção de Categoria (`screen-category`)
- **Dossiê Geopolítico**: Descrição do Modus Operandi do país selecionado
- Três categorias principais:
  1. **Grupos** (APT, Sindicatos)
     - Lucro
     - OSINT/SIGINT
     - Associado a Gov
  2. **Indivíduos** (Hackers, Criminosos)
     - Famosos
  3. **Organizações Governamentais** (CERTs, Agências)
     - Defesa e Aplicação da Lei
     - Espionagem e Operações Militares

### Tela 3: Grid de Cards (`screen-cards`)
- Cards RPG com:
  - Nome do ator
  - Bandeira do país (SVG Flag Icons)
  - Imagem de classe (subcategoria)
  - Especialidade técnica
  - Estrelas de raridade (1-5, estilo GTA Wanted)

### Tela Extra: Live Threat Map (`tela-livemap`)
- Iframe do Check Point ThreatCloud
- Visualização tática em tempo real de ataques cibernéticos

### Modal: Dossiê de Inteligência (`threat-modal`)
- Cabeçalho com nome e estrelas
- Imagem ampliada com efeito CRT (pixelated-screen)
- Classificação Operacional (tipo)
- Análise Tática (descrição detalhada)
- Especialidade Técnica
- Capacidade Operacional:
  - **TAC** (Nível Tático): 0-100
  - **EST** (Nível Estratégico): 0-100
  - Animação de contador progressivo (0 → valor real em 400ms)

---

## 🗄️ Estrutura de Dados (`js/data.js`)

### Objeto `cyberDatabase`
```javascript
{
  "grupos": [ { /* card 1 */ }, { /* card 2 */ }, ... ],
  "individuos": [ { /* card 1 */ }, { /* card 2 */ }, ... ],
  "organizacoes": [ { /* card 1 */ }, { /* card 2 */ }, ... ]
}
```

### Estrutura de um Card
```javascript
{
  "nome": "UNC3886",
  "tipo": {
    "pt": "APT / Grupo de Ameaça",
    "en": "APT / Threat Group"
  },
  "categoria": "grupos",
  "subcategoria": "governo",
  "paisCode": "china",
  "descricao": {
    "pt": "Dossiê operacional de CTI focado em análise de ameaças...",
    "en": "Operational CTI dossier focused on threat analysis..."
  },
  "especialidade": {
    "pt": "Exploitação de Hipervisores e Rootkits de Nuvem",
    "en": "Hypervisor Exploitation and Cloud Rootkits"
  },
  "raridade": "⭐⭐⭐⭐⭐",
  "estrelas": 5,
  "tac": 96,
  "est": 94,
  "imagePlaceholder": "assets/images/classe_grupos.jpg"
}
```

### Países (`countries`)
```javascript
[
  { "code": "russia", "name": { "pt": "Rússia", "en": "Russia" }, "flag": "🇷🇺" },
  { "code": "eua", "name": { "pt": "EUA", "en": "USA" }, "flag": "🇺🇸" },
  { "code": "china", "name": { "pt": "China", "en": "China" }, "flag": "🇨🇳" },
  { "code": "coreia_norte", "name": { "pt": "Coreia do Norte", "en": "North Korea" }, "flag": "🇰🇵" },
  { "code": "ira", "name": { "pt": "Irã", "en": "Iran" }, "flag": "🇮🇷" },
  { "code": "israel", "name": { "pt": "Israel", "en": "Israel" }, "flag": "🇮🇱" },
  { "code": "eu", "name": { "pt": "União Europeia", "en": "European Union" }, "flag": "🇪🇺" },
  { "code": "global", "name": { "pt": "Global", "en": "Global" }, "flag": "🌐" }
]
```

### Perfis Geopolíticos (`perfisPaises`)
Cada país possui:
- `titulo`: Título da doutrina (PT/EN)
- `modus`: Descrição do Modus Operandi (PT/EN)

---

## 🤖 Script de Automação (`builder.py`)

### Funcionalidades Principais

#### 1. Extração de Dados do MITRE ATT&CK
- **Fonte**: `enterprise-attack.json` (STIX 2.0)
- **Alvo**: Grupos APT (categoria `intrusion-set`)
- **Processamento**:
  - Limpeza de links Markdown
  - Truncamento de descrição por frases completas (4-6 linhas)
  - Tradução automática via `deep_translator` (GoogleTranslator)
  - Glossário de correção de jargões técnicos
  - Atribuição geopolítica com sistema de prioridades

#### 2. Extração da API do FBI Cyber's Most Wanted
- **Endpoint**: `https://api.fbi.gov/wanted/v1/list`
- **Filtro**: `field_offices=cyber`
- **Processamento**:
  - Geração de descrição baseada em `caution`, `description`, `remarks`
  - Fallback para descrição padrão se dados incompletos
  - Classificação automática como `subcategoria: "famosos"`

#### 3. Injeção Manual de Atores Elite
- **Indivíduos**: Kevin Mitnick, Shalev Hulio, Tal Dilian, Wau Holland
- **OSINT/SIGINT**: Bellingcat, Citizen Lab, Intellexa Consórcio

#### 4. Automação de CERTs e Agências Governamentais
- **Fonte**: JSON público de CERTs globais
- **Filtro Geopolítico**: US, RU, CN, IR, IL, KP, EU
- **Classificação**:
  - `defesa_lei`: CERTs, respostas a incidentes, defesa nacional
  - `espionagem_militar`: Inteligência militar, operações ofensivas

### Sistema de Atribuição Geográfica

#### Ordem de Prioridade:
1. **Hardcoded Overrides** (`FIXED_COUNTRY_GROUPS`)
   - Ex: `UNC3886` → `china`
2. **Exclusão de Alvos da América do Sul**
   - Se texto menciona "South America", "Brazil", etc. → `global`
3. **Palavras-chave de Origem Forte** (`ORIGIN_STRONG_KEYWORDS`)
   - Ex: "China-nexus", "Russian state-sponsored"
4. **Filtro Negativo de Alvos** (`TARGET_PHRASES`)
   - Ignora países mencionados como vítimas
5. **Fallback Global**
   - Se nenhuma atribuição clara → `paisId: "global"`

### Cálculo de Atributos

#### Raridade (Estrelas):
- 5 estrelas: TAC ≥ 95
- 4 estrelas: TAC ≥ 85
- 3 estrelas: TAC ≥ 70
- 2 estrelas: TAC ≥ 50
- 1 estrela: TAC < 50

#### TAC (Nível Tático): 50-98
Baseado em:
- Número de técnicas MITRE
- Sofisticação de TTPs
- Persistência e evasão

#### EST (Nível Estratégico): 45-95
Baseado em:
- Impacto geopolítico
- Recursos estatais
- Alcance global

---

## 🎨 Design System

### Paleta de Cores
- **Fundo Principal**: `#000000` (Preto absoluto)
- **Fundo Secundário**: `#09090b` (Preto suave)
- **Bordas**: `#27272a` (Cinza escuro)
- **Accent Primary**: `#00f0ff` (Cyan neon)
- **Accent Success**: `#22c55e` (Verde neon)
- **Accent Danger**: `#ef4444` (Vermelho)
- **Estrelas**: `#FFD700` (Amarelo dourado)

### Tipografia
- **Títulos**: "Courier New", monospace
- **Corpo**: System fonts (sans-serif)
- **Cyber Terminal**: `JetBrains Mono`, fallback monospace

### Backgrounds Dinâmicos por Subcategoria

#### Lucro (Cybercrime Financeiro)
- **Cor**: Verde Matrix (`#22c55e`)
- **Efeito**: Scanlines verticais + ASCII rain animation

#### OSINT/SIGINT
- **Cor**: Azul Radar (`#60a5fa`)
- **Efeito**: Grid tático de inteligência

#### Associado a Gov
- **Cor**: Vermelho Alerta (`#dc2626`)
- **Efeito**: Padrão de ameaça classificada

#### Famosos (Indivíduos)
- **Cor**: Magenta Glitch (`#d946ef`)
- **Efeito**: Scanlines fúcsia + arcade retrô

#### Defesa e Lei
- **Cor**: Azul Institucional (`#3b82f6`)
- **Efeito**: Linhas de segurança nacional

#### Espionagem Militar
- **Cor**: Laranja Tático (`#f97316`)
- **Efeito**: Padrão de operações secretas

### Animações

#### Fade-in (0.4s ease-in)
Aplicado em:
- Transições de tela
- Cards ao carregar
- Modal ao abrir

#### Hover Effects
- Cards: `translateY(-8px)` + `box-shadow` intenso
- Botões: Border color → accent + glow
- Bandeiras: `scale(1.1)`

#### CRT Monitor Effect (`.pixelated-screen`)
- Scanlines horizontais (repeating gradient)
- Flicker de brilho (5% alternância a cada 50ms)
- Aplicado em: Imagens de cards e modal

#### Progress Bar Animation (400ms ease-out)
- Width: 0% → valor real
- Contador numérico: 0 → valor real (sincronizado)

---

## 🔧 Funcionalidades JavaScript (`js/app.js`)

### Estado Global (`appState`)
```javascript
{
  currentScreen: 'screen-geopolitics',
  currentLanguage: 'pt',         // Salvo em localStorage
  selectedCountry: null,
  selectedCategory: null,
  selectedSubcategory: null,
  filteredData: []
}
```

### Funções Principais

#### Navegação
- `goToScreen(screenId)`: Transição suave entre telas
- `selectCountry(countryCode)`: Armazena país e exibe dossiê
- `selectSubcategory(category, subcategory)`: Filtra e renderiza cards
- `abrirLiveMap()` / `fecharLiveMap()`: Controle do iframe

#### Linguagem
- `changeLanguage(lang)`: Alterna PT/EN e salva no localStorage
- `updateLanguage()`: Atualiza todos os elementos `[data-lang]`
- `getSavedLanguage()`: Lê idioma salvo

#### Renderização
- `renderCountries()`: Grid de países com SVG flags
- `renderCards()`: Grid de cards filtrados
- `createCard(threat, lang)`: Monta card individual com:
  - Header (nome + bandeira)
  - Imagem de classe (subcategoria)
  - Especialidade
  - Estrelas dinâmicas
- `displayGeopoliticalDossier(countryCode)`: Injeta modus operandi

#### Modal
- `openThreatModal(threat, lang)`: Monta e exibe dossiê completo
- `animateOperationalStats(modalBody)`: Anima barras TAC/EST + contadores
- `closeThreatModal()`: Fecha e libera scroll

#### Estrelas (Sistema GTA Wanted)
- `resolverEstrelas(card)`: Calcula raridade (0-5) de forma inteligente
- `nivelDeAmeaca(estrelas)`: Cria elementos SVG das estrelas
- `nivelDeAmeacaHTML(estrelas, size)`: Versão string para templates
- `createMilitaryStarSVG(size)`: Cria SVG individual de estrela 5 pontas

#### Utilitários
- `getFlagIconClass(countryCode)`: Mapeia país → classe Flag Icons
- `getClassImagePath(threat)`: Resolve imagem por subcategoria
- `getCardBackgroundClass(subcategory)`: Define classe de fundo
- `aplicarEstiloCard(card, threat)`: Aplica background dinâmico
- `handleImageError(img)`: Fallback para imagens quebradas

---

## 🌐 Integração Externa

### Flag Icons CDN
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.0.0/css/flag-icons.min.css">
```
- Uso: `<span class="fi fi-ru"></span>` (bandeira da Rússia)
- Mapeamento: `getFlagIconClass(countryCode)` → `fi-{code}`

### Tailwind CSS CDN
```html
<script src="https://cdn.tailwindcss.com"></script>
```
- Uso: Classes utilitárias (`flex`, `grid`, `text-cyan-400`, etc.)

### Check Point ThreatCloud
```html
<iframe src="https://threatmap.checkpoint.com/" ...></iframe>
```
- Lazy loading: `src="about:blank"` até ativação
- Full-screen: `h-[75vh]`, sem bordas

---

## 🔐 Segurança e Performance

### Segurança
- **CSP**: Não implementado (usar CDNs confiáveis)
- **XSS**: Uso de `textContent` para user-generated content
- **CORS**: Iframe requer `referrerpolicy="no-referrer-when-downgrade"`

### Performance
- **Lazy Loading**: Imagens com `loading="lazy"`
- **Debounce**: Iframe só carrega ao abrir (`abrirLiveMap()`)
- **LocalStorage**: Persistência de idioma sem requisições
- **CSS Animations**: Hardware-accelerated (`transform`, `opacity`)
- **Image Fallback**: `onerror` handler para imagens quebradas

### Otimizações
- Scrollbar oculto (UX limpa, sem perda de funcionalidade)
- `touch-action: manipulation` (remove delay 300ms mobile)
- Fade-in gradual para evitar flash de conteúdo
- Modal fecha com ESC, overlay click, ou botão ×

---

## 📱 Responsividade

### Breakpoints (Tailwind)
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### Adaptações
- Grid de países: `grid-cols-1 md:grid-cols-2 lg:grid-cols-4`
- Grid de cards: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`
- Modal: `w-full max-w-4xl` (centralizado e responsivo)
- Textos: `text-2xl md:text-3xl lg:text-4xl`

---

## 🚀 Deployment e Uso

### Pré-requisitos
- **Python 3.8+** (para `builder.py`)
- **Bibliotecas Python**:
  ```bash
  pip install requests deep_translator
  ```
- **Servidor HTTP** (local):
  ```bash
  python -m http.server 8080
  ```

### Fluxo de Trabalho

#### 1. Geração de Dados
```bash
python builder.py
```
- Baixa `enterprise-attack.json` do MITRE
- Consome API do FBI Cyber
- Gera `js/data.js` automaticamente
- Logs coloridos no terminal

#### 2. Preview Local
```bash
python -m http.server 8080
```
- Acesse: `http://localhost:8080`

#### 3. Deploy Produção
- **GitHub Pages**: Push para branch `gh-pages`
- **Netlify/Vercel**: Deploy automático via Git
- **Cloudflare Pages**: Suporte a redirecionamentos

---

## 🐛 Troubleshooting

### Problema: ERR_EMPTY_RESPONSE (localhost:8080)
**Causa**: Porta em uso por outro processo
**Solução**:
```bash
# Windows (PowerShell)
netstat -ano | findstr :8080
taskkill /F /PID <PID>

# Linux/Mac
lsof -i :8080
kill -9 <PID>
```

### Problema: Modal não abre
**Causa**: `cyberDatabase` não carregado
**Solução**: Verificar se `js/data.js` existe e está importado antes de `app.js`

### Problema: Estrelas não aparecem
**Causa**: `card.estrelas` indefinido
**Solução**: `resolverEstrelas()` calcula automaticamente via `card.raridade` ou `card.tac`

### Problema: Tradução com texto em inglês
**Causa**: `deep_translator` não instalado ou offline
**Solução**:
```bash
pip install --upgrade deep_translator
```

### Problema: Flags não carregam
**Causa**: CDN Flag Icons offline
**Solução**: Baixar biblioteca local ou usar emojis como fallback

---

## 📚 Referências e Créditos

### Fontes de Dados
- **MITRE ATT&CK**: https://attack.mitre.org/
- **FBI Cyber Most Wanted**: https://api.fbi.gov/
- **Check Point ThreatCloud**: https://threatmap.checkpoint.com/
- **CERTs Globais**: Bases públicas e FIRST.org

### Bibliotecas e Frameworks
- **Tailwind CSS**: https://tailwindcss.com/
- **Flag Icons**: https://github.com/lipis/flag-icons
- **deep_translator**: https://github.com/nidhaloff/deep-translator

### Inspiração de Design
- **GTA Wanted Level**: Sistema de estrelas tático
- **Hacker Movies**: Estética terminal Matrix/Watch Dogs
- **Military UI**: Layouts de comando e controle

---

## 🔮 Roadmap Futuro

### Features Planejadas
- [ ] Sistema de busca/filtro avançado
- [ ] Comparação lado a lado de atores
- [ ] Histórico de operações (timeline)
- [ ] Integração com mais fontes (AlienVault OTX, MISP)
- [ ] Modo escuro/claro toggle
- [ ] Export para PDF/CSV
- [ ] PWA (Progressive Web App)
- [ ] Backend para salvar favoritos

### Melhorias Técnicas
- [ ] Testes automatizados (Jest/Cypress)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Compressão de imagens (WebP)
- [ ] Service Worker para cache offline
- [ ] Analytics (Google Analytics/Plausible)

---

## 📄 Licença e Uso

Este projeto é um **portfólio educacional** para demonstração de habilidades em:
- Desenvolvimento Frontend (HTML/CSS/JS)
- Automação de dados (Python)
- Design de interfaces táticas
- Integração de APIs públicas
- Cyber Threat Intelligence

**Nota**: Os dados de ameaças são extraídos de fontes públicas oficiais (MITRE, FBI). Não use este projeto para fins maliciosos ou ilegais.

---

## 👤 Autor

Desenvolvido como parte de um portfólio profissional em **Cybersecurity** e **Threat Intelligence**.

Para dúvidas ou sugestões, consulte o repositório Git do projeto.

---

**Última Atualização**: 22 de Julho de 2026  
**Versão do Projeto**: 2.0 (Sistema de Estrelas Amarelas GTA)
