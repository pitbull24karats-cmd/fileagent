import os
from pathlib import Path

SSH_HOST = "192.168.243.196"
SSH_USER = "aTsuYa"
SSH_KEY_PATH = str(Path.home() / ".ssh" / "jarvis_fileagent")

# iMac上のOllamaは全廃し、Windows機に一本化。OLLAMA_HOSTが設定されていれば最優先。
OLLAMA_URL = os.getenv("OLLAMA_HOST", os.getenv("WINDOWS_OLLAMA_HOST", "http://192.168.243.196:11434"))
OLLAMA_MODEL = "qwen2.5-coder:7b"

# 接続失敗は5秒で切り上げる（ローカルへの無言フォールバックはしない）。
# Windows機は複数プロジェクトでOllamaを共有しておりモデル切替に70秒前後かかることがあるため、生成は100秒まで待つ。
OLLAMA_CONNECT_TIMEOUT = 5.0
OLLAMA_READ_TIMEOUT = 100.0

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
