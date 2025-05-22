import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is not installed, or not needed (e.g., in a deployed environment
    # where environment variables are set directly by the platform).
    pass

API_BASE = os.getenv("API_BASE_URL","https://legal-ai-backend-hjuh.onrender.com")

def embed_document(content:str):
    res = requests.post(f"{API_BASE}/embed",json={"content":content})
    res.raise_for_status()
    return res.json()

def ask_question(question:str):
    res = requests.post(f"{API_BASE}/ask",json={"question":question})
    return res.json()
