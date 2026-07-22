#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE BUILDER v3.0
Automates js/data.js generation by extracting data from:
- MITRE ATT&CK (dynamic APT / intrusion-set groups)
- STATIC_GROUPS / STATIC_INDIVIDUALS / STATIC_ORGANIZATIONS (manual drawers)
═══════════════════════════════════════════════════════════════
"""

import json
import requests
import re
from datetime import datetime
from deep_translator import GoogleTranslator

# ═══════════════════════════════════════════════════════════════
# DATA SOURCE URLs
# ═══════════════════════════════════════════════════════════════
MITRE_STIX_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
CERT_DATA_URL = "https://raw.githubusercontent.com/FIRST-Tech/FIRST-member-list/main/members.json"

# Canonical country codes used by the front-end (countries[].code)
COUNTRY_CODE_CANONICAL = {
    'russia': 'RU', 'ru': 'RU', 'RU': 'RU',
    'eua': 'US', 'usa': 'US', 'us': 'US', 'US': 'US',
    'china': 'CN', 'cn': 'CN', 'CN': 'CN',
    'coreia_norte': 'KP', 'north korea': 'KP', 'kp': 'KP', 'KP': 'KP',
    'ira': 'IR', 'iran': 'IR', 'ir': 'IR', 'IR': 'IR',
    'israel': 'IL', 'il': 'IL', 'IL': 'IL',
    'india': 'IN', 'in': 'IN', 'IN': 'IN',
    'brasil': 'BR', 'brazil': 'BR', 'br': 'BR', 'BR': 'BR',
    'eu': 'EU', 'ue': 'EU', 'EU': 'EU',
    'global': 'global', 'un': 'global', 'UN': 'global',
}

def normalize_country_code(raw):
    """Normalize countryId/countryCode to the JS selector ISO code (RU, US...)."""
    if raw is None:
        return 'global'
    value = str(raw).strip()
    if not value:
        return 'global'
    if value in COUNTRY_CODE_CANONICAL:
        return COUNTRY_CODE_CANONICAL[value]
    lowered = value.lower()
    if lowered in COUNTRY_CODE_CANONICAL:
        return COUNTRY_CODE_CANONICAL[lowered]
    # 2-letter ISO
    if len(value) == 2:
        return value.upper()
    return lowered

CATEGORY_TAXONOMY = {
    'grupos': 'groups',
    'groups': 'groups',
    'individuos': 'individuals',
    'individuals': 'individuals',
    'organizacoes': 'organizations',
    'organizations': 'organizations',
}

SUBCATEGORY_TAXONOMY = {
    'lucro': 'profit',
    'profit': 'profit',
    'governo': 'government',
    'government': 'government',
    'gov': 'government',
    'associated': 'government',
    'associado a gov': 'government',
    'osint_sigint': 'osint_sigint',
    'famosos': 'famous',
    'famous': 'famous',
    'famoso': 'famous',
    'defesa_lei': 'defense_law',
    'defense_law': 'defense_law',
    'espionagem_militar': 'military_espionage',
    'military_espionage': 'military_espionage',
}

# Canonical buckets consumed by js/app.js selectors (index.html data-*)
# Design note — state-sponsored split:
#   groups/government          → non-military APTs / proxies (e.g. Killnet, APT41)
#   organizations/military_espionage → strict military cyber commands (e.g. GRU 74455)
VALID_TAXONOMY_BUCKETS = {
    'groups': frozenset({'profit', 'osint_sigint', 'government'}),
    'individuals': frozenset({'famous'}),
    'organizations': frozenset({'defense_law', 'military_espionage'}),
}

def _taxonomy_blob(*parts):
    """Join values into a lowercase searchable string (handles bilingual dicts)."""
    chunks = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, dict):
            chunks.append(str(part.get('pt', '')))
            chunks.append(str(part.get('en', '')))
        else:
            chunks.append(str(part))
    return ' '.join(chunks).strip().lower()


def normalize_taxonomies(card):
    """
    Force category/subcategory to exact front-end keys before writing js/data.js.

    Canonical output (EN — matches index.html data-* and js/app.js):
      category    → groups | individuals | organizations
      subcategory → profit | osint_sigint | government | famous
                    | defense_law | military_espionage

    Accepts polluted PT/EN hybrids (e.g. "Agência Intelligence", "Governo Military")
    and remaps them via keyword hygiene. Logs every correction.
    """
    if not isinstance(card, dict):
        return card

    out = dict(card)
    raw_cat = str(out.get('category') or out.get('categoria') or '').strip().lower()
    raw_sub = str(out.get('subcategory') or out.get('subcategoria') or '').strip().lower()
    type_blob = _taxonomy_blob(out.get('type'), out.get('tipo'))
    # Subcategory + type drive intent; category string is checked separately
    # so "government" (group subcat) does not flip category to organizations.
    hint = _taxonomy_blob(raw_sub, type_blob)

    old_cat = out.get('category') or out.get('categoria')
    old_sub = out.get('subcategory') or out.get('subcategoria')

    def _has(text, *keys):
        return any(k in text for k in keys)

    # Honor intentional placement in Espionagem (strict military commands only).
    # Non-military APTs belong in groups/government — do not auto-promote them here.
    raw_cat_mapped = CATEGORY_TAXONOMY.get(raw_cat, raw_cat)
    raw_sub_mapped = SUBCATEGORY_TAXONOMY.get(raw_sub, raw_sub)
    if (
        raw_cat_mapped == 'organizations'
        and raw_sub_mapped == 'military_espionage'
    ):
        out['category'] = 'organizations'
        out['subcategory'] = 'military_espionage'
        out.pop('categoria', None)
        out.pop('subcategoria', None)
        return out

    # Honor intentional Associado a Gov (non-military state-sponsored APTs).
    if raw_cat_mapped == 'groups' and raw_sub_mapped == 'government':
        out['category'] = 'groups'
        out['subcategory'] = 'government'
        out.pop('categoria', None)
        out.pop('subcategoria', None)
        return out

    # ── Category (strict) ──
    if _has(raw_cat, 'individuo', 'individual', 'person', 'wanted', 'famoso', 'famous'):
        category = 'individuals'
    elif _has(raw_cat, 'org', 'agency', 'agência', 'agencia', 'governo', 'gov',
              'coletivo', 'organizations', 'organizacoes'):
        category = 'organizations'
    elif _has(raw_cat, 'grupo', 'group', 'set', 'apt', 'groups', 'grupos'):
        category = 'groups'
    elif raw_cat in CATEGORY_TAXONOMY:
        category = CATEGORY_TAXONOMY[raw_cat]
    elif _has(hint, 'individuo', 'individual', 'person', 'wanted', 'famoso', 'famous'):
        category = 'individuals'
    elif _has(hint, 'agency', 'agência', 'agencia', 'cert', 'csirt', 'coletivo'):
        category = 'organizations'
    elif _has(hint, 'grupo', 'group', 'apt', 'intrusion set'):
        category = 'groups'
    else:
        category = 'groups'

    if category not in VALID_TAXONOMY_BUCKETS:
        category = 'groups'

    # ── Subcategory (strict, category-aware) ──
    # Keyword lanes (user rules → EN keys used by app.js):
    #   espionagem/militar/estado/intel agressiva → military_espionage
    #   CERT/polícia/compliance/defesa             → defense_law
    #   ransomware/extorsão/fraude/lucro           → profit
    #   OSINT/SIGINT civis                         → osint_sigint
    #   individuals                                → famous
    if category == 'individuals':
        subcategory = 'famous'
    elif _has(hint, 'espionagem', 'espionage', 'militar', 'military', 'armed force',
              'offensive', 'estado', 'state-sponsored', 'state sponsored',
              'intelligence agency', 'intel agency'):
        subcategory = 'military_espionage' if category == 'organizations' else 'government'
    elif _has(hint, 'cert', 'csirt', 'policia', 'police', 'defesa', 'defense',
              'compliance', 'lei', 'law enforcement', 'enforcement',
              'incident response', 'critical infrastructure'):
        subcategory = 'defense_law' if category == 'organizations' else 'government'
    elif _has(hint, 'ransomware', 'extors', 'fraude', 'fraud', 'roubo', 'theft',
              'financial', 'lucro', 'profit', 'banco', 'bank', 'trojan banc',
              'carding', 'extortion'):
        subcategory = 'profit' if category == 'groups' else (
            'defense_law' if category == 'organizations' else 'famous'
        )
    elif _has(hint, 'osint', 'sigint', 'open source', 'fontes abertas', 'sinais',
              'signals intelligence'):
        if category == 'groups':
            subcategory = 'osint_sigint'
        elif category == 'organizations':
            subcategory = 'military_espionage'
        else:
            subcategory = 'famous'
    elif raw_sub in SUBCATEGORY_TAXONOMY:
        subcategory = SUBCATEGORY_TAXONOMY[raw_sub]
    elif raw_sub in VALID_TAXONOMY_BUCKETS.get(category, ()):
        subcategory = raw_sub
    else:
        subcategory = {
            'groups': 'government',
            'individuals': 'famous',
            'organizations': 'defense_law',
        }[category]

    # Clamp to valid bucket for the resolved category
    valid_subs = VALID_TAXONOMY_BUCKETS[category]
    if subcategory not in valid_subs:
        fallback = {
            'groups': 'government',
            'individuals': 'famous',
            'organizations': 'defense_law',
        }[category]
        print(
            f"[!] Corrigindo classificação poluída de "
            f"{old_cat!r}/{old_sub!r} → subcategory {subcategory!r} "
            f"inválida para {category!r}; forçando {fallback!r}"
        )
        subcategory = fallback

    out['category'] = category
    out['subcategory'] = subcategory
    out.pop('categoria', None)
    out.pop('subcategoria', None)

    if str(old_cat or '') != category or str(old_sub or '') != subcategory:
        name = out.get('name') or out.get('nome') or '?'
        print(
            f"[!] Corrigindo classificação poluída de "
            f"{old_cat!r}/{old_sub!r} para {category}/{subcategory} "
            f"({name})"
        )

    return out

def _pick(src, *keys, default=None):
    """Return first present non-empty value among keys (legacy PT + EN)."""
    for key in keys:
        if key in src and src[key] is not None and src[key] != '':
            return src[key]
    return default

def sanitize_actor_keys(actor):
    """
    Normalize actor identification keys for app.js filters.
    OUTPUT: English keys only (category, subcategory, countryCode, countryId,
    name, stars, rarity, specialty, description, type, image, tactical, strategic).
    INPUT: accepts legacy Portuguese keys for backwards compatibility.
    """
    src = dict(actor)

    raw_cat = str(_pick(src, 'category', 'categoria', default='groups')).strip().lower()
    raw_sub = str(_pick(src, 'subcategory', 'subcategoria', default='')).strip().lower()
    category = CATEGORY_TAXONOMY.get(raw_cat, raw_cat)
    subcategory = SUBCATEGORY_TAXONOMY.get(raw_sub, raw_sub)

    raw_country = _pick(src, 'countryCode', 'paisCode', 'countryId', 'paisId', default='global')
    country_code = normalize_country_code(raw_country)

    country_id = _pick(src, 'countryId', 'paisId')
    if country_id is not None:
        country_id = str(country_id).strip().lower()

    name = _pick(src, 'name', 'nome', default='Unknown')
    stars = _pick(src, 'stars', 'estrelas')
    rarity = _pick(src, 'rarity', 'raridade')
    if rarity is None and stars is not None:
        n = max(0, min(5, int(stars or 0)))
        rarity = '⭐' * n if n else '⭐'

    specialty = _pick(src, 'specialty', 'especialidade')
    description = _pick(src, 'description', 'descricao')
    type_val = _pick(src, 'type', 'tipo')
    country_name = _pick(src, 'countryName', 'paisNome')

    # FBI hotlink (403) → stable local art
    img = _pick(src, 'image', 'imagem', 'imagePlaceholder')
    if isinstance(img, str):
        img = img.strip()
        if img.lower().startswith('http') and 'fbi.gov' in img.lower():
            img = 'assets/images/famous.jpg'
        if category == 'individuals' and (not img or img.startswith('http')):
            if not img or 'fbi.gov' in img.lower():
                img = 'assets/images/famous.jpg'
    else:
        img = None

    tactical = _pick(src, 'tactical', 'tatico', 'tac')
    strategic = _pick(src, 'strategic', 'estrategico', 'est')

    clean = {
        'category': category,
        'subcategory': subcategory,
        'countryCode': country_code,
        'name': name,
    }
    if country_id is not None:
        clean['countryId'] = country_id
    if country_name is not None:
        clean['countryName'] = country_name
    if stars is not None:
        clean['stars'] = int(stars)
    if rarity is not None:
        clean['rarity'] = rarity
    if specialty is not None:
        clean['specialty'] = specialty
    if description is not None:
        clean['description'] = description
    if type_val is not None:
        clean['type'] = type_val
    if img is not None:
        clean['image'] = img
    if tactical is not None:
        clean['tactical'] = int(tactical)
    if strategic is not None:
        clean['strategic'] = int(strategic)
    if 'id' in src:
        clean['id'] = src['id']

    return clean

# ═══════════════════════════════════════════════════════════════
# PERSISTENT MANUAL INJECTION (NOT wiped by the builder)
# Drop new cards into these lists. They are concatenated at the end
# with dynamic MITRE cards before generating js/data.js.
#
# Valid subcategories:
#   groups         → profit | osint_sigint | government
#   individuals    → famous
#   organizations  → defense_law | military_espionage
#
# military_espionage = strict military cyber commands / intel agencies only
# government (groups) = non-military state-sponsored APTs / proxies
#
# Suggested countryId: russia | eua | china | coreia_norte | ira |
#                   israel | india | brasil | eu | global  (normalized to RU/US/IN/BR/...)
# ═══════════════════════════════════════════════════════════════

STATIC_GROUPS = [
    {
        'id': 'javali_syndicate',
        'category': 'groups',
        'subcategory': 'profit',
        'countryId': 'brasil',
        'stars': 4,
        'name': 'Javali Syndicate (Tetrade Family)',
        'countryName': {'pt': 'Brasil', 'en': 'Brazil'},
        'tactical': 90,
        'strategic': 85,
        'specialty': {
            'pt': 'Ataques de Injeção de Código e Engenharia Social em Nuvem',
            'en': 'Code Injection Attacks & Cloud Social Engineering'
        },
        'description': {
            'pt': 'Um braço altamente sofisticado da Tetrade, um cartel brasileiro de desenvolvedores de malwares bancários que expandiu suas operações para a Europa e o restante da América Latina. O grupo utiliza links maliciosos hospedados em serviços de nuvem legítimos (como Google Drive e Azure) para distribuir cavalos de troia que sequestram sessões de internet banking. Ele monitora de forma inteligente o foco da tela do usuário para injetar janelas falsas idênticas às dos bancos, roubando credenciais e realizando transações automáticas.',
            'en': 'A highly sophisticated arm of the Tetrade, a Brazilian financial malware cartel that expanded operations into Europe and the rest of Latin America. The group leverages malicious links hosted on legitimate cloud services (like Google Drive and Azure) to deploy banking Trojans that hijack web sessions. It smartly monitors screen focus to inject real-time fake overlays identical to target bank interfaces, stealing credentials and executing unauthorized transactions.'
        },
        'type': {
            'pt': 'Lucro',
            'en': 'Profit'
        },
        'image': 'assets/images/profit.jpg'
    },
]

STATIC_INDIVIDUALS = [
    {
        'id': 'evgeniy_bogachev',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'russia',
        'stars': 5,
        'name': 'Evgeniy Mikhailovich Bogachev (Slavik)',
        'countryName': {'pt': 'Rússia', 'en': 'Russia'},
        'tactical': 98,
        'strategic': 95,
        'specialty': {
            'pt': 'Desenvolvimento de Malwares Bancários de Elite e Redes de Botnets',
            'en': 'Elite Banking Malware Development & Botnet Networks'
        },
        'description': {
            'pt': 'Uma das figuras mais icônicas da história do cibercrime mundial, operando sob o codinome "Slavik". Ele é o criador intelectual do temido cavalo de troia bancário Zeus e da botnet descentralizada Gameover Zeus, utilizada para desviar mais de 100 milhões de dólares de instituições financeiras globais. Bogachev atua sob a proteção do governo russo no Mar Negro, tendo sua infraestrutura técnica sido parcialmente requisitada pela inteligência russa (FSB) para fins de espionagem cibernética militar.',
            'en': 'One of the most iconic figures in global cybercrime history, operating under the codename "Slavik". He is the mastermind behind the feared Zeus banking Trojan and the decentralized Gameover Zeus botnet, used to siphon over $100 million from international financial institutions. Bogachev operates under open protection by the Russian government near the Black Sea, with his criminal technical infrastructure historically leveraged by Russian intelligence (FSB) for military cyber espionage operations.'
        },
        'type': {
            'pt': 'Lenda do Cibercrime / FBI Most Wanted',
            'en': 'Cybercrime Legend / FBI Most Wanted'
        },
        'image': 'assets/images/famous.jpg'
    },
    {
        'id': 'maksim_yakubets',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'russia',
        'stars': 5,
        'name': 'Maksim Viktorovich Yakubets',
        'countryName': {'pt': 'Rússia', 'en': 'Russia'},
        'tactical': 94,
        'strategic': 92,
        'specialty': {
            'pt': 'Malware Bancário Dridex e Operações de Ransomware',
            'en': 'Dridex Banking Malware & Ransomware Operations'
        },
        'description': {
            'pt': 'Líder do sindicato cibercriminoso Evil Corp, um dos grupos de malware financeiro mais destrutivos do mundo. Yakubets é acusado pelo Departamento de Justiça dos EUA de desenvolver e distribuir o malware Dridex, responsável por roubos superiores a 100 milhões de dólares. Opera a partir da Rússia com suspeita de proteção estatal.',
            'en': 'Leader of the Evil Corp cybercrime syndicate, one of the world\'s most destructive financial malware groups. Yakubets is charged by the U.S. Department of Justice with developing and distributing Dridex malware, responsible for thefts exceeding $100 million. He operates from Russia with suspected state protection.'
        },
        'type': {
            'pt': 'Líder de Sindicato / FBI Most Wanted',
            'en': 'Syndicate Leader / FBI Most Wanted'
        },
        'image': 'assets/images/famous.jpg'
    },
    {
        'id': 'roman_seleznev',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'russia',
        'stars': 5,
        'name': 'Roman Valerevich Seleznev (Track2)',
        'countryName': {'pt': 'Rússia', 'en': 'Russia'},
        'tactical': 95,
        'strategic': 90,
        'specialty': {
            'pt': 'Invasão de Sistemas de Ponto de Venda (PoS) e Carding',
            'en': 'Point-of-Sale (PoS) System Intrusion & Carding'
        },
        'description': {
            'pt': 'Filho de um proeminente parlamentar russo, Seleznev operou sob o codinome \'Track2\' e foi um dos maiores cibercriminosos do mundo focado em roubo de dados financeiros. Ele hackeou milhares de servidores de ponto de venda (PoS) de empresas ocidentais, roubando e vendendo mais de 2 milhões de cartões de crédito em fóruns clandestinos, lucrando dezenas de milhões de dólares. Sua captura pelo Serviço Secreto dos EUA nas Maldivas em 2014 gerou um grande incidente diplomático, resultando em uma condenação histórica a 27 anos de prisão em solo americano.',
            'en': 'Son of a prominent Russian parliamentarian, Seleznev operated under the alias \'Track2\' and was one of the world\'s most prolific financial cybercriminals. He breached thousands of retail Point-of-Sale (PoS) systems across Western networks, stealing and selling over 2 million credit card numbers on underground carding forums, pocketing tens of millions of dollars. His dramatic 2014 capture by the US Secret Service in the Maldives sparked a massive geopolitical row, leading to a historic 27-year federal prison sentence in the US.'
        },
        'type': {
            'pt': 'Carder / FBI Most Wanted',
            'en': 'Carder / FBI Most Wanted'
        },
        'image': 'assets/images/famous.jpg'
    },
    {
        'id': 'kevin_mitnick',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'eua',
        'stars': 5,
        'name': 'Kevin David Mitnick (Condor)',
        'countryName': {'pt': 'Estados Unidos', 'en': 'United States'},
        'tactical': 95,
        'strategic': 98,
        'specialty': {
            'pt': 'Engenharia Social Avançada e Infiltração Física de Sistemas',
            'en': 'Advanced Social Engineering & Physical Systems Intrusion'
        },
        'description': {
            'pt': 'Reconhecido mundialmente como o hacker mais famoso da história, operando sob o codinome \'Condor\'. Na década de 1980 e 1990, Mitnick invadiu os sistemas de dezenas de gigantes tecnológicos (como Motorola e Nokia) e redes governamentais utilizando sua genialidade em Engenharia Social — manipulando o comportamento humano para extrair senhas e códigos-fonte. Ele se tornou o primeiro hacker a figurar na lista dos mais procurados do FBI, sendo capturado em 1995. Após cumprir 5 anos de prisão, converteu-se em um dos consultores de cibersegurança mais respeitados e influentes do mercado global.',
            'en': 'Globally recognized as the most famous hacker in history, operating under the alias \'Condor\'. Throughout the 1980s and 1990s, Mitnick breached dozens of technology giants (including Motorola and Nokia) and government networks using his masterful Social Engineering tactics — manipulating human behavior to extract source codes and secure passwords. He became the first hacker to land on the FBI\'s Most Wanted list, leading to a dramatic arrest in 1995. After serving 5 years in prison, he transitioned into one of the global market\'s most respected and influential cybersecurity consultants.'
        },
        'type': {
            'pt': 'Lenda Histórica / Engenharia Social',
            'en': 'Historical Legend / Social Engineering'
        },
        'image': 'assets/images/classe_individuos.jpg'
    },
    # ================= UNITED STATES =================
    {
        'id': 'albert_gonzalez',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'eua',
        'stars': 5,
        'name': 'Albert Gonzalez (SoupNazi)',
        'countryName': {'pt': 'Estados Unidos', 'en': 'United States'},
        'tactical': 96,
        'strategic': 92,
        'specialty': {
            'pt': 'Injeção SQL em Larga Escala e Operações de War Driving',
            'en': 'Mass SQL Injection & War Driving Operations'
        },
        'description': {
            'pt': 'Mentor do maior roubo de cartões de crédito da história americana, desviando mais de 170 milhões de cartões de redes corporativas. Operando sob o codinome \'SoupNazi\', Gonzalez liderava o sindicato ShadowCrew e inventou táticas de War Driving, dirigindo pelas estradas caçando brechas em redes Wi-Fi de lojas de varejo para injetar malwares farejadores (Sniffers). Ele atuou secretamente como informante pago do Serviço Secreto dos EUA enquanto continuava cometendo crimes em paralelo.',
            'en': 'Mastermind behind the largest credit card theft in US history, siphoning over 170 million card numbers from corporate systems. Operating under the alias \'SoupNazi\', Gonzalez led the ShadowCrew syndicate and pioneered War Driving tactics, scouting highways to intercept Wi-Fi vulnerabilities in retail stores to deploy network sniffing malware. He notoriously worked as a paid Secret Service informant while actively running criminal operations in parallel.'
        },
        'type': {
            'pt': 'Carder / ShadowCrew',
            'en': 'Carder / ShadowCrew'
        },
        'image': 'assets/images/classe_individuos.jpg'
    },
    {
        'id': 'gary_mckinnon',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'eua',
        'stars': 4,
        'name': 'Gary McKinnon (Solo)',
        'countryName': {'pt': 'Reino Unido / EUA', 'en': 'United Kingdom / US'},
        'tactical': 88,
        'strategic': 95,
        'specialty': {
            'pt': 'Infiltração de Sistemas de Defesa e Aeroespaciais de Estado',
            'en': 'State Aerospace & Defense Systems Intrusion'
        },
        'description': {
            'pt': 'Responsável pelo maior ataque hacker a computadores militares de todos os tempos. Operando sob o codinome \'Solo\' a partir de Londres, McKinnon infiltrou-se em 97 servidores da Marinha, Exército, Força Aérea e da NASA. Ele paralisou sistemas de munição e defesa de Washington logo após o 11 de setembro, alegando que estava apenas buscando documentos ocultados pelo governo sobre OVNIs e tecnologias de energia livre.',
            'en': 'Executed the biggest military computer hack of all time. Operating under the alias \'Solo\' from London, McKinnon breached 97 secure servers belonging to the US Navy, Army, Air Force, and NASA. He shut down critical weapons tracking and defense networks right after 9/11, claiming he was simply looking for suppressed government files regarding UFO classifications and free energy systems.'
        },
        'type': {
            'pt': 'Hacktivista / Invasor de Defesa',
            'en': 'Hacktivist / Defense Intruder'
        },
        'image': 'assets/images/classe_individuos.jpg'
    },
    # ================= CHINA =================
    {
        'id': 'gu_kaiyuan',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'china',
        'stars': 5,
        'name': 'Gu Kaiyuan (UglyGorilla)',
        'countryName': {'pt': 'China', 'en': 'China'},
        'tactical': 94,
        'strategic': 96,
        'specialty': {
            'pt': 'Ciberespionagem Militar e Comprometimento de Infraestrutura',
            'en': 'Military Cyber Espionage & Infrastructure Compromise'
        },
        'description': {
            'pt': 'Oficial militar de inteligência de elite do exército da China (PLA), rastreado pelo codinome \'UglyGorilla\'. Ele foi um dos cinco oficiais indiciados pelo FBI por fazerem parte da lendária Unidade 61398 (APT1). Gu é especializado em mapear e roubar propriedade intelectual de infraestruturas críticas americanas, como tubulações de gás, redes elétricas e sistemas de controle de água, preparando o terreno para possíveis ataques de sabotagem de Estado.',
            'en': 'Elite military intelligence officer for China\'s People\'s Liberation Army (PLA), tracked under the moniker \'UglyGorilla\'. He was one of the five officers formally indicted by the FBI for his role within the legendary Unit 61398 (APT1). Gu specialized in mapping and siphoning intellectual property from US critical infrastructure, targeting gas pipelines, power grids, and water systems to stage state-level cyber sabotage.'
        },
        'type': {
            'pt': 'Oficial PLA / APT1',
            'en': 'PLA Officer / APT1'
        },
        'image': 'assets/images/classe_individuos.jpg'
    },
    # ================= RUSSIA =================
    {
        'id': 'vladimir_levin',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'russia',
        'stars': 4,
        'name': 'Vladimir Levin',
        'countryName': {'pt': 'Rússia', 'en': 'Russia'},
        'tactical': 90,
        'strategic': 88,
        'specialty': {
            'pt': 'Engenharia Reversa de Protocolos Bancários e Telecomunicações',
            'en': 'Reverse Engineering of Banking Protocols & Telecoms'
        },
        'description': {
            'pt': 'O arquiteto do primeiro assalto bancário digital de grande repercussão na história da internet. Em 1994, operando a partir de São Petersburgo com um computador modesto, Levin quebrou a segurança dos sistemas de telecomunicação do Citibank. Ele interceptou e adulterou transferências eletrônicas via satélite, desviando mais de 10 milhões de dólares para contas na Europa antes de ser caçado e preso pela Interpol em Londres.',
            'en': 'Architect behind the first major digital bank heist in internet history. In 1994, operating from St. Petersburg using a modest computer, Levin cracked the telecommunication protocols of Citibank. He intercepted and manipulated global wire transfers over satellite links, moving more than $10 million into international accounts before being captured by Interpol in London.'
        },
        'type': {
            'pt': 'Pioneiro do Cibercrime Bancário',
            'en': 'Banking Cybercrime Pioneer'
        },
        'image': 'assets/images/classe_individuos.jpg'
    },
    # ================= NORTH KOREA =================
    {
        'id': 'park_jin_hyok',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'coreia_norte',
        'stars': 5,
        'name': 'Park Jin Hyok',
        'countryName': {'pt': 'Coreia do Norte', 'en': 'North Korea'},
        'tactical': 97,
        'strategic': 99,
        'specialty': {
            'pt': 'Ataques de Ransomware Destrutivos e Roubo Bancário Swift',
            'en': 'Destructive Ransomware Attacks & Swift Bank Heists'
        },
        'description': {
            'pt': 'Oficial de inteligência cibernética norte-coreano de elite pertencente ao Lab 110 (Lazarus Group). Ele foi formalmente indiciado pelos EUA por comandar os ataques digitais mais devastadores da história, incluindo o ataque destrutivo à Sony Pictures em 2014, o roubo bilionário ao Banco Central de Bangladesh via rede SWIFT e o ataque global do ransomware WannaCry em 2017, que paralisou hospitais e governos mundiais.',
            'en': 'Elite North Korean cyber intelligence operative belonging to Lab 110 (Lazarus Group). Formally indicted by the US government for spearheading the most devastating cyber attacks in history, including the 2014 destructive breach of Sony Pictures, the multimillion-dollar SWIFT bank heist against Bangladesh Bank, and the 2017 global WannaCry ransomware outbreak that crippled hospitals worldwide.'
        },
        'type': {
            'pt': 'Operador Lazarus / Lab 110',
            'en': 'Lazarus Operative / Lab 110'
        },
        'image': 'assets/images/classe_individuos.jpg'
    },
    # ================= US (historical juvenile) =================
    {
        'id': 'jonathan_james',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'eua',
        'stars': 4,
        'name': 'Jonathan James (c0mrade)',
        'countryName': {'pt': 'Estados Unidos', 'en': 'United States'},
        'tactical': 90,
        'strategic': 92,
        'specialty': {
            'pt': 'Interceptação de Tráfego de Rede e Extração de Código-Fonte',
            'en': 'Network Traffic Interception & Source Code Extraction'
        },
        'description': {
            'pt': 'O primeiro menor de idade a ser condenado por crimes cibernéticos nos EUA sob o codinome \'c0mrade\'. Com apenas 15 anos, James invadiu os servidores de segurança da NASA e da DTRA (Agência de Redução de Ameaças de Defesa). Ele roubou o código-fonte proprietário do sistema de suporte de vida da Estação Espacial Internacional, forçando a NASA a desligar sua rede inteira por semanas para auditoria técnica.',
            'en': 'The first juvenile ever convicted of cybercrimes in the United States, operating under the alias \'c0mrade\'. At just 15 years old, James bypassed security barriers at NASA and the DTRA (Defense Threat Reduction Agency). He intercepted proprietary source code responsible for the International Space Station\'s life support systems, forcing NASA to isolate and shut down its entire network for weeks.'
        },
        'type': {
            'pt': 'Lenda Juvenil / NASA Breach',
            'en': 'Juvenile Legend / NASA Breach'
        },
        'image': 'assets/images/classe_individuos.jpg'
    },
    # ================= IRAN =================
    {
        'id': 'ahmad_khatibi',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'iran',
        'stars': 5,
        'name': 'Ahmad Khatibi (IAO / MuddyWater)',
        'countryName': {'pt': 'Irã', 'en': 'Iran'},
        'tactical': 92,
        'strategic': 90,
        'specialty': {
            'pt': 'Intrusões de Redes e Campanhas de Ransomware de Fachada',
            'en': 'Network Intrusions & Front Ransomware Operations'
        },
        'description': {
            'pt': 'Afiliado a empresas de fachada de tecnologia em Teerã vinculadas ao Corpo da Guarda Revolucionária Islâmica (IRGC). Khatibi foi indiciado pelo Departamento de Justiça dos EUA por coordenar campanhas massivas de invasão a infraestruturas críticas globais (incluindo redes de saúde e governos municipais), utilizando criptografia de ransomware para disfarçar operações de espionagem de Estado como se fossem crimes financeiros comuns.',
            'en': 'Affiliated with Tehran-based technology front companies linked to the Islamic Revolutionary Guard Corps (IRGC). Khatibi was indicted by the US Department of Justice for coordinating massive intrusion campaigns against global critical infrastructure (including healthcare networks and municipal governments), deploying ransomware encryption to mask state-sponsored espionage operations as basic financial cybercrime.'
        },
        'type': {
            'pt': 'Operador IAO / MuddyWater',
            'en': 'IAO Operative / MuddyWater'
        },
        'image': 'assets/images/famous.jpg'
    },
    {
        'id': 'alireza_shafie_nasab',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'iran',
        'stars': 4,
        'name': 'Alireza Shafie Nasab (Cyber Av3ngers)',
        'countryName': {'pt': 'Irã', 'en': 'Iran'},
        'tactical': 88,
        'strategic': 92,
        'specialty': {
            'pt': 'Engenharia Social Avançada e Spear-Phishing',
            'en': 'Advanced Social Engineering & Spear-Phishing'
        },
        'description': {
            'pt': 'Operador cibernético sênior caçado pelo FBI por sua atuação em campanhas de spear-phishing direcionadas contra os setores de defesa, inteligência e contratantes militares dos EUA. Shafie Nasab utilizava identidades falsas complexas e personas femininas nas redes sociais para enganar engenheiros de segurança, induzindo-os a baixar malwares de acesso remoto que davam ao regime iraniano controle total sobre redes restritas.',
            'en': 'Senior cyber operative wanted by the FBI for his execution of targeted spear-phishing campaigns against US defense, intelligence, and military contractors. Shafie Nasab leveraged complex spoofed identities and fake social media personas to deceive security engineers, tricking them into deploying Remote Access Trojans that granted the Iranian regime deep control over restricted networks.'
        },
        'type': {
            'pt': 'Especialista em Engenharia Social / Cyber Av3ngers',
            'en': 'Social Engineering Specialist / Cyber Av3ngers'
        },
        'image': 'assets/images/famous.jpg'
    },
    {
        'id': 'mansour_ahmadi',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'iran',
        'stars': 4,
        'name': 'Mansour Ahmadi (APT35)',
        'countryName': {'pt': 'Irã', 'en': 'Iran'},
        'tactical': 90,
        'strategic': 85,
        'specialty': {
            'pt': 'Exploitação de Vulnerabilidades em Servidores e VPNs',
            'en': 'Vulnerability Exploitation in Public VPNs & Servers'
        },
        'description': {
            'pt': 'Diretor de uma empresa privada de segurança digital em Teerã que operava secretamente como braço de intrusão do APT35 (Charming Kitten). Ahmadi especializou-se em escanear e explorar vulnerabilidades conhecidas em servidores Microsoft Exchange e dispositivos VPN corporativos. Ele liderou ataques que sequestraram dados de empresas ocidentais, exigindo resgates milionários enquanto colhia inteligência estratégica para o Ministério de Inteligência do Irã (MOIS).',
            'en': 'CEO of a private Tehran digital defense firm that secretly operated as an intrusion arm for APT35 (Charming Kitten). Ahmadi specialized in weaponizing known vulnerabilities within Microsoft Exchange servers and corporate VPN devices. He spearheaded attacks that locked Western corporate networks, demanding millions in ransom while harvesting strategic telemetry for Iran\'s Ministry of Intelligence (MOIS).'
        },
        'type': {
            'pt': 'Líder de Infraestrutura / APT35',
            'en': 'Infrastructure Lead / APT35'
        },
        'image': 'assets/images/famous.jpg'
    },
    {
        'id': 'mojtaba_masoumpour',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'iran',
        'stars': 5,
        'name': 'Mojtaba Masoumpour (APT33)',
        'countryName': {'pt': 'Irã', 'en': 'Iran'},
        'tactical': 95,
        'strategic': 96,
        'specialty': {
            'pt': 'Desenvolvimento de Malwares Wipers Destrutivos',
            'en': 'Destructive Wiper Malware Development'
        },
        'description': {
            'pt': 'Engenheiro de software e desenvolvedor de armas cibernéticas associado ao infame grupo APT33 (Elfin). Masoumpour participou ativamente da arquitetura e codificação de variantes de malwares limpadores de disco (Wipers, como o Shamoon), projetados especificamente para deletar registros de boot e destruir fisicamente dados de redes de petroquímica, aviação e energia no Oriente Médio e EUA.',
            'en': 'Software engineer and cyber weapon developer associated with the infamous APT33 (Elfin) group. Masoumpour actively participated in the architecture and coding of disk-wiping malware variants (Wipers, like Shamoon), designed specifically to overwrite master boot records and physically destroy networks inside petro-chemical, aviation, and energy sectors in the Middle East and the US.'
        },
        'type': {
            'pt': 'Engenheiro de Wipers / APT33',
            'en': 'Wiper Engineer / APT33'
        },
        'image': 'assets/images/famous.jpg'
    },
    {
        'id': 'marcos_fagundes',
        'category': 'individuals',
        'subcategory': 'famous',
        'countryId': 'brasil',
        'stars': 4,
        'name': 'Marcos Roberto Fagundes (Vovô do Malware)',
        'countryName': {'pt': 'Brasil', 'en': 'Brazil'},
        'tactical': 92,
        'strategic': 86,
        'specialty': {
            'pt': 'Desenvolvimento Core de Trojans Bancários e Evasão de Antivírus',
            'en': 'Core Banking Trojan Development & Antivirus Evasion'
        },
        'description': {
            'pt': 'Rastreado de perto pela Polícia Federal brasileira e agências internacionais durante grandes operações (como a Operação Grandoreiro), ele é considerado um dos desenvolvedores de código-base mais prolíficos da América do Sul. Especializado em escrever códigos em Delphi com alta capacidade de ofuscação e bypass de sistemas de detecção e resposta de endpoints (EDR), suas criações estruturais serviram de matriz para as maiores botnets de roubo financeiro transfronteiriço operadas no país.',
            'en': "Closely tracked by the Brazilian Federal Police and international task forces during major operations (such as Operation Grandoreiro), he is considered one of South America's most prolific malware base-code developers. Specializing in highly obfuscated Delphi programming and endpoint detection (EDR) bypasses, his architectural blueprints served as the matrix for the biggest cross-border financial botnets operating out of the country."
        },
        'type': {
            'pt': 'Famosos',
            'en': 'Famous'
        },
        'image': 'assets/images/famous.jpg'
    },
]

STATIC_ORGANIZATIONS = [
    {
        'id': 'cyber_command_brazil',
        'category': 'organizations',
        'subcategory': 'military_espionage',
        'countryId': 'brasil',
        'stars': 4,
        'name': 'Comando de Defesa Cibernética (ComDCiber)',
        'countryName': {'pt': 'Brasil', 'en': 'Brazil'},
        'tactical': 86,
        'strategic': 92,
        'specialty': {
            'pt': 'Proteção de Infraestrutura Crítica e Guerra Eletrônica',
            'en': 'Critical Infrastructure Shielding & Electronic Warfare'
        },
        'description': {
            'pt': 'O braço oficial e conjunto das Forças Armadas do Brasil encarregado de planejar, coordenar e executar operações de defesa cibernética e guerra eletrônica do Estado. O ComDCiber opera blindando as redes estratégicas de segurança nacional, sistemas de comunicação militar e monitorando ameaças contra infraestruturas críticas civis do país, como redes elétricas e sistemas de abastecimento, além de coordenar a segurança digital de grandes eventos geopolíticos de Estado.',
            'en': 'The official joint cyber branch of the Brazilian Armed Forces tasked with planning, coordinating, and executing state-level cyber defense and electronic warfare operations. ComDCiber operates by shielding national security networks, military communication pipelines, and monitoring advanced threats against critical civilian infrastructure like power grids, alongside coordinating risk assessments for high-profile geopolitical summits.'
        },
        'type': {
            'pt': 'Espionagem e Operações Militares',
            'en': 'Espionage & Military Operations'
        },
        'image': 'assets/images/classe_espionagem.jpg'
    },
    {
        'id': 'pf_cyber_division',
        'category': 'organizations',
        'subcategory': 'defense_law',
        'countryId': 'brasil',
        'stars': 5,
        'name': 'Polícia Federal - Coordenação-Geral de Combate a Crimes Cibernéticos (CGCIB)',
        'countryName': {'pt': 'Brasil', 'en': 'Brazil'},
        'tactical': 92,
        'strategic': 90,
        'specialty': {
            'pt': 'Investigação de Alta Tecnologia e Cooperação Internacional (Europol/Interpol)',
            'en': 'High-Tech Forensics & International Cooperation (Europol/Interpol)'
        },
        'description': {
            'pt': 'A unidade de elite da Polícia Federal do Brasil focada no desmantelamento de grandes organizações criminosas tecnológicas. A CGCIB ganhou extremo respeito internacional no mercado de CTI por coordenar operações conjuntas com a Europol, Interpol e agências americanas, resultando na desarticulação e prisão de líderes de sindicatos globais de desenvolvedores de malwares e administradores de servidores de comando e controle (C2) operando em solo brasileiro.',
            'en': 'The elite intelligence unit within the Brazilian Federal Police dedicated to dismantling organized cybercrime syndicates. CGCIB gained immense international acclaim in the CTI landscape for spearheading joint operations alongside Europol, Interpol, and US agencies, leading to the takedown and arrest of global banking malware developers and Command and Control (C2) operational cells on Brazilian soil.'
        },
        'type': {
            'pt': 'Defesa e Aplicação da Lei',
            'en': 'Defense & Law Enforcement'
        },
        'image': 'assets/images/enforce.jpg'
    },
]

# ═══════════════════════════════════════════════════════════════
# CTI JARGON DICTIONARY (Cyber Glossary)
# Fixes bizarre literal translations while keeping technical context
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
# GEOPOLITICAL ATTRIBUTION (Origin vs Targets)
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
# GEOPOLITICAL ATTRIBUTION - SMART FILTER SYSTEM
# ═══════════════════════════════════════════════════════════════

# POSITIVE FILTER: Compound phrases that lock actor origin
ORIGIN_STRONG_KEYWORDS = {
    'CN': [
        'china-nexus', 'china-based', 'china-linked', 'chinese state-sponsored',
        'chinese state', 'chinese intelligence', 'associated with chinese intelligence',
        'operated by china', 'pla unit', "people's liberation army", 'mss ',
        'beijing-based', 'prc ', 'chinese military', 'chinese apt', 'chinese threat actor',
        'attributed to china', 'linked to china', 'operates from china'
    ],
    'RU': [
        'russia-based', 'russian military', 'russian intelligence', 'russian state',
        'gru unit', 'fsb ', 'svr ', 'linked to russia', 'attributed to russia',
        'operates from russia', 'russian federation', 'kremlin', 'moscow-based',
        'russian threat', 'russian cyber'
    ],
    'US': [
        'us-based', 'united states-based', 'nsa ', 'fbi cyber', 'cia ',
        'american intelligence', 'u.s. intelligence', 'operates from the united states',
        'us intelligence', 'us military'
    ],
    'IR': [
        'iran-based', 'iranian threat', 'iranian intelligence', 'iranian state',
        'linked to iran', 'attributed to iran', 'operates from iran', 'operating out of iran',
        'irgc', 'iranian revolutionary guard', 'mois', 'ministry of intelligence',
        'tehran-based', 'iranian cyber', 'iranian hacker', 'islamic republic of iran'
    ],
    'KP': [
        'north korean', 'north korea-based', 'dprk', 'attributed to north korea',
        'linked to north korea', 'based in pyongyang', 'pyongyang-based',
        'bureau 121', 'reconnaissance general bureau', 'rgb ', 'lazarus group'
    ],
    'IL': [
        'israeli-affiliated', 'israeli intelligence', 'operating from israel',
        'affiliated with israeli', 'israel-based', 'unit 8200', 'israeli cyber',
        'idf cyber', 'mossad', 'israeli government'
    ],
    'IN': [
        'india-based', 'indian threat', 'indian intelligence', 'indian state',
        'linked to india', 'attributed to india', 'operates from india',
        'operating out of india', 'new delhi-based', 'indian cyber',
        'indian apt', 'pro-india', 'indian nexus', 'raw ', 'india-nexus'
    ],
    'BR': [
        'brazil-based', 'brasil-based', 'brazilian threat', 'brazilian cybercrime',
        'brazilian banking', 'linked to brazil', 'attributed to brazil',
        'operates from brazil', 'operating out of brazil', 'sao paulo-based',
        'brazilian trojan', 'brazilian syndicate', 'brazilian hacker',
        'cibercrime brasileiro', 'trojan bancario brasileiro'
    ],
    'EU': [
        'europe-based', 'european threat', 'operates from europe',
        'based in germany', 'based in france', 'based in uk',
        'british intelligence', 'french intelligence', 'german intelligence'
    ]
}

# NEGATIVE FILTER: Phrases indicating the country is a TARGET/VICTIM (not origin)
TARGET_PHRASES = [
    'targeting organizations in',
    'targeting organizations located in',
    'located in',
    'attacks against',
    'attacks against the',
    'against entities in',
    'operations in',
    'focused on',
    'targeting',
    'targets',
    'aimed at',
    'directed at',
    'compromised',
    'victimized',
    'organizations based in',
    'victims in',
    'government entities in',
    'companies in',
    'entities located in'
]

# HARDCODED OVERRIDES: Critical groups with 100% guaranteed attribution
FIXED_COUNTRY_GROUPS = {
    # IRAN
    'muddywater': 'IR', 'apt33': 'IR', 'apt34': 'IR', 'apt35': 'IR', 'apt39': 'IR',
    'oilrig': 'IR', 'charming kitten': 'IR', 'magic hound': 'IR', 'rocket kitten': 'IR',
    'agrius': 'IR', 'cyberav3ngers': 'IR', 'fox kitten': 'IR', 'moses staff': 'IR',
    'pioneer kitten': 'IR', 'cotton sandstorm': 'IR',
    # RUSSIA
    'sandworm': 'RU', 'apt28': 'RU', 'apt29': 'RU', 'turla': 'RU', 'cozy bear': 'RU',
    'fancy bear': 'RU', 'dragonfly': 'RU', 'wizard spider': 'RU', 'silence': 'RU',
    'gamaredon': 'RU', 'ember bear': 'RU', 'energetic bear': 'RU', 'voodoo bear': 'RU',
    'berserk bear': 'RU', 'venomous bear': 'RU', 'conti': 'RU', 'lockbit': 'RU',
    # NORTH KOREA
    'lazarus': 'KP', 'apt38': 'KP', 'kimsuky': 'KP', 'andariel': 'KP', 'bluenoroff': 'KP',
    'thallium': 'KP', 'hidden cobra': 'KP', 'applejeus': 'KP', 'beagleboys': 'KP',
    # ISRAEL
    'predatory sparrow': 'IL', 'gonjeshke darande': 'IL',
    # INDIA
    'sidewinder': 'IN', 'patchwork': 'IN', 'dropping elephant': 'IN',
    'confucius': 'IN', 'donot': 'IN', 'hangover': 'IN', 'viceroy tiger': 'IN',
    # BRAZIL (financial cybercrime syndicates / banking trojans)
    'guildma': 'BR', 'grandoreiro': 'BR', 'mekotio': 'BR', 'javali': 'BR',
    'ursa': 'BR', 'melcoz': 'BR', 'casbaneiro': 'BR',
    # CHINA (critical)
    'apt1': 'CN', 'apt3': 'CN', 'apt10': 'CN', 'apt12': 'CN', 'apt15': 'CN',
    'apt16': 'CN', 'apt17': 'CN', 'apt19': 'CN', 'apt30': 'CN', 'apt40': 'CN',
    'apt41': 'CN', 'menupass': 'CN', 'winnti': 'CN', 'bronze': 'CN',
    'unc3886': 'CN', 'g1048': 'CN', 'volt typhoon': 'CN', 'camaro dragon': 'CN',
    'stone panda': 'CN', 'putter panda': 'CN', 'buckeye': 'CN', 'gothic panda': 'CN'
}


# ═══════════════════════════════════════════════════════════════
# ISO-2 COUNTRY MAPPING TO OUR CODES
# ═══════════════════════════════════════════════════════════════
ISO2_TO_COUNTRY = {
    'US': 'US', 'RU': 'RU', 'CN': 'CN', 'IR': 'IR', 'IL': 'IL', 'KP': 'KP',
    'IN': 'IN', 'BR': 'BR',
    # European Union
    'DE': 'EU', 'FR': 'EU', 'GB': 'EU', 'UK': 'EU', 'IT': 'EU', 'ES': 'EU',
    'NL': 'EU', 'BE': 'EU', 'SE': 'EU', 'PL': 'EU', 'AT': 'EU', 'DK': 'EU',
    'FI': 'EU', 'NO': 'EU', 'CH': 'EU', 'PT': 'EU', 'CZ': 'EU', 'GR': 'EU',
    'HU': 'EU', 'RO': 'EU', 'IE': 'EU', 'SK': 'EU', 'BG': 'EU', 'HR': 'EU'
}

# ═══════════════════════════════════════════════════════════════
# GOVERNMENT AGENCY CLASSIFIERS
# ═══════════════════════════════════════════════════════════════
DEFENSE_LAW_KEYWORDS = [
    'cert', 'csirt', 'agency', 'defense', 'infrastructure', 'security',
    'protection', 'emergency', 'response', 'incident', 'coordination',
    'cybersecurity', 'critical', 'national', 'center', 'centre'
]

ESPIONAGE_MILITARY_KEYWORDS = [
    'military', 'command', 'intelligence', 'cyber command', 'signal',
    'offensive', 'operations', 'unit', 'force', 'army', 'navy',
    'air force', 'strategic', 'tactical', 'warfare'
]

# ═══════════════════════════════════════════════════════════════
# GEOPOLITICAL DOSSIERS - CYBER WARFARE MODUS OPERANDI
# ═══════════════════════════════════════════════════════════════
COUNTRY_PROFILES = {
    'US': {
        'title': {
            'pt': 'DOUTRINA DE SUPERIORIDADE E CAÇA PROATIVA',
            'en': 'DOCTRINE OF SUPERIORITY & HUNT FORWARD'
        },
        'modus': {
            'pt': 'Os Estados Unidos focam em operações de inteligência cirúrgica de sinais (SIGINT) de altíssima complexidade e na doutrina "Hunt Forward", projetando poder militar cibernético para redes aliadas globais para interceptar ameaças estatais na origem antes que atinjam o território americano.',
            'en': 'The United States focuses on surgical, highly complex signals intelligence (SIGINT) operations and the "Hunt Forward" doctrine, deploying cyber military power into global allied networks to intercept state-sponsored threats at the source before they strike US soil.'
        }
    },
    'RU': {
        'title': {
            'pt': 'DOUTRINA DE SABOTAGEM E OPERAÇÕES PSICOLÓGICAS',
            'en': 'DOCTRINE OF SABOTAGE & PSYCHOLOGICAL OPERATIONS'
        },
        'modus': {
            'pt': 'A Rússia utiliza o ciberespaço como uma extensão da guerra híbrida. Suas operações são agressivas, focadas em sabotagem destrutiva de infraestrutura crítica industrial (malwares Wipers) combinada com campanhas maciças de desinformação, operações de vazamento de dados (Hack-and-Leak) e interferência política.',
            'en': 'Russia utilizes cyberspace as an extension of hybrid warfare. Its operations are highly aggressive, focusing on destructive sabotage of critical industrial infrastructure (Wiper malware) combined with massive disinformation campaigns, leak operations (Hack-and-Leak), and political interference.'
        }
    },
    'CN': {
        'title': {
            'pt': 'DOUTRINA DE ESPIONAGEM ECONÔMICA EM LARGA ESCALA',
            'en': 'DOCTRINE OF LARGE-SCALE ECONOMIC ESPIONAGE'
        },
        'modus': {
            'pt': 'A estratégia da China é marcada pela persistência furtiva a longo prazo. O foco principal é o roubo em massa de propriedade intelectual, segredos comerciais e dados industriais ocidentais (setores de defesa, aeroespacial e semicondutores) para acelerar seu próprio desenvolvimento econômico e militar.',
            'en': 'China\'s strategy is characterized by stealthy, long-term persistence. Its primary focus is the mass theft of intellectual property, trade secrets, and Western industrial data (defense, aerospace, and semiconductor sectors) to accelerate its own economic and military development.'
        }
    },
    'IR': {
        'title': {
            'pt': 'DOUTRINA DE RETALIAÇÃO ASSIMÉTRICA E CAOS CIVIL',
            'en': 'DOCTRINE OF ASYMMETRIC RETALIATION & CIVIL CHAOS'
        },
        'modus': {
            'pt': 'O Irã opera através de uma estratégia cibernética assimétrica e altamente reativa. Focado em rivais regionais e no Ocidente, o país utiliza ataques de ransomware de fachada, sabotagem de sites e vazamentos teatrais de dados para projetar força política e retaliar sanções econômicas.',
            'en': 'Iran operates through an asymmetric and highly reactive cyber strategy. Focused on regional rivals and the West, the country utilizes front ransomware attacks, website defacements, and theatrical data leaks to project political power and retaliate against economic sanctions.'
        }
    },
    'IL': {
        'title': {
            'pt': 'DOUTRINA DE ANTECIPAÇÃO TÁTICA E INTRUSÃO DE ELITE',
            'en': 'DOCTRINE OF TACTICAL ANTICIPATION & ELITE INTRUSION'
        },
        'modus': {
            'pt': 'A doutrina de Israel baseia-se na defesa preventiva ativa e na superioridade tecnológica absoluta. Especialistas em desenvolver engenharia reversa e exploits de "Clique Zero" extremamente sofisticados, suas agências infiltram-se em redes adversárias para neutralizar ameaças físicas ou digitais antes que se materializem.',
            'en': 'Israel\'s doctrine is built on active preventive defense and absolute technological superiority. Experts in developing highly sophisticated "Zero-Click" exploits and reverse-engineering, its agencies infiltrate adversary networks to neutralize physical or digital threats before they materialize.'
        }
    },
    'KP': {
        'title': {
            'pt': 'DOUTRINA DE SUBVERSÃO FINANCEIRA E ROUBO DE ATIVOS',
            'en': 'DOCTRINE OF FINANCIAL SUBVERSION & ASSET THEFT'
        },
        'modus': {
            'pt': 'Única nação do mundo que utiliza operações cibernéticas estatais focadas diretamente em ganho financeiro. Sob o comando direto do regime de Pyongyang, seus grupos APT executam assaltos digitais massivos a bancos internacionais e corretoras de criptomoedas para lavar dinheiro e financiar o programa de armas do país.',
            'en': 'The only nation in the world that utilizes state-sponsored cyber operations directly focused on financial gain. Under Pyongyang\'s command, its APT groups execute massive digital heists against international banks and cryptocurrency exchanges to launder money and fund weapons programs.'
        }
    },
    'EU': {
        'title': {
            'pt': 'DOUTRINA DE RESILIÊNCIA REGULATÓRIA E DEFESA COOPERATIVA',
            'en': 'DOCTRINE OF REGULATORY RESILIENCE & COOPERATIVE DEFENSE'
        },
        'modus': {
            'pt': 'A União Europeia adota uma postura focada em resiliência cibernética, imposição de padrões rígidos de privacidade (GDPR) e cooperação policial transfronteiriça. Suas agências focam em inteligência defensiva, atribuição de ameaças estatais e no desmantelamento de botnets e sindicatos globais de crime digital.',
            'en': 'The European Union adopts a posture focused on cyber resilience, enforcing strict privacy standards (GDPR), and cross-border law enforcement cooperation. Its agencies focus on defensive intelligence, state threat attribution, and dismantling global botnets and cybercrime syndicates.'
        }
    },
    'IN': {
        'title': {
            'pt': 'DOUTRINA DE ESPIONAGEM REGIONAL E CONTRA-INTELIGÊNCIA',
            'en': 'DOCTRINE OF REGIONAL ESPIONAGE & COUNTER-INTEL'
        },
        'modus': {
            'pt': 'A Índia foca suas operações cibernéticas estatais em alvos governamentais, diplomáticos e militares vizinhos na Ásia Meridional, operando de forma persistente através de campanhas de Spear-Phishing cirúrgicas e malwares customizados para a coleta de inteligência estratégica.',
            'en': 'India focuses its state-sponsored cyber operations on neighboring government, diplomatic, and military targets in South Asia, operating persistently through surgical Spear-Phishing campaigns and custom malware to gather strategic intelligence.'
        }
    },
    'BR': {
        'title': {
            'pt': 'DOUTRINA DE SUBVERSÃO FINANCEIRA E TROJANS DE ELITE',
            'en': 'DOCTRINE OF FINANCIAL SUBVERSION & ELITE TROJANS'
        },
        'modus': {
            'pt': 'O Brasil é uma superpotência global em cibercrime financeiro. Sua assinatura é marcada pelo desenvolvimento de Trojans bancários altamente sofisticados, técnicas avançadas de evasão de automação e engenharia social criativa, operando grandes sindicatos que atacam instituições financeiras na Europa e Américas.',
            'en': 'Brazil is a global superpower in financial cybercrime. Its signature is characterized by the development of highly sophisticated banking Trojans, advanced automation evasion techniques, and creative social engineering, running massive syndicates targeting financial institutions across Europe and the Americas.'
        }
    },
    'global': {
        'title': {
            'pt': 'OPERAÇÕES TRANSNACIONAIS E ATORES NÃO-ALINHADOS',
            'en': 'TRANSNATIONAL OPERATIONS & NON-ALIGNED ACTORS'
        },
        'modus': {
            'pt': 'Esta seção centraliza atores de ameaças transnacionais, sindicatos de cibercrime financeiro descentralizados e grupos APT de regiões não-alinhadas às grandes potências (como América do Sul, África e Oceania), cujas operações cruzam fronteiras físicas e operam de forma independente.',
            'en': 'This section centralizes transnational threat actors, decentralized financial cybercrime syndicates, and APT groups from regions non-aligned with major cyber powers (such as South America, Africa, and Oceania), whose operations cross physical borders and run independently.'
        }
    }
}

# ═══════════════════════════════════════════════════════════════
# ELITE HISTORICAL ACTORS (Israel and EU)
# ═══════════════════════════════════════════════════════════════
ELITE_ACTORS = [
    {
        'name': 'Shalev Hulio',
        'countryCode': 'IL',
        'category': 'individuals',
        'subcategory': 'famous',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Cofundador e ex-CEO da NSO Group, empresa israelense responsável pela criação do Pegasus, o spyware de zero-click mais sofisticado do mundo. O Pegasus foi usado por governos para vigilância de dissidentes, jornalistas e ativistas. Hulio construiu um império bilionário vendendo armas cibernéticas de nível militar.',
            'en': 'Co-founder and former CEO of NSO Group, Israeli company responsible for creating Pegasus, the world\'s most sophisticated zero-click spyware. Pegasus was used by governments for surveillance of dissidents, journalists and activists. Hulio built a billion-dollar empire selling military-grade cyber weapons.'
        },
        'specialty': {
            'pt': 'Zero-Click Exploits, Spyware Commercial, Cyber Arms Trade',
            'en': 'Zero-Click Exploits, Commercial Spyware, Cyber Arms Trade'
        },
        'type': {
            'pt': 'Mercenário Cibernético / Elite',
            'en': 'Cyber Mercenary / Elite'
        },
        'tactical': 98,
        'strategic': 95,
        'image': 'assets/images/classe_individuos.jpg'
    },
    {
        'name': 'Tal Dilian',
        'countryCode': 'IL',
        'category': 'individuals',
        'subcategory': 'famous',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Ex-comandante da Unidade 8200 e fundador da Intellexa, criadora do Predator spyware. Dilian comercializa ferramentas de espionagem móvel para governos autoritários e corporações. Opera através de uma rede complexa de empresas de fachada em paraísos fiscais.',
            'en': 'Former Unit 8200 commander and founder of Intellexa, creator of Predator spyware. Dilian markets mobile espionage tools to authoritarian governments and corporations. Operates through a complex network of shell companies in tax havens.'
        },
        'specialty': {
            'pt': 'Mobile Surveillance, Exploit-as-a-Service, SIGINT Operations',
            'en': 'Mobile Surveillance, Exploit-as-a-Service, SIGINT Operations'
        },
        'type': {
            'pt': 'Mercenário Cibernético / Lucro',
            'en': 'Cyber Mercenary / Profit'
        },
        'tactical': 95,
        'strategic': 92,
        'image': 'assets/images/classe_individuos.jpg'
    },
    {
        'name': 'Sandro Gauci',
        'countryCode': 'EU',
        'category': 'individuals',
        'subcategory': 'famous',
        'rarity': '⭐⭐⭐⭐',
        'description': {
            'pt': 'Pesquisador sênior de segurança em VoIP e telecomunicações, criador do SIPVicious, um dos frameworks de auditoria de segurança SIP/VoIP mais utilizados no mundo. Gauci é reconhecido globalmente por suas contribuições para a segurança de infraestruturas de telecomunicações.',
            'en': 'Senior security researcher in VoIP and telecommunications, creator of SIPVicious, one of the world\'s most used SIP/VoIP security audit frameworks. Gauci is globally recognized for his contributions to telecommunications infrastructure security.'
        },
        'specialty': {
            'pt': 'VoIP Security, Telecom Auditing, SIP Protocol Research',
            'en': 'VoIP Security, Telecom Auditing, SIP Protocol Research'
        },
        'type': {
            'pt': 'Pesquisador de Segurança / Elite',
            'en': 'Security Researcher / Elite'
        },
        'tactical': 92,
        'strategic': 80,
        'image': 'assets/images/classe_individuos.jpg'
    },
    {
        'name': 'Wau Holland',
        'countryCode': 'EU',
        'category': 'individuals',
        'subcategory': 'famous',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Lendário cofundador do Chaos Computer Club (CCC) em 1981, o maior e mais antigo coletivo de hackers éticos da Europa. Holland foi pioneiro do hacktivismo político e defensor da privacidade digital. Sua filosofia de "hackear é aprender" influenciou gerações de pesquisadores de segurança.',
            'en': 'Legendary co-founder of Chaos Computer Club (CCC) in 1981, Europe\'s largest and oldest ethical hacker collective. Holland was a pioneer of political hacktivism and digital privacy advocate. His philosophy of "hacking is learning" influenced generations of security researchers.'
        },
        'specialty': {
            'pt': 'Ethical Hacking, Digital Rights Activism, Hacker Culture',
            'en': 'Ethical Hacking, Digital Rights Activism, Hacker Culture'
        },
        'type': {
            'pt': 'Lenda Histórica / Hacktivista',
            'en': 'Historical Legend / Hacktivist'
        },
        'tactical': 88,
        'strategic': 90,
        'image': 'assets/images/classe_individuos.jpg'
    }
]

# ═══════════════════════════════════════════════════════════════
# ELITE GOVERNMENT ORGANIZATIONS (Defense & Espionage)
# Taxonomy: defense_law + military_espionage
# ═══════════════════════════════════════════════════════════════
GOV_ORGANIZATIONS = [
    # US - MILITARY ESPIONAGE
    {
        'name': 'NSA - Tailored Access Operations (TAO)',
        'countryCode': 'US',
        'category': 'organizations',
        'subcategory': 'military_espionage',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Divisão ultra-secreta da NSA especializada em operações de acesso sob medida contra alvos de alto valor. A TAO desenvolve exploits customizados baseados em hardware, realiza implantes em equipamentos de rede e executa operações de inteligência cibernética ofensiva. Revelada por Edward Snowden, é considerada a unidade de elite de guerra cibernética dos EUA.',
            'en': 'Ultra-secret NSA division specialized in tailored access operations against high-value targets. TAO develops custom hardware-based exploits, performs network equipment implants and executes offensive cyber intelligence operations. Revealed by Edward Snowden, it is considered the elite US cyber warfare unit.'
        },
        'specialty': {
            'pt': 'Operações de Acesso Sob Medida e Exploits Baseados em Hardware',
            'en': 'Tailored Access Operations & Hardware-Based Exploits'
        },
        'type': {
            'pt': 'Agência de Inteligência / Operações Ofensivas',
            'en': 'Intelligence Agency / Offensive Operations'
        },
        'tactical': 98,
        'strategic': 96,
        'image': '🎯'
    },
    # US - DEFENSE & LAW
    {
        'name': 'CISA (Cybersecurity and Infrastructure Security Agency)',
        'countryCode': 'US',
        'category': 'organizations',
        'subcategory': 'defense_law',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Agência federal dos EUA responsável pela proteção de infraestruturas críticas cibernéticas e físicas. Mantém o catálogo KEV (Known Exploited Vulnerabilities) com diretrizes de mitigação urgente. Coordena respostas a incidentes cibernéticos de nível nacional e emite alertas técnicos para organizações públicas e privadas.',
            'en': 'US federal agency responsible for protecting critical cyber and physical infrastructures. Maintains the KEV (Known Exploited Vulnerabilities) catalog with urgent mitigation guidelines. Coordinates national-level cyber incident response and issues technical alerts to public and private organizations.'
        },
        'specialty': {
            'pt': 'Diretrizes de Emergência e Mitigação de Vulnerabilidades Conhecidas (KEV)',
            'en': 'Emergency Guidelines & Known Exploited Vulnerabilities (KEV) Mitigation'
        },
        'type': {
            'pt': 'Agência de Defesa Cibernética / Infraestrutura Crítica',
            'en': 'Cyber Defense Agency / Critical Infrastructure'
        },
        'tactical': 80,
        'strategic': 95,
        'image': '🎯'
    },
    {
        'name': 'FBI Cyber Division',
        'countryCode': 'US',
        'category': 'organizations',
        'subcategory': 'defense_law',
        'rarity': '⭐⭐⭐⭐',
        'description': {
            'pt': 'Divisão especializada do FBI focada em investigações de crimes cibernéticos e operações de desmantelamento de infraestruturas criminosas. Liderou operações históricas como o takedown da Hive Ransomware e a apreensão de botnets massivas. Conduz investigações transfronteiriças em coordenação com agências internacionais.',
            'en': 'Specialized FBI division focused on cybercrime investigations and criminal infrastructure takedown operations. Led historic operations like the Hive Ransomware takedown and massive botnet seizures. Conducts cross-border investigations in coordination with international agencies.'
        },
        'specialty': {
            'pt': 'Desmantelamento de Infraestruturas de Ransomware e Botnets',
            'en': 'Ransomware Infrastructure Takedown & Botnet Dismantling'
        },
        'type': {
            'pt': 'Polícia Federal / Cibercrime',
            'en': 'Federal Police / Cybercrime'
        },
        'tactical': 88,
        'strategic': 85,
        'image': '🎯'
    },
    # RUSSIA - ESPIONAGEM MILITAR
    {
        'name': 'GRU - Unidade 74455 (Centro Principal de Tecnologias Especiais)',
        'countryCode': 'RU',
        'category': 'organizations',
        'subcategory': 'military_espionage',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Unidade de elite do GRU russo (inteligência militar) conhecida publicamente como Sandworm Team. Especializada em sabotagem destrutiva de infraestrutura crítica industrial usando malware wiper e ataques ICS/SCADA. Responsável por apagões na Ucrânia (2015, 2016), NotPetya (2017) e ataques aos Jogos Olímpicos de Inverno.',
            'en': 'Elite GRU unit (Russian military intelligence) publicly known as Sandworm Team. Specialized in destructive sabotage of critical industrial infrastructure using wiper malware and ICS/SCADA attacks. Responsible for Ukraine blackouts (2015, 2016), NotPetya (2017) and Winter Olympics attacks.'
        },
        'specialty': {
            'pt': 'Sabotagem Destrutiva de Infraestrutura Crítica Industrial (ICS/SCADA)',
            'en': 'Destructive Sabotage of Critical Industrial Infrastructure (ICS/SCADA)'
        },
        'type': {
            'pt': 'Inteligência Militar / Sabotagem Cibernética',
            'en': 'Military Intelligence / Cyber Sabotage'
        },
        'tactical': 94,
        'strategic': 99,
        'image': '🎯'
    },
    # ISRAEL - MILITARY ESPIONAGE
    {
        'name': 'Unidade 8200 (Aman)',
        'countryCode': 'IL',
        'category': 'organizations',
        'subcategory': 'military_espionage',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'A lendária unidade de inteligência de sinais das Forças de Defesa de Israel. Considerada o berço da indústria de cibersegurança israelense, a 8200 treina hackers de elite e desenvolve capacidades SIGINT avançadas. Ex-membros fundaram empresas como NSO Group, Check Point e CyberArk. Opera em alta classificação de sigilo.',
            'en': 'The legendary signals intelligence unit of Israel Defense Forces. Considered the cradle of Israeli cybersecurity industry, Unit 8200 trains elite hackers and develops advanced SIGINT capabilities. Former members founded companies like NSO Group, Check Point and CyberArk. Operates under high classification secrecy.'
        },
        'specialty': {
            'pt': 'Inteligência de Sinais (SIGINT) e Decodificação Crítica de Dados',
            'en': 'Signals Intelligence (SIGINT) & Critical Data Decryption'
        },
        'type': {
            'pt': 'Inteligência Militar / SIGINT',
            'en': 'Military Intelligence / SIGINT'
        },
        'tactical': 96,
        'strategic': 94,
        'image': '🎯'
    },
    # EUROPEAN UNION - DEFENSE & LAW
    {
        'name': 'Europol European Cybercrime Centre (EC3)',
        'countryCode': 'EU',
        'category': 'organizations',
        'subcategory': 'defense_law',
        'rarity': '⭐⭐⭐⭐',
        'description': {
            'pt': 'Centro de coordenação policial transfronteiriça da Europol focado em combate ao cibercrime organizado. Especializado em operações de apreensão de servidores de botnets, marketplaces da dark web e infraestruturas de ransomware. Coordena Joint Investigation Teams (JITs) com múltiplas jurisdições europeias.',
            'en': 'Europol cross-border police coordination center focused on combating organized cybercrime. Specialized in server seizure operations of botnets, dark web marketplaces and ransomware infrastructures. Coordinates Joint Investigation Teams (JITs) with multiple European jurisdictions.'
        },
        'specialty': {
            'pt': 'Coordenação Policial Transfronteiriça e Apreensão de Servidores',
            'en': 'Cross-Border Police Coordination & Server Seizures'
        },
        'type': {
            'pt': 'Polícia Internacional / Cibercrime',
            'en': 'International Police / Cybercrime'
        },
        'tactical': 85,
        'strategic': 82,
        'image': '🎯'
    }
]

# ═══════════════════════════════════════════════════════════════
# OSINT/SIGINT GROUPS (Open-Source Investigation)
# ═══════════════════════════════════════════════════════════════
OSINT_SIGINT_ACTORS = [
    # BELLINGCAT - European Union (Netherlands)
    {
        'name': 'Bellingcat',
        'countryCode': 'EU',
        'category': 'groups',
        'subcategory': 'osint_sigint',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Coletivo investigativo internacional pioneiro em jornalismo de fontes abertas (OSINT). Famoso por expor a identidade de oficiais do GRU/FSB envolvidos no envenenamento de Sergei Skripal usando dados vazados de telefonia e registros de passaportes russos. Utilizaram geolocalização geoespacial para mapear crimes de guerra na Síria e Ucrânia, combinando imagens de satélite com vídeos de redes sociais. Suas investigações levaram a indiciamentos internacionais pelo Tribunal de Haia.',
            'en': 'International investigative collective pioneering open-source journalism (OSINT). Famous for exposing the identity of GRU/FSB officers involved in the Sergei Skripal poisoning using leaked Russian phone data and passport records. Used geospatial geolocation to map war crimes in Syria and Ukraine, combining satellite imagery with social media videos. Their investigations led to international indictments by the Hague Tribunal.'
        },
        'specialty': {
            'pt': 'Investigação de Fontes Abertas e Geolocalização Geoespacial',
            'en': 'Open Source Investigation & Geospatial Geolocation'
        },
        'type': {
            'pt': 'Coletivo Investigativo / OSINT',
            'en': 'Investigative Collective / OSINT'
        },
        'tactical': 85,
        'strategic': 92,
        'image': '🔍'
    },
    # THE CITIZEN LAB - Canada/Western allies (mapped as EU)
    {
        'name': 'The Citizen Lab',
        'countryCode': 'EU',
        'category': 'groups',
        'subcategory': 'osint_sigint',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Laboratório interdisciplinar da Universidade de Toronto especializado em análise forense de spywares e telemetria digital. Descobriram e isolaram infecções ativas do Pegasus (NSO Group) analisando logs de memória de iPhones de ativistas, jornalistas e políticos pelo mundo. Responsáveis por expor a infraestrutura global de spyware comercial, incluindo Predator (Intellexa) e FinFisher. Publicam relatórios técnicos detalhados com indicadores de comprometimento (IOCs) e assinaturas de malware.',
            'en': 'Interdisciplinary laboratory at University of Toronto specialized in forensic analysis of spyware and digital telemetry. Discovered and isolated active Pegasus (NSO Group) infections by analyzing memory logs from iPhones of activists, journalists and politicians worldwide. Responsible for exposing the global commercial spyware infrastructure, including Predator (Intellexa) and FinFisher. Publish detailed technical reports with indicators of compromise (IOCs) and malware signatures.'
        },
        'specialty': {
            'pt': 'Análise Forense de Spywares e Telemetria Digital',
            'en': 'Spyware Forensic Analysis & Digital Telemetry'
        },
        'type': {
            'pt': 'Laboratório de Pesquisa / Análise Forense',
            'en': 'Research Laboratory / Forensic Analysis'
        },
        'tactical': 90,
        'strategic': 88,
        'image': '🔍'
    },
    # INTELLEXA CONSORTIUM - Israel
    {
        'name': 'Intellexa Consortium (Private SIGINT)',
        'countryCode': 'IL',
        'category': 'groups',
        'subcategory': 'osint_sigint',
        'rarity': '⭐⭐⭐⭐⭐',
        'description': {
            'pt': 'Consórcio privado de inteligência de sinais fundado por ex-oficiais da Unidade 8200 e comandos da IDF. Desenvolvem e comercializam o Predator spyware, capaz de interceptação tática de sinais celulares e exploração de vulnerabilidades em redes 5G. Operam através de uma rede complexa de subsidiárias em paraísos fiscais (Chipre, Grécia, Madagascar). Seus sistemas realizam deep packet inspection em nível de operadora de telecomunicações, permitindo vigilância massiva sem implantes nos dispositivos-alvo.',
            'en': 'Private signals intelligence consortium founded by former Unit 8200 officers and IDF commandos. Develop and market Predator spyware, capable of tactical interception of cellular signals and exploitation of 5G network vulnerabilities. Operate through a complex network of subsidiaries in tax havens (Cyprus, Greece, Madagascar). Their systems perform deep packet inspection at telecom operator level, enabling mass surveillance without implants on target devices.'
        },
        'specialty': {
            'pt': 'Interceptação Tática de Sinais Celulares e Redes 5G',
            'en': 'Tactical Cellular Signal Interception & 5G Networks'
        },
        'type': {
            'pt': 'Mercenário Cibernético / SIGINT Comercial',
            'en': 'Cyber Mercenary / Commercial SIGINT'
        },
        'tactical': 96,
        'strategic': 90,
        'image': '🔍'
    }
]

# ═══════════════════════════════════════════════════════════════
# CLEANUP AND TRANSLATION HELPERS
# ═══════════════════════════════════════════════════════════════

def clean_markdown_links(text):
    """Strip Markdown links [text](url), keep visible text only."""
    return re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

def clean_citations(text):
    """Strip MITRE-style (Citation: ...) markers."""
    return re.sub(r'\(Citation:[^\)]+\)', '', text)

def clean_text(text):
    """Fully normalize whitespace and punctuation."""
    text = clean_markdown_links(text)
    text = clean_citations(text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,;!?])', r'\1', text)
    text = re.sub(r'([.,;!?])\s+', r'\1 ', text)
    return text.strip()

def extract_complete_sentences(text, num_sentences=3):
    """Extract the first N complete sentences from text."""
    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    selected_sentences = sentences[:num_sentences]
    result = ' '.join(selected_sentences)
    if result and not result.endswith(('.', '!', '?')):
        result += '.'
    return result

def translate_to_portuguese(text):
    """Translate English text to Portuguese."""
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
        print(f"[WARN] Translation error: {e}. Keeping original text.")
        return text

def fix_cyber_jargon(text):
    """Post-process translated text, fixing literal jargon mistranslations."""
    if not text:
        return text
    corrected_text = text
    for wrong_term, correct_term in CYBER_JARGON_FIXES.items():
        pattern = re.compile(re.escape(wrong_term), re.IGNORECASE)
        corrected_text = pattern.sub(correct_term, corrected_text)
    return corrected_text

# ═══════════════════════════════════════════════════════════════
# GEOPOLITICAL ATTRIBUTION
# ═══════════════════════════════════════════════════════════════

def is_sentence_about_target(sentence, country_keyword):
    """
    Check whether a sentence mentions the country as a TARGET (victim).
    Returns True when attack-targeting phrases are present.
    """
    sentence_lower = sentence.lower()

    if country_keyword not in sentence_lower:
        return False

    for target_phrase in TARGET_PHRASES:
        if target_phrase in sentence_lower:
            return True

    return False

def detect_country_from_text(description, name):
    """
    Detect ORIGIN country for a group/individual via smart filters.

    Pipeline:
    1. Hardcoded overrides (zero-error path for critical groups)
    2. South-America exclusion filter (avoids US false positives)
    3. Strong positive filter (compound origin phrases)
    4. Negative filter (ignore countries mentioned as targets)
    5. Fallback to "global" (transnational / non-aligned actors)
    """
    text = f"{description} {name}".lower()
    name_lower = name.lower()
    
    # ═══════════════════════════════════════════════════════════════
    # PRIORITY 1: HARDCODED OVERRIDES (Critical Groups)
    # ═══════════════════════════════════════════════════════════════
    for group_name, country_code in FIXED_COUNTRY_GROUPS.items():
        if group_name in name_lower:
            print(f"  [OVERRIDE] {name} -> {country_code} (hardcoded)")
            return country_code
    
    # ═══════════════════════════════════════════════════════════════
    # PRIORITY 2: SOUTH-AMERICA EXCLUSION FILTER
    # Brazil is a first-class origin (BR). Other LatAm mentions → global.
    # Victim mentions of Brazil/India are still ignored via TARGET_PHRASES.
    # ═══════════════════════════════════════════════════════════════
    south_america_keywords = [
        'south america', 'latin america',
        'argentina', 'argentinian', 'colombia', 'colombian', 'venezuela',
        'chilean', 'chile', 'peru', 'peruvian', 'spanish-speaking',
        'south american', 'latin american'
    ]
    
    for sa_keyword in south_america_keywords:
        if sa_keyword in text:
            print(f"  [GLOBAL - SOUTH-AMERICA] {name} -> global ('{sa_keyword}' detected)")
            return 'global'
    
    # ═══════════════════════════════════════════════════════════════
    # PRIORITY 3: STRONG POSITIVE FILTER (Compound Phrases)
    # ═══════════════════════════════════════════════════════════════
    for country_code, strong_keywords in ORIGIN_STRONG_KEYWORDS.items():
        for keyword in strong_keywords:
            if keyword in text:
                print(f"  [STRONG ORIGIN] {name} -> {country_code} ('{keyword}')")
                return country_code
    
    # ═══════════════════════════════════════════════════════════════
    # PRIORITY 4: SWEEP WITH NEGATIVE FILTER (Hygiene)
    # Protects India/Brazil: "targeting Indian/Brazilian orgs" ≠ origin.
    # ═══════════════════════════════════════════════════════════════
    # Split text into sentences (period as delimiter)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Simple country keywords (fallback with context validation)
    country_simple_keywords = {
        'CN': ['china', 'chinese', 'beijing', 'prc'],
        'RU': ['russia', 'russian', 'moscow'],
        'US': ['united states', 'american', 'u.s.'],
        'IR': ['iran', 'iranian', 'tehran'],
        'KP': ['north korea', 'pyongyang'],
        'IL': ['israel', 'israeli'],
        'IN': ['india', 'indian', 'new delhi', 'hindustan'],
        'BR': ['brazil', 'brasil', 'brazilian', 'brasileiro', 'brasileira', 'são paulo', 'sao paulo'],
        'EU': ['europe', 'european', 'germany', 'france', 'uk']
    }
    
    for country_code, simple_keywords in country_simple_keywords.items():
        for keyword in simple_keywords:
            if keyword not in text:
                continue
            
            # Inspect each sentence individually
            for sentence in sentences:
                if keyword in sentence.lower():
                    # Country mention without target context ⇒ origin
                    if not is_sentence_about_target(sentence, keyword):
                        print(f"  [ORIGIN VALIDATED] {name} -> {country_code} ('{keyword}' in neutral context)")
                        return country_code
                    else:
                        print(f"  [IGNORED TARGET] {name}: '{keyword}' detected as victim")
    
    # ═══════════════════════════════════════════════════════════════
    # PRIORITY 5: FALLBACK TO GLOBAL (Transnational Actors)
    # ═══════════════════════════════════════════════════════════════
    print(f"  [GLOBAL - NON-ALIGNED] {name} -> global (no clear attribution)")
    return 'global'

# ═══════════════════════════════════════════════════════════════
# GROUP PROCESSING (MITRE ATT&CK)
# ═══════════════════════════════════════════════════════════════

def download_mitre_data():
    """Download MITRE ATT&CK STIX bundle."""
    print("\n[1/5] Downloading MITRE ATT&CK data...")
    try:
        response = requests.get(MITRE_STIX_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"[OK] {len(data.get('objects', []))} STIX objects loaded.")
        return data
    except Exception as e:
        print(f"[ERROR] Failed to download MITRE: {e}")
        return None

def process_mitre_groups(mitre_data):
    """Process MITRE ATT&CK intrusion sets into group cards."""
    print("\n[2/5] Processing MITRE ATT&CK groups...")
    
    groups = []
    objects = mitre_data.get('objects', [])
    
    for obj in objects:
        if obj.get('type') != 'intrusion-set':
            continue
        
        name = obj.get('name', 'Unknown')
        description = obj.get('description', '')
        external_refs = obj.get('external_references', [])
        
        # HARDCODED OVERRIDE: UNC3886 (G1048)
        name_lower = name.lower()
        mitre_id = None
        for ref in external_refs:
            if ref.get('source_name') == 'mitre-attack':
                mitre_id = ref.get('external_id', '').lower()
                break
        
        if 'unc3886' in name_lower or mitre_id == 'g1048':
            print(f"[OVERRIDE] UNC3886 (G1048) detected - forcing China attribution")
            clean_desc_en = extract_complete_sentences(description, 3)
            clean_desc_pt = translate_to_portuguese(clean_desc_en)
            clean_desc_pt = fix_cyber_jargon(clean_desc_pt)
            
            groups.append({
                'name': name,
                'countryCode': 'CN',
                'category': 'groups',
                'subcategory': 'government',
                'rarity': '⭐⭐⭐⭐⭐',
                'description': {'pt': clean_desc_pt, 'en': clean_desc_en},
                'specialty': {
                    'pt': 'Exploitação de Hipervisores e Rootkits de Nuvem',
                    'en': 'Hypervisor Exploitation & Cloud Rootkits'
                },
                'type': {'pt': 'APT / Grupo de Ameaça', 'en': 'APT / Threat Group'},
                'tactical': 96,
                'strategic': 94,
                'image': '🎯'
            })
            continue
        
        country_code = detect_country_from_text(description, name)
        if not country_code:
            continue
        
        # Classify subcategory
        text = description.lower()
        if any(kw in text for kw in ['ransomware', 'extortion', 'financial', 'cryptocurrency', 'money']):
            subcategory = 'profit'
            rarity = '⭐⭐⭐⭐⭐'
            tactical, strategic = 90, 85
        elif any(kw in text for kw in ['wiper', 'destructive', 'ics', 'scada', 'infrastructure', 'sabotage']):
            subcategory = 'government'
            rarity = '⭐⭐⭐⭐⭐'
            tactical, strategic = 95, 98
        elif any(kw in text for kw in ['espionage', 'intelligence', 'surveillance', 'apt']):
            subcategory = 'government'
            rarity = '⭐⭐⭐⭐'
            tactical, strategic = 80, 90
        else:
            subcategory = 'osint_sigint'
            rarity = '⭐⭐⭐'
            tactical, strategic = 70, 65
        
        # Synthesize description
        clean_desc_en = extract_complete_sentences(description, 3)
        clean_desc_pt = translate_to_portuguese(clean_desc_en)
        clean_desc_pt = fix_cyber_jargon(clean_desc_pt)
        
        groups.append({
            'name': name,
            'countryCode': country_code,
            'category': 'groups',
            'subcategory': subcategory,
            'rarity': rarity,
            'description': {'pt': clean_desc_pt, 'en': clean_desc_en},
            'specialty': {'pt': 'Operações Cibernéticas', 'en': 'Cyber Operations'},
            'type': {'pt': 'APT / Grupo de Ameaça', 'en': 'APT / Threat Group'},
            'tactical': tactical,
            'strategic': strategic,
            'image': '🎯'
        })
    
    print(f"[OK] {len(groups)} MITRE groups processed.")
    return groups

# ═══════════════════════════════════════════════════════════════
# GOVERNMENT ORG PROCESSING (CERTs/CSIRTs) — optional / unused in main
# Kept as seed utilities; pipeline no longer downloads CERTs dynamically.
# ═══════════════════════════════════════════════════════════════

def download_cert_data():
    """Download public global CERT/CSIRT membership data."""
    print("\n[4/6] Downloading CERT and government agency data...")
    
    # Alternate public source URLs
    cert_sources = [
        "https://raw.githubusercontent.com/FIRST-Tech/FIRST-member-list/main/members.json",
        "https://www.first.org/members/teams/listing"
    ]
    
    # Attempt 1: structured JSON
    try:
        response = requests.get(cert_sources[0], timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] CERT data loaded successfully.")
            return data
    except Exception as e:
        print(f"[WARN] Primary source unavailable: {e}")
    
    # Fallback: return hardcoded elite CERT list
    print("[FALLBACK] Using hardcoded elite CERT / national agency list...")
    return get_hardcoded_certs()

def get_hardcoded_certs():
    """Hardcoded elite CERT / national agency seed list."""
    return [
        # USA
        {'name': 'US-CERT (CISA)', 'country': 'US', 'type': 'National CERT', 
         'description': 'United States Computer Emergency Readiness Team, part of CISA. Provides cybersecurity coordination and incident response for federal agencies and critical infrastructure.'},
        {'name': 'NSA Cybersecurity Directorate', 'country': 'US', 'type': 'Intelligence',
         'description': 'NSA division responsible for preventing and eradicating threats to national security systems and critical infrastructure. Publishes security guidance and threat intelligence.'},
        
        # Russia
        {'name': 'RU-CERT (ГосСОПКА)', 'country': 'RU', 'type': 'National CERT',
         'description': 'Russian national Computer Emergency Response Team. Coordinates cybersecurity incident response and threat intelligence for government and critical infrastructure.'},
        {'name': 'Federal Security Service (FSB) Cyber Division', 'country': 'RU', 'type': 'Intelligence',
         'description': 'FSB cyber operations division responsible for domestic cybersecurity and counter-intelligence. Conducts offensive cyber operations and surveillance.'},
        
        # China
        {'name': 'CNCERT/CC', 'country': 'CN', 'type': 'National CERT',
         'description': 'China National Computer Network Emergency Response Technical Team/Coordination Center. National cybersecurity coordination body under the Ministry of Industry and Information Technology.'},
        {'name': 'Strategic Support Force Network Systems Department', 'country': 'CN', 'type': 'Military',
         'description': 'PLA Strategic Support Force cyber warfare division. Responsible for offensive cyber operations, electronic warfare, and information operations.'},
        
        # Iran
        {'name': 'MAHER Center (Iran CERT)', 'country': 'IR', 'type': 'National CERT',
         'description': 'Iranian national Computer Emergency Response Team. Coordinates cybersecurity for government networks and critical infrastructure protection.'},
        {'name': 'IRGC Cyber Electronic Command', 'country': 'IR', 'type': 'Military',
         'description': 'Islamic Revolutionary Guard Corps cyber warfare division. Conducts offensive cyber operations and surveillance against regional adversaries.'},
        
        # Israel
        {'name': 'CERT-IL', 'country': 'IL', 'type': 'National CERT',
         'description': 'Israel National Cyber Directorate CERT. Coordinates national cybersecurity incidents and provides threat intelligence to government and private sector.'},
        {'name': 'IDF Cyber Defense Directorate', 'country': 'IL', 'type': 'Military',
         'description': 'Israel Defense Forces cyber defense organization. Works alongside Unit 8200 for defensive cyber operations and critical infrastructure protection.'},
        
        # North Korea
        {'name': 'KP-CERT', 'country': 'KP', 'type': 'National CERT',
         'description': 'North Korean Computer Emergency Response Team. Nominally responsible for cybersecurity coordination, operates under strict military control.'},
        {'name': 'Reconnaissance General Bureau Cyber Warfare Guidance Unit', 'country': 'KP', 'type': 'Military',
         'description': 'North Korean military intelligence cyber operations unit. Conducts offensive cyber operations for espionage and financial gain.'},
        
        # European Union
        {'name': 'CERT-EU', 'country': 'EU', 'type': 'Regional CERT',
         'description': 'Computer Emergency Response Team for EU institutions, bodies and agencies. Provides cybersecurity services and incident response coordination.'},
        {'name': 'BSI (Germany)', 'country': 'DE', 'type': 'National CERT',
         'description': 'Bundesamt für Sicherheit in der Informationstechnik. German Federal Office for Information Security, responsible for national cybersecurity coordination.'},
        {'name': 'ANSSI (France)', 'country': 'FR', 'type': 'Intelligence',
         'description': 'Agence nationale de la sécurité des systèmes d\'information. French national cybersecurity agency with both defensive and offensive capabilities.'},
        {'name': 'NCSC (UK)', 'country': 'GB', 'type': 'Intelligence',
         'description': 'National Cyber Security Centre, part of GCHQ. Provides cybersecurity guidance and coordinates UK national cyber defense.'}
    ]

def classify_cert_subcategory(name, description, org_type):
    """Classify CERT/agency as defense_law or military_espionage."""
    text = f"{name} {description} {org_type}".lower()
    
    # Prefer espionage/military keywords
    espionage_score = sum(1 for kw in ESPIONAGE_MILITARY_KEYWORDS if kw in text)
    defense_score = sum(1 for kw in DEFENSE_LAW_KEYWORDS if kw in text)
    
    if espionage_score > defense_score:
        return 'military_espionage'
    return 'defense_law'

def process_cert_organizations(cert_data):
    """Process CERTs and government agencies into organization cards."""
    print("\n[5/6] Processing CERTs and government agencies...")
    
    organizations = []
    country_counts = {}
    
    for cert in cert_data:
        # Extract base fields
        name = cert.get('name', 'Unknown')
        country_iso = cert.get('country', '')
        org_type = cert.get('type', '')
        description = cert.get('description', '')
        
        # Map country
        country_code = ISO2_TO_COUNTRY.get(country_iso)
        if not country_code:
            continue
        
        # Keep elite government agencies only
        name_lower = name.lower()
        if any(excl in name_lower for excl in ['university', 'academic', 'private', 'commercial', 'corporate']):
            continue
        
        if not any(kw in name_lower for kw in ['national', 'government', 'federal', 'military', 'cert', 'csirt', 'cyber', 'defense', 'intelligence']):
            continue
        
        # Classify subcategory
        subcategory = classify_cert_subcategory(name, description, org_type)
        
        # Assign stats from subcategory
        if subcategory == 'military_espionage':
            rarity = '⭐⭐⭐⭐⭐'
            tactical, strategic = 94, 96
        else:
            rarity = '⭐⭐⭐⭐'
            tactical, strategic = 82, 88
        
        # Process description
        if not description or len(description) < 50:
            description = f"{name} is a national cybersecurity coordination body responsible for incident response and threat intelligence sharing."
        
        clean_desc_en = extract_complete_sentences(description, 3)
        clean_desc_pt = translate_to_portuguese(clean_desc_en)
        clean_desc_pt = fix_cyber_jargon(clean_desc_pt)
        
        # Specialty from org type
        if 'intelligence' in org_type.lower() or subcategory == 'military_espionage':
            specialty_en = 'Offensive Cyber Operations & SIGINT'
            specialty_pt = 'Operações Cibernéticas Ofensivas e SIGINT'
        else:
            specialty_en = 'Incident Response & Critical Infrastructure Protection'
            specialty_pt = 'Resposta a Incidentes e Proteção de Infraestrutura Crítica'
        
        organizations.append({
            'name': name,
            'countryCode': country_code,
            'category': 'organizations',
            'subcategory': subcategory,
            'rarity': rarity,
            'description': {'pt': clean_desc_pt, 'en': clean_desc_en},
            'specialty': {'pt': specialty_pt, 'en': specialty_en},
            'type': (
                {
                    'pt': 'Espionagem e Operações Militares',
                    'en': 'Espionage & Military Operations',
                }
                if subcategory == 'military_espionage'
                else {
                    'pt': 'Defesa e Aplicação da Lei',
                    'en': 'Defense & Law Enforcement',
                }
            ),
            'tactical': tactical,
            'strategic': strategic,
            'image': '🎯'
        })
        
        # Tally by country
        country_counts[country_code] = country_counts.get(country_code, 0) + 1
    
    # Per-country breakdown log
    print(f"\n[BREAKDOWN BY COUNTRY]")
    for country_code in sorted(country_counts.keys()):
        count = country_counts[country_code]
        country_name = {'US': 'USA', 'RU': 'Russia', 'CN': 'China', 'IR': 'Iran',
                       'IL': 'Israel', 'KP': 'North Korea', 'EU': 'European Union'}.get(country_code, country_code)
        print(f"  {country_name} ({country_code}): {count} agency(ies)")
    
    print(f"\n[OK] {len(organizations)} government organizations processed.")
    return organizations

# ═══════════════════════════════════════════════════════════════
# FINAL FILE GENERATION
# ═══════════════════════════════════════════════════════════════

def generate_js_file(all_data):
    """Emit js/data.js."""
    print("\n[6/6] Generating js/data.js...")
    
    # Organize by structure — sanitize ALL keys before grouping
    database = {
        'groups': {'profit': [], 'osint_sigint': [], 'government': []},
        'individuals': {'famous': []},
        'organizations': {'defense_law': [], 'military_espionage': []}
    }
    
    for actor in all_data:
        clean = normalize_taxonomies(sanitize_actor_keys(actor))
        category = clean.get('category', 'groups')
        subcategory = clean.get('subcategory', 'government')
        if category in database and subcategory in database[category]:
            database[category][subcategory].append(clean)
        else:
            print(f"  [WARN] Actor dropped (invalid key): {clean.get('name')} "
                  f"cat={category!r} sub={subcategory!r}")
    
    js_content = f"""// ═══════════════════════════════════════════════════════════════
// CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE v4.0 (EN keys)
// Auto-generated by builder.py
// Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Sources: MITRE ATT&CK (dynamic) + STATIC_GROUPS / STATIC_INDIVIDUALS / STATIC_ORGANIZATIONS
// ═══════════════════════════════════════════════════════════════

const cyberDatabase = {json.dumps(database, indent=4, ensure_ascii=False)};

const countries = [
    {{ code: "RU", name: {{ pt: "Rússia", en: "Russia" }}, flag: "🇷🇺" }},
    {{ code: "US", name: {{ pt: "EUA", en: "USA" }}, flag: "🇺🇸" }},
    {{ code: "CN", name: {{ pt: "China", en: "China" }}, flag: "🇨🇳" }},
    {{ code: "KP", name: {{ pt: "Coreia do Norte", en: "North Korea" }}, flag: "🇰🇵" }},
    {{ code: "IR", name: {{ pt: "Irã", en: "Iran" }}, flag: "🇮🇷" }},
    {{ code: "IL", name: {{ pt: "Israel", en: "Israel" }}, flag: "🇮🇱" }},
    {{ code: "IN", name: {{ pt: "Índia", en: "India" }}, flag: "🇮🇳" }},
    {{ code: "BR", name: {{ pt: "Brasil", en: "Brazil" }}, flag: "🇧🇷" }},
    {{ code: "EU", name: {{ pt: "União Europeia", en: "European Union" }}, flag: "🇪🇺" }},
    {{ code: "global", name: {{ pt: "Global", en: "Global" }}, flag: "🌐" }}
];

// ═══════════════════════════════════════════════════════════════
// GEOPOLITICAL DOSSIERS - CYBER WARFARE MODUS OPERANDI
// ═══════════════════════════════════════════════════════════════
const countryProfiles = {json.dumps(COUNTRY_PROFILES, indent=4, ensure_ascii=False)};

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
        "subcat-famous": "Famosos",
        "subcat-defense-law": "Defesa e Aplicação da Lei",
        "subcat-espionage-military": "Espionagem e Operações Militares",
        "title-cards": "Cards de Ameaças",
        "btn-back": "Voltar",
        "btn-live-map": "MAPA EM TEMPO REAL",
        "indicator-available": "[ Disponível ]",
        "title-live-map": "ThreatCloud Live Cyber Attack Map",
        "subtitle-live-map": "Check Point · Visualização tática em tempo real",
        "btn-donate": "₿",
        "donate-title": "APOIE SE VOCÊ GOSTOU DO PROJETO",
        "donate-desc": "Nos ajude doando qualquer valor via Bitcoin ou Pix para continuarmos o projeto e manter o banco de dados de CTI atualizado.",
        "donate-copy": "COPIAR ENDEREÇO"
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
        "subcat-famous": "Famous",
        "subcat-defense-law": "Defense & Law Enforcement",
        "subcat-espionage-military": "Espionage & Military Operations",
        "title-cards": "Threat Cards",
        "btn-back": "Back",
        "btn-live-map": "LIVE THREAT MAP",
        "indicator-available": "[ Available ]",
        "title-live-map": "ThreatCloud Live Cyber Attack Map",
        "subtitle-live-map": "Check Point · Real-time tactical visualization",
        "btn-donate": "₿",
        "donate-title": "SUPPORT IF YOU LIKED THE PROJECT",
        "donate-desc": "Help us by donating any amount via Bitcoin or Pix to keep our project and CTI threat database updated.",
        "donate-copy": "COPY ADDRESS"
    }}
}};
"""
    
    with open('js/data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    total = sum(len(subs) for cat in database.values() for subs in cat.values())
    famous_ru = [a for a in database['individuals']['famous'] if a.get('countryCode') == 'RU']
    print(f"[OK] js/data.js generated with {total} actors!")
    print(f"[OK] Famous individuals: {len(database['individuals']['famous'])} "
          f"(RU: {len(famous_ru)})")

# ═══════════════════════════════════════════════════════════════
# MAIN - ORCHESTRATION
# ═══════════════════════════════════════════════════════════════

def main():
    """Builder entrypoint — MITRE dynamic + static drawers only."""
    print("\n" + "=" * 70)
    print("  CYBER THREAT INTELLIGENCE PORTFOLIO - DATABASE BUILDER v3.0")
    print("  Sources: MITRE ATT&CK (dynamic) + STATIC drawers (manual)")
    print("=" * 70)

    # ── Dynamic source (MITRE only) ──
    dynamic_mitre_cards = []
    mitre_data = download_mitre_data()
    if mitre_data:
        dynamic_mitre_cards = process_mitre_groups(mitre_data)

    # ── Final concatenation (strict) ──
    final_json_data = (
        dynamic_mitre_cards
        + STATIC_GROUPS
        + STATIC_INDIVIDUALS
        + STATIC_ORGANIZATIONS
    )

    # ═══════════════════════════════════════════════════════════════
    # MANUAL_CORRECTIONS
    # Force country/subcategory for mis-attributed dynamic MITRE cards.
    # Runs BEFORE sanitize_actor_keys / normalize_taxonomies.
    # ═══════════════════════════════════════════════════════════════
    def apply_manual_corrections(cards):
        # name.lower() → (category, subcategory, countryCode)
        taxonomy_overrides = {
            'unc2452': ('groups', 'government', 'RU'),
            'rtm': ('groups', 'profit', 'RU'),
            'gorgon group': ('groups', 'government', 'global'),
            'fin7': ('groups', 'profit', 'RU'),
            'molerats': ('groups', 'government', 'global'),
            'dust storm': ('groups', 'government', 'CN'),
            # Non-military state APTs → Associado a Gov
            'orangeworm': ('groups', 'government', 'IR'),
            'admin@338': ('groups', 'government', 'CN'),
            'blacktech': ('groups', 'government', 'CN'),
            'apt41': ('groups', 'government', 'CN'),
            'gallium': ('groups', 'government', 'CN'),
            'tonto team': ('groups', 'government', 'CN'),
            'deep panda': ('groups', 'government', 'CN'),
            'suckfly': ('groups', 'government', 'CN'),
            'chimera': ('groups', 'government', 'CN'),
            'night dragon': ('groups', 'government', 'CN'),
            'higaisa': ('organizations', 'military_espionage', 'global'),
            'threat group-3390': ('groups', 'government', 'CN'),
            'putter panda': ('groups', 'government', 'CN'),
            'ta459': ('groups', 'government', 'CN'),
            'scarlet mimic': ('groups', 'government', 'CN'),
            'moafee': ('groups', 'government', 'CN'),
            'pittytiger': ('groups', 'government', 'CN'),
            'pitty tiger': ('groups', 'government', 'CN'),
        }

        for card in cards:
            name = str(card.get('name') or '').strip().lower()
            desc = card.get('description') or {}
            pt = desc.get('pt') if isinstance(desc, dict) else None

            if name == 'silence' and isinstance(pt, str) and pt.startswith('O silêncio'):
                desc = dict(desc)
                desc['pt'] = 'O Silence' + pt[len('O silêncio'):]
                card['description'] = desc

            if name == 'water galura' and isinstance(pt, str):
                desc = dict(desc)
                desc['pt'] = pt.replace(
                    'A Water Galura está ativa',
                    'O Water Galura está ativo'
                )
                card['description'] = desc

            # groups/government = non-military state APTs
            # organizations/military_espionage = strict military commands
            target = taxonomy_overrides.get(name)
            if target is None and name.startswith('cinnamon'):
                target = ('groups', 'government', 'CN')
            if target is None and 'pitty' in name and 'tiger' in name:
                target = ('groups', 'government', 'CN')

            if target:
                cat, sub, cc = target
                card['category'] = cat
                card['subcategory'] = sub
                card['countryCode'] = cc
                if cc == 'global':
                    card['countryId'] = 'global'
        return cards

    final_json_data = apply_manual_corrections(final_json_data)

    # Sanitize EN keys + force taxonomy before write
    final_json_data = [
        normalize_taxonomies(sanitize_actor_keys(a)) for a in final_json_data
    ]

    print(
        f"\n[MERGE] MITRE={len(dynamic_mitre_cards)} | "
        f"STATIC_GROUPS={len(STATIC_GROUPS)} | "
        f"STATIC_INDIVIDUALS={len(STATIC_INDIVIDUALS)} | "
        f"STATIC_ORGANIZATIONS={len(STATIC_ORGANIZATIONS)}"
    )

    for actor in STATIC_GROUPS:
        print(f"  [+] STATIC GROUP: {actor.get('name')}")
    for actor in STATIC_INDIVIDUALS:
        print(f"  [+] STATIC INDIVIDUAL: {actor.get('name')}")
    for actor in STATIC_ORGANIZATIONS:
        print(f"  [+] STATIC ORG: {actor.get('name')}")

    generate_js_file(final_json_data)

    categories_count = {
        'groups': len([a for a in final_json_data if a.get('category') == 'groups']),
        'individuals': len([a for a in final_json_data if a.get('category') == 'individuals']),
        'organizations': len([a for a in final_json_data if a.get('category') == 'organizations']),
    }

    print("\n" + "=" * 70)
    print("  [BUILD COMPLETE] js/data.js is ready!")
    print(f"  Total actors: {len(final_json_data)}")
    print(f"    - Groups: {categories_count['groups']}")
    print(f"    - Individuals: {categories_count['individuals']}")
    print(f"    - Organizations: {categories_count['organizations']}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
