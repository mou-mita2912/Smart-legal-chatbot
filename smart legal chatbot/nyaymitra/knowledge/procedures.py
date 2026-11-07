"""
Procedural workflows and step-by-step navigation guides for common citizen legal procedures.
"""

PROCEDURAL_GUIDES = {
    "rti": {
        "title": "How to File a Right to Information (RTI) Application",
        "governing_law": "Right to Information Act, 2005 (India)",
        "steps": [
            {
                "step": 1,
                "title": "Identify Public Authority & Public Information Officer (PIO)",
                "details": "Determine which Central or State government ministry, department, or municipal body holds the records you require."
            },
            {
                "step": 2,
                "title": "Draft the Application (Section 6(1))",
                "details": "State clearly what information, certified copies, or inspection of records is sought. Keep questions specific, objective, and numbered. You do not need to give any reason for requesting the information."
            },
            {
                "step": 3,
                "title": "Pay the Statutory Fee",
                "details": "Central Government fee is INR 10 (cash, demand draft, Indian Postal Order, or online via debit/credit/netbanking). Applicants below the poverty line (BPL) are exempt on producing proof."
            },
            {
                "step": 4,
                "title": "Submit the Application",
                "details": "For Central authorities: Submit online at https://rtionline.gov.in. For State bodies: Submit via respective state RTI portals or send via Registered / Speed Post to the Central Public Information Officer (CPIO) / State PIO (SPIO)."
            },
            {
                "step": 5,
                "title": "Track the 30-Day Statutory Timeline",
                "details": "Under Section 7(1), the PIO must reply within 30 calendar days (or 48 hours if concerning life and liberty). If transferred to another authority under Section 6(3), 5 additional days apply."
            },
            {
                "step": 6,
                "title": "Appeal if Rejected or No Response (Section 19)",
                "details": "File a First Appeal under Section 19(1) within 30 days to the First Appellate Authority (FAA). If unresolved, file a Second Appeal under Section 19(3) within 90 days before the Central Information Commission (CIC) or State Information Commission (SIC)."
            }
        ]
    },
    "fir": {
        "title": "How to Register an FIR (First Information Report) & Remedies for Refusal",
        "governing_law": "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) - Section 173 (Replacing CrPC 154)",
        "steps": [
            {
                "step": 1,
                "title": "Approach Police Station or Use e-FIR Portal",
                "details": "For cognizable offenses (e.g., theft, assault, fraud, kidnapping), police are mandated to record an FIR. Under Section 173(1) BNSS, you can also submit information electronically (e-FIR), which must be signed by the informant within three days."
            },
            {
                "step": 2,
                "title": "Zero FIR Provision",
                "details": "If the incident occurred outside the police station's territorial jurisdiction, police are still legally obligated to register a 'Zero FIR' and subsequently transfer the investigation to the jurisdictional police station."
            },
            {
                "step": 3,
                "title": "Verification & Free Copy",
                "details": "Under Section 173(2) BNSS, the contents must be read over to the informant, and a copy of the FIR must be provided immediately, free of cost."
            },
            {
                "step": 4,
                "title": "Remedy against Refusal to Register (BNSS Section 175(3))",
                "details": "If the Station House Officer (SHO) refuses to register the FIR, send the substance of the information in writing by registered post to the Superintendent of Police (SP) or Deputy Commissioner of Police (DCP)."
            },
            {
                "step": 5,
                "title": "Judicial Remedy: Application to Magistrate (BNSS Section 175(4) / Section 175(3))",
                "details": "If the SP fails to act, file an application before the Judicial Magistrate having jurisdiction under Section 175(4) BNSS (formerly Section 156(3) CrPC) along with an affidavit, requesting an order directing the police to register and investigate the FIR."
            }
        ]
    },
    "consumer_complaint": {
        "title": "How to File a Consumer Dispute Complaint",
        "governing_law": "Consumer Protection Act, 2019 & Consumer Protection Rules, 2021",
        "steps": [
            {
                "step": 1,
                "title": "Pre-Litigation: Issue a Legal Notice",
                "details": "Send a formal notice in writing detailing the defect in goods or deficiency in services, giving the trader/service provider 15 to 30 days to replace the item, refund, or rectify the issue."
            },
            {
                "step": 2,
                "title": "Determine Forum by Pecuniary Jurisdiction",
                "details": "District Commission: Up to INR 50 Lakhs | State Commission: Exceeding INR 50 Lakhs up to INR 2 Crores | National Commission (NCDRC): Exceeding INR 2 Crores (calculated based on consideration paid)."
            },
            {
                "step": 3,
                "title": "Territorial Jurisdiction",
                "details": "Unlike earlier laws, under Section 34(2) CPA 2019, you can file the complaint in the Commission within whose local limits the complainant resides or personally works for gain."
            },
            {
                "step": 4,
                "title": "Online Filing via e-Daakhil Portal",
                "details": "Register at https://edaakhil.nic.in, upload the petition, supporting affidavit, invoices, emails/communications, and pay the nominal statutory filing fee online."
            },
            {
                "step": 5,
                "title": "Statutory Limitation Period",
                "details": "Under Section 69, the complaint must be filed within 2 years from the date on which the cause of action arose."
            }
        ]
    },
    "cybercrime": {
        "title": "How to Report Cybercrime & Financial Fraud",
        "governing_law": "Information Technology Act, 2000 & National Cyber Crime Reporting Portal",
        "steps": [
            {
                "step": 1,
                "title": "Immediate Golden Hour Action (Financial Fraud)",
                "details": "Call the National Cyber Financial Fraud Helpline at **1930** immediately. Quick reporting freezes the fraudster's mule account before funds are laundered."
            },
            {
                "step": 2,
                "title": "Preserve Digital Evidence",
                "details": "Take screenshots, preserve SMS/WhatsApp message threads, record transaction IDs/UTR numbers, email headers, and bank account statements."
            },
            {
                "step": 3,
                "title": "File Online Complaint on National Portal",
                "details": "Visit https://cybercrime.gov.in and report under 'Financial Fraud' or 'Women & Children Related Cyber Crimes'. Obtain the acknowledgment number."
            },
            {
                "step": 4,
                "title": "Notify Bank in Writing",
                "details": "Submit a formal written dispute with your bank within 3 working days to secure zero-liability protection under RBI's Customer Liability in Unauthorized Electronic Transactions circular."
            }
        ]
    }
}

