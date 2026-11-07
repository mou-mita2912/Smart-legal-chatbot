"""
Mapping and cross-reference between Indian Penal Code (IPC 1860) / CrPC (1973)
and the New Criminal Laws: Bharatiya Nyaya Sanhita (BNS 2023) / BNSS (2023) / BSA (2023).
"""

# Key IPC -> BNS mappings
IPC_TO_BNS = {
    "302": {
        "title": "Murder",
        "ipc": "Section 302 IPC",
        "bns": "Section 103 BNS",
        "punishment": "Death or imprisonment for life, and fine.",
        "notes": "Under BNS 103(2), mob lynching on grounds of race, caste, sex, etc., is punishable by death or life imprisonment."
    },
    "304": {
        "title": "Culpable Homicide not amounting to Murder",
        "ipc": "Section 304 IPC",
        "bns": "Section 105 BNS",
        "punishment": "Life imprisonment or imprisonment up to 10 years, and fine.",
        "notes": "Divided into acts done with intention vs acts done with knowledge."
    },
    "304a": {
        "title": "Causing Death by Negligence (Hit-and-Run / Rash Driving)",
        "ipc": "Section 304A IPC",
        "bns": "Section 106 BNS",
        "punishment": "BNS 106(1): Imprisonment up to 5 years. BNS 106(2) [Hit & Run]: Failure to report to police/magistrate can lead to up to 10 years and fine.",
        "notes": "Section 106(2) introduced strict reporting duties for drivers."
    },
    "307": {
        "title": "Attempt to Murder",
        "ipc": "Section 307 IPC",
        "bns": "Section 109 BNS",
        "punishment": "Imprisonment up to 10 years and fine; if hurt is caused, up to life imprisonment.",
        "notes": "Similar principles carry over to BNS Section 109."
    },
    "375": {
        "title": "Rape (Definition)",
        "ipc": "Section 375 IPC",
        "bns": "Section 63 BNS",
        "punishment": "Punishment detailed in Section 64 BNS.",
        "notes": "BNS Section 69 also introduces a distinct offense for sexual intercourse on false promise of marriage or deceitful employment promises."
    },
    "376": {
        "title": "Punishment for Rape",
        "ipc": "Section 376 IPC",
        "bns": "Section 64 BNS",
        "punishment": "Rigorous imprisonment of not less than 10 years, extendable to life, and fine.",
        "notes": "Gang rape is penalized under Section 70 BNS (minimum 20 years or life imprisonment)."
    },
    "420": {
        "title": "Cheating and dishonestly inducing delivery of property",
        "ipc": "Section 420 IPC",
        "bns": "Section 318(4) BNS",
        "punishment": "Imprisonment up to 7 years and fine.",
        "notes": "Cheating is defined under Section 318(1), with aggravated fraud under Section 318(4)."
    },
    "406": {
        "title": "Criminal Breach of Trust",
        "ipc": "Section 406 IPC",
        "bns": "Section 316 BNS",
        "punishment": "Imprisonment up to 5 years or fine or both (increased from 3 years in IPC).",
        "notes": "Section 316(1) defines Criminal Breach of Trust; Section 316(2) provides general punishment."
    },
    "498a": {
        "title": "Cruelty by Husband or Relatives of Husband",
        "ipc": "Section 498A IPC",
        "bns": "Section 85 & 86 BNS",
        "punishment": "Imprisonment up to 3 years and fine.",
        "notes": "Section 85 prescribes punishment; Section 86 formally defines what acts constitute cruelty."
    },
    "506": {
        "title": "Criminal Intimidation",
        "ipc": "Section 506 IPC",
        "bns": "Section 351 BNS",
        "punishment": "Imprisonment up to 2 years, or fine, or both; if threat is of death/grievous hurt, up to 7 years.",
        "notes": "Section 351(1) defines; Section 351(2) & 351(3) specify penalty tiers."
    },
    "509": {
        "title": "Word, gesture or act intended to insult modesty of a woman",
        "ipc": "Section 509 IPC",
        "bns": "Section 79 BNS",
        "punishment": "Simple imprisonment up to 3 years and fine.",
        "notes": "Expanded scope under BNS to protect dignity of women."
    },
    "378": {
        "title": "Theft",
        "ipc": "Section 378 / 379 IPC",
        "bns": "Section 303 BNS",
        "punishment": "Imprisonment up to 3 years or fine or both; petty theft under BNS 303(2) may include community service.",
        "notes": "First introduction of 'Community Service' as an alternative punishment."
    },
    "124a": {
        "title": "Sedition (Repealed / Replaced)",
        "ipc": "Section 124A IPC",
        "bns": "Section 152 BNS",
        "punishment": "Imprisonment for life or up to 7 years and fine.",
        "notes": "The archaic term 'sedition' is dropped. Section 152 covers 'Act endangering sovereignty, unity and integrity of India'."
    }
}

# Key CrPC -> BNSS mappings
CRPC_TO_BNSS = {
    "154": {
        "title": "Information in cognizable cases (First Information Report - FIR)",
        "crpc": "Section 154 CrPC",
        "bnss": "Section 173 BNSS",
        "highlights": "Formally codifies e-FIR and Zero FIR. Electronic info must be signed within 3 days."
    },
    "41a": {
        "title": "Notice of appearance before police officer",
        "crpc": "Section 41A CrPC",
        "bnss": "Section 35(3) BNSS",
        "highlights": "Prior sanction of Deputy SP required before arresting elderly (60+) or infirm for offenses punishable by less than 3 years."
    },
    "164": {
        "title": "Recording of confessions and statements by Magistrate",
        "crpc": "Section 164 CrPC",
        "bnss": "Section 183 BNSS",
        "highlights": "Mandatory audio-video electronic recording permitted and encouraged."
    },
    "437": {
        "title": "Bail in non-bailable offenses",
        "crpc": "Section 437 / 436A CrPC",
        "bnss": "Section 479 BNSS",
        "highlights": "First-time offenders (undertrials) can be released on bail after serving 1/3rd of the maximum sentence (reduced from 1/2)."
    }
}

def lookup_penal_section(query_section: str) -> dict:
    """
    Looks up section mapping between IPC and BNS.
    Accepts inputs like '420', '302', '318', 'ipc 420', 'bns 103'.
    """
    clean = query_section.lower().replace("section", "").replace("sec", "").replace("ipc", "").replace("bns", "").strip()
    
    # Check direct IPC key
    if clean in IPC_TO_BNS:
        return IPC_TO_BNS[clean]
    
    # Check if query matches a BNS section number
    for ipc_key, data in IPC_TO_BNS.items():
        if clean in data["bns"].lower():
            return data
            
    # Check CrPC / BNSS
    if clean in CRPC_TO_BNSS:
        return CRPC_TO_BNSS[clean]
    for crpc_key, data in CRPC_TO_BNSS.items():
        if clean in data["bnss"].lower():
            return data

    return {}

