"""
Foreign and comparative legal frameworks:
UK Employment Law and US / Delaware Contract & Commercial Law.
"""

UK_EMPLOYMENT_LAW = {
    "jurisdiction": "United Kingdom (England and Wales)",
    "statutes": [
        "Employment Rights Act 1996 (ERA 1996)",
        "Equality Act 2010 (EqA 2010)",
        "Trade Union and Labour Relations (Consolidation) Act 1992",
        "National Minimum Wage Act 1998"
    ],
    "key_principles": {
        "unfair_dismissal": {
            "statutory_basis": "Section 94 ERA 1996",
            "qualifying_period": "Generally 2 years of continuous service (subject to automatically unfair exceptions such as whistleblowing or health and safety).",
            "potentially_fair_reasons": ["Conduct", "Capability or qualifications", "Redundancy", "Statutory illegality", "Some other substantial reason (SOSR)"],
            "procedure": "Employer must follow a fair procedure compliant with the ACAS Code of Practice on Disciplinary and Grievance Procedures."
        },
        "constructive_dismissal": {
            "doctrine": "Western Excavating (ECC) Ltd v Sharp [1978] - Requires a fundamental breach of contract going to the root of the employment relationship (e.g. breach of implied term of trust and confidence), resignation in response, and no excessive delay."
        },
        "discrimination": {
            "statutory_basis": "Equality Act 2010",
            "protected_characteristics": ["Age", "Disability", "Gender reassignment", "Marriage and civil partnership", "Pregnancy and maternity", "Race", "Religion or belief", "Sex", "Sexual orientation"],
            "remedies": "Uncapped compensatory awards for injury to feelings and financial loss."
        },
        "dispute_resolution": "Mandatory ACAS Early Conciliation is required before lodging an Employment Tribunal claim. Strict 3-month limitation period (less one day) from the effective date of termination or discriminatory act."
    }
}

DELAWARE_COMMERCIAL_LAW = {
    "jurisdiction": "State of Delaware (USA)",
    "statutes": [
        "Delaware General Corporation Law (DGCL)",
        "Delaware Uniform Commercial Code (UCC Title 6)",
        "Delaware Limited Liability Company Act (6 Del. C. § 18-101 et seq.)"
    ],
    "key_principles": {
        "freedom_of_contract": "Delaware courts strongly uphold party autonomy and the literal enforceability of sophisticated commercial contracts.",
        "implied_covenant": "The Implied Covenant of Good Faith and Fair Dealing is recognized by Delaware courts, but applied narrowly only to fill unanticipated contractual gaps; it cannot override express contractual terms.",
        "limitation_of_liability": "Delaware generally enforces limitation of liability clauses and consequential damage waivers between commercial parties, absent fraud or intentional torts.",
        "indemnification": "Delaware permits broad contractual indemnification provisions, including defense obligations and fee-shifting, provided the scope is clear.",
        "restrictive_covenants": "Delaware Court of Chancery scrutinizes non-compete agreements strictly for reasonableness in geographic scope, duration, and legitimate protectable business interest; overly broad covenants risk being invalidated rather than 'blue-penciled'."
    }
}

