"""
Main Application Launcher for NyayMitra (LegalAssist).
Starts the built-in HTTP Web Server with automatic port fallback.
"""
from nyaymitra.config import SERVER_HOST, SERVER_PORT
from nyaymitra.web.server import run_server

def main():
    run_server(host=SERVER_HOST, port=SERVER_PORT, open_browser=True)

if __name__ == "__main__":
    main()

