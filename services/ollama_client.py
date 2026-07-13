import httpx
import logging
from config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_CONNECT_TIMEOUT, OLLAMA_READ_TIMEOUT

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(connect=OLLAMA_CONNECT_TIMEOUT, read=OLLAMA_READ_TIMEOUT, write=10.0, pool=5.0)


async def _chat(base_url: str, model: str, messages: list) -> str:
    payload = {"model": model, "messages": messages, "stream": False}
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
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
        return await _chat(OLLAMA_URL, OLLAMA_MODEL, messages)
    except httpx.ConnectError as e:
        logger.error(f"Ollama(Windows: {OLLAMA_URL})に接続できません: {e}")
        raise
