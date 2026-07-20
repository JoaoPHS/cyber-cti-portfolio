#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE BUILDER
Automatiza a criação do arquivo js/data.js extraindo dados do MITRE ATT&CK
═══════════════════════════════════════════════════════════════
"""

import json
import requests
import re
from datetime import datetime

# URLs do MITRE ATT&CK STIX
MITRE_STIX_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# Mapeamento de palavras-chave para países
COUNTRY_KEYWORDS = {
    'RU': ['russia', 'russian', 'kremlin', 'gru', 'svr', 'fsb', 'moscow'],
    'CN': ['china', 'chinese', 'prc', "people's republic", 'beijing'],
    'US': ['united states', 'american', 'u.s.', 'usa', 'nsa', 'fbi'],
    'IR': ['iran', 'iranian', 'tehran', 'persian'],
    'IL': ['israel', 'israeli', 'tel aviv', 'jerusalem', 'idf'],
    'KP': ['north korea', 'dprk', 'north korean', 'pyongyang', 'bureau 121', 'lazarus', 'kimsuky'],
    'EU': ['europe', 'european', 'eu ', 'germany', 'france', 'uk', 'britain']
}

# Atores lendários com dados hardcoded para garantir precisão
LEGENDARY_ACTORS = {
    'Sandworm Team': {
        'nome': 'Sandworm Team (GRU Unit 74455)',
        'paisCode': 'RU',
        'categoria': 'grupos',
        'subcategoria': 'governo',
        'raridade': '⭐⭐⭐⭐⭐',
        'descricao': {
            'pt': 'Unidade de elite do GRU russo considerada o APT mais destrutivo do mundo. Responsável por BlackEnergy, NotPetya (US$ 10 bilhões em danos), quedas da rede elétrica ucraniana (2015, 2016) e sabotagem das Olimpíadas de Pyeongchang 2018.',
            'en': 'Elite GRU unit considered world\'s most destructive APT. Responsible for BlackEnergy, NotPetya ($10B in damages), Ukrainian power grid blackouts (2015, 2016) and 2018 Pyeongchang Olympics sabotage.'
        },
        'especialidade': {
            'pt': 'Sabotagem Industrial, ICS/SCADA, Wiper Malware, Guerra Híbrida',
            'en': 'Industrial Sabotage, ICS/SCADA, Wiper Malware, Hybrid Warfare'
        },
        'tipo': {
            'pt': 'APT Estatal / Governo',
            'en': 'State APT / Government'
        },
        'imagePlaceholder': 'assets/images/military.png'
    },
    'Lazarus Group': {
        'nome': 'Lazarus Group / APT38',
        'paisCode': 'KP',
        'categoria': 'grupos',
        'subcategoria': 'lucro',
        'raridade': '⭐⭐⭐⭐⭐',
        'descricao': {
            'pt': 'Grupo estatal norte-coreano focado em heists financeiros bilionários. Responsável pelo roubo de US$ 81 milhões do Bangladesh Bank, hack da Sony Pictures e WannaCry. Opera mixers de criptomoedas para financiar o programa nuclear.',
            'en': 'North Korean state group focused on billion-dollar financial heists. Responsible for $81M Bangladesh Bank theft, Sony Pictures hack, and WannaCry. Operates crypto mixers to fund nuclear program.'
        },
        'especialidade': {
            'pt': 'Heists SWIFT, Lavagem de Criptomoedas, Wiper Malware',
            'en': 'SWIFT Heists, Cryptocurrency Laundering, Wiper Malware'
        },
        'tipo': {
            'pt': 'Lucro Estatal / APT',
            'en': 'State Profit / APT'
        },
        'imagePlaceholder': '🇰🇵'
    },
    'APT29': {
        'nome': 'APT29 (Cozy Bear)',
        'paisCode': 'RU',
        'categoria': 'grupos',
        'subcategoria': 'governo',
        'raridade': '⭐⭐⭐⭐⭐',
        'descricao': {
            'pt': 'Grupo vinculado ao SVR russo, focado em espionagem de longo prazo contra think tanks, governos e pesquisas sensíveis. Responsável pelo SolarWinds (2020), maior hack de supply chain da história.',
            'en': 'Group linked to Russian SVR, focused on long-term espionage against think tanks, governments and sensitive research. Responsible for SolarWinds (2020), largest supply chain hack in history.'
        },
        'especialidade': {
            'pt': 'Supply Chain Attacks, Persistência Avançada, Stealth Operacional',
            'en': 'Supply Chain Attacks, Advanced Persistence, Operational Stealth'
        },
        'tipo': {
            'pt': 'APT Estatal / Governo',
            'en': 'State APT / Government'
        },
        'imagePlaceholder': 'assets/images/military.png'
    },
    'Kimsuky': {
        'nome': 'Kimsuky (Thallium)',
        'paisCode': 'KP',
        'categoria': 'grupos',
        'subcategoria': 'governo',
        'raridade': '⭐⭐⭐⭐',
        'descricao': {
            'pt': 'Grupo norte-coreano focado em coleta de inteligência sobre políticas nucleares, sanções e relações diplomáticas. Usa engenharia social sofisticada contra think tanks, pesquisadores e diplomatas globais.',
            'en': 'North Korean group focused on intelligence gathering about nuclear policies, sanctions and diplomatic relations. Uses sophisticated social engineering against think tanks, researchers and global diplomats.'
        },
        'especialidade': {
            'pt': 'Inteligência Geopolítica, Engenharia Social, Coleta de OSINT',
            'en': 'Geopolitical Intelligence, Social Engineering, OSINT Collection'
        },
        'tipo': {
            'pt': 'APT Estatal / Governo',
            'en': 'State APT / Government'
        },
        'imagePlaceholder': 'assets/images/military.png'
    }
}


def print_banner():
    """Exibe o banner de inicialização"""
    print("\n" + "="*70)
    print("  CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE BUILDER")
    print("  Automação de dados do MITRE ATT&CK para js/data.js")
    print("="*70 + "\n")


def download_mitre_data():
    """Baixa os dados do MITRE ATT&CK via STIX"""
    print("[1/5] Baixando dados do MITRE ATT&CK...")
    
    try:
        response = requests.get(MITRE_STIX_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"[OK] Sucesso! {len(data.get('objects', []))} objetos STIX carregados.")
        return data
    except Exception as e:
        print(f"[ERRO] Erro ao baixar dados: {e}")
        return None


def detect_country(description, name):
    """Detecta o país de origem baseado em palavras-chave"""
    text = f"{description} {name}".lower()
    
    # Ordem de prioridade: verificar países mais específicos primeiro
    # para evitar falsos positivos (ex: "North Korea" antes de "Korea")
    priority_order = ['KP', 'IL', 'IR', 'CN', 'RU', 'US', 'EU']
    
    for country_code in priority_order:
        keywords = COUNTRY_KEYWORDS[country_code]
        for keyword in keywords:
            if keyword in text:
                return country_code
    
    return None


def calculate_rpg_stats(description, name):
    """Calcula atributos de RPG baseando-se no perfil técnico"""
    text = f"{description} {name}".lower()
    
    # Grupos destrutivos/ICS
    if any(kw in text for kw in ['wiper', 'destructive', 'ics', 'scada', 'power grid', 'infrastructure']):
        return {
            'raridade': '⭐⭐⭐⭐⭐',
            'subcategoria': 'governo',
            'tac': 95,
            'est': 98
        }
    
    # Espionagem cibernética pura
    elif any(kw in text for kw in ['espionage', 'intelligence', 'surveillance', 'apt']):
        return {
            'raridade': '⭐⭐⭐⭐',
            'subcategoria': 'governo',
            'tac': 80,
            'est': 90
        }
    
    # Ransomware/Lucro
    elif any(kw in text for kw in ['ransomware', 'extortion', 'financial', 'cryptocurrency']):
        return {
            'raridade': '⭐⭐⭐⭐⭐',
            'subcategoria': 'lucro',
            'tac': 90,
            'est': 85
        }
    
    # Hacktivismo/OSINT
    elif any(kw in text for kw in ['hacktivist', 'activist', 'ddos', 'defacement']):
        return {
            'raridade': '⭐⭐⭐',
            'subcategoria': 'osint_sigint',
            'tac': 70,
            'est': 65
        }
    
    # Padrão
    else:
        return {
            'raridade': '⭐⭐⭐',
            'subcategoria': 'governo',
            'tac': 75,
            'est': 75
        }


def clean_markdown_links(text):
    """Remove links Markdown [texto](url) mantendo apenas o texto"""
    # Padrão: [texto](url) -> texto
    cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    return cleaned


def clean_citations(text):
    """Remove citações do estilo (Citation: ...)"""
    # Remove (Citation: ...)
    cleaned = re.sub(r'\(Citation:[^\)]+\)', '', text)
    return cleaned


def clean_text(text):
    """Limpa completamente o texto removendo links, citações e caracteres indesejados"""
    # Remover links Markdown
    text = clean_markdown_links(text)
    
    # Remover citações
    text = clean_citations(text)
    
    # Remover múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    
    # Remover espaços antes de pontuação
    text = re.sub(r'\s+([.,;!?])', r'\1', text)
    
    # Remover espaços extras após pontuação
    text = re.sub(r'([.,;!?])\s+', r'\1 ', text)
    
    return text.strip()


def extract_complete_sentences(text, num_sentences=3):
    """Extrai as primeiras N frases completas do texto"""
    # Limpar o texto primeiro
    text = clean_text(text)
    
    # Dividir por pontos finais seguidos de espaço e letra maiúscula ou fim de string
    # Isso preserva abreviações como "U.S." e "e.g."
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Filtrar frases vazias e muito curtas
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Pegar apenas as primeiras N frases
    selected_sentences = sentences[:num_sentences]
    
    # Juntar as frases
    result = ' '.join(selected_sentences)
    
    # Garantir que termina com ponto
    if result and not result.endswith(('.', '!', '?')):
        # Se não termina com pontuação, adicionar ponto
        result += '.'
    
    return result


def synthesize_description(description, lang='pt', actor_name=''):
    """Sintetiza um dossiê de inteligência com frases completas"""
    # Extrair 3 frases completas
    clean_desc = extract_complete_sentences(description, num_sentences=3)
    
    # Como não há tradução automática real, manter texto em inglês para ambos idiomas
    # mas adicionar nota em português para a versão PT
    if lang == 'pt' and actor_name:
        prefix = f"[Análise CTI] Ator: {actor_name}. "
        return prefix + clean_desc
    
    return clean_desc


def extract_specialty(description):
    """Extrai termos técnicos marcantes para especialidade"""
    # Limpar links primeiro
    description = clean_markdown_links(description)
    
    keywords = [
        'Zero-Click Exploits', 'Supply Chain Attacks', 'Living off the Land',
        'Spear Phishing', 'Watering Hole', 'DDoS', 'Ransomware',
        'Data Exfiltration', 'Credential Harvesting', 'Malware Development',
        'Social Engineering', 'ICS/SCADA', 'APT', 'Persistence',
        'Zero-Day', 'Backdoor', 'Command and Control', 'Lateral Movement'
    ]
    
    found = []
    for keyword in keywords:
        if keyword.lower() in description.lower():
            found.append(keyword)
    
    return ', '.join(found[:3]) if found else 'Cyber Operations'


def process_mitre_data(mitre_data):
    """Processa os dados do MITRE e extrai intrusion-sets"""
    print("[2/5] Filtrando e processando intrusion-sets...")
    
    intrusion_sets = []
    objects = mitre_data.get('objects', [])
    
    for obj in objects:
        if obj.get('type') == 'intrusion-set':
            name = obj.get('name', 'Unknown')
            description = obj.get('description', '')
            
            # Detectar país
            country_code = detect_country(description, name)
            if not country_code:
                continue  # Descartar atores sem país mapeado
            
            # Calcular stats de RPG
            stats = calculate_rpg_stats(description, name)
            
            # Montar ator
            actor = {
                'nome': name,
                'paisCode': country_code,
                'categoria': 'grupos',
                'subcategoria': stats['subcategoria'],
                'raridade': stats['raridade'],
                'descricao': {
                    'pt': synthesize_description(description, 'pt', name),
                    'en': synthesize_description(description, 'en', name)
                },
                'especialidade': {
                    'pt': extract_specialty(description),
                    'en': extract_specialty(description)
                },
                'tipo': {
                    'pt': 'APT / Grupo de Ameaça',
                    'en': 'APT / Threat Group'
                },
                'imagePlaceholder': '🎯'
            }
            
            intrusion_sets.append(actor)
    
    print(f"[OK] {len(intrusion_sets)} atores processados do MITRE ATT&CK.")
    return intrusion_sets


def merge_legendary_actors(actors):
    """Mescla atores lendários hardcoded com os extraídos do MITRE"""
    print("[3/5] Mesclando atores lendarios hardcoded...")
    
    # Remover atores do MITRE que têm versão hardcoded
    legendary_names = set(LEGENDARY_ACTORS.keys())
    filtered_actors = [a for a in actors if not any(ln in a['nome'] for ln in legendary_names)]
    
    # Adicionar atores lendários
    for legendary in LEGENDARY_ACTORS.values():
        filtered_actors.append(legendary)
    
    print(f"[OK] {len(LEGENDARY_ACTORS)} atores lendarios injetados.")
    return filtered_actors


def organize_by_structure(actors):
    """Organiza atores na estrutura do cyberDatabase"""
    print("[4/5] Organizando na estrutura do banco de dados...")
    
    database = {
        'grupos': {
            'lucro': [],
            'osint_sigint': [],
            'governo': []
        },
        'individuos': {
            'lendas': [],
            'especialistas': [],
            'lucro': []
        },
        'organizacoes': {
            'militares': [],
            'inteligencia': [],
            'policia_especializada': []
        }
    }
    
    for actor in actors:
        categoria = actor.get('categoria', 'grupos')
        subcategoria = actor.get('subcategoria', 'governo')
        
        if categoria in database and subcategoria in database[categoria]:
            database[categoria][subcategoria].append(actor)
    
    # Contabilizar
    total = sum(len(subs) for cat in database.values() for subs in cat.values())
    print(f"[OK] {total} atores organizados na estrutura.")
    
    return database


def generate_javascript_file(database):
    """Gera o arquivo js/data.js com o formato JavaScript"""
    print("[5/5] Gerando arquivo js/data.js...")
    
    js_content = f"""// ═══════════════════════════════════════════════════════════════
// CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE
// Gerado automaticamente por builder.py
// Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// ═══════════════════════════════════════════════════════════════

const cyberDatabase = {json.dumps(database, indent=4, ensure_ascii=False)};

// Lista de países (usada na Tela 1)
const countries = [
    {{ code: "RU", name: {{ pt: "Rússia", en: "Russia" }}, flag: "🇷🇺" }},
    {{ code: "US", name: {{ pt: "EUA", en: "USA" }}, flag: "🇺🇸" }},
    {{ code: "CN", name: {{ pt: "China", en: "China" }}, flag: "🇨🇳" }},
    {{ code: "KP", name: {{ pt: "Coreia do Norte", en: "North Korea" }}, flag: "🇰🇵" }},
    {{ code: "IR", name: {{ pt: "Irã", en: "Iran" }}, flag: "🇮🇷" }},
    {{ code: "IL", name: {{ pt: "Israel", en: "Israel" }}, flag: "🇮🇱" }},
    {{ code: "EU", name: {{ pt: "União Europeia", en: "European Union" }}, flag: "🇪🇺" }}
];

// Traduções da interface
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
    
    # Salvar arquivo
    with open('js/data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("[OK] Arquivo js/data.js gerado com sucesso!")


def main():
    """Função principal do builder"""
    print_banner()
    
    # Passo 1: Baixar dados do MITRE
    mitre_data = download_mitre_data()
    if not mitre_data:
        print("\n[ERRO] Falha ao baixar dados. Abortando.")
        return
    
    # Passo 2: Processar intrusion-sets
    actors = process_mitre_data(mitre_data)
    
    # Passo 3: Mesclar com atores lendários
    actors = merge_legendary_actors(actors)
    
    # Passo 4: Organizar na estrutura do banco
    database = organize_by_structure(actors)
    
    # Passo 5: Gerar arquivo JavaScript
    generate_javascript_file(database)
    
    print("\n" + "="*70)
    print("  [BUILD COMPLETO] O arquivo js/data.js esta pronto para uso.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
