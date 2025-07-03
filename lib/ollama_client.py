import os, requests, json

def query_ollama(prompt):
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    url = f"{base}/api/generate"
    payload = {"model": "mistral", "prompt": prompt, "stream": False}
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json().get("response", "")
