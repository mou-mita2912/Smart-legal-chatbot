"""
Safety guardrails and compliance filters for NyayMitra.
Enforces jurisdiction declaration, disclaimer mandate, outcome-guarantee prohibition,
and hallucination mitigation.
"""
import re
from typing import Optional
from nyaymitra.config import MANDATORY_DISCLAIMER, UNVERIFIED_SECTION_STATEMENT, DEFAULT_JURISDICTION

OUTCOME_GUARANTEE_PATTERNS = [
    r"\byou will (?:definitely|certainly|guaranteed to) win\b",
    r"\bguarantee(?:d)? (?:outcome|success|verdict|ruling)\b",
    r"\bthe court will (?:definitely|certainly) (?:rule|order|grant)\b",
    r"\b100% (?:guarantee|success|chance of winning)\b",
    r"\byou are guaranteed\b",
]

def contains_disclaimer(text: str) -> bool:
    """Checks whether text contains the core disclaimer phrasing."""
    key_phrase = "does not constitute formal legal advice"
    return key_phrase.lower() in text.lower()

def enforce_disclaimer(text: str, position: str = "end") -> str:
    """
    Ensures the response includes the mandatory legal disclaimer.
    Attaches it to the start or end if missing.
    """
    if contains_disclaimer(text):
        return text

    disclaimer_block = f"\n\n---\n> **Disclaimer:** {MANDATORY_DISCLAIMER}"
    if position == "start":
        return f"> **Disclaimer:** {MANDATORY_DISCLAIMER}\n\n---\n\n{text}"
    return f"{text}{disclaimer_block}"

def enforce_jurisdiction(text: str, jurisdiction: Optional[str] = None) -> str:
    """
    Ensures the response explicitly states the active legal jurisdiction.
    """
    effective_jurisdiction = jurisdiction or DEFAULT_JURISDICTION
    
    # Check if jurisdiction is already explicitly declared
    if "jurisdiction:" in text.lower() or f"governing law: {effective_jurisdiction.lower()}" in text.lower():
        return text
    
    header = f"**Jurisdiction:** {effective_jurisdiction}\n\n"
    return header + text

def sanitize_outcome_guarantees(text: str) -> str:
    """
    Detects and softens unauthorized practice of law or outcome guarantees.
    """
    sanitized = text
    for pattern in OUTCOME_GUARANTEE_PATTERNS:
        replacement = "there is a legal basis to argue this, though outcomes depend on judicial discretion and evidence"
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
    return sanitized

def verify_section_citation(section_str: str, known_sections: dict) -> str:
    """
    Verifies a statutory section against known bare acts database.
    If uncertain, returns safety statement.
    """
    clean_sec = section_str.strip().lower()
    if clean_sec in known_sections:
        return known_sections[clean_sec]
    return UNVERIFIED_SECTION_STATEMENT

def post_process_response(text: str, jurisdiction: Optional[str] = None) -> str:
    """
    Complete guardrail pipeline applied to all agent outputs.
    """
    cleaned = sanitize_outcome_guarantees(text)
    with_jurisdiction = enforce_jurisdiction(cleaned, jurisdiction)
    final_output = enforce_disclaimer(with_jurisdiction, position="end")
    return final_output

