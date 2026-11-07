import re
import unittest
from pathlib import Path

class TestFrontendAssets(unittest.TestCase):
    def test_dom_ids_exist_in_html(self):
        js_path = Path("nyaymitra/web/static/app.js")
        html_path = Path("nyaymitra/web/static/index.html")

        self.assertTrue(js_path.exists())
        self.assertTrue(html_path.exists())

        js_content = js_path.read_text(encoding="utf-8")
        html_content = html_path.read_text(encoding="utf-8")

        # Find all getElementById occurrences
        ids_in_js = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js_content)
        self.assertGreater(len(ids_in_js), 10)

        for el_id in set(ids_in_js):
            # If dynamically assigned (like msg-...), skip
            if el_id.startswith("msg-"):
                continue
            with self.subTest(element_id=el_id):
                self.assertTrue(
                    f'id="{el_id}"' in html_content or f"id='{el_id}'" in html_content,
                    f"DOM element ID '{el_id}' used in app.js is missing from index.html"
                )

if __name__ == "__main__":
    unittest.main()

