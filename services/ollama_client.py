import httpx
from config import OLLAMA_URL, OLLAMA_FALLBACK_URL, OLLAMA_MODEL, OLLAMA_FALLBACK_MODEL, OLLAMA_TIMEOUT


async def _chat(base_url: str, model: str, messages: list, timeout: float = OLLAMA_TIMEOUT) -> str:
    payload = {"model": model, "messages": messages, "stream": False}
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(f"{base_url}/api/chat", json=payload)
        resp.raise_for_status()
        return resp.json()["message"]["content"]


async def generate_code(prompt: str, language: str = "", context: str = "") -> str:
    system = "You are an expert programmer. Return only code without explanation unless asked."
    user_prompt = prompt
    if language:
        user_prompt = f"Language: {language}\n\n{prompt}"
    if context:
        user_prompt = f"{user_prompt}\n\nContext:\n{context}"

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_prompt},
    ]

    try:
        # Try Windows Ollama with short connect timeout; fall back to local on any error
        return await _chat(OLLAMA_URL, OLLAMA_MODEL, messages, timeout=8)
    except Exception:
        return await _chat(OLLAMA_FALLBACK_URL, OLLAMA_FALLBACK_MODEL, messages, timeout=OLLAMA_TIMEOUT)
