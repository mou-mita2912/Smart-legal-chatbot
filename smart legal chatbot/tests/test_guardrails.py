import unittest
from nyaymitra.guardrails import (
    enforce_disclaimer,
    enforce_jurisdiction,
    sanitize_outcome_guarantees,
    post_process_response,
    contains_disclaimer
)
from nyaymitra.config import MANDATORY_DISCLAIMER, DEFAULT_JURISDICTION

class TestGuardrails(unittest.TestCase):

    def test_disclaimer_appended_when_missing(self):
        sample = "Here is an explanation of Section 420."
        processed = enforce_disclaimer(sample)
        self.assertTrue(contains_disclaimer(processed))
        self.assertIn("Disclaimer:", processed)

    def test_disclaimer_not_duplicated_when_already_present(self):
        sample = f"Explanation of law.\n\nDisclaimer: {MANDATORY_DISCLAIMER}"
        processed = enforce_disclaimer(sample)
        # Should not duplicate disclaimer
        self.assertEqual(processed.count("does not constitute formal legal advice"), 1)

    def test_jurisdiction_enforced(self):
        sample = "Information about criminal procedure."
        processed = enforce_jurisdiction(sample, "Republic of India")
        self.assertTrue("Jurisdiction:" in processed)
        self.assertTrue("Republic of India" in processed)

    def test_outcome_guarantee_sanitized(self):
        sample = "Don't worry, you will definitely win this lawsuit against your employer."
        sanitized = sanitize_outcome_guarantees(sample)
        self.assertNotIn("definitely win", sanitized.lower())
        self.assertIn("judicial discretion", sanitized)

    def test_complete_post_process_pipeline(self):
        raw = "You are guaranteed to win. File an FIR under Section 154."
        final = post_process_response(raw, jurisdiction="Republic of India")
        self.assertNotIn("guaranteed to win", final.lower())
        self.assertTrue(contains_disclaimer(final))
        self.assertIn("Republic of India", final)
        self.assertIn("Jurisdiction:", final)

if __name__ == "__main__":
    unittest.main()
