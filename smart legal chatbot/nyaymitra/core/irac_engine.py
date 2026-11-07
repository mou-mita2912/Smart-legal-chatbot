"""
IRAC (Issue, Rule, Application, Conclusion) Legal Reasoning Engine.
Performs rigorous statutory and case-law analysis on factual scenarios.
"""
from typing import Optional, Dict, Any
from nyaymitra.core.llm_client import GeminiClient
from nyaymitra.guardrails import post_process_response
from nyaymitra.knowledge.bns_ipc_mapping import lookup_penal_section
from nyaymitra.knowledge.indian_statutes import (
    CONSTITUTIONAL_RIGHTS, CONSUMER_PROTECTION_ACT_2019,
    RTI_ACT_2005, NI_ACT_SECTION_138
)
from nyaymitra.knowledge.foreign_jurisdictions import (
    UK_EMPLOYMENT_LAW, DELAWARE_COMMERCIAL_LAW
)

IRAC_PROMPT_TEMPLATE = """
Analyze the following factual scenario under {jurisdiction}:

Scenario:
\"\"\"{scenario}\"\"\"

Apply the legal IRAC framework to break down the situation strictly under the following four numbered headings:
1. Primary Legal Issues: Identify each discrete legal controversy and actionable cause of action.
2. Relevant Statutes and Precedent Cases: Cite specific applicable statutory provisions, bare acts, and authoritative landmark judicial rulings.
3. How the Law Applies to These Facts (Analysis):
   - Arguments & Strengths for Claimant / Moving Party / Prosecution
   - Arguments & Defences for Respondent / Defending Party
   - Evidentiary burdens and factual weaknesses
4. Recommended Next Steps or Preliminary Strategies: Actionable immediate steps, pre-action protocols (e.g. notices, conciliation), limitation periods, and document preservation.
"""

class IRACEngine:
    """Produces structured legal reasoning using the IRAC method."""

    def __init__(self, llm_client: Optional[GeminiClient] = None):
        self.llm = llm_client or GeminiClient()

    def analyze(self, scenario: str, jurisdiction: str = "Republic of India") -> str:
        """
        Executes an IRAC legal assessment.
        Uses Gemini LLM if available; otherwise uses domain-matched analytical fallback.
        """
        if not scenario or not scenario.strip():
            return "Please provide a factual scenario to analyze."

        # 1. Attempt LLM generation
        if self.llm.is_available():
            prompt = IRAC_PROMPT_TEMPLATE.format(
                jurisdiction=jurisdiction,
                scenario=scenario.strip()
            )
            response = self.llm.generate(prompt=prompt)
            if response:
                return post_process_response(response, jurisdiction=jurisdiction)

        # 2. Local Fallback Domain Engine
        return self._heuristic_irac(scenario, jurisdiction)

    def _heuristic_irac(self, scenario: str, jurisdiction: str) -> str:
        """Heuristic legal reasoning framework based on pattern recognition."""
        text = scenario.lower()
        lines = []

        is_uk_jur = any(k in jurisdiction.lower() for k in ["uk", "united kingdom", "england", "wales", "britain"])
        is_uk_emp = is_uk_jur or any(k in text for k in ["employment", "dismiss", "boss", "fired", "redundancy", "worker"])
        is_cheque = "cheque" in text or "check" in text or "bounce" in text or "dishonour" in text or "insufficient funds" in text
        is_consumer = "consumer" in text or "defective" in text or "refund" in text or "warranty" in text
        is_fraud = "fraud" in text or "cheated" in text or "scam" in text or "money" in text or "police" in text

        lines.append(f"### IRAC Legal Assessment")
        lines.append(f"**Target Jurisdiction:** {jurisdiction}")
        lines.append(f"**Factual Summary:** {scenario[:200]}..." if len(scenario) > 200 else f"**Factual Summary:** {scenario}")
        lines.append("")

        if is_uk_emp and is_uk_jur:
            # UK Employment Law IRAC
            lines.append("### 1. Primary Legal Issues")
            lines.append("- Whether the termination constitutes an **Unfair Dismissal** under Section 94 of the Employment Rights Act 1996 (ERA 1996).")
            lines.append("- Whether the employer's conduct amounted to a fundamental breach of the implied term of mutual trust and confidence (**Constructive Dismissal**).")
            lines.append("- Whether any adverse employment action was related to a protected characteristic under the **Equality Act 2010**.")

            lines.append("\n### 2. Relevant Statutes and Precedent Cases")
            lines.append("- **Statutes:** Employment Rights Act 1996 (Sections 94, 98), Equality Act 2010 (Sections 13, 19, 26, 27).")
            lines.append("- **Precedents:**")
            lines.append("  * *Western Excavating (ECC) Ltd v Sharp [1978]*: Test for constructive dismissal requiring fundamental breach going to the root of the contract.")
            lines.append("  * *Polkey v AE Dayton Services Ltd [1987]*: Procedural unfairness renders a dismissal unfair, even if fair dismissal would have occurred eventually (subject to Polkey deduction).")
            lines.append("  * *British Home Stores v Burchell [1978]*: Three-part test for genuine belief on reasonable grounds following a reasonable investigation.")

            lines.append("\n### 3. Application to Facts (Bilateral Analysis)")
            lines.append("**Claimant / Employee Strengths:**")
            lines.append("- Potential failure by employer to adhere to the ACAS Code of Practice on Disciplinary and Grievance Procedures (notice, hearing, right to representation).")
            lines.append("- Lack of documentary warnings or opportunity to improve before punitive sanction.")
            lines.append("\n**Respondent / Employer Defences:**")
            lines.append("- Employer may plead a potentially fair statutory reason under s.98 ERA (conduct, capability, or some other substantial reason).")
            lines.append("- If employee has under 2 years of continuous service, ordinary unfair dismissal protection may not apply (unless whistleblowing/discrimination exception applies).")
            lines.append("\n**Weaknesses & Evidentiary Gaps:**")
            lines.append("- Written notes of performance meetings, formal warning letters, and contemporaneous emails must be inspected.")

            lines.append("\n### 4. Recommended Next Steps & Preliminary Strategies")
            lines.append("1. **Submit Formal Written Grievance:** Invoke the employer's internal grievance mechanism immediately.")
            lines.append("2. **Initiate ACAS Early Conciliation:** Mandatory prerequisite before lodging an Employment Tribunal claim (notifies ACAS to explore settlement).")
            lines.append("3. **Monitor Statutory Limitation:** Employment Tribunal claim (Form ET1) must be submitted within **3 months minus one day** from the effective date of termination.")
            lines.append("4. **Preserve Documentation:** Secure copy of employment contract, employee handbook, payslips, and all correspondence.")

        elif is_cheque:
            # Cheque Bounce (Section 138 NI Act)
            lines.append("### 1. Primary Legal Issues")
            lines.append("- Whether the dishonour of the negotiable instrument constitutes a criminal offence under **Section 138 of the Negotiable Instruments Act, 1881**.")
            lines.append("- Whether the cheque was issued in discharge of an enforceable debt or legal liability.")
            lines.append("- Strict compliance with statutory notice periods and limitation.")

            lines.append("\n### 2. Relevant Statutes and Precedent Cases")
            lines.append("- **Statute:** Negotiable Instruments Act, 1881 (Sections 138, 139, 141, 142).")
            lines.append("- **Precedents:**")
            lines.append("  * *Rangappa v. Sri Mohan (2010) 11 SCC 441*: Supreme Court confirmed statutory presumption under Section 139 in favor of the holder.")
            lines.append("  * *Bir Singh v. Mukesh Kumar (2019) 4 SCC 197*: A signed blank cheque voluntarily handed over triggers Section 139 presumption once dishonoured.")

            lines.append("\n### 3. Application to Facts (Bilateral Analysis)")
            lines.append("**Complainant's Strengths:**")
            lines.append("- Legal presumption under Sections 118 and 139 of the NI Act presumes the cheque was issued for valid consideration.")
            lines.append("- Strict liability offence once statutory notice is delivered and unpaid.")
            lines.append("\n**Accused's Potential Defences:**")
            lines.append("- Rebutting the presumption by demonstrating the cheque was security-only without an existing crystallised debt.")
            lines.append("- Procedural defects: Delay in serving legal notice beyond 30 days of receiving bank memo.")

            lines.append("\n### 4. Recommended Next Steps & Preliminary Strategies")
            lines.append("1. **Issue Statutory Demand Notice:** Must be dispatched via Registered Post A.D. within **30 days** of receiving the bank dishonour memo.")
            lines.append("2. **Wait 15-Day Cure Period:** Accused has 15 calendar days from the date of receipt to make payment.")
            lines.append("3. **File Criminal Complaint:** If payment is not made, file complaint before the Judicial Magistrate within **1 month** of the expiry of the 15 days.")

        else:
            # General / Indian Criminal & Civil Framework
            lines.append("### 1. Primary Legal Issues")
            lines.append("- Identification of actionable civil wrongs (breach of contract, negligence, deficiency of service) or cognizable criminal offences.")
            lines.append("- Determination of forum jurisdiction, standing (locus standi), and accrual of cause of action.")

            lines.append("\n### 2. Relevant Statutes and Precedent Cases")
            lines.append("- **Statutory Provisions:** Indian Contract Act 1872 / Bharatiya Nyaya Sanhita 2023 (BNS) / Consumer Protection Act 2019.")
            lines.append("- **Guiding Principles:** Doctrine of privity, standard of reasonable care, and burden of proof under Bharatiya Sakshya Adhiniyam 2023 (BSA).")

            lines.append("\n### 3. Application to Facts (Bilateral Analysis)")
            lines.append("**Claimant / Aggrieved Party Case:**")
            lines.append("- Elements of breach or wrongful act can be established through contemporaneous communications and documentary trail.")
            lines.append("\n**Counterparty / Defending Position:**")
            lines.append("- Defences of contractual limitation, lack of notice, waiver, or absence of proximate causal damage.")
            lines.append("\n**Evidentiary Scrutiny:**")
            lines.append("- Admissibility of electronic records requires compliance with Section 63 BSA (formerly Section 65B Indian Evidence Act).")

            lines.append("\n### 4. Recommended Next Steps & Preliminary Strategies")
            lines.append("1. **Send Formal Pre-Action Legal Notice:** Detail specific claims and set a 15-to-30 day deadline for response or cure.")
            lines.append("2. **Collate & Preserve Evidence:** Audit contracts, invoices, electronic messages, and financial ledgers.")
            lines.append("3. **Engage Legal Counsel:** Consult a licensed advocate to formalize proceedings before the appropriate forum.")

        return post_process_response("\n".join(lines), jurisdiction=jurisdiction)
