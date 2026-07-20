# 🎯 Cyber Threat Intelligence Portfolio

Portfolio interativo de Cyber Threat Intelligence baseado em Card Game de RPG (estilo Yu-Gi-Oh + War), com sistema bilíngue automático e filtros geopolíticos.

## 📁 Estrutura do Projeto

```
meu-portfolio-cyber/
├── index.html          # Interface principal com 3 telas de navegação
├── css/
│   └── styles.css      # Estilos customizados e padrões de fundo dinâmicos
├── js/
│   ├── data.js         # Banco de dados centralizado (Grupos, Indivíduos, Órgãos Gov)
│   └── app.js          # Lógica de filtros, idiomas e renderização
└── assets/
    └── images/         # Imagens dos cards (geradas no Midjourney)
```

## 🎮 Funcionalidades

### Sistema de Navegação (3 Telas)

#### **Tela 1: Escolha de Categoria**
- 3 categorias principais:
  - **Grupos** 💀 (Ransomware, Hacktivismo, Espionagem)
  - **Indivíduos** 👤 (Lucro, Fama, Adolescentes)
  - **Org. Governamentais** 🏛️ (Inteligência, Militar, Polícia)

#### **Tela 2: Seleção Geopolítica**
- Grid de países com bandeiras emoji
- 14 países/regiões disponíveis
- Filtro visual interativo

#### **Tela 3: Grid de Cards RPG**
- Cards dinâmicos estilo Yu-Gi-Oh
- Padrões de fundo temáticos por subcategoria
- Sistema de raridade (⭐)
- Informações bilíngues

### 🌍 Sistema Bilíngue (PT/EN)
- Alternância global em tempo real
- Tradução completa de interface e conteúdo
- Botões de idioma fixos no topo direito

### 🎨 Padrões Visuais por Subcategoria

| Subcategoria | Padrão Visual |
|-------------|---------------|
| **Lucro** 💰 | Cifrões em gradiente verde |
| **Governo** 🏛️ | Camuflagem cinza/preta |
| **Adolescentes** 👨‍💻 | Glitch neon com animação |
| **Org. Gov** 🌐 | Cores nacionais nas bordas |
| **Ransomware** 🔒 | Vermelho sangue escuro |
| **Hacktivismo** ⚔️ | Verde hacker matrix |
| **Espionagem** 🕵️ | Azul escuro stealth |

## 🗄️ Banco de Dados Atual

### Grupos (9 entidades)
- **Ransomware**: LockBit, ALPHV/BlackCat, Conti
- **Hacktivismo**: Anonymous, Killnet
- **Espionagem**: APT28 (Fancy Bear), APT29 (Cozy Bear), Lazarus Group

### Indivíduos (6 entidades)
- **Lucro**: Marcus Hutchins, Albert Gonzalez
- **Fama**: Kevin Mitnick, Adrian Lamo
- **Adolescentes**: Arion Kurtaj (Lapsus$), Jonathan James

### Organizações Gov (6 entidades)
- **Inteligência**: NSA TAO, Unit 8200, GCHQ
- **Militar**: US Cyber Command, PLA Unit 61398
- **Polícia**: FBI Cyber Division, Europol EC3

## 🚀 Como Usar

1. **Abrir o projeto**:
   ```bash
   # Navegue até a pasta do projeto
   cd C:\Users\termi\Documents\meu-portfolio-cyber
   
   # Abra o index.html no navegador
   start index.html
   ```

2. **Fluxo de Navegação**:
   - Escolha uma categoria (Grupos, Indivíduos ou Org. Gov)
   - Clique em uma subcategoria (ex: Ransomware, Lucro, Inteligência)
   - Selecione um país/região
   - Veja os cards filtrados com informações detalhadas

3. **Alternar Idioma**:
   - Clique em **PT** ou **EN** no canto superior direito
   - A interface e todos os cards serão traduzidos automaticamente

## 📝 Como Adicionar Novos Dados

### Adicionar uma nova ameaça

Edite o arquivo `js/data.js` e adicione ao array correspondente:

```javascript
// Exemplo: Adicionar novo grupo de ransomware
cyberDatabase.grupos.ransomware.push({
    nome: "Nome do Grupo",
    pais: { pt: "País PT", en: "País EN" },
    paisCode: "XX", // Código ISO do país
    descricao: {
        pt: "Descrição em português...",
        en: "Description in English..."
    },
    especialidade: {
        pt: "Especialidades PT",
        en: "Specialties EN"
    },
    raridade: "⭐⭐⭐⭐⭐", // 1 a 5 estrelas
    tipo: { pt: "Tipo PT", en: "Type EN" },
    imagePlaceholder: "🎯" // Emoji temporário
});
```

### Adicionar imagens reais

1. Gere imagens no Midjourney
2. Salve em `assets/images/`
3. Modifique `createCard()` em `app.js` para carregar as imagens:

```javascript
// Substitua o imagePlaceholder por:
const img = document.createElement('img');
img.className = 'card-image';
img.src = `assets/images/${threat.nome.toLowerCase().replace(/\s/g, '-')}.png`;
img.alt = threat.nome;
imageContainer.appendChild(img);
```

## 🎨 Prompts Sugeridos para Midjourney

Use estes prompts para gerar imagens dos cards:

```
# Para Grupos de Ransomware:
cyberpunk hacker logo, dark red and black, skull motif, digital glitch effect, 
aggressive style, game card art, high contrast --ar 3:4

# Para Indivíduos (Lucro):
portrait of cyber criminal in hoodie, money symbols background, dark atmosphere, 
digital art, trading card style, dramatic lighting --ar 3:4

# Para Adolescentes:
teenage hacker portrait, neon colors, glitch aesthetic, bedroom setup with monitors,
anime style, game card illustration --ar 3:4

# Para Organizações Governamentais:
military cyber unit emblem, official government style, shield and eagle motif,
dark blue and gold colors, professional design --ar 3:4
```

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estrutura semântica
- **Tailwind CSS** (via CDN): Framework CSS utilitário
- **CSS3 Puro**: Animações e padrões customizados
- **JavaScript Vanilla**: Lógica e interatividade
- **Design Responsivo**: Grid layout adaptativo

## 🎯 Próximos Passos

- [ ] Gerar imagens no Midjourney e substituir emojis
- [ ] Adicionar mais entidades ao banco de dados
- [ ] Implementar modal com detalhes expandidos ao clicar no card
- [ ] Adicionar sistema de busca/pesquisa
- [ ] Implementar animações de transição entre telas
- [ ] Criar modo escuro/claro opcional
- [ ] Adicionar linha do tempo de atividades
- [ ] Integrar com API de threat intelligence real (opcional)

## 📄 Licença

Este é um projeto de portfolio educacional. As informações de threat intelligence são baseadas em dados públicos e fontes abertas (OSINT).

## 👤 Autor

Portfolio criado para demonstração de conhecimentos em Cyber Threat Intelligence e desenvolvimento web interativo.

---

**Nota**: Este projeto usa emojis de bandeiras como placeholders. Para produção, considere usar imagens SVG de bandeiras para melhor compatibilidade entre navegadores.