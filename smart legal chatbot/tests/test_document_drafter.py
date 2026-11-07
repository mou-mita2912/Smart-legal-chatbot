import unittest
from nyaymitra.core.document_drafter import DocumentDrafter

class TestDocumentDrafter(unittest.TestCase):

    def setUp(self):
        self.drafter = DocumentDrafter()

    def test_cease_and_desist_draft(self):
        result = self.drafter.draft(
            doc_type="Cease and Desist Letter",
            party_a="CyberSecurity Labs Pvt Ltd",
            party_b="Infringing Tech LLP",
            purpose_dispute="Unauthorized copying of proprietary source code",
            governing_law="Republic of India",
            demands_terms="Cease usage within 10 business days and destroy all copies"
        )
        self.assertIn("CEASE AND DESIST", result)
        self.assertIn("CyberSecurity Labs Pvt Ltd", result)
        self.assertIn("Infringing Tech LLP", result)
        self.assertIn("WITHOUT PREJUDICE", result)
        self.assertIn("does not constitute formal legal advice", result)

    def test_nda_draft(self):
        result = self.drafter.draft(
            doc_type="Mutual Non-Disclosure Agreement",
            party_a="Alpha Corp",
            party_b="Beta LLC",
            purpose_dispute="Evaluating joint cloud software venture",
            governing_law="State of Delaware (USA)",
            demands_terms="2-year non-disclosure with trade secret carveout"
        )
        self.assertIn("NON-DISCLOSURE AGREEMENT", result)
        self.assertIn("Alpha Corp", result)
        self.assertIn("Beta LLC", result)
        self.assertIn("State of Delaware (USA)", result)

    def test_cheque_bounce_notice(self):
        result = self.drafter.draft(
            doc_type="Section 138 NI Act Cheque Bounce Notice",
            party_a="Vendor Enterprises",
            party_b="Defaulting Retailer",
            purpose_dispute="Dishonour of Cheque No. 998811 for INR 3,00,000",
            governing_law="Republic of India"
        )
        self.assertIn("SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT", result)
        self.assertIn("fifteen (15) calendar days", result)

if __name__ == "__main__":
    unittest.main()

