"""
Contract & Clause Risk Analysis Engine.
Performs executive summarization, high-risk clause identification (indemnity, liability,
termination, non-compete), ambiguity detection, and markup/redline suggestions.
"""
import re
from typing import Optional, Dict, Any
from nyaymitra.core.llm_client import GeminiClient
from nyaymitra.guardrails import post_process_response

CONTRACT_PROMPT_TEMPLATE = """
Review the following contract/agreement/clause under {jurisdiction}:

```text
{contract_text}
```

Party Stance / Role: {party_role}

Please perform a comprehensive risk analysis formatted strictly under these four sections:
1. Executive Summary: High-level purpose, commercial intent, and key obligations.
2. High-Risk Clauses: Highlight indemnification, liability caps, termination rights, or non-competes that favor the counterparty or create disproportionate exposure.
3. Ambiguities & Red Flags: Terms that are overly vague, one-sided, or missing essential definitions/carve-outs.
4. Suggested Revisions: Provide specific markup/redline suggestions (using `[bracketed additions]` and ~~strikethroughs~~) with balanced redrafted wording for each identified risky clause.
"""

class ContractAnalyzer:
    """Analyzes contracts and specific clauses for legal and commercial risks."""

    def __init__(self, llm_client: Optional[GeminiClient] = None):
        self.llm = llm_client or GeminiClient()

    def analyze(
        self,
        contract_text: str,
        jurisdiction: str = "Republic of India",
        party_role: str = "Client / Reviewing Party"
    ) -> str:
        """
        Executes a 4-part legal risk analysis.
        Uses Gemini API if online, or local heuristic analysis engine if offline.
        """
        if not contract_text or not contract_text.strip():
            return "Please provide the text of the contract, agreement, or clause to analyze."

        # 1. Attempt LLM Analysis if available
        if self.llm.is_available():
            prompt = CONTRACT_PROMPT_TEMPLATE.format(
                jurisdiction=jurisdiction,
                contract_text=contract_text.strip(),
                party_role=party_role
            )
            response = self.llm.generate(prompt=prompt)
            if response:
                return post_process_response(response, jurisdiction=jurisdiction)

        # 2. Local Fallback Heuristic Legal Risk Engine
        return self._heuristic_analysis(contract_text, jurisdiction, party_role)

    def _heuristic_analysis(self, text: str, jurisdiction: str, party_role: str) -> str:
        """Rule-based legal risk assessment engine."""
        lower_text = text.lower()
        findings = []
        redflags = []
        revisions = []

        # Check Indemnification
        if "indemnif" in lower_text or "hold harmless" in lower_text or "defend" in lower_text:
            is_unilateral = ("party a shall indemnify" in lower_text or "you agree to indemnify" in lower_text) and not ("mutual" in lower_text or "each party shall indemnify" in lower_text)
            has_defense = "defend" in lower_text
            findings.append({
                "clause": "Indemnification & Defense",
                "risk_level": "CRITICAL" if is_unilateral else "MODERATE",
                "concern": "Broad or unilateral indemnity obligation. The inclusion of 'defend' requires paying legal fees upfront before liability is adjudicated.",
                "remedy": "Make indemnity bilateral, add standard carve-outs (counterparty gross negligence, willful misconduct, breach), and limit defense to final non-appealable judgments."
            })
            revisions.append(
                "**Indemnification Redline:**\n"
                "> Each Party (the 'Indemnifying Party') shall indemnify, ~~defend~~ and hold harmless the other Party "
                "from and against direct third-party damages `[excluding indirect or consequential losses]`, "
                "`[except to the extent caused by the gross negligence or willful misconduct of the indemnified party]`."
            )

        # Check Limitation of Liability
        if "limitation of liability" in lower_text or "liability shall not exceed" in lower_text or "consequential damages" in lower_text:
            findings.append({
                "clause": "Limitation of Liability & Damage Waivers",
                "risk_level": "HIGH",
                "concern": "Exclusion of consequential/indirect damages may bar recovery for legitimate business disruption or data breaches unless mutual caps and explicit carve-outs are specified.",
                "remedy": "Cap aggregate liability to fees paid during the preceding 6 or 12 months, and establish symmetric reciprocal exceptions for confidentiality breaches and indemnification."
            })
            revisions.append(
                "**Limitation of Liability Redline:**\n"
                "> In no event shall either party's aggregate liability under this Agreement exceed "
                "`[the total fees paid or payable by Client in the preceding twelve (12) months]`~~an amount of zero~~."
            )
        elif "unlimited" in lower_text or "no cap" in lower_text:
            findings.append({
                "clause": "Uncapped Liability Exposure",
                "risk_level": "SEVERE",
                "concern": "Contract contains uncapped monetary liability, exposing assets to catastrophic damage awards.",
                "remedy": "Insist on a hard monetary aggregate cap (e.g., 1x or 2x contract value)."
            })

        # Check Termination
        if "termination" in lower_text or "terminate" in lower_text:
            if "convenience" in lower_text:
                findings.append({
                    "clause": "Termination for Convenience",
                    "risk_level": "HIGH",
                    "concern": "Allows unilateral termination without cause, risking sunk mobilization costs and revenue instability.",
                    "remedy": "Require a minimum 60-day advance notice period and payment for all completed work or non-cancelable commitments."
                })
            if "cure" not in lower_text and "remedy" not in lower_text:
                redflags.append("Missing notice-and-cure period (standard is 30 calendar days) before termination for material breach can be triggered.")

        # Check Non-Compete / Restrictive Covenants
        if any(w in lower_text for w in ["non-compete", "not compete", "not to compete", "compete", "restraint", "restrict"]):
            is_india = "india" in jurisdiction.lower()
            if is_india:
                findings.append({
                    "clause": "Post-Termination Non-Compete (Indian Law)",
                    "risk_level": "HIGH / VOID RISK",
                    "concern": "Under Section 27 of the Indian Contract Act, 1872, agreements in restraint of lawful profession or trade are void ab initio post-employment/termination (Percept D'Mark v. Zaheer Khan).",
                    "remedy": "Convert to reasonable non-solicitation of clients/employees and strict confidentiality covenants instead of a blanket non-compete."
                })
            else:
                findings.append({
                    "clause": "Non-Compete Restrictive Covenant",
                    "risk_level": "HIGH",
                    "concern": "Examine scope for temporal length (exceeding 12 months is frequently scrutinized) and lack of geographic limitation.",
                    "remedy": "Narrow geography to actual client operating territories and duration to 6–12 months maximum."
                })

        # Check Vague Terms & Red Flags
        if "sole discretion" in lower_text:
            redflags.append("Use of 'sole discretion' allows arbitrary counterparty decisions; replace with 'reasonable discretion' or objective benchmarks.")
        if "material breach" in lower_text and "defined" not in lower_text:
            redflags.append("'Material breach' is invoked without an express definition, leaving contract termination vulnerable to dispute.")
        if "best efforts" in lower_text:
            redflags.append("'Best efforts' sets a potentially burdensome legal standard; prefer 'commercially reasonable efforts'.")

        # Compile structured output
        out = []
        out.append("### 1. Executive Summary")
        out.append(f"**Target Jurisdiction:** {jurisdiction}")
        out.append(f"**Reviewing Perspective:** {party_role}")
        out.append("This agreement establishes commercial terms and legal obligations between the contracting parties. Key operative mechanisms involve performance deliverables, risk allocations, restrictive covenants, and dispute procedures. The primary legal objective is to ensure mutuality of obligations and prevent disproportionate unilateral liability.")
        
        out.append("\n### 2. High-Risk Clauses Matrix")
        if findings:
            for f in findings:
                out.append(f"- **{f['clause']}** `[Risk: {f['risk_level']}]`")
                out.append(f"  * **Exposure:** {f['concern']}")
                out.append(f"  * **Recommendation:** {f['remedy']}")
        else:
            out.append("- *No overt high-risk triggers detected in the provided snippet. However, standard review for liability caps, indemnity, and termination reciprocity is strongly advised.*")

        out.append("\n### 3. Ambiguities & Red Flags")
        if redflags:
            for rf in redflags:
                out.append(f"- ⚠️ **Red Flag:** {rf}")
        else:
            out.append("- Ensure all capitalized defined terms (e.g., 'Confidential Information', 'Effective Date', 'Services') have precise, unambiguous definitions.")
            out.append("- Verify that statutory dispute resolution, governing law, and exclusive venue clauses are unequivocally identified.")

        out.append("\n### 4. Suggested Revisions (Redline & Markups)")
        if revisions:
            for rev in revisions:
                out.append(rev)
                out.append("")
        else:
            out.append("```diff\n- Counterparty shall have sole discretion to terminate this Agreement immediately upon written notice.\n+ Either party may terminate this Agreement for material breach upon thirty (30) days' prior written notice, provided such breach remains uncured during the notice period.\n```")

        return post_process_response("\n".join(out), jurisdiction=jurisdiction)
