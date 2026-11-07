import unittest
from nyaymitra.knowledge.bns_ipc_mapping import lookup_penal_section

class TestBNSMapping(unittest.TestCase):

    def test_cheating_mapping(self):
        res = lookup_penal_section("420")
        self.assertIsNotNone(res)
        self.assertIn("Section 420 IPC", res["ipc"])
        self.assertIn("Section 318(4) BNS", res["bns"])

    def test_murder_mapping(self):
        res = lookup_penal_section("302")
        self.assertIsNotNone(res)
        self.assertIn("Section 302 IPC", res["ipc"])
        self.assertIn("Section 103 BNS", res["bns"])

    def test_fir_mapping(self):
        res = lookup_penal_section("154")
        self.assertIsNotNone(res)
        self.assertIn("Section 154 CrPC", res["crpc"])
        self.assertIn("Section 173 BNSS", res["bnss"])

    def test_hit_and_run_mapping(self):
        res = lookup_penal_section("304A")
        self.assertIsNotNone(res)
        self.assertIn("Section 106 BNS", res["bns"])

    def test_unknown_section(self):
        res = lookup_penal_section("999999")
        self.assertEqual(res, {})

if __name__ == "__main__":
    unittest.main()

