import unittest
from nyaymitra.core.contract_analyzer import ContractAnalyzer

class TestContractAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = ContractAnalyzer()

    def test_risk_analysis_four_sections(self):
        clause = """
        Client agrees to defend, indemnify, and hold harmless Vendor against all claims.
        Total aggregate liability of Vendor is capped at zero dollars.
        Vendor may terminate this Agreement at its sole discretion without notice.
        """
        result = self.analyzer.analyze(clause, jurisdiction="Republic of India", party_role="Client")

        # Must include all 4 required sections
        self.assertIn("1. Executive Summary", result)
        self.assertIn("2. High-Risk Clauses", result)
        self.assertIn("3. Ambiguities & Red Flags", result)
        self.assertIn("4. Suggested Revisions", result)

        # Must include redlines / markup
        self.assertTrue("~~" in result or "`[" in result or "diff" in result)

        # Must include mandatory disclaimer
        self.assertIn("does not constitute formal legal advice", result)

    def test_non_compete_under_indian_law(self):
        clause = "Employee agrees not to compete or work with any rival company anywhere in India for 3 years post-termination."
        result = self.analyzer.analyze(clause, jurisdiction="Republic of India")
        self.assertIn("Section 27", result)
        self.assertIn("Indian Contract Act", result)

if __name__ == "__main__":
    unittest.main()

