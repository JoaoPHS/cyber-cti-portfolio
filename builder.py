#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE BUILDER v2.0
Automatiza a criação do arquivo js/data.js extraindo dados de:
- MITRE ATT&CK (Grupos)
- FBI Cyber's Most Wanted (Indivíduos)
- Atores históricos de Israel e UE (hardcoded)
═══════════════════════════════════════════════════════════════
"""

import json
import requests
import re
from datetime import datetime
from deep_translator import GoogleTranslator

# ═══════════════════════════════════════════════════════════════
# URLs DAS FONTES DE DADOS
# ═══════════════════════════════════════════════════════════════
MITRE_STIX_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
FBI_CYBER_API_URL = "https://api.fbi.gov/@wanted-person"

# ═══════════════════════════════════════════════════════════════
# DICIONÁRIO DE JARGÕES DE CTI (Cyber Glossary)
# Corrige traduções literais bizarras mantendo contexto técnico
# ═══════════════════════════════════════════════════════════════
CYBER_JARGON_FIXES = {
    'bebedouro': 'Watering Hole Attack',
    'buraco de água': 'Watering Hole Attack',
    'buraco aquático': 'Watering Hole Attack',
    'lança-phishing': 'Spear-Phishing',
    'phishing de lança': 'Spear-Phishing',
    'lança de pesca': 'Spear-Phishing',
    'pesca com lança': 'Spear-Phishing',
    'software de resgate': 'Ransomware',
    'programa de resgate': 'Ransomware',
    'limpador': 'Wiper Malware',
    'limpadores de disco': 'Wiper Malware',
    'limpadores': 'Wiper Malware',
    'comando e controle': 'C2 (Command & Control)',
    'comando-e-controle': 'C2',
    'controle e comando': 'C2',
    'vulnerabilidade de dia zero': 'Zero-Day Exploit',
    'dia zero': 'Zero-Day',
    'exploit de dia zero': 'Zero-Day Exploit',
    'cadeia de suprimentos': 'Supply Chain Attack',
    'cadeia de fornecimento': 'Supply Chain Attack',
    'porta dos fundos': 'Backdoor',
    'porta traseira': 'Backdoor',
    'movimento lateral': 'Lateral Movement',
    'movimentação lateral': 'Lateral Movement',
    'colheita de credenciais': 'Credential Harvesting',
    'exfiltração de dados': 'Data Exfiltration',
    'vivendo da terra': 'Living off the Land (LotL)',
    'operações cibernéticas': 'Cyber Operations',
    'operação cibernética': 'Cyber Ops'
}

# ═══════════════════════════════════════════════════════════════
# ATRIBUIÇÃO GEOPOLÍTICA (Origem vs Alvos)
# ═══════════════════════════════════════════════════════════════

ORIGIN_KEYWORDS = {
    'RU': ['russia-based', 'russian intelligence', 'russian threat', 'russian federation',
           'linked to russia', 'attributed to russia', 'operates from russia',
           'gru unit', 'svr ', 'fsb ', 'kremlin', 'moscow-based',
           'russian state', 'russian military', 'russian cyber'],
    'CN': ['china-based', 'chinese state', 'chinese intelligence', 'chinese threat',
           'linked to china', 'attributed to china', 'operates from china',
           'pla unit', 'people\'s liberation army', 'mss ', 'beijing-based',
           'prc ', 'people\'s republic of china', 'chinese military'],
    'US': ['united states', 'u.s. intelligence', 'american intelligence',
           'nsa ', 'fbi cyber', 'operates from the united states'],
    'IR': ['iranian threat', 'iran-based', 'iranian intelligence', 'iranian state',
           'linked to iran', 'attributed to iran', 'operates from iran', 'operating out of iran',
           'irgc', 'iranian revolutionary guard', 'mois', 'ministry of intelligence',
           'tehran-based', 'iranian cyber', 'iranian hacker', 'islamic republic of iran'],
    'IL': ['israeli-affiliated', 'israeli intelligence', 'operating from israel',
           'affiliated with israeli', 'israel-based', 'unit 8200', 'israeli cyber', 'idf cyber'],
    'KP': ['north korean', 'north korea-based', 'dprk', 'attributed to north korea',
           'linked to north korea', 'based in pyongyang', 'pyongyang-based',
           'bureau 121', 'reconnaissance general bureau', 'rgb '],
    'EU': ['europe-based', 'european threat', 'operates from europe',
           'based in germany', 'based in france', 'based in uk',
           'british intelligence', 'french intelligence', 'german intelligence']
}

TARGET_EXCLUSION_KEYWORDS = [
    'targeting', 'targets', 'against', 'attacks on', 'attacking',
    'focused on', 'aimed at', 'directed at', 'compromised', 'victimized', 'targeted at'
]

FIXED_COUNTRY_GROUPS = {
    'muddywater': 'IR', 'apt33': 'IR', 'apt34': 'IR', 'apt35': 'IR', 'apt39': 'IR',
    'oilrig': 'IR', 'charming kitten': 'IR', 'magic hound': 'IR', 'rocket kitten': 'IR',
    'agrius': 'IR', 'cyberav3ngers': 'IR', 'fox kitten': 'IR', 'moses staff': 'IR',
    'sandworm': 'RU', 'apt28': 'RU', 'apt29': 'RU', 'turla': 'RU', 'cozy bear': 'RU',
    'fancy bear': 'RU', 'dragonfly': 'RU', 'wizard spider': 'RU', 'silence': 'RU',
    'gamaredon': 'RU', 'ember bear': 'RU',
    'lazarus': 'KP', 'apt38': 'KP', 'kimsuky': 'KP', 'andariel': 'KP', 'bluenoroff': 'KP',
    'thallium': 'KP', 'hidden cobra': 'KP', 'applejeus': 'KP',
    'predatory sparrow': 'IL', 'gonjeshke darande': 'IL',
    'apt1': 'CN', 'apt3': 'CN', 'apt10': 'CN', 'apt12': 'CN', 'apt15': 'CN',
    'apt16': 'CN', 'apt17': 'CN', 'apt19': 'CN', 'apt30': 'CN', 'apt40': 'CN',
    'apt41': 'CN', 'menupass': 'CN', 'winnti': 'CN', 'bronze': 'CN'
}

# ═══════════════════════════════════════════════════════════════
# ATORES HISTÓRICOS DE ELITE (Israel e UE)
# ═══════════════════════════════════════════════════════════════
ELITE_ACTORS = [
    {
        'nome': 'Shalev Hulio',
        'paisCode': 'IL',
        'categoria': 'individuos',
        'subcategoria': 'especialistas',
        'raridade': '⭐⭐⭐⭐⭐',
        'descricao': {
            'pt': 'Cofundador e ex-CEO da NSO Group, empresa israelense responsável pela criação do Pegasus, o spyware de zero-click mais sofisticado do mundo. O Pegasus foi usado por governos para vigilância de dissidentes, jornalistas e ativistas. Hulio construiu um império bilionário vendendo armas cibernéticas de nível militar.',
            'en': 'Co-founder and former CEO of NSO Group, Israeli company responsible for creating Pegasus, the world\'s most sophisticated zero-click spyware. Pegasus was used by governments for surveillance of dissidents, journalists and activists. Hulio built a billion-dollar empire selling military-grade cyber weapons.'
        },
        'especialidade': {
            'pt': 'Zero-Click Exploits, Spyware Commercial, Cyber Arms Trade',
            'en': 'Zero-Click Exploits, Commercial Spyware, Cyber Arms Trade'
        },
        'tipo': {
            'pt': 'Mercenário Cibernético / Elite',
            'en': 'Cyber Mercenary / Elite'
        },
        'tac': 98,
        'est': 95,
        'imagePlaceholder': '👤'
    },
    {
        'nome': 'Tal Dilian',
        'paisCode': 'IL',
        'categoria': 'individuos',
        'subcategoria': 'lucro',
        'raridade': '⭐⭐⭐⭐⭐',
        'descricao': {
            'pt': 'Ex-comandante da Unidade 8200 e fundador da Intellexa, criadora do Predator spyware. Dilian comercializa ferramentas de espionagem móvel para governos autoritários e corporações. Opera através de uma rede complexa de empresas de fachada em paraísos fiscais.',
            'en': 'Former Unit 8200 commander and founder of Intellexa, creator of Predator spyware. Dilian markets mobile espionage tools to authoritarian governments and corporations. Operates through a complex network of shell companies in tax havens.'
        },
        'especialidade': {
            'pt': 'Mobile Surveillance, Exploit-as-a-Service, SIGINT Operations',
            'en': 'Mobile Surveillance, Exploit-as-a-Service, SIGINT Operations'
        },
        'tipo': {
            'pt': 'Mercenário Cibernético / Lucro',
            'en': 'Cyber Mercenary / Profit'
        },
        'tac': 95,
        'est': 92,
        'imagePlaceholder': '👤'
    },
    {
        'nome': 'Sandro Gauci',
        'paisCode': 'EU',
        'categoria': 'individuos',
        'subcategoria': 'especialistas',
        'raridade': '⭐⭐⭐⭐',
        'descricao': {
            'pt': 'Pesquisador sênior de segurança em VoIP e telecomunicações, criador do SIPVicious, um dos frameworks de auditoria de segurança SIP/VoIP mais utilizados no mundo. Gauci é reconhecido globalmente por suas contribuições para a segurança de infraestruturas de telecomunicações.',
            'en': 'Senior security researcher in VoIP and telecommunications, creator of SIPVicious, one of the world\'s most used SIP/VoIP security audit frameworks. Gauci is globally recognized for his contributions to telecommunications infrastructure security.'
        },
        'especialidade': {
            'pt': 'VoIP Security, Telecom Auditing, SIP Protocol Research',
            'en': 'VoIP Security, Telecom Auditing, SIP Protocol Research'
        },
        'tipo': {
            'pt': 'Pesquisador de Segurança / Elite',
            'en': 'Security Researcher / Elite'
        },
        'tac': 92,
        'est': 80,
        'imagePlaceholder': '👤'
    },
    {
        'nome': 'Wau Holland',
        'paisCode': 'EU',
        'categoria': 'individuos',
        'subcategoria': 'lendas',
        'raridade': '⭐⭐⭐⭐⭐',
        'descricao': {
            'pt': 'Lendário cofundador do Chaos Computer Club (CCC) em 1981, o maior e mais antigo coletivo de hackers éticos da Europa. Holland foi pioneiro do hacktivismo político e defensor da privacidade digital. Sua filosofia de "hackear é aprender" influenciou gerações de pesquisadores de segurança.',
            'en': 'Legendary co-founder of Chaos Computer Club (CCC) in 1981, Europe\'s largest and oldest ethical hacker collective. Holland was a pioneer of political hacktivism and digital privacy advocate. His philosophy of "hacking is learning" influenced generations of security researchers.'
        },
        'especialidade': {
            'pt': 'Ethical Hacking, Digital Rights Activism, Hacker Culture',
            'en': 'Ethical Hacking, Digital Rights Activism, Hacker Culture'
        },
        'tipo': {
            'pt': 'Lenda Histórica / Hacktivista',
            'en': 'Historical Legend / Hacktivist'
        },
        'tac': 88,
        'est': 90,
        'imagePlaceholder': '👤'
    }
]

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES DE LIMPEZA E TRADUÇÃO
# ═══════════════════════════════════════════════════════════════

def clean_markdown_links(text):
    """Remove links Markdown [texto](url) mantendo apenas o texto"""
    return re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

def clean_citations(text):
    """Remove citações do estilo (Citation: ...)"""
    return re.sub(r'\(Citation:[^\)]+\)', '', text)

def clean_text(text):
    """Limpa completamente o texto"""
    text = clean_markdown_links(text)
    text = clean_citations(text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,;!?])', r'\1', text)
    text = re.sub(r'([.,;!?])\s+', r'\1 ', text)
    return text.strip()

def extract_complete_sentences(text, num_sentences=3):
    """Extrai as primeiras N frases completas do texto"""
    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    selected_sentences = sentences[:num_sentences]
    result = ' '.join(selected_sentences)
    if result and not result.endswith(('.', '!', '?')):
        result += '.'
    return result

def translate_to_portuguese(text):
    """Traduz texto de inglês para português"""
    try:
        translator = GoogleTranslator(source='en', target='pt')
        if len(text) > 4500:
            sentences = text.split('. ')
            translated_sentences = []
            for sentence in sentences:
                if sentence.strip():
                    translated = translator.translate(sentence)
                    translated_sentences.append(translated)
            return '. '.join(translated_sentences)
        else:
            return translator.translate(text)
    except Exception as e:
        print(f"[AVISO] Erro na traducao: {e}. Mantendo texto original.")
        return text

def fix_cyber_jargon(text):
    """Pós-processa texto traduzido corrigindo traduções literais de jargões"""
    if not text:
        return text
    corrected_text = text
    for wrong_term, correct_term in CYBER_JARGON_FIXES.items():
        pattern = re.compile(re.escape(wrong_term), re.IGNORECASE)
        corrected_text = pattern.sub(correct_term, corrected_text)
    return corrected_text

# ═══════════════════════════════════════════════════════════════
# ATRIBUIÇÃO GEOPOLÍTICA
# ═══════════════════════════════════════════════════════════════

def is_target_mention(text, country_keyword):
    """Verifica se a menção do país é no contexto de ALVO"""
    keyword_index = text.find(country_keyword)
    if keyword_index == -1:
        return False
    start = max(0, keyword_index - 50)
    end = min(len(text), keyword_index + len(country_keyword) + 50)
    context = text[start:end]
    for target_word in TARGET_EXCLUSION_KEYWORDS:
        if target_word in context:
            return True
    return False

def detect_country_from_text(description, name):
    """Detecta o país de ORIGEM do grupo/indivíduo"""
    text = f"{description} {name}".lower()
    
    # Prioridade 1: Grupos fixos
    name_lower = name.lower()
    for group_name, country_code in FIXED_COUNTRY_GROUPS.items():
        if group_name in name_lower:
            return country_code
    
    # Prioridade 2: Palavras-chave de origem forte
    for country_code, origin_keywords in ORIGIN_KEYWORDS.items():
        for keyword in origin_keywords:
            if keyword in text:
                if not is_target_mention(text, keyword):
                    return country_code
    
    return None

# ═══════════════════════════════════════════════════════════════
# PROCESSAMENTO DE GRUPOS (MITRE ATT&CK)
# ═══════════════════════════════════════════════════════════════

def download_mitre_data():
    """Baixa os dados do MITRE ATT&CK"""
    print("\n[1/5] Baixando dados do MITRE ATT&CK...")
    try:
        response = requests.get(MITRE_STIX_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"[OK] {len(data.get('objects', []))} objetos STIX carregados.")
        return data
    except Exception as e:
        print(f"[ERRO] Erro ao baixar MITRE: {e}")
        return None

def process_mitre_groups(mitre_data):
    """Processa grupos do MITRE ATT&CK"""
    print("\n[2/5] Processando grupos do MITRE ATT&CK...")
    
    groups = []
    objects = mitre_data.get('objects', [])
    
    for obj in objects:
        if obj.get('type') != 'intrusion-set':
            continue
        
        name = obj.get('name', 'Unknown')
        description = obj.get('description', '')
        
        country_code = detect_country_from_text(description, name)
        if not country_code:
            continue
        
        # Classificar subcategoria
        text = description.lower()
        if any(kw in text for kw in ['ransomware', 'extortion', 'financial', 'cryptocurrency', 'money']):
            subcategoria = 'lucro'
            raridade = '⭐⭐⭐⭐⭐'
            tac, est = 90, 85
        elif any(kw in text for kw in ['wiper', 'destructive', 'ics', 'scada', 'infrastructure', 'sabotage']):
            subcategoria = 'governo'
            raridade = '⭐⭐⭐⭐⭐'
            tac, est = 95, 98
        elif any(kw in text for kw in ['espionage', 'intelligence', 'surveillance', 'apt']):
            subcategoria = 'governo'
            raridade = '⭐⭐⭐⭐'
            tac, est = 80, 90
        else:
            subcategoria = 'osint_sigint'
            raridade = '⭐⭐⭐'
            tac, est = 70, 65
        
        # Sintetizar descrição
        clean_desc_en = extract_complete_sentences(description, 3)
        clean_desc_pt = translate_to_portuguese(clean_desc_en)
        clean_desc_pt = fix_cyber_jargon(clean_desc_pt)
        
        groups.append({
            'nome': name,
            'paisCode': country_code,
            'categoria': 'grupos',
            'subcategoria': subcategoria,
            'raridade': raridade,
            'descricao': {'pt': clean_desc_pt, 'en': clean_desc_en},
            'especialidade': {'pt': 'Operações Cibernéticas', 'en': 'Cyber Operations'},
            'tipo': {'pt': 'APT / Grupo de Ameaça', 'en': 'APT / Threat Group'},
            'tac': tac,
            'est': est,
            'imagePlaceholder': '🎯'
        })
    
    print(f"[OK] {len(groups)} grupos processados do MITRE.")
    return groups

# ═══════════════════════════════════════════════════════════════
# PROCESSAMENTO DE INDIVÍDUOS (FBI CYBER)
# ═══════════════════════════════════════════════════════════════

def download_fbi_data():
    """Baixa dados do FBI Cyber's Most Wanted"""
    print("\n[3/5] Baixando dados do FBI Cyber's Most Wanted...")
    try:
        response = requests.get(FBI_CYBER_API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])
        print(f"[OK] {len(items)} procurados do FBI carregados.")
        return items
    except Exception as e:
        print(f"[AVISO] Erro ao baixar FBI: {e}. Continuando sem dados do FBI.")
        return []

def process_fbi_individuals(fbi_items):
    """Processa indivíduos procurados pelo FBI"""
    print("\n[4/5] Processando indivíduos do FBI Cyber...")
    
    individuals = []
    fbi_legendary = ['bogachev', 'yakubets', 'seleznev', 'karim baratov']
    
    for item in fbi_items:
        if not item.get('title'):
            continue
        
        name = item.get('title', 'Unknown')
        description = item.get('description', '')
        details = item.get('details', '')
        text = f"{description} {details}".lower()
        
        # Detectar país
        country_code = detect_country_from_text(text, name)
        if not country_code:
            if 'russia' in text or 'moscow' in text:
                country_code = 'RU'
            elif 'china' in text or 'beijing' in text:
                country_code = 'CN'
            elif 'iran' in text or 'tehran' in text:
                country_code = 'IR'
            else:
                country_code = 'US'
        
        # Detectar agentes de inteligência
        if any(kw in text for kw in ['fsb', 'gru', 'intelligence officer', 'military intelligence']):
            subcategoria = 'especialistas'
            raridade = '⭐⭐⭐⭐⭐'
            tac, est = 95, 92
        elif any(leg in name.lower() for leg in fbi_legendary):
            subcategoria = 'lendas'
            raridade = '⭐⭐⭐⭐⭐'
            tac, est = 98, 95
        else:
            subcategoria = 'lucro'
            raridade = '⭐⭐⭐⭐'
            tac, est = 85, 80
        
        # Extrair foto
        imagem = '👤'
        if 'images' in item and item['images']:
            for img in item['images']:
                if img.get('original'):
                    imagem = img['original']
                    break
                elif img.get('large'):
                    imagem = img['large']
                    break
        
        # Descrição
        clean_desc_en = extract_complete_sentences(description or details, 2)
        clean_desc_pt = translate_to_portuguese(clean_desc_en)
        clean_desc_pt = fix_cyber_jargon(clean_desc_pt)
        
        individuals.append({
            'nome': name,
            'paisCode': country_code,
            'categoria': 'individuos',
            'subcategoria': subcategoria,
            'raridade': raridade,
            'descricao': {'pt': clean_desc_pt, 'en': clean_desc_en},
            'especialidade': {'pt': 'Cybercrime', 'en': 'Cybercrime'},
            'tipo': {'pt': 'Procurado / FBI Cyber', 'en': 'Wanted / FBI Cyber'},
            'tac': tac,
            'est': est,
            'imagePlaceholder': imagem
        })
    
    print(f"[OK] {len(individuals)} indivíduos processados do FBI.")
    return individuals

# ═══════════════════════════════════════════════════════════════
# GERAÇÃO DO ARQUIVO FINAL
# ═══════════════════════════════════════════════════════════════

def generate_js_file(all_data):
    """Gera o arquivo js/data.js"""
    print("\n[5/5] Gerando arquivo js/data.js...")
    
    # Organizar por estrutura
    database = {
        'grupos': {'lucro': [], 'osint_sigint': [], 'governo': []},
        'individuos': {'lendas': [], 'especialistas': [], 'lucro': []},
        'organizacoes': {'militares': [], 'inteligencia': [], 'policia_especializada': []}
    }
    
    for actor in all_data:
        categoria = actor.get('categoria', 'grupos')
        subcategoria = actor.get('subcategoria', 'governo')
        if categoria in database and subcategoria in database[categoria]:
            database[categoria][subcategoria].append(actor)
    
    js_content = f"""// ═══════════════════════════════════════════════════════════════
// CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE v2.0
// Gerado automaticamente por builder.py
// Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Fontes: MITRE ATT&CK, FBI Cyber's Most Wanted, Atores Históricos
// ═══════════════════════════════════════════════════════════════

const cyberDatabase = {json.dumps(database, indent=4, ensure_ascii=False)};

const countries = [
    {{ code: "RU", name: {{ pt: "Rússia", en: "Russia" }}, flag: "🇷🇺" }},
    {{ code: "US", name: {{ pt: "EUA", en: "USA" }}, flag: "🇺🇸" }},
    {{ code: "CN", name: {{ pt: "China", en: "China" }}, flag: "🇨🇳" }},
    {{ code: "KP", name: {{ pt: "Coreia do Norte", en: "North Korea" }}, flag: "🇰🇵" }},
    {{ code: "IR", name: {{ pt: "Irã", en: "Iran" }}, flag: "🇮🇷" }},
    {{ code: "IL", name: {{ pt: "Israel", en: "Israel" }}, flag: "🇮🇱" }},
    {{ code: "EU", name: {{ pt: "União Europeia", en: "European Union" }}, flag: "🇪🇺" }},
    {{ code: "UN", name: {{ pt: "Global", en: "Global" }}, flag: "🌐" }}
];

const translations = {{
    pt: {{
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
        "subcat-government": "Associado a Gov",
        "subcat-osint-sigint": "OSINT/SIGINT",
        "subcat-legends": "Lendas",
        "subcat-specialists": "Especialistas",
        "subcat-military": "Militares",
        "subcat-intelligence": "Inteligência",
        "subcat-police": "Polícia Especializada",
        "title-cards": "Cards de Ameaças",
        "btn-back": "Voltar"
    }},
    en: {{
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
        "subcat-government": "Associated with Gov",
        "subcat-osint-sigint": "OSINT/SIGINT",
        "subcat-legends": "Legends",
        "subcat-specialists": "Specialists",
        "subcat-military": "Military",
        "subcat-intelligence": "Intelligence",
        "subcat-police": "Specialized Police",
        "title-cards": "Threat Cards",
        "btn-back": "Back"
    }}
}};
"""
    
    with open('js/data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    total = sum(len(subs) for cat in database.values() for subs in cat.values())
    print(f"[OK] Arquivo js/data.js gerado com {total} atores!")

# ═══════════════════════════════════════════════════════════════
# MAIN - ORQUESTRAÇÃO
# ═══════════════════════════════════════════════════════════════

def main():
    """Função principal do builder"""
    print("\n" + "="*70)
    print("  CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE BUILDER v2.0")
    print("  Fontes: MITRE ATT&CK + FBI Cyber's Most Wanted + Atores de Elite")
    print("="*70)
    
    all_actors = []
    
    # Processar MITRE ATT&CK (Grupos)
    mitre_data = download_mitre_data()
    if mitre_data:
        groups = process_mitre_groups(mitre_data)
        all_actors.extend(groups)
    
    # Processar FBI Cyber (Indivíduos)
    fbi_items = download_fbi_data()
    if fbi_items:
        individuals = process_fbi_individuals(fbi_items)
        all_actors.extend(individuals)
    
    # Injetar atores de elite (Israel e UE)
    print("\n[ELITE] Injetando atores históricos de Israel e União Europeia...")
    all_actors.extend(ELITE_ACTORS)
    print(f"[OK] {len(ELITE_ACTORS)} atores de elite injetados.")
    
    # Gerar arquivo final
    generate_js_file(all_actors)
    
    print("\n" + "="*70)
    print("  [BUILD COMPLETO] O arquivo js/data.js está pronto!")
    print(f"  Total de atores: {len(all_actors)}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
