"""
Statutory reference database for Indian Core Statutes:
Constitution, Consumer Protection Act 2019, RTI Act 2005, NI Act 1881, IT Act 2000, and POSH Act 2013.
"""

CONSTITUTIONAL_RIGHTS = {
    "article_14": {
        "article": "Article 14",
        "title": "Equality Before Law & Equal Protection of Laws",
        "summary": "Prohibits arbitrary state actions, guarantees non-discrimination, and ensures equal treatment for similarly situated individuals.",
        "landmark_cases": ["E.P. Royappa v. State of Tamil Nadu (1974) - Arbitrariness is antithetical to equality", "Maneka Gandhi v. Union of India (1978)"]
    },
    "article_19": {
        "article": "Article 19",
        "title": "Six Fundamental Freedoms",
        "summary": "Guarantees freedom of speech and expression (19(1)(a)), assembly (19(1)(b)), association (19(1)(c)), movement (19(1)(d)), residence (19(1)(e)), and trade/profession (19(1)(g)), subject to reasonable restrictions under Articles 19(2) to 19(6).",
        "landmark_cases": ["Shreya Singhal v. Union of India (2015) - Struck down Section 66A of the IT Act for chilling online free speech"]
    },
    "article_21": {
        "article": "Article 21",
        "title": "Protection of Life and Personal Liberty",
        "summary": "No person shall be deprived of life or personal liberty except according to procedure established by law. Expansively interpreted to include the right to privacy, clean environment, speedy trial, dignity, and livelihood.",
        "landmark_cases": [
            "Maneka Gandhi v. Union of India (1978) - Procedure must be just, fair, and reasonable",
            "K.S. Puttaswamy v. Union of India (2017) - Unanimously declared Right to Privacy as a fundamental right under Article 21",
            "Olga Tellis v. Bombay Municipal Corp. (1985) - Right to livelihood is part of life"
        ]
    },
    "article_22": {
        "article": "Article 22",
        "title": "Protection against Arrest and Detention",
        "summary": "Guarantees the right to be informed of the grounds of arrest, the right to consult and be defended by a legal practitioner, and the obligation to produce the arrested person before a Magistrate within 24 hours.",
        "landmark_cases": ["D.K. Basu v. State of West Bengal (1997) - Comprehensive guidelines against custodial violence and for arrest procedures"]
    },
    "article_32_226": {
        "article": "Articles 32 & 226",
        "title": "Constitutional Remedies & Prerogative Writs",
        "summary": "Article 32 allows citizens to approach the Supreme Court directly for Fundamental Rights enforcement ('Heart and Soul of the Constitution'). Article 226 empowers High Courts to issue writs for both Fundamental Rights and any other legal right.",
        "writs": ["Habeas Corpus (unlawful detention)", "Mandamus (compelling public duty)", "Certiorari (quashing lower tribunal orders)", "Prohibition (restraining lower courts)", "Quo Warranto (challenging public office entitlement)"]
    }
}

CONSUMER_PROTECTION_ACT_2019 = {
    "pecuniary_jurisdiction": {
        "District Consumer Commission": "Claims up to INR 50 Lakhs (revised under 2021 Rules).",
        "State Consumer Commission": "Claims exceeding INR 50 Lakhs up to INR 2 Crores.",
        "National Commission (NCDRC)": "Claims exceeding INR 2 Crores."
    },
    "key_provisions": {
        "Section 2(7)": "Defines 'Consumer' - includes buyers of goods and hirers of services for personal use; excludes commercial resale.",
        "Section 2(10)": "Defect in goods (fault, imperfection, or shortcoming in quality, quantity, or purity).",
        "Section 2(11)": "Deficiency in service (fault, imperfection, shortcoming, or inadequacy in performance quality).",
        "Section 2(47)": "Unfair Trade Practice (deceptive advertising, misleading discounts, non-issuance of bill/cash memo).",
        "Product Liability": "Sections 82-87 hold manufacturers, service providers, and product sellers liable for harm caused by defective products.",
        "e-Filing": "Consumers can file complaints digitally through the e-Daakhil portal (edaakhil.nic.in) from any location."
    }
}

RTI_ACT_2005 = {
    "filing": "Section 6 allows any Indian citizen to submit a written or electronic request to the Public Information Officer (PIO).",
    "timeline": {
        "Standard Request": "Information must be supplied within 30 calendar days (Section 7(1)).",
        "Life & Liberty": "Must be provided within 48 hours if concerning life or liberty of an individual.",
        "Third Party Info": "40 days if third-party disclosure procedure under Section 11 is triggered."
    },
    "appeals": {
        "First Appeal (Section 19(1))": "To be filed within 30 days of receiving no reply or rejection, to the designated First Appellate Authority (FAA) within the same department.",
        "Second Appeal (Section 19(3))": "To be filed within 90 days to the Central Information Commission (CIC) or State Information Commission (SIC)."
    },
    "exemptions": "Section 8(1) lists 10 exemptions including national sovereignty/security (8(1)(a)), contempt of court (8(1)(b)), commercial confidence/trade secrets (8(1)(d)), fiduciary capacity (8(1)(e)), and personal privacy with no public interest (8(1)(j))."
}

NI_ACT_SECTION_138 = {
    "offense": "Dishonour of Cheque for insufficiency of funds or exceeding arrangements.",
    "mandatory_prerequisites": [
        "1. Cheque must be presented within its validity period (usually 3 months).",
        "2. Bank Return Memo received confirming dishonour ('Funds Insufficient', 'Account Closed', 'Stop Payment').",
        "3. Statutory Demand Notice sent in writing within 30 calendar days of receiving the return memo.",
        "4. Drawee fails to make payment within 15 calendar days from the date of receipt of the legal notice.",
        "5. Criminal complaint must be filed before the Judicial Magistrate / Metropolitan Magistrate within 1 month from the expiry of the 15-day notice period."
    ],
    "penalties": "Imprisonment up to 2 years, or fine up to twice the cheque amount, or both."
}

