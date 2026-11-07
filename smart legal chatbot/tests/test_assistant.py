import unittest
from nyaymitra.core.assistant import NyayMitraAssistant

class TestNyayMitraAssistant(unittest.TestCase):

    def setUp(self):
        self.assistant = NyayMitraAssistant()

    def test_section_query_routing(self):
        resp = self.assistant.process_query("What does Section 420 IPC mean under BNS?")
        self.assertIn("Section 420 IPC", resp)
        self.assertIn("Section 318(4) BNS", resp)
        self.assertIn("does not constitute formal legal advice", resp)

    def test_procedure_query_routing(self):
        resp = self.assistant.process_query("How to file an RTI application?")
        self.assertIn("Right to Information (RTI) Application", resp)
        self.assertIn("Section 6(1)", resp)
        self.assertIn("30", resp)

    def test_draft_query_routing(self):
        resp = self.assistant.process_query("Draft a cease and desist letter")
        self.assertIn("CEASE AND DESIST", resp)
        self.assertIn("WITHOUT PREJUDICE", resp)

    def test_constitutional_rights_query(self):
        resp = self.assistant.process_query("What are my rights under Article 21?")
        self.assertIn("Article 21", resp)
        self.assertIn("Maneka Gandhi", resp)

if __name__ == "__main__":
    unittest.main()

