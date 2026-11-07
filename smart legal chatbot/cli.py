"""
Interactive Command-Line Interface (CLI) for NyayMitra.
Enables full terminal access to legal queries, contract reviews, IRAC analysis,
statutory section conversions, and document drafting.
"""
import sys
from nyaymitra.config import DEFAULT_JURISDICTION, APP_NAME
from nyaymitra.core.assistant import NyayMitraAssistant
from nyaymitra.knowledge.bns_ipc_mapping import lookup_penal_section
from nyaymitra.knowledge.procedures import PROCEDURAL_GUIDES

def print_banner():
    print("=" * 68)
    print(f"  ⚖️  {APP_NAME} - Smart Legal Chatbot & Virtual Legal Assistant")
    print("=" * 68)
    print("  Type any legal query, or use these commands:")
    print("    /bns <sec>       - Cross-reference IPC <-> BNS or CrPC <-> BNSS")
    print("    /contract        - Interactive Contract Risk Analysis")
    print("    /irac            - IRAC Factual Case Analysis")
    print("    /draft           - Legal Document Drafting Wizard")
    print("    /procedure <id>  - Procedural guide (rti, fir, consumer, cybercrime)")
    print("    /jurisdiction    - View or change current jurisdiction")
    print("    /help            - Show this menu")
    print("    quit / exit      - Exit the assistant")
    print("=" * 68)

def main():
    assistant = NyayMitraAssistant()
    active_jurisdiction = DEFAULT_JURISDICTION
    print_banner()

    while True:
        try:
            user_input = input(f"\n[{active_jurisdiction}] NyayMitra > ").strip()
            if not user_input:
                continue

            cmd_lower = user_input.lower()
            if cmd_lower in ["exit", "quit", "q"]:
                print("\nExiting NyayMitra. May justice prevail.")
                break

            elif cmd_lower in ["/help", "help"]:
                print_banner()

            elif cmd_lower.startswith("/jurisdiction"):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    active_jurisdiction = parts[1].strip()
                    print(f"-> Active jurisdiction set to: {active_jurisdiction}")
                else:
                    print(f"-> Current active jurisdiction: {active_jurisdiction}")

            elif cmd_lower.startswith("/bns"):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    res = lookup_penal_section(parts[1])
                    if res:
                        print(assistant._format_section_lookup(res, parts[1]))
                    else:
                        print(f"No direct mapping found for '{parts[1]}'. I cannot verify the exact section for this specific scenario; please consult legal counsel.")
                else:
                    print("Usage: /bns <section_number_or_keyword> (e.g. /bns 420, /bns 302, /bns FIR)")

            elif cmd_lower.startswith("/procedure"):
                parts = user_input.split(maxsplit=1)
                proc_key = parts[1].strip() if len(parts) > 1 else "rti"
                print(assistant._format_procedure(proc_key, jurisdiction=active_jurisdiction))

            elif cmd_lower == "/contract":
                print("\n--- CONTRACT RISK REVIEW MODE ---")
                print("Paste your clause/contract text below (enter END on a new line when finished):")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                contract_text = "\n".join(lines).strip()
                if contract_text:
                    role = input("Enter your party role (default: Client / Reviewing Party): ").strip() or "Client / Reviewing Party"
                    print("\nAnalyzing clause risks...")
                    print(assistant.contract_analyzer.analyze(contract_text, jurisdiction=active_jurisdiction, party_role=role))
                else:
                    print("No text entered.")

            elif cmd_lower == "/irac":
                print("\n--- IRAC CASE ANALYZER MODE ---")
                print("Enter your factual scenario (enter END on a new line when finished):")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                scenario = "\n".join(lines).strip()
                if scenario:
                    print("\nGenerating IRAC assessment...")
                    print(assistant.irac_engine.analyze(scenario, jurisdiction=active_jurisdiction))
                else:
                    print("No scenario entered.")

            elif cmd_lower == "/draft":
                print("\n--- LEGAL DOCUMENT DRAFTING WIZARD ---")
                print("Available types: Cease and Desist, NDA, Settlement, Cheque Bounce Notice, Rent Agreement, Consumer Complaint, RTI")
                doc_type = input("Enter document type: ").strip() or "Mutual Non-Disclosure Agreement"
                party_a = input("First Party (Sender / Client): ").strip() or "[Party A Name]"
                party_b = input("Second Party (Recipient): ").strip() or "[Party B Name]"
                purpose = input("Core Purpose / Dispute: ").strip() or "[Commercial Purpose / Dispute]"
                demands = input("Key Demands / Terms: ").strip() or "[Specific Demands or Terms]"
                print("\nGenerating document draft...")
                print(assistant.document_drafter.draft(
                    doc_type=doc_type,
                    party_a=party_a,
                    party_b=party_b,
                    purpose_dispute=purpose,
                    governing_law=active_jurisdiction,
                    demands_terms=demands
                ))

            else:
                # Standard Conversational Query
                response = assistant.process_query(user_input, jurisdiction=active_jurisdiction)
                print(f"\n{response}\n")

        except KeyboardInterrupt:
            print("\nExiting NyayMitra.")
            break

if __name__ == "__main__":
    main()

