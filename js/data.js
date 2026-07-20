// Banco de Dados Centralizado - Cyber Threat Intelligence Portfolio
// TAXONOMIA TÉCNICA RIGOROSA V2.0

const cyberDatabase = {
    // ═══════════════════════════════════════════════════════════════
    // GRUPOS DE AMEAÇA
    // Subcategorias: "lucro", "governo", "osint_sigint"
    // ═══════════════════════════════════════════════════════════════
    
    grupos: {
        // LUCRO - Ransomware, Extorsão, Crimes Financeiros
        lucro: [
            // RÚSSIA
            {
                nome: "LockBit",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                subcategoria: "lucro",
                descricao: {
                    pt: "Sindicato global de Ransomware-as-a-Service mais prolífico de 2022-2023. Desmantelado pela Operação Cronos em 2024 após ataques a mais de 2.000 organizações globais com extorsões de dupla e tripla camada.",
                    en: "Most prolific global Ransomware-as-a-Service syndicate of 2022-2023. Dismantled by Operation Cronos in 2024 after attacking over 2,000 global organizations with double and triple extortion."
                },
                especialidade: {
                    pt: "Ransomware-as-a-Service (RaaS), Dupla Extorsão, Afiliados Internacionais",
                    en: "Ransomware-as-a-Service (RaaS), Double Extortion, International Affiliates"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Ransomware / Lucro", en: "Ransomware / Profit" },
                imagePlaceholder: "🔒"
            },
            {
                nome: "DarkSide / BlackMatter",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                subcategoria: "lucro",
                descricao: {
                    pt: "Grupo profissional responsável pelo ataque ao Colonial Pipeline (2021), causando crise nacional de combustível nos EUA. Rebranded como BlackMatter após pressão governamental russa.",
                    en: "Professional group responsible for Colonial Pipeline attack (2021), causing national fuel crisis in USA. Rebranded as BlackMatter after Russian government pressure."
                },
                especialidade: {
                    pt: "Infraestrutura Crítica, Ransomware Corporativo, Negociação Estratégica",
                    en: "Critical Infrastructure, Corporate Ransomware, Strategic Negotiation"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Ransomware / Lucro", en: "Ransomware / Profit" },
                imagePlaceholder: "⛽"
            },
            {
                nome: "Conti",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                subcategoria: "lucro",
                descricao: {
                    pt: "Organização criminosa dissolvida em 2022 após massivo vazamento interno. Originou Royal, BlackBasta e outros sucessores que dominam a cena atual de ransomware.",
                    en: "Criminal organization dissolved in 2022 after massive internal leak. Spawned Royal, BlackBasta and other successors dominating current ransomware scene."
                },
                especialidade: {
                    pt: "RaaS Profissionalizado, Ataques a Governos, Desenvolvimento de Malware",
                    en: "Professionalized RaaS, Government Attacks, Malware Development"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Ransomware / Lucro", en: "Ransomware / Profit" },
                imagePlaceholder: "💰"
            },
            
            // COREIA DO NORTE
            {
                nome: "Lazarus Group / APT38",
                pais: { pt: "Coreia do Norte", en: "North Korea" },
                paisCode: "KP",
                subcategoria: "lucro",
                descricao: {
                    pt: "Grupo estatal norte-coreano focado em heists financeiros bilionários. Responsável pelo roubo de US$ 81 milhões do Bangladesh Bank, hack da Sony Pictures e WannaCry. Opera mixers de criptomoedas para financiar o programa nuclear.",
                    en: "North Korean state group focused on billion-dollar financial heists. Responsible for $81M Bangladesh Bank theft, Sony Pictures hack, and WannaCry. Operates crypto mixers to fund nuclear program."
                },
                especialidade: {
                    pt: "Heists SWIFT, Lavagem de Criptomoedas, Wiper Malware",
                    en: "SWIFT Heists, Cryptocurrency Laundering, Wiper Malware"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Lucro Estatal / APT", en: "State Profit / APT" },
                imagePlaceholder: "🇰🇵"
            },
        ],
        
        // OSINT/SIGINT - Hacktivismo, Coleta de Dados, Surveillance
        osint_sigint: [
            // RÚSSIA
            {
                nome: "Killnet | Deanon Club",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                subcategoria: "osint_sigint",
                descricao: {
                    pt: "Coletivo pró-Kremlin formado durante a invasão da Ucrânia. Especializado em DDoS em massa contra alvos da OTAN, instituições europeias e infraestruturas críticas. Braço cibernético não-oficial da guerra de informação russa.",
                    en: "Pro-Kremlin collective formed during Ukraine invasion. Specialized in mass DDoS against NATO targets, European institutions and critical infrastructures. Unofficial cyber arm of Russian information warfare."
                },
                especialidade: {
                    pt: "DDoS Coordenado, Guerra de Informação, Defacement Político",
                    en: "Coordinated DDoS, Information Warfare, Political Defacement"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Hacktivismo / Fama", en: "Hacktivism / Fame" },
                imagePlaceholder: "⚔️"
            },
            
            // GLOBAL
            {
                nome: "Anonymous",
                pais: { pt: "Global", en: "Global" },
                paisCode: "UN",
                subcategoria: "osint_sigint",
                descricao: {
                    pt: "Coletivo descentralizado mais icônico da era digital. Ativo desde 2003 contra scientology, governos autoritários e corporações. Operou OpPedophilia, OpTunisia, OpIran e ressurgiu em 2022 com OpRussia.",
                    en: "Most iconic decentralized collective of digital era. Active since 2003 against scientology, authoritarian governments and corporations. Operated OpPedophilia, OpTunisia, OpIran and resurged in 2022 with OpRussia."
                },
                especialidade: {
                    pt: "DDoS Distribuído, Vazamento de Dados, Justiça Hacker",
                    en: "Distributed DDoS, Data Leaks, Hacker Justice"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Hacktivismo / Lenda", en: "Hacktivism / Legend" },
                imagePlaceholder: "🎭"
            },
            
            // UNIÃO EUROPEIA
            {
                nome: "Chaos Computer Club (CCC)",
                pais: { pt: "União Europeia", en: "European Union" },
                paisCode: "EU",
                subcategoria: "osint_sigint",
                descricao: {
                    pt: "Maior e mais antigo coletivo hacker ético da Europa, fundado em 1981 na Alemanha. Responsável por expor vulnerabilidades governamentais, defender privacidade digital e organizar o famoso Chaos Communication Congress anual.",
                    en: "Largest and oldest ethical hacker collective in Europe, founded in 1981 in Germany. Responsible for exposing government vulnerabilities, defending digital privacy and organizing famous annual Chaos Communication Congress."
                },
                especialidade: {
                    pt: "Pesquisa de Segurança, Ativismo Digital, Exposição de Vulnerabilidades",
                    en: "Security Research, Digital Activism, Vulnerability Disclosure"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Hacktivismo Ético / Fama", en: "Ethical Hacktivism / Fame" },
                imagePlaceholder: "🇪🇺"
            },
        ],
        
        // GOVERNO - APTs Estatais, Espionagem Cibernética
        governo: [
            // RÚSSIA
            {
                nome: "Sandworm Team (GRU Unit 74455)",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                subcategoria: "governo",
                descricao: {
                    pt: "Unidade de elite do GRU russo considerada o APT mais destrutivo do mundo. Responsável por BlackEnergy, NotPetya (US$ 10 bilhões em danos), quedas da rede elétrica ucraniana e sabotagem das Olimpíadas de Pyeongchang 2018.",
                    en: "Elite GRU unit considered world's most destructive APT. Responsible for BlackEnergy, NotPetya ($10B in damages), Ukrainian power grid blackouts and 2018 Pyeongchang Olympics sabotage."
                },
                especialidade: {
                    pt: "Sabotagem Industrial, ICS/SCADA, Wiper Malware, Guerra Híbrida",
                    en: "Industrial Sabotage, ICS/SCADA, Wiper Malware, Hybrid Warfare"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "APT Estatal / Governo", en: "State APT / Government" },
                imagePlaceholder: "assets/images/military.png"
            },
            {
                nome: "APT28 (Fancy Bear)",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                subcategoria: "governo",
                descricao: {
                    pt: "Grupo vinculado ao GRU russo, ativo desde 2004. Responsável pelo hack do DNC em 2016, ataques ao Bundestag alemão e operações contra governos, militares e mídia na Europa e EUA.",
                    en: "Group linked to Russian GRU, active since 2004. Responsible for 2016 DNC hack, German Bundestag attacks and operations against governments, military and media in Europe and USA."
                },
                especialidade: {
                    pt: "Spear Phishing, Exploits Zero-Day, Interferência Eleitoral",
                    en: "Spear Phishing, Zero-Day Exploits, Election Interference"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "APT Estatal / Governo", en: "State APT / Government" },
                imagePlaceholder: "assets/images/military.png"
            },
            {
                nome: "APT29 (Cozy Bear)",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                subcategoria: "governo",
                descricao: {
                    pt: "Grupo vinculado ao SVR russo, focado em espionagem de longo prazo contra think tanks, governos e pesquisas sensíveis. Responsável pelo SolarWinds (2020), maior hack de supply chain da história.",
                    en: "Group linked to Russian SVR, focused on long-term espionage against think tanks, governments and sensitive research. Responsible for SolarWinds (2020), largest supply chain hack in history."
                },
                especialidade: {
                    pt: "Supply Chain Attacks, Persistência Avançada, Stealth Operacional",
                    en: "Supply Chain Attacks, Advanced Persistence, Operational Stealth"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "APT Estatal / Governo", en: "State APT / Government" },
                imagePlaceholder: "assets/images/military.png"
            },
            
            // CHINA
            {
                nome: "APT41 (Double Dragon)",
                pais: { pt: "China", en: "China" },
                paisCode: "CN",
                subcategoria: "governo",
                descricao: {
                    pt: "Grupo híbrido único que combina espionagem estatal chinesa com crimes financeiros pessoais. Alvo de indiciamento pelo DOJ em 2020. Opera desde 2012 contra telecomunicações, saúde e indústria de jogos.",
                    en: "Unique hybrid group combining Chinese state espionage with personal financial crimes. Targeted by DOJ indictment in 2020. Operating since 2012 against telecommunications, healthcare and gaming industry."
                },
                especialidade: {
                    pt: "Espionagem Dupla, Supply Chain, Monetização Paralela",
                    en: "Dual Espionage, Supply Chain, Parallel Monetization"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "APT Estatal / Governo", en: "State APT / Government" },
                imagePlaceholder: "assets/images/military.png"
            },
            {
                nome: "Volt Typhoon",
                pais: { pt: "China", en: "China" },
                paisCode: "CN",
                subcategoria: "governo",
                descricao: {
                    pt: "APT chinês descoberto em 2023 focado em pré-posicionamento estratégico e persistência oculta em infraestruturas críticas civis dos EUA (energia, água, comunicações). Living-off-the-land para evasão.",
                    en: "Chinese APT discovered in 2023 focused on strategic pre-positioning and stealthy persistence in US critical civilian infrastructures (energy, water, communications). Living-off-the-land for evasion."
                },
                especialidade: {
                    pt: "Pre-positioning, Living off the Land, Infraestrutura Crítica",
                    en: "Pre-positioning, Living off the Land, Critical Infrastructure"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "APT Estatal / Governo", en: "State APT / Government" },
                imagePlaceholder: "assets/images/military.png"
            },
            
            // IRÃ
            {
                nome: "MuddyWater (APT33)",
                pais: { pt: "Irã", en: "Iran" },
                paisCode: "IR",
                subcategoria: "governo",
                descricao: {
                    pt: "Grupo vinculado ao MOIS (Ministério de Inteligência iraniano). Focado em espionagem regional contra setores de aviação, energia, petroquímica e defesa no Oriente Médio, Europa e EUA.",
                    en: "Group linked to Iranian MOIS (Ministry of Intelligence). Focused on regional espionage against aviation, energy, petrochemical and defense sectors in Middle East, Europe and USA."
                },
                especialidade: {
                    pt: "Spear Phishing Avançado, PowerShell Malware, Persistência Regional",
                    en: "Advanced Spear Phishing, PowerShell Malware, Regional Persistence"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "APT Estatal / Governo", en: "State APT / Government" },
                imagePlaceholder: "assets/images/military.png"
            },
            {
                nome: "Charming Kitten (APT35)",
                pais: { pt: "Irã", en: "Iran" },
                paisCode: "IR",
                subcategoria: "governo",
                descricao: {
                    pt: "APT iraniano focado em campanhas cirúrgicas de spear-phishing contra dissidentes, ativistas, jornalistas e funcionários governamentais. Especializado em credential harvesting e vigilância digital.",
                    en: "Iranian APT focused on surgical spear-phishing campaigns against dissidents, activists, journalists and government officials. Specialized in credential harvesting and digital surveillance."
                },
                especialidade: {
                    pt: "Credential Harvesting, Engenharia Social, Vigilância Política",
                    en: "Credential Harvesting, Social Engineering, Political Surveillance"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "APT Estatal / Governo", en: "State APT / Government" },
                imagePlaceholder: "assets/images/military.png"
            },
            
            // COREIA DO NORTE
            {
                nome: "Kimsuky (Thallium)",
                pais: { pt: "Coreia do Norte", en: "North Korea" },
                paisCode: "KP",
                subcategoria: "governo",
                descricao: {
                    pt: "Grupo norte-coreano focado em coleta de inteligência sobre políticas nucleares, sanções e relações diplomáticas. Usa engenharia social sofisticada contra think tanks, pesquisadores e diplomatas globais.",
                    en: "North Korean group focused on intelligence gathering about nuclear policies, sanctions and diplomatic relations. Uses sophisticated social engineering against think tanks, researchers and global diplomats."
                },
                especialidade: {
                    pt: "Inteligência Geopolítica, Engenharia Social, Coleta de OSINT",
                    en: "Geopolitical Intelligence, Social Engineering, OSINT Collection"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "APT Estatal / Governo", en: "State APT / Government" },
                imagePlaceholder: "assets/images/military.png"
            },
        ],
    },

    // ═══════════════════════════════════════════════════════════════
    // INDIVÍDUOS
    // Subcategorias: "lendas", "especialistas", "lucro"
    // ═══════════════════════════════════════════════════════════════
    
    individuos: {
        // LENDAS - Hackers Históricos e Famosos
        lendas: [
            // EUA
            {
                nome: "Kevin Mitnick",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                subcategoria: "lendas",
                descricao: {
                    pt: "O hacker mais procurado dos EUA nos anos 90. Pioneiro da engenharia social moderna, invadiu Nokia, Motorola e Pentágono. Após prisão, tornou-se consultor de segurança renomado e autor best-seller. Faleceu em 2023.",
                    en: "Most wanted hacker in USA in the 90s. Pioneer of modern social engineering, breached Nokia, Motorola and Pentagon. After prison, became renowned security consultant and best-selling author. Passed away in 2023."
                },
                especialidade: {
                    pt: "Engenharia Social Avançada, Phreaking, Exploração de Confiança",
                    en: "Advanced Social Engineering, Phreaking, Trust Exploitation"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Lenda / Pioneiro", en: "Legend / Pioneer" },
                imagePlaceholder: "👑"
            },
            {
                nome: "Adrian Lamo",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                subcategoria: "lendas",
                descricao: {
                    pt: "Conhecido como 'Hacker Sem-Teto', invadiu Microsoft, Yahoo e New York Times usando conexões públicas de cafeterias. Tornou-se controverso ao delatar Chelsea Manning ao FBI em 2010. Faleceu em 2018.",
                    en: "Known as 'Homeless Hacker', breached Microsoft, Yahoo and New York Times using public cafe connections. Became controversial for turning in Chelsea Manning to FBI in 2010. Passed away in 2018."
                },
                especialidade: {
                    pt: "Pentesting Não-Autorizado, Exploração Oportunista",
                    en: "Unauthorized Pentesting, Opportunistic Exploitation"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Lenda / Controverso", en: "Legend / Controversial" },
                imagePlaceholder: "🏴"
            },
        ],
        
        // ESPECIALISTAS - Alto Nível Técnico, Exploits, Pesquisa
        especialistas: [
            // RÚSSIA
            {
                nome: "Phineas Fisher",
                pais: { pt: "Rússia", en: "Russia" },
                paisCode: "RU",
                subcategoria: "especialistas",
                descricao: {
                    pt: "Hacker vigilante anônimo responsável por invadir e vazar dados da Hacking Team (2015) e Cayman National Bank. Publica tutoriais técnicos detalhados de suas invasões promovendo hacktivismo contra empresas de surveillance.",
                    en: "Anonymous vigilante hacker responsible for breaching and leaking Hacking Team (2015) and Cayman National Bank data. Publishes detailed technical tutorials of breaches promoting hacktivism against surveillance companies."
                },
                especialidade: {
                    pt: "Exploits Zero-Day, Infiltração Corporativa, Hacktivismo Técnico",
                    en: "Zero-Day Exploits, Corporate Infiltration, Technical Hacktivism"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Especialista / Vigilante", en: "Expert / Vigilante" },
                imagePlaceholder: "🦊"
            },
        ],
        
        // LUCRO - Cibercriminosos, Fraudes Financeiras
        lucro: [
            // EUA
            {
                nome: "Albert Gonzalez",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                subcategoria: "lucro",
                descricao: {
                    pt: "Líder do maior roubo de cartões de crédito da história (170 milhões de cartões). Hackeou TJX, Heartland Payment Systems, 7-Eleven e outros varejistas. Preso em 2008, condenado a 20 anos de prisão federal.",
                    en: "Leader of largest credit card theft in history (170 million cards). Hacked TJX, Heartland Payment Systems, 7-Eleven and other retailers. Arrested in 2008, sentenced to 20 years federal prison."
                },
                especialidade: {
                    pt: "SQL Injection, Packet Sniffing, Carding em Massa",
                    en: "SQL Injection, Packet Sniffing, Mass Carding"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Cibercriminoso / Lucro", en: "Cybercriminal / Profit" },
                imagePlaceholder: "💳"
            },
            {
                nome: "Marcus Hutchins (MalwareTech)",
                pais: { pt: "União Europeia", en: "European Union" },
                paisCode: "EU",
                subcategoria: "lucro",
                descricao: {
                    pt: "Pesquisador que acidentalmente parou o WannaCry em 2017 descobrindo kill switch. Anteriormente desenvolveu o banking trojan Kronos. Condenado nos EUA por malware, mas recebeu sentença suspensa.",
                    en: "Researcher who accidentally stopped WannaCry in 2017 by discovering kill switch. Previously developed Kronos banking trojan. Convicted in USA for malware but received suspended sentence."
                },
                especialidade: {
                    pt: "Malware Banking, Análise Reversa, Kill Switch Discovery",
                    en: "Banking Malware, Reverse Engineering, Kill Switch Discovery"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Duplo Papel / Lucro-Herói", en: "Dual Role / Profit-Hero" },
                imagePlaceholder: "🦸"
            },
        ],
    },

    // ═══════════════════════════════════════════════════════════════
    // ORGANIZAÇÕES GOVERNAMENTAIS
    // Subcategorias: "militares", "inteligencia", "policia_especializada"
    // ═══════════════════════════════════════════════════════════════
    
    organizacoes: {
        // MILITARES - Guerra Cibernética, Forças Armadas
        militares: [
            // EUA
            {
                nome: "Cyber National Mission Force (CNMF)",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                subcategoria: "militares",
                descricao: {
                    pt: "Força-tarefa ofensiva do US Cyber Command. Conduz operações 'Hunt Forward' proativas em parceria com aliados, identificando e neutralizando ameaças adversárias antes que ataquem redes americanas.",
                    en: "Offensive task force of US Cyber Command. Conducts proactive 'Hunt Forward' operations partnering with allies, identifying and neutralizing adversary threats before they attack American networks."
                },
                especialidade: {
                    pt: "Operações Ofensivas, Hunt Forward, Neutralização de Ameaças",
                    en: "Offensive Operations, Hunt Forward, Threat Neutralization"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Militar / Ofensivo", en: "Military / Offensive" },
                imagePlaceholder: "🎖️"
            },
            
            // CHINA
            {
                nome: "Strategic Support Force (SSF)",
                pais: { pt: "China", en: "China" },
                paisCode: "CN",
                subcategoria: "militares",
                descricao: {
                    pt: "Comando central chinês unificando guerra espacial, eletrônica e cibernética. Criado em 2015 para integrar capacidades de informação do PLA. Responsável por coordenar todos os APTs militares chineses.",
                    en: "Chinese unified central command integrating space, electronic and cyber warfare. Created in 2015 to integrate PLA information capabilities. Responsible for coordinating all Chinese military APTs."
                },
                especialidade: {
                    pt: "Guerra Multi-Domínio, Coordenação de APTs, Operações Espaciais",
                    en: "Multi-Domain Warfare, APT Coordination, Space Operations"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Militar / Estratégico", en: "Military / Strategic" },
                imagePlaceholder: "🛰️"
            },
            {
                nome: "PLA Unit 61398 (APT1)",
                pais: { pt: "China", en: "China" },
                paisCode: "CN",
                subcategoria: "militares",
                descricao: {
                    pt: "Unidade militar chinesa exposta pela Mandiant em 2013. Opera em prédio de 12 andares em Xangai realizando espionagem industrial massiva contra empresas ocidentais de tecnologia, defesa e energia.",
                    en: "Chinese military unit exposed by Mandiant in 2013. Operates from 12-story building in Shanghai conducting massive industrial espionage against Western technology, defense and energy companies."
                },
                especialidade: {
                    pt: "Espionagem Industrial, Roubo de PI, Persistência de Longo Prazo",
                    en: "Industrial Espionage, IP Theft, Long-Term Persistence"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Militar / Espionagem", en: "Military / Espionage" },
                imagePlaceholder: "🏢"
            },
            
            // IRÃ
            {
                nome: "IRGC Cyber Electronic Command",
                pais: { pt: "Irã", en: "Iran" },
                paisCode: "IR",
                subcategoria: "militares",
                descricao: {
                    pt: "Braço cibernético da Guarda Revolucionária Islâmica iraniana. Responsável por ataques destrutivos contra infraestrutura saudita (Shamoon) e operações de influência durante protestos internos.",
                    en: "Cyber arm of Iranian Islamic Revolutionary Guard Corps. Responsible for destructive attacks against Saudi infrastructure (Shamoon) and influence operations during internal protests."
                },
                especialidade: {
                    pt: "Wiper Attacks, Operações Destrutivas, Guerra de Informação Regional",
                    en: "Wiper Attacks, Destructive Operations, Regional Information Warfare"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Militar / Destrutivo", en: "Military / Destructive" },
                imagePlaceholder: "💣"
            },
            
            // COREIA DO NORTE
            {
                nome: "Bureau 121",
                pais: { pt: "Coreia do Norte", en: "North Korea" },
                paisCode: "KP",
                subcategoria: "militares",
                descricao: {
                    pt: "Agência militar secreta de guerra cibernética norte-coreana baseada em Pyongyang. Comandada pelo Reconnaissance General Bureau, opera células em China e Sudeste Asiático para operações globais.",
                    en: "North Korean secret military cyber warfare agency based in Pyongyang. Commanded by Reconnaissance General Bureau, operates cells in China and Southeast Asia for global operations."
                },
                especialidade: {
                    pt: "Guerra Cibernética Assimétrica, Células Internacionais, Operações Secretas",
                    en: "Asymmetric Cyber Warfare, International Cells, Covert Operations"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Militar / Covert", en: "Military / Covert" },
                imagePlaceholder: "🔐"
            },
        ],
        
        // INTELIGÊNCIA - Espionagem, SIGINT, Operações Encobertas
        inteligencia: [
            // EUA
            {
                nome: "NSA Tailored Access Operations (TAO)",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                subcategoria: "inteligencia",
                descricao: {
                    pt: "Unidade de elite da NSA focada em infiltrações sob medida e exploits customizados. Exposta por Edward Snowden e Shadow Brokers, desenvolve ferramentas como EternalBlue usado no WannaCry.",
                    en: "Elite NSA unit focused on tailored infiltrations and customized exploits. Exposed by Edward Snowden and Shadow Brokers, develops tools like EternalBlue used in WannaCry."
                },
                especialidade: {
                    pt: "Exploits Zero-Day, Implantes de Hardware, SIGINT Ofensivo",
                    en: "Zero-Day Exploits, Hardware Implants, Offensive SIGINT"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Inteligência / Elite", en: "Intelligence / Elite" },
                imagePlaceholder: "🦅"
            },
            
            // ISRAEL
            {
                nome: "Unit 8200",
                pais: { pt: "Israel", en: "Israel" },
                paisCode: "IL",
                subcategoria: "inteligencia",
                descricao: {
                    pt: "Lendária unidade de SIGINT das FDI, equivalente israelense da NSA. Responsável por Stuxnet (com EUA), vigilância regional avançada e berço de empresas de cybersecurity como Check Point e Palo Alto Networks.",
                    en: "Legendary IDF SIGINT unit, Israeli equivalent of NSA. Responsible for Stuxnet (with USA), advanced regional surveillance and birthplace of cybersecurity companies like Check Point and Palo Alto Networks."
                },
                especialidade: {
                    pt: "SIGINT Avançado, Cyber Warfare, Descriptografia Criptográfica",
                    en: "Advanced SIGINT, Cyber Warfare, Cryptographic Decryption"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Inteligência / Elite", en: "Intelligence / Elite" },
                imagePlaceholder: "🇮🇱"
            },
            {
                nome: "Unit 9900",
                pais: { pt: "Israel", en: "Israel" },
                paisCode: "IL",
                subcategoria: "inteligencia",
                descricao: {
                    pt: "Unidade das FDI focada em inteligência visual, geoespacial e análise de imagens cibernéticas. Combina GEOINT tradicional com análise de dados digitais para operações de precisão.",
                    en: "IDF unit focused on visual intelligence, geospatial and cyber image analysis. Combines traditional GEOINT with digital data analysis for precision operations."
                },
                especialidade: {
                    pt: "GEOINT Cibernético, Análise Visual, Inteligência Geoespacial",
                    en: "Cyber GEOINT, Visual Analysis, Geospatial Intelligence"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Inteligência / GEOINT", en: "Intelligence / GEOINT" },
                imagePlaceholder: "🛰️"
            },
            {
                nome: "Mossad Cyber Division",
                pais: { pt: "Israel", en: "Israel" },
                paisCode: "IL",
                subcategoria: "inteligencia",
                descricao: {
                    pt: "Divisão cibernética do Mossad focada em operações ofensivas contra programa nuclear iraniano, terrorismo e espionagem estratégica. Responsável por Flame, Duqu e sabotagem física via cyber de centrifugas iranianas.",
                    en: "Mossad cyber division focused on offensive operations against Iranian nuclear program, terrorism and strategic espionage. Responsible for Flame, Duqu and cyber-physical sabotage of Iranian centrifuges."
                },
                especialidade: {
                    pt: "Sabotagem Cibernética, Operações Encobertas, Cyber-Physical Attacks",
                    en: "Cyber Sabotage, Covert Operations, Cyber-Physical Attacks"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Inteligência / Covert", en: "Intelligence / Covert" },
                imagePlaceholder: "🔯"
            },
            
            // UNIÃO EUROPEIA
            {
                nome: "ANSSI",
                pais: { pt: "União Europeia", en: "European Union" },
                paisCode: "EU",
                subcategoria: "inteligencia",
                descricao: {
                    pt: "Agência Nacional de Segurança de Sistemas de Informação da França. Responsável por defesa cibernética nacional, resposta a incidentes e desenvolvimento de capacidades ofensivas francesas.",
                    en: "French National Agency for Information Systems Security. Responsible for national cyber defense, incident response and development of French offensive capabilities."
                },
                especialidade: {
                    pt: "Defesa Nacional, Resposta a Incidentes, Capacidades Ofensivas",
                    en: "National Defense, Incident Response, Offensive Capabilities"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Inteligência / Nacional", en: "Intelligence / National" },
                imagePlaceholder: "🇫🇷"
            },
        ],
        
        // POLÍCIA ESPECIALIZADA - Law Enforcement, Investigação, Takedowns
        policia_especializada: [
            // EUA
            {
                nome: "FBI Cyber Division",
                pais: { pt: "EUA", en: "USA" },
                paisCode: "US",
                subcategoria: "policia_especializada",
                descricao: {
                    pt: "Divisão de elite do FBI focada em combate ao cibercrime transnacional. Responsável por operações globais de apreensão de infraestrutura (Operação Cronos contra LockBit, takedown da AlphaBay e Silk Road).",
                    en: "Elite FBI division focused on fighting transnational cybercrime. Responsible for global infrastructure seizure operations (Operation Cronos against LockBit, AlphaBay and Silk Road takedowns)."
                },
                especialidade: {
                    pt: "Investigação de Ransomware, Takedowns Globais, Operações Undercover",
                    en: "Ransomware Investigation, Global Takedowns, Undercover Operations"
                },
                raridade: "⭐⭐⭐⭐⭐",
                tipo: { pt: "Polícia / Elite", en: "Police / Elite" },
                imagePlaceholder: "👮"
            },
            
            // UNIÃO EUROPEIA
            {
                nome: "Europol EC3",
                pais: { pt: "União Europeia", en: "European Union" },
                paisCode: "EU",
                subcategoria: "policia_especializada",
                descricao: {
                    pt: "Centro Europeu de Cibercrime da Europol. Coordena operações multinacionais de desmantelamento de botnets, marketplaces da dark web e redes de ransomware através de Joint Cybercrime Action Taskforce.",
                    en: "European Cybercrime Centre of Europol. Coordinates multinational operations dismantling botnets, dark web marketplaces and ransomware networks through Joint Cybercrime Action Taskforce."
                },
                especialidade: {
                    pt: "Cooperação Internacional, Desmantelamento de Botnets, Dark Web Operations",
                    en: "International Cooperation, Botnet Dismantling, Dark Web Operations"
                },
                raridade: "⭐⭐⭐⭐",
                tipo: { pt: "Polícia / Internacional", en: "Police / International" },
                imagePlaceholder: "🚨"
            },
        ],
    },
};

// Lista de países (usada na Tela 1)
const countries = [
    { code: "RU", name: { pt: "Rússia", en: "Russia" }, flag: "🇷🇺" },
    { code: "US", name: { pt: "EUA", en: "USA" }, flag: "🇺🇸" },
    { code: "CN", name: { pt: "China", en: "China" }, flag: "🇨🇳" },
    { code: "KP", name: { pt: "Coreia do Norte", en: "North Korea" }, flag: "🇰🇵" },
    { code: "IR", name: { pt: "Irã", en: "Iran" }, flag: "🇮🇷" },
    { code: "IL", name: { pt: "Israel", en: "Israel" }, flag: "🇮🇱" },
    { code: "EU", name: { pt: "União Europeia", en: "European Union" }, flag: "🇪🇺" },
    { code: "UN", name: { pt: "Global", en: "Global" }, flag: "🌐" }
];

// Traduções da interface
const translations = {
    pt: {
        "title-geopolitics": "Selecione o País de Origem",
        "subtitle-geopolitics": "Escolha a região geopolítica para iniciar a análise",
        
        "title-category": "Escolha a Categoria de Ameaça",
        "subtitle-category": "Selecione o tipo de ator de ameaça que deseja explorar",
        "category-groups": "Grupos",
        "desc-groups": "Organizações criminosas e coletivos",
        "category-individuals": "Indivíduos",
        "desc-individuals": "Hackers e criminosos solitários",
        "category-gov": "Organizações Governamentais",
        "desc-gov": "Agências estatais e militares",
        
        "subcat-profit": "Lucro",
        "subcat-government": "Governo",
        "subcat-osint-sigint": "OSINT/SIGINT",
        "subcat-legends": "Lendas",
        "subcat-specialists": "Especialistas",
        "subcat-military": "Militares",
        "subcat-intelligence": "Inteligência",
        "subcat-police": "Polícia Especializada",
        
        "title-cards": "Cards de Ameaças",
        
        "btn-back": "Voltar"
    },
    en: {
        "title-geopolitics": "Select Country of Origin",
        "subtitle-geopolitics": "Choose the geopolitical region to start analysis",
        
        "title-category": "Choose Threat Category",
        "subtitle-category": "Select the type of threat actor you want to explore",
        "category-groups": "Groups",
        "desc-groups": "Criminal organizations and collectives",
        "category-individuals": "Individuals",
        "desc-individuals": "Lone hackers and criminals",
        "category-gov": "Government Organizations",
        "desc-gov": "State agencies and military",
        
        "subcat-profit": "Profit",
        "subcat-government": "Government",
        "subcat-osint-sigint": "OSINT/SIGINT",
        "subcat-legends": "Legends",
        "subcat-specialists": "Specialists",
        "subcat-military": "Military",
        "subcat-intelligence": "Intelligence",
        "subcat-police": "Specialized Police",
        
        "title-cards": "Threat Cards",
        
        "btn-back": "Back"
    }
};