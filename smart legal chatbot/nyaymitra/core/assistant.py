"""
Main NyayMitra Legal Assistant Orchestrator.
Coordinates conversational queries, IPC/BNS conversions, procedural guides,
contract reviews, IRAC analyses, and document drafting while enforcing guardrails.
"""
import re
from typing import List, Dict, Optional, Any

from nyaymitra.config import DEFAULT_JURISDICTION
from nyaymitra.guardrails import post_process_response
from nyaymitra.core.llm_client import GeminiClient
from nyaymitra.core.contract_analyzer import ContractAnalyzer
from nyaymitra.core.irac_engine import IRACEngine
from nyaymitra.core.document_drafter import DocumentDrafter
from nyaymitra.knowledge.bns_ipc_mapping import lookup_penal_section, IPC_TO_BNS, CRPC_TO_BNSS
from nyaymitra.knowledge.indian_statutes import (
    CONSTITUTIONAL_RIGHTS, CONSUMER_PROTECTION_ACT_2019,
    RTI_ACT_2005, NI_ACT_SECTION_138
)
from nyaymitra.knowledge.procedures import PROCEDURAL_GUIDES

class NyayMitraAssistant:
    """The central conversational and reasoning legal assistant."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.llm = GeminiClient(api_key=api_key, model=model)
        self.contract_analyzer = ContractAnalyzer(llm_client=self.llm)
        self.irac_engine = IRACEngine(llm_client=self.llm)
        self.document_drafter = DocumentDrafter(llm_client=self.llm)
        self.history: List[Dict[str, str]] = []

    def set_api_key(self, api_key: str):
        """Dynamically update the Gemini API key."""
        self.llm = GeminiClient(api_key=api_key)
        self.contract_analyzer = ContractAnalyzer(llm_client=self.llm)
        self.irac_engine = IRACEngine(llm_client=self.llm)
        self.document_drafter = DocumentDrafter(llm_client=self.llm)

    def process_query(self, query: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
        """
        Main query router: routes to appropriate engine, formats, and applies safety guardrails.
        """
        if not query or not query.strip():
            return "Please enter a legal query, scenario, or document drafting request."

        clean_query = query.strip()
        lower_q = clean_query.lower()

        # 1. Check for specific Section Lookup (IPC / BNS / CrPC / BNSS)
        sec_match = re.search(r"\b(?:section|sec\.?)\s*(\d+[a-zA-Z]?)\b", lower_q) or re.search(r"\b(?:ipc|bns|crpc|bnss)\s*(\d+[a-zA-Z]?)\b", lower_q)
        if sec_match and ("bns" in lower_q or "ipc" in lower_q or "crpc" in lower_q or "bnss" in lower_q or "section" in lower_q):
            sec_num = sec_match.group(1)
            mapping_result = lookup_penal_section(sec_num)
            if mapping_result:
                resp = self._format_section_lookup(mapping_result, sec_num)
                self.history.append({"role": "user", "content": clean_query})
                self.history.append({"role": "assistant", "content": resp})
                return resp

        # 2. Check for Procedural Guide requests
        if "how to" in lower_q or "procedure" in lower_q or "steps to" in lower_q or "process to" in lower_q:
            if "rti" in lower_q or "right to information" in lower_q:
                return self._format_procedure("rti", jurisdiction)
            elif "fir" in lower_q or "police complaint" in lower_q:
                return self._format_procedure("fir", jurisdiction)
            elif "consumer" in lower_q or "consumer court" in lower_q or "consumer forum" in lower_q:
                return self._format_procedure("consumer_complaint", jurisdiction)
            elif "cyber" in lower_q or "online fraud" in lower_q or "1930" in lower_q:
                return self._format_procedure("cybercrime", jurisdiction)

        # 3. Check for Contract Risk Review intent
        if ("review" in lower_q or "risk analysis" in lower_q or "clause" in lower_q) and ("contract" in lower_q or "agreement" in lower_q or "indemnif" in lower_q or "liability" in lower_q):
            resp = self.contract_analyzer.analyze(clean_query, jurisdiction=jurisdiction)
            self.history.append({"role": "user", "content": clean_query})
            self.history.append({"role": "assistant", "content": resp})
            return resp

        # 4. Check for IRAC Framework intent
        if "irac" in lower_q or ("factual scenario" in lower_q and "issue" in lower_q):
            resp = self.irac_engine.analyze(clean_query, jurisdiction=jurisdiction)
            self.history.append({"role": "user", "content": clean_query})
            self.history.append({"role": "assistant", "content": resp})
            return resp

        # 5. Check for Document Drafting intent
        if "draft" in lower_q or "template" in lower_q or "letter" in lower_q or "agreement" in lower_q or "notice" in lower_q:
            if any(term in lower_q for term in ["cease", "desist", "nda", "settlement", "cheque", "138", "rent", "lease", "consumer"]):
                doc_type = "Legal Document"
                if "cease" in lower_q: doc_type = "Cease and Desist Letter"
                elif "nda" in lower_q or "non-disclosure" in lower_q: doc_type = "Mutual Non-Disclosure Agreement"
                elif "settle" in lower_q: doc_type = "Settlement and Release Agreement"
                elif "138" in lower_q or "cheque" in lower_q: doc_type = "Section 138 NI Act Legal Notice"
                elif "rent" in lower_q or "lease" in lower_q: doc_type = "Residential Rent Agreement"
                elif "consumer" in lower_q: doc_type = "Consumer Dispute Petition"
                
                resp = self.document_drafter.draft(doc_type=doc_type, governing_law=jurisdiction)
                self.history.append({"role": "user", "content": clean_query})
                self.history.append({"role": "assistant", "content": resp})
                return resp

        # 6. Fallback to LLM if online
        if self.llm.is_available():
            llm_resp = self.llm.generate(prompt=clean_query, history=self.history[-6:])
            if llm_resp:
                final_resp = post_process_response(llm_resp, jurisdiction=jurisdiction)
                self.history.append({"role": "user", "content": clean_query})
                self.history.append({"role": "assistant", "content": final_resp})
                return final_resp

        # 7. Knowledge-Base matching fallback
        response = self._knowledge_match(clean_query, jurisdiction)
        self.history.append({"role": "user", "content": clean_query})
        self.history.append({"role": "assistant", "content": response})
        return response

    def _format_section_lookup(self, data: dict, query_sec: str) -> str:
        """Formats statutory section transition cards."""
        out = []
        out.append(f"### Statutory Cross-Reference: {data.get('title', 'Offence')}")
        if "ipc" in data and "bns" in data:
            out.append(f"- **Indian Penal Code (IPC 1860):** `{data['ipc']}`")
            out.append(f"- **Bharatiya Nyaya Sanhita (BNS 2023):** `{data['bns']}`")
            out.append(f"- **Prescribed Penalty:** {data.get('punishment', 'As prescribed by law.')}")
            if "notes" in data:
                out.append(f"- **Key Legal Reform:** {data['notes']}")
        elif "crpc" in data and "bnss" in data:
            out.append(f"- **Code of Criminal Procedure (CrPC 1973):** `{data['crpc']}`")
            out.append(f"- **Bharatiya Nagarik Suraksha Sanhita (BNSS 2023):** `{data['bnss']}`")
            if "highlights" in data:
                out.append(f"- **Key Procedure:** {data['highlights']}")
        return post_process_response("\n".join(out), jurisdiction="Republic of India")

    def _format_procedure(self, proc_key: str, jurisdiction: str) -> str:
        """Retrieves and formats procedural checklists."""
        guide = PROCEDURAL_GUIDES.get(proc_key)
        if not guide:
            return post_process_response("Procedure information not found.", jurisdiction=jurisdiction)

        out = []
        out.append(f"### {guide['title']}")
        out.append(f"**Governing Law:** {guide['governing_law']}\n")
        out.append("Follow these chronological steps:")
        for s in guide["steps"]:
            out.append(f"**Step {s['step']}: {s['title']}**")
            out.append(f"{s['details']}\n")
        return post_process_response("\n".join(out), jurisdiction=jurisdiction)

    def _knowledge_match(self, query: str, jurisdiction: str) -> str:
        """Matches against core constitutional, consumer, or RTI concepts."""
        lower = query.lower()
        out = []

        if "article 21" in lower or "right to life" in lower or "privacy" in lower:
            info = CONSTITUTIONAL_RIGHTS["article_21"]
            out.append(f"### Constitutional Law: {info['title']} ({info['article']})")
            out.append(f"{info['summary']}\n")
            out.append("**Key Landmark Precedents:**")
            for c in info["landmark_cases"]:
                out.append(f"- *{c}*")
        elif "article 14" in lower or "equality" in lower:
            info = CONSTITUTIONAL_RIGHTS["article_14"]
            out.append(f"### Constitutional Law: {info['title']} ({info['article']})")
            out.append(f"{info['summary']}\n")
            out.append("**Key Landmark Precedents:**")
            for c in info["landmark_cases"]:
                out.append(f"- *{c}*")
        elif "cheque" in lower or "bounce" in lower or "138" in lower:
            info = NI_ACT_SECTION_138
            out.append(f"### Negotiable Instruments Act, 1881 - Section 138 (Cheque Dishonour)")
            out.append(f"**Offence:** {info['offense']}")
            out.append("\n**Mandatory Statutory Prerequisites:**")
            for req in info["mandatory_prerequisites"]:
                out.append(f"- {req}")
            out.append(f"\n**Penalties:** {info['penalties']}")
        elif "consumer" in lower:
            cpa = CONSUMER_PROTECTION_ACT_2019
            out.append("### Consumer Protection Act, 2019 (Pecuniary Jurisdiction & Rights)")
            out.append("**Pecuniary Tiers (Revised 2021 Rules):**")
            for forum, cap in cpa["pecuniary_jurisdiction"].items():
                out.append(f"- **{forum}:** {cap}")
            out.append("\n**Key Rights & Mechanisms:**")
            for prov, desc in cpa["key_provisions"].items():
                out.append(f"- **{prov}:** {desc}")
        else:
            out.append(f"### Legal Information Request")
            out.append(f"Thank you for your inquiry regarding: *{query}*.")
            out.append("\nTo give you the most accurate legal guidance, please consider:")
            out.append("1. **Specific Facts:** Describe the relevant dates, parties, and actions taken.")
            out.append("2. **Specific Tool:** You can use our specialized tabs for **Contract Risk Review**, **IRAC Case Analysis**, **Document Drafting**, or **Procedural Guides**.")
            out.append("3. **Jurisdiction:** Active jurisdiction is set to `" + jurisdiction + "`.")

        return post_process_response("\n".join(out), jurisdiction=jurisdiction)

