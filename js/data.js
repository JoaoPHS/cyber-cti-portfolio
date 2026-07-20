// Banco de Dados Centralizado - Cyber Threat Intelligence Portfolio

const cyberDatabase = {
    // Grupos de Ameaça
    grupos: {
        ransomware: [
            {
                nome: "LockBit",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                descricao: {
                    pt: "Grupo de ransomware mais prolífico de 2022-2023, conhecido por ataques automatizados e afiliados globais. Desmantelado pela Operação Cronos em 2024.",
                    en: "Most prolific ransomware group of 2022-2023, known for automated attacks and global affiliates. Dismantled by Operation Cronos in 2024."
                },
                especialidade: {
                    pt: "Ransomware-as-a-Service (RaaS), Dupla Extorsão",
                    en: "Ransomware-as-a-Service (RaaS), Double Extortion"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Ransomware", en: "Ransomware" },
                imagePlaceholder: "🔒"
            },
            {
                nome: "ALPHV/BlackCat",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                descricao: {
                    pt: "Primeiro ransomware escrito em Rust, altamente personalizável e difícil de detectar. Atacou setores críticos como saúde e energia.",
                    en: "First ransomware written in Rust, highly customizable and hard to detect. Attacked critical sectors like healthcare and energy."
                },
                especialidade: {
                    pt: "Linguagem Rust, API REST, Tripla Extorsão",
                    en: "Rust Language, REST API, Triple Extortion"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Ransomware", en: "Ransomware" },
                imagePlaceholder: "🐱"
            },
            {
                nome: "Conti",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                descricao: {
                    pt: "Grupo dissolvido em 2022 após vazamento interno. Originou múltiplos sucessores e influenciou a cena do ransomware moderno.",
                    en: "Group dissolved in 2022 after internal leak. Spawned multiple successors and influenced modern ransomware scene."
                },
                especialidade: {
                    pt: "Ataque a Infraestrutura Crítica, RaaS",
                    en: "Critical Infrastructure Attacks, RaaS"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Ransomware", en: "Ransomware" },
                imagePlaceholder: "💰"
            }
        ],
        hacktivismo: [
            {
                nome: "Anonymous",
                pais: { pt: "Global", en: "Global" },
                paisCode: "UN",
                descricao: {
                    pt: "Coletivo descentralizado de hacktivistas, ativo desde 2003. Conhecido por operações contra governos, corporações e organizações.",
                    en: "Decentralized collective of hacktivists, active since 2003. Known for operations against governments, corporations, and organizations."
                },
                especialidade: {
                    pt: "DDoS, Defacement, Vazamento de Dados",
                    en: "DDoS, Defacement, Data Leaks"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Hacktivismo", en: "Hacktivism" },
                imagePlaceholder: "🎭"
            },
            {
                nome: "Killnet",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                descricao: {
                    pt: "Grupo pró-Rússia focado em ataques DDoS contra alvos da OTAN e apoiadores da Ucrânia durante o conflito de 2022-2026.",
                    en: "Pro-Russia group focused on DDoS attacks against NATO targets and Ukraine supporters during 2022-2026 conflict."
                },
                especialidade: {
                    pt: "DDoS em Massa, Guerra de Informação",
                    en: "Mass DDoS, Information Warfare"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Hacktivismo", en: "Hacktivism" },
                imagePlaceholder: "⚔️"
            }
        ],
        espionagem: [
            {
                nome: "APT28 (Fancy Bear)",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                descricao: {
                    pt: "Grupo ligado ao GRU russo, ativo desde 2004. Alvos incluem governos, militares e organizações políticas na Europa e EUA.",
                    en: "Group linked to Russian GRU, active since 2004. Targets include governments, military, and political organizations in Europe and USA."
                },
                especialidade: {
                    pt: "Spear Phishing, Exploits Zero-Day, OPSEC",
                    en: "Spear Phishing, Zero-Day Exploits, OPSEC"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Espionagem", en: "Espionage" },
                imagePlaceholder: "🐻"
            },
            {
                nome: "APT29 (Cozy Bear)",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                descricao: {
                    pt: "Grupo vinculado ao SVR russo, focado em espionagem de longo prazo contra think tanks, governos e instituições de pesquisa.",
                    en: "Group linked to Russian SVR, focused on long-term espionage against think tanks, governments, and research institutions."
                },
                especialidade: {
                    pt: "Persistência Avançada, Stealth, Exfiltração",
                    en: "Advanced Persistence, Stealth, Exfiltration"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Espionagem", en: "Espionage" },
                imagePlaceholder: "🕵️"
            },
            {
                nome: "Lazarus Group",
                pais: { pt: "Coreia do Norte", en: "North Korea" },
                paisCode: "KP",
                descricao: {
                    pt: "Grupo apoiado pelo estado norte-coreano, responsável pelo hack da Sony (2014), WannaCry (2017) e roubos de criptomoedas bilionários.",
                    en: "State-backed North Korean group, responsible for Sony hack (2014), WannaCry (2017), and billion-dollar crypto heists."
                },
                especialidade: {
                    pt: "Wiper Malware, Heists Financeiros, APT",
                    en: "Wiper Malware, Financial Heists, APT"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Espionagem", en: "Espionage" },
                imagePlaceholder: "🇰🇵"
            }
        ]
    },

    // Indivíduos Notórios
    individuos: {
        lucro: [
            {
                nome: "Marcus Hutchins (MalwareTech)",
                pais: { pt: "Reino Unido", en: "United Kingdom" },
                paisCode: "GB",
                descricao: {
                    pt: "Pesquisador que parou o WannaCry em 2017. Anteriormente desenvolveu o banking trojan Kronos. Condenado nos EUA, mas absolvido posteriormente.",
                    en: "Researcher who stopped WannaCry in 2017. Previously developed Kronos banking trojan. Convicted in USA but later pardoned."
                },
                especialidade: {
                    pt: "Malware Banking, Análise de Malware, Kill Switch",
                    en: "Banking Malware, Malware Analysis, Kill Switch"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Lucro/Herói", en: "Profit/Hero" },
                imagePlaceholder: "🦸"
            },
            {
                nome: "Albert Gonzalez",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                descricao: {
                    pt: "Líder do maior roubo de cartões de crédito da história (170 milhões). Roubou da TJX, Heartland e outros. Preso em 2008, condenado a 20 anos.",
                    en: "Leader of largest credit card theft in history (170 million). Stole from TJX, Heartland, and others. Arrested 2008, sentenced to 20 years."
                },
                especialidade: {
                    pt: "SQL Injection, Sniffing, Carding",
                    en: "SQL Injection, Sniffing, Carding"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Lucro", en: "Profit" },
                imagePlaceholder: "💳"
            }
        ],
        fama: [
            {
                nome: "Kevin Mitnick",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                descricao: {
                    pt: "Hacker mais procurado dos EUA nos anos 90. Invadiu Nokia, Motorola e Pentágono. Após prisão, tornou-se consultor de segurança e autor.",
                    en: "Most wanted hacker in USA in the 90s. Breached Nokia, Motorola, and Pentagon. After prison, became security consultant and author."
                },
                especialidade: {
                    pt: "Engenharia Social, Phreaking, Exploits",
                    en: "Social Engineering, Phreaking, Exploits"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Fama/Lenda", en: "Fame/Legend" },
                imagePlaceholder: "👑"
            },
            {
                nome: "Adrian Lamo",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                descricao: {
                    pt: "Conhecido como 'Hacker Sem-Teto', invadiu Microsoft, Yahoo e New York Times. Delatou Chelsea Manning ao FBI em 2010.",
                    en: "Known as 'Homeless Hacker', breached Microsoft, Yahoo, and New York Times. Turned in Chelsea Manning to FBI in 2010."
                },
                especialidade: {
                    pt: "Pentesting Não-Autorizado, Exploração de Redes",
                    en: "Unauthorized Pentesting, Network Exploitation"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Fama", en: "Fame" },
                imagePlaceholder: "🏴"
            }
        ],
        adolescentes: [
            {
                nome: "Arion Kurtaj (Lapsus$)",
                pais: { pt: "Reino Unido", en: "United Kingdom" },
                paisCode: "GB",
                descricao: {
                    pt: "Líder de 18 anos do grupo Lapsus$. Hackeou Uber, Rockstar Games (GTA 6) e NVIDIA usando SIM swap e engenharia social. Preso em 2023.",
                    en: "18-year-old leader of Lapsus$ group. Hacked Uber, Rockstar Games (GTA 6), and NVIDIA using SIM swap and social engineering. Arrested 2023."
                },
                especialidade: {
                    pt: "SIM Swapping, Engenharia Social, Acesso Não-Autorizado",
                    en: "SIM Swapping, Social Engineering, Unauthorized Access"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Adolescente", en: "Teen" },
                imagePlaceholder: "👨‍💻"
            },
            {
                nome: "Jonathan James",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                descricao: {
                    pt: "Primeiro juvenil preso por cibercrime nos EUA (16 anos). Invadiu NASA e Departamento de Defesa em 1999. Suicidou-se em 2008.",
                    en: "First juvenile imprisoned for cybercrime in USA (16 years old). Breached NASA and Department of Defense in 1999. Committed suicide in 2008."
                },
                especialidade: {
                    pt: "Backdoors, Roubo de Código-Fonte, Intrusão Militar",
                    en: "Backdoors, Source Code Theft, Military Intrusion"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Adolescente/Trágico", en: "Teen/Tragic" },
                imagePlaceholder: "💔"
            }
        ]
    },

    // Organizações Governamentais
    organizacoes: {
        inteligencia: [
            {
                nome: "NSA TAO",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                descricao: {
                    pt: "Tailored Access Operations - unidade de elite da NSA focada em operações ofensivas cibernéticas. Exposta por Edward Snowden e Shadow Brokers.",
                    en: "Tailored Access Operations - NSA elite unit focused on offensive cyber operations. Exposed by Edward Snowden and Shadow Brokers."
                },
                especialidade: {
                    pt: "Zero-Days, Implantes, SIGINT Ofensivo",
                    en: "Zero-Days, Implants, Offensive SIGINT"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Inteligência", en: "Intelligence" },
                imagePlaceholder: "🦅"
            },
            {
                nome: "Unit 8200",
                pais: { pt: "Israel", en: "Israel" },
                paisCode: "IL",
                descricao: {
                    pt: "Unidade de inteligência de sinais de Israel, responsável por Stuxnet (com EUA), vigilância regional e desenvolvimento de ferramentas ofensivas.",
                    en: "Israeli signals intelligence unit, responsible for Stuxnet (with USA), regional surveillance, and offensive tool development."
                },
                especialidade: {
                    pt: "SIGINT, Cyber Warfare, Exploits Avançados",
                    en: "SIGINT, Cyber Warfare, Advanced Exploits"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Inteligência", en: "Intelligence" },
                imagePlaceholder: "🇮🇱"
            },
            {
                nome: "GCHQ",
                pais: { pt: "Reino Unido", en: "United Kingdom" },
                paisCode: "GB",
                descricao: {
                    pt: "Government Communications Headquarters - agência britânica parceira da NSA, com capacidades avançadas em criptoanálise e intercepção.",
                    en: "Government Communications Headquarters - British agency partnering with NSA, with advanced capabilities in cryptanalysis and interception."
                },
                especialidade: {
                    pt: "Criptoanálise, Five Eyes, Vigilância em Massa",
                    en: "Cryptanalysis, Five Eyes, Mass Surveillance"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Inteligência", en: "Intelligence" },
                imagePlaceholder: "🕵️‍♂️"
            }
        ],
        militar: [
            {
                nome: "US Cyber Command",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                descricao: {
                    pt: "Comando cibernético unificado das Forças Armadas dos EUA. Responsável por operações defensivas e ofensivas no ciberespaço.",
                    en: "Unified cyber command of US Armed Forces. Responsible for defensive and offensive operations in cyberspace."
                },
                especialidade: {
                    pt: "Operações Militares Cibernéticas, Defesa de Redes",
                    en: "Cyber Military Operations, Network Defense"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Militar", en: "Military" },
                imagePlaceholder: "🎖️"
            },
            {
                nome: "PLA Unit 61398",
                pais: { pt: "China", en: "China" },
                paisCode: "CN",
                descricao: {
                    pt: "Unidade do Exército de Libertação Popular chinês responsável por espionagem cibernética em larga escala contra alvos ocidentais.",
                    en: "People's Liberation Army unit responsible for large-scale cyber espionage against Western targets."
                },
                especialidade: {
                    pt: "APT1, Espionagem Industrial, Persistência",
                    en: "APT1, Industrial Espionage, Persistence"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Militar", en: "Military" },
                imagePlaceholder: "🇨🇳"
            }
        ],
        policia: [
            {
                nome: "FBI Cyber Division",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                descricao: {
                    pt: "Divisão do FBI focada em combate ao cibercrime, terrorismo cibernético e operações contra ransomware e fraudes financeiras.",
                    en: "FBI division focused on fighting cybercrime, cyber terrorism, and operations against ransomware and financial fraud."
                },
                especialidade: {
                    pt: "Investigação de Crimes Cibernéticos, Takedowns",
                    en: "Cybercrime Investigation, Takedowns"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Polícia", en: "Police" },
                imagePlaceholder: "👮"
            },
            {
                nome: "Europol EC3",
                pais: { pt: "União Europeia", en: "European Union" },
                paisCode: "EU",
                descricao: {
                    pt: "Centro Europeu de Cibercrime, coordena operações multinacionais contra grupos criminosos digitais e fraudes online.",
                    en: "European Cybercrime Centre, coordinates multinational operations against digital criminal groups and online fraud."
                },
                especialidade: {
                    pt: "Cooperação Internacional, Desmantelamento de Botnets",
                    en: "International Cooperation, Botnet Takedowns"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Polícia", en: "Police" },
                imagePlaceholder: "🇪🇺"
            }
        ]
    }
};

// Lista de países (usada na Tela 2)
const countries = [
    { code: "RU", name: { pt: "Rússia", en: "Russia" }, flag: "🇷🇺" },
    { code: "US", name: { pt: "EUA", en: "USA" }, flag: "🇺🇸" },
    { code: "CN", name: { pt: "China", en: "China" }, flag: "🇨🇳" },
    { code: "KP", name: { pt: "Coreia do Norte", en: "North Korea" }, flag: "🇰🇵" },
    { code: "IR", name: { pt: "Irã", en: "Iran" }, flag: "🇮🇷" },
    { code: "KR", name: { pt: "Coreia do Sul", en: "South Korea" }, flag: "🇰🇷" },
    { code: "IL", name: { pt: "Israel", en: "Israel" }, flag: "🇮🇱" },
    { code: "GB", name: { pt: "Reino Unido", en: "United Kingdom" }, flag: "🇬🇧" },
    { code: "DE", name: { pt: "Alemanha", en: "Germany" }, flag: "🇩🇪" },
    { code: "FR", name: { pt: "França", en: "France" }, flag: "🇫🇷" },
    { code: "BR", name: { pt: "Brasil", en: "Brazil" }, flag: "🇧🇷" },
    { code: "IN", name: { pt: "Índia", en: "India" }, flag: "🇮🇳" },
    { code: "UN", name: { pt: "Global", en: "Global" }, flag: "🌐" },
    { code: "EU", name: { pt: "União Europeia", en: "European Union" }, flag: "🇪🇺" }
];

// Traduções da interface
const translations = {
    pt: {
        "title-category": "Escolha a Categoria de Ameaça",
        "subtitle-category": "Selecione o tipo de ator de ameaça que deseja explorar",
        "category-groups": "Grupos",
        "desc-groups": "Organizações criminosas e coletivos",
        "category-individuals": "Indivíduos",
        "desc-individuals": "Hackers e criminosos solitários",
        "category-gov": "Organizações Governamentais",
        "desc-gov": "Agências estatais e militares",
        
        "subcat-ransomware": "Ransomware",
        "subcat-hacktivism": "Hacktivismo",
        "subcat-espionage": "Espionagem",
        "subcat-profit": "Lucro",
        "subcat-fame": "Fama",
        "subcat-teens": "Adolescentes",
        "subcat-intelligence": "Inteligência",
        "subcat-military": "Militar",
        "subcat-police": "Polícia",
        
        "title-geopolitics": "Selecione o País de Origem",
        "subtitle-geopolitics": "Escolha a região geopolítica para filtrar as ameaças",
        
        "title-cards": "Cards de Ameaças",
        
        "btn-back": "Voltar"
    },
    en: {
        "title-category": "Choose Threat Category",
        "subtitle-category": "Select the type of threat actor you want to explore",
        "category-groups": "Groups",
        "desc-groups": "Criminal organizations and collectives",
        "category-individuals": "Individuals",
        "desc-individuals": "Lone hackers and criminals",
        "category-gov": "Government Organizations",
        "desc-gov": "State agencies and military",
        
        "subcat-ransomware": "Ransomware",
        "subcat-hacktivism": "Hacktivism",
        "subcat-espionage": "Espionage",
        "subcat-profit": "Profit",
        "subcat-fame": "Fame",
        "subcat-teens": "Teenagers",
        "subcat-intelligence": "Intelligence",
        "subcat-military": "Military",
        "subcat-police": "Police",
        
        "title-geopolitics": "Select Country of Origin",
        "subtitle-geopolitics": "Choose the geopolitical region to filter threats",
        
        "title-cards": "Threat Cards",
        
        "btn-back": "Back"
    }
};