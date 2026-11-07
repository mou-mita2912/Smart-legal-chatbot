"""
Built-in HTTP server and REST API for NyayMitra.
Uses standard library http.server and urllib to run with zero external pip dependencies.
"""
import os
import json
import mimetypes
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from typing import Tuple

from nyaymitra.config import SERVER_PORT, SERVER_HOST, DEFAULT_JURISDICTION
from nyaymitra.core.assistant import NyayMitraAssistant
from nyaymitra.knowledge.procedures import PROCEDURAL_GUIDES
from nyaymitra.knowledge.bns_ipc_mapping import lookup_penal_section

# Ensure correct MIME types on Windows
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/html", ".html")
mimetypes.add_type("application/json", ".json")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
assistant = NyayMitraAssistant()

class NyayMitraRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler with REST API routing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS and disable aggressive caching for development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _send_json(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API: Section Lookup
        if path == "/api/bns-lookup":
            q = query.get("q", [""])[0]
            if not q:
                self._send_json({"error": "Missing query parameter 'q'"}, status=400)
                return
            result = lookup_penal_section(q)
            self._send_json({"query": q, "result": result})
            return

        # API: Procedural Guide
        if path.startswith("/api/procedure/"):
            proc_id = path.replace("/api/procedure/", "").strip()
            if proc_id in PROCEDURAL_GUIDES:
                self._send_json({"id": proc_id, "guide": PROCEDURAL_GUIDES[proc_id]})
            else:
                self._send_json({"error": "Procedure not found", "available": list(PROCEDURAL_GUIDES.keys())}, status=404)
            return

        # API: Status
        if path == "/api/status":
            self._send_json({
                "status": "online",
                "app": "NyayMitra",
                "has_gemini_key": assistant.llm.is_available(),
                "default_jurisdiction": DEFAULT_JURISDICTION
            })
            return

        # Serve static index.html or fallback
        if path == "/" or not os.path.exists(os.path.join(STATIC_DIR, path.lstrip("/"))):
            self.path = "/index.html"
            return super().do_GET()

        return super().do_GET()

    def do_POST(self):
        path = self.path
        body = self._read_json_body()

        # 1. Chat API
        if path == "/api/chat":
            user_msg = body.get("message", "")
            jurisdiction = body.get("jurisdiction", DEFAULT_JURISDICTION)
            response = assistant.process_query(user_msg, jurisdiction=jurisdiction)
            self._send_json({"response": response, "jurisdiction": jurisdiction})
            return

        # 2. Contract Review API
        if path == "/api/contract-review":
            contract_text = body.get("contract_text", "")
            jurisdiction = body.get("jurisdiction", DEFAULT_JURISDICTION)
            party_role = body.get("party_role", "Client / Reviewing Party")
            result = assistant.contract_analyzer.analyze(
                contract_text=contract_text,
                jurisdiction=jurisdiction,
                party_role=party_role
            )
            self._send_json({"result": result, "jurisdiction": jurisdiction})
            return

        # 3. IRAC Analysis API
        if path == "/api/irac":
            scenario = body.get("scenario", "")
            jurisdiction = body.get("jurisdiction", DEFAULT_JURISDICTION)
            result = assistant.irac_engine.analyze(scenario=scenario, jurisdiction=jurisdiction)
            self._send_json({"result": result, "jurisdiction": jurisdiction})
            return

        # 4. Document Drafting API
        if path == "/api/draft":
            doc_type = body.get("doc_type", "Mutual Non-Disclosure Agreement")
            party_a = body.get("party_a", "[Party A Name]")
            party_b = body.get("party_b", "[Party B Name]")
            purpose = body.get("purpose_dispute", "[Purpose of Agreement / Dispute]")
            gov_law = body.get("governing_law", DEFAULT_JURISDICTION)
            demands = body.get("demands_terms", "[Specific Demands or Terms]")

            result = assistant.document_drafter.draft(
                doc_type=doc_type,
                party_a=party_a,
                party_b=party_b,
                purpose_dispute=purpose,
                governing_law=gov_law,
                demands_terms=demands
            )
            self._send_json({"draft": result, "doc_type": doc_type, "governing_law": gov_law})
            return

        # 5. Settings API (Set API Key)
        if path == "/api/settings":
            new_key = body.get("gemini_api_key", "")
            if new_key:
                assistant.set_api_key(new_key)
            self._send_json({"success": True, "has_gemini_key": assistant.llm.is_available()})
            return

        self._send_json({"error": "Endpoint not found"}, status=404)

def run_server(host: str = SERVER_HOST, port: int = SERVER_PORT, open_browser: bool = False):
    """Starts the NyayMitra HTTP Server with automatic port fallback if port is in use."""
    ports_to_try = [port, 8080, 8085, 8888, 5000, 5050, 0]
    httpd = None
    actual_port = port

    for p in ports_to_try:
        try:
            server_address = (host, p)
            httpd = ThreadingHTTPServer(server_address, NyayMitraRequestHandler)
            actual_port = httpd.server_address[1]
            break
        except OSError as e:
            if p == ports_to_try[-1]:
                raise e
            continue

    print(f"================================================================")
    print(f"  ⚖️  NyayMitra (LegalAssist) Web Server Running")
    print(f"  URL: http://{host}:{actual_port}")
    print(f"  Default Jurisdiction: {DEFAULT_JURISDICTION}")
    print(f"  Guardrails Active: Disclaimer Mandate, Jurisdiction Verification")
    print(f"  Press Ctrl+C to stop.")
    print(f"================================================================")

    if open_browser:
        try:
            import webbrowser
            webbrowser.open(f"http://{host}:{actual_port}")
        except Exception:
            pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

