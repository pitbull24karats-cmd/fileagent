from pathlib import Path

SSH_HOST = "192.168.243.196"
SSH_USER = "aTsuYa"
SSH_KEY_PATH = str(Path.home() / ".ssh" / "jarvis_fileagent")

OLLAMA_URL = "http://192.168.243.196:11434"
OLLAMA_FALLBACK_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5-coder:7b"
OLLAMA_FALLBACK_MODEL = "qwen2.5:7b"
OLLAMA_TIMEOUT = 60

MAC_ALLOWED_PATHS = [
    str(Path.home() / "Desktop" / "Jarvis"),
    str(Path.home() / "jarvis_server"),
    str(Path.home() / "Desktop" / "devbrain"),
    str(Path.home() / "Desktop" / "fixai"),
    str(Path.home() / "Desktop" / "fileagent"),
    str(Path.home() / "Desktop" / "Flowpost"),
    str(Path.home() / "Desktop" / "Cryptagent"),
    str(Path.home() / "Desktop" / "Calendar-Yuto"),
]

WIN_ALLOWED_PATHS = [
    r"F:\Jarvis",
    r"E:\Jarvis",
]
