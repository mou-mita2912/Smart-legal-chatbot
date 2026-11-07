"""
Optional Streamlit Interface for NyayMitra (LegalAssist).
Can be launched using: streamlit run streamlit_app.py
"""
import sys
import os

try:
    import streamlit as st
except ImportError:
    print("Streamlit is not installed. To run the Streamlit interface, run: pip install streamlit")
    print("Alternatively, run the built-in web app with: python app.py")
    sys.exit(1)

from nyaymitra.config import APP_NAME, APP_SUBTITLE, DEFAULT_JURISDICTION, MANDATORY_DISCLAIMER
from nyaymitra.core.assistant import NyayMitraAssistant
from nyaymitra.knowledge.procedures import PROCEDURAL_GUIDES
from nyaymitra.knowledge.bns_ipc_mapping import lookup_penal_section

st.set_page_config(
    page_title=f"{APP_NAME} - Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-family: 'Cinzel', serif; color: #0A1128; }
    .disclaimer-box { background-color: #FFFBEB; border-left: 4px solid #D97706; padding: 12px; margin-bottom: 20px; border-radius: 4px; font-size: 0.85rem; color: #92400E; }
</style>
""", unsafe_allow_html=True)

# Mandatory Disclaimer
st.markdown(f"""
<div class="disclaimer-box">
    <strong>Disclaimer:</strong> {MANDATORY_DISCLAIMER}
</div>
""", unsafe_allow_html=True)

# Initialize Assistant
if "assistant" not in st.session_state:
    st.session_state.assistant = NyayMitraAssistant()

# Sidebar
st.sidebar.title("⚖️ NyayMitra")
st.sidebar.caption(APP_SUBTITLE)
jurisdiction = st.sidebar.selectbox(
    "Active Jurisdiction",
    ["Republic of India", "United Kingdom (England & Wales)", "State of Delaware (USA)", "United States (Federal)"]
)

api_key = st.sidebar.text_input("Gemini API Key (Optional)", type="password")
if api_key:
    st.session_state.assistant.set_api_key(api_key)

# Tabs
tab_chat, tab_contract, tab_irac, tab_draft, tab_bns, tab_proc = st.tabs([
    "💬 Chatbot",
    "🔍 Contract Review",
    "⚖️ IRAC Analyzer",
    "📝 Document Drafter",
    "🔄 IPC ⇄ BNS",
    "🧭 Procedures"
])

# 1. Chatbot
with tab_chat:
    st.subheader("Legal Guidance & Query Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a legal question (e.g. rights under Article 21, procedure for bail, consumer rights)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.session_state.assistant.process_query(prompt, jurisdiction=jurisdiction)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 2. Contract Review
with tab_contract:
    st.subheader("Contract & Clause Risk Review")
    st.caption("Perform an executive summary, high-risk clause audit, ambiguity detection, and redline markup.")
    role = st.selectbox("Your Role / Perspective", ["Client / Buyer", "Vendor / Service Provider", "Employee", "Receiving Party", "Disclosing Party"])
    contract_text = st.text_area("Contract / Clause Text", height=200, placeholder="Paste indemnification, liability, non-compete, or termination clauses...")
    if st.button("Run Risk Analysis"):
        if contract_text.strip():
            with st.spinner("Analyzing risk exposure..."):
                res = st.session_state.assistant.contract_analyzer.analyze(contract_text, jurisdiction=jurisdiction, party_role=role)
                st.markdown(res)
        else:
            st.warning("Please paste contract text.")

# 3. IRAC Analyzer
with tab_irac:
    st.subheader("IRAC Legal Reasoning Analyzer")
    st.caption("Break down factual scenarios into Issue, Rule, Application, and Conclusion/Strategy.")
    scenario = st.text_area("Factual Scenario", height=180, placeholder="Describe the factual sequence, actions, and disputes...")
    if st.button("Generate IRAC Breakdown"):
        if scenario.strip():
            with st.spinner("Evaluating statutes and precedents..."):
                res = st.session_state.assistant.irac_engine.analyze(scenario, jurisdiction=jurisdiction)
                st.markdown(res)
        else:
            st.warning("Please enter a scenario.")

# 4. Document Drafter
with tab_draft:
    st.subheader("Legal Document Drafter")
    col1, col2 = st.columns(2)
    with col1:
        doc_type = st.selectbox("Document Type", [
            "Cease and Desist Letter",
            "Mutual Non-Disclosure Agreement",
            "Settlement and Mutual Release Agreement",
            "Section 138 NI Act Cheque Bounce Notice",
            "Residential Lease / Rent Agreement",
            "Consumer Dispute Petition",
            "RTI Application (Section 6(1))"
        ])
        party_a = st.text_input("First Party / Sender", "[Party A Name]")
        party_b = st.text_input("Second Party / Recipient", "[Party B Name]")
    with col2:
        purpose = st.text_input("Dispute Subject / Purpose", "[Core Dispute or Consideration]")
        demands = st.text_area("Specific Demands / Terms", "[List key demands, timeline, or conditions]", height=100)

    if st.button("Generate Legal Draft"):
        with st.spinner("Drafting instrument with standard boilerplate..."):
            draft = st.session_state.assistant.document_drafter.draft(
                doc_type=doc_type,
                party_a=party_a,
                party_b=party_b,
                purpose_dispute=purpose,
                governing_law=jurisdiction,
                demands_terms=demands
            )
            st.markdown(draft)
            st.download_button("Download Draft (.txt)", draft, file_name=f"{doc_type.replace(' ', '_')}.txt")

# 5. IPC <-> BNS
with tab_bns:
    st.subheader("New Criminal Laws Cross-Reference (IPC ⇄ BNS)")
    query_sec = st.text_input("Enter IPC or BNS section number (e.g. 420, 302, 304A, 154, FIR):")
    if query_sec:
        res = lookup_penal_section(query_sec)
        if res:
            st.markdown(st.session_state.assistant._format_section_lookup(res, query_sec))
        else:
            st.info("I cannot verify the exact section for this specific scenario; please consult legal counsel.")

# 6. Procedures
with tab_proc:
    st.subheader("Procedural Workflows")
    proc_choice = st.selectbox("Select Procedure", ["rti", "fir", "consumer_complaint", "cybercrime"], format_func=lambda x: {
        "rti": "File RTI Application (RTI Act 2005)",
        "fir": "Register FIR / Zero FIR (BNSS Section 173)",
        "consumer_complaint": "File Consumer Dispute (e-Daakhil)",
        "cybercrime": "Report Cyber Fraud (1930 / cybercrime.gov.in)"
    }[x])
    guide = PROCEDURAL_GUIDES.get(proc_choice)
    if guide:
        st.markdown(f"### {guide['title']}")
        st.write(f"**Governing Law:** {guide['governing_law']}")
        for s in guide["steps"]:
            with st.expander(f"Step {s['step']}: {s['title']}", expanded=True):
                st.write(s['details'])

