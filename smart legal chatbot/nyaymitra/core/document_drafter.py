"""
Document Drafting Engine for NyayMitra.
Generates structured legal instruments, notice templates, agreements,
and dispute petitions with marked placeholders and standard boilerplate.
"""
from typing import Optional, Dict, Any
from datetime import datetime
from nyaymitra.core.llm_client import GeminiClient
from nyaymitra.guardrails import post_process_response

DRAFTING_PROMPT_TEMPLATE = """
Draft a formal {doc_type} under the jurisdiction of {governing_law}.

Parameters provided:
- Party A (Sender / First Party): {party_a}
- Party B (Recipient / Second Party): {party_b}
- Core Purpose / Dispute / Consideration: {purpose_dispute}
- Key Terms / Demands / Deadlines: {demands_terms}
- Governing Law & Jurisdiction: {governing_law}

Requirements:
- Professional, authoritative, and legally sound tone.
- Standard legal boilerplate included (without prejudice reservations, severability, entire agreement, notices).
- Clear, standardized placeholders for unfilled terms like `[Date]`, `[Specific Amount]`, `[Address]`, `[Witness Name]`.
- Clean headings and numbered paragraphs.
"""

class DocumentDrafter:
    """Generates formal legal documents, agreements, and notices."""

    def __init__(self, llm_client: Optional[GeminiClient] = None):
        self.llm = llm_client or GeminiClient()

    def draft(
        self,
        doc_type: str,
        party_a: str = "[Party A / Sender]",
        party_b: str = "[Party B / Recipient]",
        purpose_dispute: str = "[Description of Dispute or Business Purpose]",
        governing_law: str = "Republic of India",
        demands_terms: str = "[Specific Demands or Agreement Terms]"
    ) -> str:
        """
        Drafts a formal legal instrument.
        Uses Gemini LLM if available; otherwise falls back to comprehensive modular templates.
        """
        # 1. Attempt LLM generation
        if self.llm.is_available():
            prompt = DRAFTING_PROMPT_TEMPLATE.format(
                doc_type=doc_type,
                party_a=party_a,
                party_b=party_b,
                purpose_dispute=purpose_dispute,
                demands_terms=demands_terms,
                governing_law=governing_law
            )
            response = self.llm.generate(prompt=prompt)
            if response:
                return post_process_response(response, jurisdiction=governing_law)

        # 2. Local High-Fidelity Template Engine
        return self._template_draft(
            doc_type=doc_type,
            party_a=party_a,
            party_b=party_b,
            purpose_dispute=purpose_dispute,
            governing_law=governing_law,
            demands_terms=demands_terms
        )

    def _template_draft(
        self,
        doc_type: str,
        party_a: str,
        party_b: str,
        purpose_dispute: str,
        governing_law: str,
        demands_terms: str
    ) -> str:
        """Template selection and placeholder injection."""
        dt = doc_type.lower()
        now_date = datetime.now().strftime("%d %B %Y")

        if "cease" in dt or "desist" in dt:
            text = self._cease_and_desist_template(party_a, party_b, purpose_dispute, governing_law, demands_terms, now_date)
        elif "nda" in dt or "non-disclosure" in dt or "confidential" in dt:
            text = self._nda_template(party_a, party_b, purpose_dispute, governing_law, demands_terms, now_date)
        elif "settle" in dt or "release" in dt:
            text = self._settlement_template(party_a, party_b, purpose_dispute, governing_law, demands_terms, now_date)
        elif "138" in dt or "cheque" in dt or "dishonour" in dt:
            text = self._cheque_bounce_notice_template(party_a, party_b, purpose_dispute, governing_law, demands_terms, now_date)
        elif "rent" in dt or "lease" in dt or "tenancy" in dt:
            text = self._rent_agreement_template(party_a, party_b, purpose_dispute, governing_law, demands_terms, now_date)
        elif "consumer" in dt or "complaint" in dt:
            text = self._consumer_complaint_template(party_a, party_b, purpose_dispute, governing_law, demands_terms, now_date)
        elif "rti" in dt:
            text = self._rti_application_template(party_a, party_b, purpose_dispute, governing_law, demands_terms, now_date)
        else:
            text = self._general_legal_notice_template(party_a, party_b, purpose_dispute, governing_law, demands_terms, now_date)

        return post_process_response(text, jurisdiction=governing_law)

    def _cease_and_desist_template(self, p_a, p_b, purpose, gov_law, demands, now_date) -> str:
        return f"""**CONFIDENTIAL & WITHOUT PREJUDICE**

**DATE:** {now_date}  
**DELIVERY VIA:** Registered Post A.D. / Electronic Mail  

**TO:**  
**{p_b}**  
`[Recipient Full Legal Address]`  
`[Recipient Contact Email / Phone]`  

**FROM:**  
**{p_a}**  
`[Sender Full Legal Address]`  
`[Sender Authorized Representative / Legal Counsel]`  

---

### SUBJECT: FORMAL NOTICE TO CEASE AND DESIST UNLAWFUL CONDUCT

Dear Sir/Madam,

This formal communication serves as a final demand on behalf of **{p_a}** ("Client") to **{p_b}** to immediately cease and desist from certain unlawful, tortious, and actionable activities concerning:

> **{purpose}**

#### 1. Factual Summary and Rights of the Client
1.1 Our Client is the rightful owner and holder of lawful rights, intellectual property, and contractual interests pertaining to `[insert relevant assets, trademarks, or agreements]`.  
1.2 It has come to our Client's attention that you have engaged in unauthorized acts, including but not limited to:  
* `{purpose}`  
* Continuous actions without the license, permission, or consent of our Client.  

#### 2. Violations and Legal Exposure
Your unauthorized actions constitute a direct infringement and actionable wrong under the laws of **{gov_law}**, exposing you to substantial civil damages, injunctive relief, accounting of profits, and statutory penalties.

#### 3. Immediate Demands
You are hereby formally demanded to perform the following actions within **`[10 business days / 15 calendar days]`** of receipt of this notice:
1. **Immediately cease and desist** from all acts infringing or interfering with our Client's rights, including `{demands}`.
2. Provide written confirmation and written undertaking signed by an authorized signatory affirming that all infringing materials or conduct have permanently ceased.
3. Deliver/destroy all unauthorized materials, records, or proprietary assets in your possession.

#### 4. Reservation of All Rights and Remedies
Failure to comply with these demands within the stipulated timeframe will compel our Client to initiate formal legal proceedings before the competent courts of **{gov_law}**, seeking emergency interlocutory injunctions, damages, interest, and full legal costs without further notice to you.

This letter is written **without prejudice** to any other rights, remedies, or claims available to our Client in law or equity.

Sincerely,

_____________________________  
**For and on behalf of:**  
**{p_a}**  
`[Authorized Signatory / Legal Counsel Name]`  
`[Advocate / Bar Enrollment No., if applicable]`  
"""

    def _nda_template(self, p_a, p_b, purpose, gov_law, demands, now_date) -> str:
        return f"""## MUTUAL NON-DISCLOSURE AGREEMENT

THIS MUTUAL NON-DISCLOSURE AGREEMENT (this "Agreement") is entered into on this **`[{now_date}]`** (the "Effective Date"), by and between:

**1. {p_a}**, `[entity type, e.g., a private limited company incorporated under the laws of India]`, having its registered office at `[Address Party A]` (hereinafter referred to as the **"First Party"**); and  

**2. {p_b}**, `[entity type, e.g., a corporation / partnership]`, having its office at `[Address Party B]` (hereinafter referred to as the **"Second Party"**).  

*(Each of the First Party and Second Party may be referred to individually as a "Party" and collectively as the "Parties").*

---

### RECITALS
WHEREAS, the Parties wish to explore and engage in discussions regarding **{purpose}** (the "Permitted Purpose"); and  
WHEREAS, in connection with the Permitted Purpose, each Party may disclose to the other Party proprietary, confidential, and non-public technical, commercial, or operational information.

NOW, THEREFORE, the Parties agree as follows:

#### 1. Definition of Confidential Information
"Confidential Information" means all non-public information disclosed by one Party ("Disclosing Party") to the other ("Receiving Party"), whether orally, visually, electronically, or in writing, including without limitation trade secrets, software code, customer data, pricing, business plans, and `{demands}`.

#### 2. Exclusions from Confidential Information
Confidential Information does not include information that:
(a) is or becomes publicly known through no breach of this Agreement;  
(b) was already known to the Receiving Party prior to disclosure without confidentiality restrictions;  
(c) is independently developed without reference to the Disclosing Party's information; or  
(d) is rightfully received from a third party without duty of confidence.

#### 3. Standard of Care & Obligations
The Receiving Party shall:
3.1 Hold Confidential Information in strict confidence, exercising at least the degree of care it uses for its own confidential data (and not less than reasonable care).  
3.2 Use Confidential Information solely for the Permitted Purpose.  
3.3 Restrict disclosure strictly to directors, officers, employees, and professional advisers who have a need to know and are bound by confidentiality terms at least as restrictive as this Agreement.

#### 4. Term and Survival
This Agreement shall remain in effect for a term of **`[Two (2) years]`** from the Effective Date. The confidentiality obligations regarding disclosed information shall survive for a period of **`[Three (3) years]`** following termination (or indefinitely for trade secrets).

#### 5. Governing Law & Dispute Resolution
This Agreement shall be governed by and construed in accordance with the laws of **{gov_law}**. Any disputes arising under this Agreement shall be subject to the exclusive jurisdiction of the competent courts of `[City / Venue, e.g., New Delhi / Wilmington]`.

IN WITNESS WHEREOF, the Parties have executed this Mutual Non-Disclosure Agreement as of the Effective Date written above.

**FOR {p_a}:**  
Signature: ___________________________  
Name: `[Authorized Representative Name]`  
Title: `[Director / CEO]`  

**FOR {p_b}:**  
Signature: ___________________________  
Name: `[Authorized Representative Name]`  
Title: `[Director / CEO]`  
"""

    def _settlement_template(self, p_a, p_b, purpose, gov_law, demands, now_date) -> str:
        return f"""## CONFIDENTIAL SETTLEMENT AND MUTUAL RELEASE AGREEMENT

This Settlement and Mutual Release Agreement ("Agreement") is made effective as of **`[{now_date}]`**, by and between:

* **{p_a}** ("First Party"), having address at `[Address A]`, and  
* **{p_b}** ("Second Party"), having address at `[Address B]`.  

### RECITALS
A. A dispute has arisen between the Parties regarding `{purpose}` (the "Dispute").  
B. The Parties desire to amicably resolve, compromise, and settle all existing and potential claims, controversies, and disputes between them without admission of liability.

NOW, THEREFORE, in consideration of the mutual covenants contained herein, the Parties agree as follows:

#### 1. Settlement Consideration & Terms
1.1 The Second Party shall pay to the First Party the sum of **`[INR / USD / GBP ________]`** (the "Settlement Amount") on or before **`[Date / Schedule]`** by wire transfer to account `[Bank Account Details]`.  
1.2 Specific conditions to be fulfilled: `{demands}`.

#### 2. Mutual Release of Claims
Upon receipt of the full Settlement Amount, each Party hereby irrevocably releases, acquits, and forever discharges the other Party and its affiliates, directors, officers, and employees from any and all claims, demands, liabilities, causes of action, damages, and costs arising out of or related to the Dispute.

#### 3. No Admission of Liability
This Agreement is entered into strictly as a commercial compromise. Nothing herein shall be construed as an admission of fault, liability, or wrongdoing by either Party.

#### 4. Non-Disparagement & Confidentiality
Neither Party shall make any public statement, defamatory remarks, or derogatory disclosures regarding the other Party. The terms of this settlement shall remain strictly confidential.

#### 5. Governing Law
This Agreement is governed by the laws of **{gov_law}**.

Signed:  
**{p_a}:** ______________________ Date: ___________  
**{p_b}:** ______________________ Date: ___________  
"""

    def _cheque_bounce_notice_template(self, p_a, p_b, purpose, gov_law, demands, now_date) -> str:
        return f"""**LEGAL DEMAND NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881**

**REGISTERED POST WITH ACKNOWLEDGMENT DUE / SPEED POST**

**Date:** {now_date}  

**TO:**  
**{p_b}**  
`[Complete Address of Accused/Drawer]`  

**FROM (Through Legal Counsel):**  
**Advocate `[Advocate Name]`**  
On behalf of my Client: **{p_a}**  
`[Client Full Residential / Business Address]`  

Sir/Madam,

Under instructions from and on behalf of my client **{p_a}**, I hereby serve upon you this Statutory Legal Notice under Section 138 of the Negotiable Instruments Act, 1881:

1. That you, the addressee, were under a legally enforceable debt/liability towards my client arising from `{purpose}`.
2. In discharge of your legally enforceable debt, you issued in favour of my client the following Cheque:
   * **Cheque No.:** `[Cheque Number]`
   * **Dated:** `[Date of Cheque]`
   * **Amount:** `[INR Specific Amount in Figures and Words]`
   * **Drawn on:** `[Bank Name & Branch]`
3. That my client presented the said cheque for encashment through their banker `[Bank Name]`. However, the cheque was returned dishonoured and unpaid with the Bank Return Memo dated `[Date of Memo]` stating the reason: **"`[Funds Insufficient / Account Closed / Exceeds Arrangement]`"**.
4. That you were fully aware of the insufficiency of funds at the time of issuing the cheque, thereby committing intentional fraud and dishonour.
5. In terms of Section 138(c) of the Negotiable Instruments Act, 1881, you are hereby called upon to pay the entire amount of **`[INR ________]`** to my client within **fifteen (15) calendar days** from the date of receipt of this notice.
6. Please note that in the event of failure to pay the cheque amount within the statutory period of 15 days, my client shall be constrained to initiate criminal proceedings against you under Section 138 read with Section 141 and 142 of the Negotiable Instruments Act, 1881, as well as under Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 (BNS) for criminal breach and cheating, holding you liable for imprisonment up to two years and fine up to double the cheque amount, along with legal costs.

A copy of this notice is retained in my office for future legal action.

Yours faithfully,

_____________________________  
**Advocate `[Name]`**  
Enrolment No.: `[State Bar Council No.]`  
"""

    def _rent_agreement_template(self, p_a, p_b, purpose, gov_law, demands, now_date) -> str:
        return f"""## RESIDENTIAL LEASE / RENT AGREEMENT

This Lease Agreement is made and executed at `[City]` on this **`[{now_date}]`**, by and between:

**1. {p_a}**, S/o or D/o `[Father's Name]`, residing at `[Permanent Address]`, PAN: `[PAN No.]` (hereinafter called the **"LESSOR / LANDLORD"**); and  

**2. {p_b}**, S/o or D/o `[Father's Name]`, residing at `[Permanent Address]`, PAN: `[PAN No.]` (hereinafter called the **"LESSEE / TENANT"**).  

### 1. Demised Premises
The Landlord is the sole legal owner of the residential property situated at **`[Full Address of Rented Flat/House]`** comprising `[2 BHK / 3 BHK]` (the "Premises").

### 2. Term & Period of Tenancy
The tenancy shall be for an initial period of **`[11 months]`** commencing on `[Start Date]` and expiring on `[End Date]`, renewable upon mutual written consent.

### 3. Monthly Rent & Maintenance
3.1 The Tenant agrees to pay a monthly rent of **`[INR ______]`** on or before the **`[5th / 7th]`** day of each calendar month.  
3.2 Society maintenance charges of `[INR ______]` shall be paid by `[Tenant / Landlord]`.

### 4. Security Deposit
The Tenant has deposited an interest-free refundable security deposit of **`[INR ______]`** with the Landlord, refundable at the time of vacating the Premises after adjusting for unpaid utility bills or structural damage.

### 5. Termination & Notice
Either party may terminate this agreement by providing **`[1 Month / 30 Days]`** advance written notice.

### 6. Governing Law
Governed by the Transfer of Property Act, 1882 and applicable State Tenancy Laws of **{gov_law}**.

IN WITNESS WHEREOF, the parties hereto have signed this Agreement on the day, month, and year first written above.

**LESSOR (Landlord):** ___________________  
**LESSEE (Tenant):** ___________________  

**WITNESS 1:** ___________________  
**WITNESS 2:** ___________________  
"""

    def _consumer_complaint_template(self, p_a, p_b, purpose, gov_law, demands, now_date) -> str:
        return f"""**BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION AT `[DISTRICT NAME]`**

**CONSUMER COMPLAINT NO. ________ / 2026**

**IN THE MATTER OF:**  
**{p_a}**  
`[Complainant Full Address & Contact Details]`  
... COMPLAINANT  

**VERSUS**  

**{p_b}**  
`[Opposite Party Full Name, Corporate Address]`  
... OPPOSITE PARTY  

---

### COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019

**MOST RESPECTFULLY SHOWETH:**

1. That the Complainant is a 'Consumer' within the definition of Section 2(7) of the Consumer Protection Act, 2019, having purchased `[Product/Service Description]` for consideration from the Opposite Party.
2. That the Opposite Party is a company/firm engaged in the business of manufacturing/selling `[Product/Service]`.
3. **Factual Matrix & Deficiency:**  
   That on `[Date]`, the Complainant purchased `{purpose}` for total consideration of `[INR Amount]`. However, the Opposite Party supplied defective goods / provided deficient service as detailed below:  
   `{demands}`
4. **Pre-Litigation Notice:**  
   The Complainant served a legal notice dated `[Date]` calling upon the Opposite Party to rectify the defect or refund the amount, but the Opposite Party failed to respond or resolve the issue.
5. **Jurisdiction & Limitation:**  
   The transaction value is within the pecuniary jurisdiction of this Hon'ble Commission (under INR 50 Lakhs), and the complaint is filed within the two-year limitation period under Section 69.

### PRAYER
In the premises, it is respectfully prayed that this Hon'ble Commission may be pleased to direct the Opposite Party to:
a. Refund the sum of `[INR Amount]` with interest @ 12% p.a. from the date of payment;  
b. Pay compensation of `[INR Amount]` for mental harassment, agony, and inconvenience;  
c. Award litigation costs of `[INR 25,000]` to the Complainant.  

**COMPLAINANT**  
Through Advocate: `[Advocate Name]`  
"""

    def _rti_application_template(self, p_a, p_b, purpose, gov_law, demands, now_date) -> str:
        return f"""**APPLICATION UNDER SECTION 6(1) OF THE RIGHT TO INFORMATION ACT, 2005**

**Date:** {now_date}  

**To:**  
The Central Public Information Officer (CPIO) / State PIO  
**{p_b}**  
`[Department / Ministry / Municipal Office Name]`  
`[Complete Official Address]`  

**1. Full Name of Applicant:** **{p_a}**  
**2. Address for Correspondence:** `[Full Residential Address]`  
**3. Contact Details:** Email: `[Email]` | Mobile: `[Phone]`  
**4. Citizenship:** Citizen of India  

---

**5. Particulars of Information Sought:**  
Please provide certified copies / answers to the following numbered points under the RTI Act, 2005 concerning **{purpose}**:

1. `{demands}`  
2. Certified copies of all file notings, orders, and correspondence concerning the above subject.  
3. Name and designation of the officials responsible for processing this matter.  

**6. Statutory Period:**  
The information is requested within the statutory period of thirty (30) calendar days as stipulated under Section 7(1) of the RTI Act, 2005.

**7. Application Fee Details:**  
Statutory application fee of INR 10 is paid via `[IPO No. / Demand Draft / Online Transaction Ref: ________]`. (If BPL card holder, proof attached).

Applicant Signature: ___________________________  
**{p_a}**  
"""

    def _general_legal_notice_template(self, p_a, p_b, purpose, gov_law, demands, now_date) -> str:
        return f"""**LEGAL NOTICE (WITHOUT PREJUDICE)**

**Date:** {now_date}  

**TO:**  
**{p_b}**  
`[Recipient Address]`  

**FROM:**  
**{p_a}**  
`[Sender Address]`  

Under instructions from my client **{p_a}**, you are hereby served with this formal legal notice:

1. **Background:** `{purpose}`  
2. **Breach / Grievance:** You have failed to fulfill your obligations and caused actionable harm under the laws of **{gov_law}**.  
3. **Demands:** You are called upon to comply with `{demands}` within **fifteen (15) days** from the receipt of this notice.  
4. **Consequences:** Failure to comply will lead to initiation of civil and criminal proceedings at your sole cost and consequence.  

**For {p_a}**  
_____________________________  
`[Authorized Signatory / Advocate]`  
"""

