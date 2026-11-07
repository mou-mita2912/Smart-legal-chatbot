import unittest
from nyaymitra.core.irac_engine import IRACEngine

class TestIRACEngine(unittest.TestCase):

    def setUp(self):
        self.engine = IRACEngine()

    def test_uk_employment_irac(self):
        scenario = "Employee with 3 years service was dismissed on the spot without notice or hearing after raising health concerns."
        result = self.engine.analyze(scenario, jurisdiction="United Kingdom (England & Wales)")

        # Verify 4 IRAC headings
        self.assertIn("1. Primary Legal Issues", result)
        self.assertIn("2. Relevant Statutes and Precedent Cases", result)
        self.assertIn("3. Application", result)
        self.assertIn("4. Recommended Next Steps", result)

        # Statutory & case citations
        self.assertIn("Employment Rights Act 1996", result)
        self.assertIn("ACAS", result)

        # Guardrails
        self.assertIn("United Kingdom (England & Wales)", result)
        self.assertIn("does not constitute formal legal advice", result)

    def test_cheque_bounce_irac(self):
        scenario = "Cheque of INR 500,000 bounced due to insufficient funds. Bank memo received yesterday."
        result = self.engine.analyze(scenario, jurisdiction="Republic of India")
        self.assertIn("Section 138", result)
        self.assertIn("Negotiable Instruments Act", result)
        self.assertIn("15", result)

if __name__ == "__main__":
    unittest.main()

