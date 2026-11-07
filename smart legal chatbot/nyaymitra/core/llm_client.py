"""
Zero-dependency LLM client for Google Gemini API with graceful offline fallback.
Uses standard library urllib.request to avoid external dependency requirements.
"""
import json
import urllib.request
import urllib.error
from typing import Optional, List, Dict
from nyaymitra.config import GEMINI_API_KEY, DEFAULT_MODEL, SYSTEM_PERSONA_PROMPT

class GeminiClient:
    """Client for calling Google Gemini API without third-party dependencies."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model or DEFAULT_MODEL

    def is_available(self) -> bool:
        """Returns True if an API key is configured."""
        return bool(self.api_key and self.api_key.strip())

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.2
    ) -> Optional[str]:
        """
        Sends a generation request to the Gemini API.
        Returns the generated text or None if offline/unavailable/failed.
        """
        if not self.is_available():
            return None

        # Prefer modern models; fallback if needed
        model_name = self.model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"

        contents = []
        if history:
            for item in history:
                role = "user" if item.get("role") == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": item.get("content", "")}]
                })
        
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "topP": 0.95,
                "maxOutputTokens": 4096,
            }
        }

        sys_inst = system_instruction or SYSTEM_PERSONA_PROMPT
        if sys_inst:
            payload["systemInstruction"] = {
                "parts": [{"text": sys_inst}]
            }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=25) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception):
            # Gracefully handle network issues, sandbox isolation, or invalid key
            return None

        return None

